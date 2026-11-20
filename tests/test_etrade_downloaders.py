"""Offline behavioral tests; all network responses and credentials are synthetic."""

from __future__ import annotations

import contextlib
import io
import json
import shlex
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/swedish-k4-tax/scripts"))

import etrade_common as common  # noqa: E402
import etrade_download as confirmations  # noqa: E402
import etrade_orders as orders  # noqa: E402

SECRET = "SYNTHETIC-SESSION-DO-NOT-LOG"
PDF = b"%PDF-1.7\nsynthetic fixture\n%%EOF\n"


def capture(endpoint: str) -> str:
    body = json.dumps({"value": {"encryptedEmployeeId": SECRET, "accountSelector": "test"}})
    return (
        f"curl 'https://us.etrade.com/webapisp/stockplan/ah/{endpoint}.json' "
        f"-H 'Cookie: {SECRET}' --data-raw {shlex.quote(body)}"
    )


def inventory() -> bytes:
    return json.dumps(
        {
            "data": {
                "confirmation": {
                    "confirmations": [
                        {
                            "planTypeCode": "Restricted Stock",
                            "confirmationId": "123",
                            "confirmationDate": "01/02/2025",
                        },
                        {
                            "planTypeCode": "STOCK OPTIONS",
                            "confirmationId": "456",
                            "confirmationDate": "02/03/2025",
                        },
                        {
                            "planTypeCode": "Restricted Stock",
                            "confirmationId": "789",
                            "confirmationDate": "01/02/2026",
                        },
                    ]
                }
            }
        }
    ).encode()


