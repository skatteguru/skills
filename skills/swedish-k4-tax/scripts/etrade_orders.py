"""Download order-history JSON as reconciliation/execution evidence, not extra trades.

Adapted from Skatteguru's download-my-documents-from-etrade/etrade_orders.py.
Copyright (c) 2025-2026 Skatteguru. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import copy
from datetime import date
from urllib.parse import urlsplit

from etrade_common import (
    ORIGIN,
    DownloadError,
    add_arguments,
    date_range,
    fetch,
    json_response,
    prepare_output,
    read_capture,
    records,
    report_error,
    save_original,
)

ORDER_PATHS = (
    ("data", "pse", "list"),
    ("data", "pse", "orders"),
    ("data", "orders", "list"),
    ("data", "orders"),
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_arguments(parser)
    parser.add_argument("--years", nargs="+", type=int)
    args = parser.parse_args(argv)
    if args.years:
        if args.start_date or args.end_date or any(y < 1900 or y > 9999 for y in args.years):
            parser.error("Use valid --years or a start/end range, not both.")
        ranges = [(date(y, 1, 1), date(y, 12, 31)) for y in sorted(set(args.years))]
    else:
        ranges = [date_range(parser, args)]
    try:
        capture = read_capture(args.request_file)
        if not urlsplit(capture.url).path.endswith("/orders.json"):
            raise DownloadError("Capture orders.json for order-history downloads.")
        output = prepare_output(args.output_dir)
        succeeded = failed = 0
        for start, end in ranges:
            payload = copy.deepcopy(capture.payload)
            payload["value"].update(
                {
                    "startDate": start.strftime("%m/%d/%Y"),
                    "endDate": end.strftime("%m/%d/%Y"),
                    "dateRangeSet": 1,
                    "getTradeDetails": "Y",
                    "getOrderHistory": "Y",
                    "getNetProceeds": "Y",
                }
            )
            try:
                content = fetch(
                    f"{ORIGIN}/webapisp/stockplan/ah/orders.json", capture.headers, payload
                )
                rows = records(json_response(content), ORDER_PATHS)
                if any("tradeId" not in row for row in rows):
                    raise DownloadError("Order response contains unrecognized records.")
                name = f"orders_{start.isoformat()}_to_{end.isoformat()}.json"
                save_original(output / name, content)
                print(
                    f"Period {start.isoformat()} to {end.isoformat()}: {len(rows)} order records."
                )
                succeeded += 1
            except (DownloadError, OSError) as error:
                report_error(error)
                failed += 1
        print(f"Periods saved/unchanged: {succeeded}; failed: {failed}.")
        print("Verify coverage and timestamps before using these records as evidence.")
        return 1 if failed else 0
    except (DownloadError, OSError, ValueError, TypeError) as error:
        report_error(error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
