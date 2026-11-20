# Interactive Brokers

Status: detailed browser workflow instructions; no dedicated downloader bundled. The
2026-11-20 browser investigation recommended Activity Statement CSV for current
use. Validate deployed parser coverage and the actual downloaded report; the
existence of this guide does not establish support for every asset or section.

## Preferred collection route

Run [browser preflight](../browser.md) for navigation, login and file downloads.
This route does not require full CDP; use normal browser controls and do not ask
the user to enable it. Use Client Portal and let the user handle login/session renewal.

1. Open **Performance & Reports → Statements**.
2. Under **Default Statements**, select **Activity Statement → Run**.
3. Choose **Annual** and the required income year, then **Download CSV**.
4. Download relevant earlier years for acquisition history. If the needed period
   cannot be obtained annually, use available custom periods and record coverage.
5. Preserve the original CSV, section headers, account/currency information and
   actual date range. Use the PDF as a comparison exhibit if helpful, not as a
   replacement for the supported machine-readable export.

Check account selection, period, nonempty expected sections, row/detail levels
and truncation. An account with no securities trades can legitimately have cash
activity only; that is not evidence that a trade parser supports populated trading
histories. Expired login and unavailable archived years are distinct conditions.

## Activity, Flex and supplementary evidence

Activity describes report coverage; Flex describes customization. Avoid making
the user configure a Flex Query when the ordinary Activity Statement suffices.

| Export | Role |
| --- | --- |
| Activity Statement CSV | Preferred primary source; inspect supported trades, cash and lifecycle sections |
| Activity Flex CSV | Supplemental lot/detail evidence only when required and its exact schema is supported |
| Trade Confirmation Flex | Optional execution evidence; not the default whole-account workflow |
| Activity Flex XML | Planned richer option; do not recommend it as supported without deployed confirmation |

Verify support for the exact Activity Statement or supplemental Flex format through
the live service and public documentation. Do not infer blanket Flex CSV/XML support.
For a required Flex export, specify the supported sections, fields, detail levels,
cash categories, account and base currency. “Select All” fields does not select
all transaction categories. Avoid collecting all Account Information fields:
addresses, birth dates and beneficiaries are unnecessary for this workflow.

Review trades, commissions/currencies, corrections, identifiers, transfers,
corporate actions, opening positions and any instruments the deployed parser
does not support. Reconcile execution/order rows against lot/summary rows so
the same trade is not posted repeatedly. Never import IBKR's tax-lot cost basis
as Swedish average acquisition cost without the canonical analysis.

Use [MCP review](../mcp-review.md). When reports overlap, compare financial events
and evidence roles. Request specific earlier records or verified opening history
instead of silently inventing basis. Historical availability varies; do not promise
a universal archive cutoff. A Flex Web Service downloader is a future optional
route, not a reason to ask for an API token in chat.

## Sources

- [Skatteguru guide](https://www.skatteguru.se/help-center/import/ibkr-csv)
- [IBKR Flex overview](https://www.ibkrguides.com/clientportal/performanceandstatements/flex.htm)
- [Activity Flex sections](https://www.ibkrguides.com/reportingreference/reportguide/activity%20flex%20query%20reference.htm)

Some older Skatteguru instructions recommend Trade Confirmation Flex. If the
current guide and observed deployment disagree, identify that conflict and verify
accepted records before choosing a different route.
