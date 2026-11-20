"""Shared E*TRADE download IO. Python 3.10+, standard library only.

Adapted from Skatteguru's download-my-documents-from-etrade helpers.
Copyright (c) 2025-2026 Skatteguru. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import sys
import tempfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ORIGIN = "https://us.etrade.com"
MAX_RESPONSE = 50 * 1024 * 1024


class DownloadError(Exception):
    """A safe diagnostic containing no raw request or response material."""


@dataclass
class Capture:
    url: str
    headers: dict[str, str]
    payload: dict[str, Any]


def validate_url(url: str) -> None:
    try:
        parsed = urlsplit(url)
        valid = (
            parsed.scheme == "https"
            and parsed.hostname == "us.etrade.com"
            and parsed.port in (None, 443)
            and not parsed.username
            and not parsed.password
            and not parsed.fragment
            and parsed.path.startswith("/webapisp/stockplan/")
        )
    except ValueError:
        valid = False
    if not valid:
        raise DownloadError("Only HTTPS E*TRADE stock-plan endpoints are allowed.")


def parse_capture(text: str) -> Capture:
    """Parse Copy as cURL as data; never execute shell syntax or commands."""
    try:
        args = shlex.split(text.replace("\\\n", " "))
    except ValueError:
        raise DownloadError("Invalid cURL quoting; capture a fresh request.") from None
    if not args or args[0] != "curl":
        raise DownloadError("Expected a Copy as cURL request.")
    url = ""
    headers: dict[str, str] = {}
    body = ""
    i = 1
    while i < len(args):
        token = args[i]
        if token in (
            "-H",
            "--header",
            "-b",
            "--cookie",
            "--data-raw",
            "--data",
            "--data-binary",
            "-d",
            "--url",
            "-X",
            "--request",
        ):
            i += 1
            if i >= len(args):
                raise DownloadError("Incomplete captured request.")
            value = args[i]
            if token in ("-H", "--header"):
                name, separator, content = value.partition(":")
                if not separator or not name.strip() or "\n" in value or "\r" in value:
                    raise DownloadError("Invalid captured header.")
                headers[name.strip().lower()] = content.strip()
            elif token in ("-b", "--cookie"):
                if "\n" in value or "\r" in value:
                    raise DownloadError("Invalid captured cookie.")
                headers["cookie"] = "; ".join(filter(None, [headers.get("cookie"), value]))
            elif token in ("-X", "--request"):
                if value.upper() != "POST":
                    raise DownloadError("Capture the broker's POST request.")
            elif token == "--url":
                if url:
                    raise DownloadError("Expected one captured URL.")
                url = value
            else:
                body = value
        elif token in ("--compressed", "--globoff", "--silent", "--show-error"):
            pass
        elif not token.startswith("-") and not url:
            url = token
        else:
            raise DownloadError("Unsupported cURL option; capture a plain browser request.")
        i += 1
    validate_url(url)
    if not urlsplit(url).path.endswith(("/confirmations.json", "/orders.json")):
        raise DownloadError("Capture confirmations.json or orders.json, not another endpoint.")
    try:
        payload = json.loads(body)
    except (ValueError, TypeError):
        raise DownloadError("Captured request must contain a JSON body.") from None
    if (
        not isinstance(payload, dict)
        or not isinstance(payload.get("value"), dict)
        or not isinstance(payload["value"].get("encryptedEmployeeId"), str)
        or not payload["value"]["encryptedEmployeeId"]
    ):
        raise DownloadError("Captured request is missing stock-plan account context.")
    for name in ("host", "content-length", "accept-encoding", "connection", "transfer-encoding"):
        headers.pop(name, None)
    headers["content-type"] = "application/json"
    return Capture(url, headers, payload)


def read_capture(path: Path | None) -> Capture:
    if path is None:
        text = sys.stdin.read(2 * 1024 * 1024 + 1)
    else:
        if path.is_symlink() or not path.is_file():
            raise DownloadError("Request capture must be a regular private file.")
        try:
            with path.open(encoding="utf-8") as stream:
                text = stream.read(2 * 1024 * 1024 + 1)
        finally:
            # --request-file explicitly consumes this temporary capture.
            path.unlink()
    if len(text) > 2 * 1024 * 1024:
        raise DownloadError("Captured request is too large.")
    return parse_capture(text)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


def fetch(url: str, headers: dict[str, str], payload: dict[str, Any] | None = None) -> bytes:
    validate_url(url)
    body = json.dumps(payload).encode() if payload is not None else None
    request = Request(url, headers=headers, data=body, method="POST" if body else "GET")
    try:
        with build_opener(NoRedirect()).open(request, timeout=45) as response:
            data: bytes = response.read(MAX_RESPONSE + 1)
    except HTTPError as error:
        raise DownloadError(
            f"Broker returned HTTP {error.code}; check the session before retrying."
        ) from None
    except (URLError, OSError, ValueError):
        raise DownloadError("Broker request failed; check connectivity and session.") from None
    if len(data) > MAX_RESPONSE:
        raise DownloadError("Broker response exceeded the download limit.")
    return data


def json_response(data: bytes) -> dict[str, Any]:
    try:
        value = json.loads(data)
    except (ValueError, UnicodeError):
        raise DownloadError("Broker returned invalid JSON; check the session.") from None
    if not isinstance(value, dict):
        raise DownloadError("Unexpected broker JSON response.")
    return value


def check_envelope(node: dict[str, Any], rows: int) -> None:
    """Reject known application errors and signs that more pages are needed."""
    if node.get("error") or node.get("errors") or node.get("success") is False:
        raise DownloadError("Broker response reports an error; check the session.")
    if any(node.get(k) for k in ("hasMore", "hasNext", "nextToken", "nextPageToken")):
        raise DownloadError("Response indicates more pages; use the browser to verify coverage.")
    for key in ("count", "total", "totalCount", "totalRecords"):
        value = node.get(key)
        if value is not None:
            try:
                count = int(value)
            except (TypeError, ValueError):
                raise DownloadError("Invalid broker record count.") from None
            if count > rows:
                raise DownloadError("Response is incomplete; use the browser to verify coverage.")


def records(value: dict[str, Any], paths: tuple[tuple[str, ...], ...]) -> list[dict[str, Any]]:
    for path in paths:
        node: Any = value
        parents = [value]
        for key in path:
            if not isinstance(node, dict) or key not in node:
                break
            node = node[key]
            if isinstance(node, dict):
                parents.append(node)
        else:
            if isinstance(node, list) and all(isinstance(row, dict) for row in node):
                for parent in parents:
                    check_envelope(parent, len(node))
                return node
    raise DownloadError("Unrecognized broker response; no complete record list was found.")


def parse_date(value: str) -> date:
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    raise argparse.ArgumentTypeError("Use YYYY-MM-DD or MM/DD/YYYY.")


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--start-date", type=parse_date)
    parser.add_argument("--end-date", type=parse_date)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--request-file",
        type=Path,
        help="Private temporary cURL capture; consumed and deleted after reading. Otherwise stdin.",
    )


def date_range(parser: argparse.ArgumentParser, args: argparse.Namespace) -> tuple[date, date]:
    start, end = args.start_date, args.end_date
    if not isinstance(start, date) or not isinstance(end, date) or start > end:
        parser.error("Provide --start-date and --end-date in chronological order.")
    return start, end


def prepare_output(path: Path) -> Path:
    result = path.resolve()
    if result.is_relative_to(Path(__file__).resolve().parent.parent):
        raise DownloadError("Keep downloads outside the installed skill directory.")
    result.mkdir(parents=True, exist_ok=True, mode=0o700)
    return result


def save_original(path: Path, content: bytes) -> None:
    """Publish a private file atomically; never overwrite different existing bytes."""
    if path.is_symlink():
        raise DownloadError("Refusing a symlink output file.")
    if path.exists():
        if (
            not path.is_file()
            or hashlib.sha256(path.read_bytes()).digest() != hashlib.sha256(content).digest()
        ):
            raise DownloadError(
                "Existing output differs; keep it and choose another output directory."
            )
        return
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".download-")
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
        try:
            os.link(temporary, path)
        except FileExistsError:
            raise DownloadError(
                "Output appeared during download; inspect it before retrying."
            ) from None
    finally:
        Path(temporary).unlink(missing_ok=True)


def report_error(error: Exception) -> None:
    # Unexpected exception strings may contain private paths, URLs or payloads.
    print(
        str(error)
        if isinstance(error, DownloadError)
        else "Download failed; inspect local files before retrying.",
        file=sys.stderr,
    )
