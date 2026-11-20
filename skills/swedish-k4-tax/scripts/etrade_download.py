"""Download Restricted Stock and Stock Options confirmation PDFs.

Adapted from Skatteguru's download-my-documents-from-etrade/etrade_download.py.
Copyright (c) 2025-2026 Skatteguru. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import copy
import re
from datetime import date
from urllib.parse import urlencode, urlsplit

from etrade_common import (
    ORIGIN,
    DownloadError,
    add_arguments,
    date_range,
    fetch,
    json_response,
    parse_date,
    prepare_output,
    read_capture,
    records,
    report_error,
    save_original,
)


def valid_pdf(content: bytes) -> bool:
    # Basic download validation, not a full PDF parser/security assessment.
    return content.startswith(b"%PDF-") and b"%%EOF" in content[-1024:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_arguments(parser)
    args = parser.parse_args(argv)
    start, end = date_range(parser, args)
    try:
        capture = read_capture(args.request_file)
        if not urlsplit(capture.url).path.endswith("/confirmations.json"):
            raise DownloadError("Capture confirmations.json for confirmation downloads.")
        output = prepare_output(args.output_dir)
        payload = copy.deepcopy(capture.payload)
        payload["value"].update(
            {
                "taxYear": "",
                "startDate": start.strftime("%m/%d/%Y"),
                "endDate": end.strftime("%m/%d/%Y"),
                "planTypeCode": "All",
                "appType": "STOCKPLAN",
            }
        )
        rows = records(
            json_response(fetch(capture.url, capture.headers, payload)),
            (("data", "confirmation", "confirmations"),),
        )
        employee = payload["value"]["encryptedEmployeeId"]
        selected: list[tuple[str, str, date]] = []
        seen: set[tuple[str, str]] = set()
        for row in rows:
            kind = row.get("planTypeCode")
            if kind not in ("Restricted Stock", "STOCK OPTIONS"):
                continue
            identifier = str(row.get("confirmationId", ""))
            if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", identifier):
                raise DownloadError("Invalid confirmation identifier.")
            try:
                day = parse_date(row.get("confirmationDate", ""))
            except (argparse.ArgumentTypeError, TypeError):
                raise DownloadError("Invalid confirmation date; review broker coverage.") from None
            key = (str(kind), identifier)
            if start <= day <= end and key not in seen:
                selected.append((str(kind), identifier, day))
                seen.add(key)
        succeeded = failed = 0
        for kind, identifier, day in selected:
            is_option = kind == "STOCK OPTIONS"
            query = urlencode({"eId": employee, "tId" if is_option else "cId": identifier})
            endpoint = "getExerciseConfirmation.pdf" if is_option else "getReleaseConfirmation.pdf"
            url = f"{ORIGIN}/webapisp/stockplan/pdf/{endpoint}?{query}"
            try:
                content = fetch(url, capture.headers)
                if not valid_pdf(content):
                    raise DownloadError("Response is not a complete PDF download.")
                name = f"{day.isoformat()}_{kind.lower().replace(' ', '_')}_{identifier}.pdf"
                save_original(output / name, content)
                succeeded += 1
            except (DownloadError, OSError) as error:
                report_error(error)
                failed += 1
        print(
            f"Selected confirmations: {len(selected)}; saved/unchanged: {succeeded}; failed: {failed}."
        )
        print(
            "Verify source coverage in the broker; separate trade confirmations are not included."
        )
        return 1 if failed else 0
    except (DownloadError, OSError, ValueError, TypeError) as error:
        report_error(error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