class DownloadTests(unittest.TestCase):
    def test_capture_parsing_preserves_private_values_without_execution(self) -> None:
        value = common.parse_capture(capture("confirmations"))
        self.assertEqual(value.headers["cookie"], SECRET)
        self.assertEqual(value.payload["value"]["encryptedEmployeeId"], SECRET)
        with self.assertRaises(common.DownloadError):
            common.parse_capture(capture("orders") + " ; echo PRIVATE")

    def test_rejects_foreign_origin_and_trading_endpoint(self) -> None:
        for text in (
            capture("orders").replace("us.etrade.com", "example.invalid"),
            capture("orders").replace("https://", "http://"),
            capture("orders").replace("/orders.json", "/placeOrder.json"),
        ):
            with self.subTest(text=text), self.assertRaises(common.DownloadError):
                common.parse_capture(text)

    def test_consumed_capture_is_deleted_even_when_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "request.txt"
            path.write_text("not a valid request")
            with self.assertRaises(common.DownloadError):
                common.read_capture(path)
            self.assertFalse(path.exists())

    def test_redirect_and_auth_errors_do_not_expose_response_or_url(self) -> None:
        for status in (302, 401, 403):
            error = HTTPError(f"https://example.invalid/{SECRET}", status, SECRET, {}, None)
            with patch.object(common, "build_opener") as opener:
                opener.return_value.open.side_effect = error
                with self.assertRaises(common.DownloadError) as result:
                    common.fetch("https://us.etrade.com/webapisp/stockplan/ah/orders.json", {})
                self.assertNotIn(SECRET, str(result.exception))
                self.assertIn(str(status), str(result.exception))
        self.assertIsNone(common.NoRedirect().redirect_request(None, None, 302, "", {}, ""))

    def test_incomplete_or_error_envelopes_are_not_successful(self) -> None:
        for metadata in (
            {"hasMore": True},
            {"totalCount": 2},
            {"error": SECRET},
            {"success": False},
        ):
            payload = {"data": {"pse": {"list": [{"tradeId": 1}], **metadata}}}
            with self.subTest(metadata=metadata), self.assertRaises(common.DownloadError):
                common.records(payload, orders.ORDER_PATHS)
        with self.assertRaises(common.DownloadError):
            common.records({"data": {"pse": {"list": [1]}}}, orders.ORDER_PATHS)

    def test_preserves_originals_and_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "file.pdf"
            common.save_original(path, PDF)
            common.save_original(path, PDF)
            with self.assertRaises(common.DownloadError):
                common.save_original(path, b"changed")
            self.assertEqual(path.read_bytes(), PDF)
            link = Path(temp) / "link.pdf"
            link.symlink_to(path)
            with self.assertRaises(common.DownloadError):
                common.save_original(link, PDF)
            self.assertEqual(list(Path(temp).glob(".download-*")), [])

    def test_confirmation_download_respects_dates_and_preserves_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            request = Path(temp) / "request.txt"
            request.write_text(capture("confirmations"))
            output = Path(temp) / "docs"
            with patch.object(confirmations, "fetch", side_effect=[inventory(), PDF, PDF]) as fetch:
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    result = confirmations.main(
                        [
                            "--start-date",
                            "2025-01-01",
                            "--end-date",
                            "2025-12-31",
                            "--output-dir",
                            str(output),
                            "--request-file",
                            str(request),
                        ]
                    )
            self.assertEqual(result, 0)
            self.assertEqual(len(list(output.glob("*.pdf"))), 2)
            self.assertTrue(all(p.read_bytes() == PDF for p in output.glob("*.pdf")))
            self.assertEqual(fetch.call_args_list[0].args[2]["value"]["endDate"], "12/31/2025")
            self.assertNotIn(SECRET, stdout.getvalue())
            self.assertFalse(request.exists())

    def test_invalid_pdf_is_failure_and_not_written(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "docs"
            with patch.object(
                confirmations, "fetch", side_effect=[inventory(), b"<html>login</html>", PDF]
            ):
                with patch("sys.stdin", io.StringIO(capture("confirmations"))):
                    with (
                        contextlib.redirect_stdout(io.StringIO()),
                        contextlib.redirect_stderr(io.StringIO()),
                    ):
                        result = confirmations.main(
                            [
                                "--start-date",
                                "2025-01-01",
                                "--end-date",
                                "2025-12-31",
                                "--output-dir",
                                str(output),
                            ]
                        )
            self.assertEqual(result, 1)
            self.assertEqual(len(list(output.glob("*.pdf"))), 1)

    def test_unsafe_confirmation_id_cannot_escape_output(self) -> None:
        data = json.loads(inventory())
        data["data"]["confirmation"]["confirmations"][0]["confirmationId"] = "../../escape"
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(confirmations, "fetch", return_value=json.dumps(data).encode()):
                with patch("sys.stdin", io.StringIO(capture("confirmations"))):
                    with contextlib.redirect_stderr(io.StringIO()):
                        result = confirmations.main(
                            [
                                "--start-date",
                                "2025-01-01",
                                "--end-date",
                                "2025-12-31",
                                "--output-dir",
                                str(Path(temp) / "docs"),
                            ]
                        )
            self.assertEqual(result, 1)
            self.assertFalse(list(Path(temp).rglob("*.pdf")))

    def test_orders_partial_failure_returns_nonzero_and_keeps_original_json(self) -> None:
        raw = b'{"data": {"pse": {"list": [{"tradeId": 1, "executionDate": "20250102123456"}]}}}'
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(
                orders, "fetch", side_effect=[raw, common.DownloadError("HTTP 403")]
            ) as fetch:
                with patch("sys.stdin", io.StringIO(capture("orders"))):
                    with (
                        contextlib.redirect_stdout(io.StringIO()) as stdout,
                        contextlib.redirect_stderr(io.StringIO()),
                    ):
                        result = orders.main(["--years", "2025", "2026", "--output-dir", temp])
            self.assertEqual(result, 1)
            self.assertEqual(
                (Path(temp) / "orders_2025-01-01_to_2025-12-31.json").read_bytes(), raw
            )
            self.assertEqual(fetch.call_args_list[1].args[2]["value"]["startDate"], "01/01/2026")
            self.assertNotIn(SECRET, stdout.getvalue())

    def test_no_implicit_dates_or_mixed_years(self) -> None:
        for module, args in (
            (confirmations, ["--output-dir", "/unused"]),
            (orders, ["--years", "2025", "--start-date", "2025-01-01", "--output-dir", "/unused"]),
        ):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                module.main(args)
            self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
