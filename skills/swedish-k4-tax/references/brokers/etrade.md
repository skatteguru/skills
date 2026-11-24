# E*TRADE / Morgan Stanley stock plans

Status: bundled confirmation and order-history helpers, maintained here and tested
with synthetic offline responses. Live authenticated verification of these versions
is pending. Python 3.10+ is required; no third-party packages are needed. No MCP
transfer, automatic resume or journal verification is performed by these scripts.

## Access policy and user choice

The [E*TRADE Security Center](https://us.etrade.com/security-center) AI-agent FAQ
requires Morgan Stanley's written authorization for AI-agent access to its systems.
It states that users remain responsible for agent actions even when authorized,
that access may be restricted or terminated, and that losses resulting from agent
activity are excluded from the Customer Protection Guarantee. This is a public
policy summary checked against official indexed text on 2026-11-24; recheck the
current policy for the proposed route. No stock-plan PDF-download exception was
established by this review.

Offer user-performed downloads and processing of the resulting files. Built-in
browsing, computer use and authenticated helpers require the same
[broker-policy preflight](../browser.md), including applicable written authorization
and robots checks. Neither read-only tax collection, a user-created request capture
nor user acceptance of risk establishes an exception. Bundled scripts and offline
tests establish no broker permission. Do not ask for login or CDP access before
resolving the policy condition.

## Collect

Run [browser preflight](../browser.md) and honor the selected permitted method.
For manual collection, guide the user through the routes below without accessing
the account. User logs in and handles verification. Establish required historical
coverage through December 31 of the income year, including relevant earlier
acquisitions. Supply the dates explicitly to the helpers.

| Source | Purpose | Route |
| --- | --- | --- |
| Restricted Stock confirmations | Acquisitions from vesting/release | Account → Quick links → Stock plan confirmations; custom dates, Restricted Stock, Apply/View all |
| Stock Options confirmations | Exercises and included same-day sales | Repeat stock-plan route for Stock Options |
| Separate Trade Confirmations | Independent buys/sales missing from exercise records | Documents → Trade Confirmations; each relevant year; guide documents batches of up to 12 |
| Order-history JSON | Reconciliation and execution evidence | `etrade_orders.py`, explicit years or date range |
| Cash activity | Separate currency-account work when requested | Linked cash-activity guide; not covered by confirmation downloader |

Use the bulk route for large collections only when broker permission, user consent,
robots checks and host capability support it. Capture
the required authenticated request through approved CDP/network tools. The
confirmation helper uses `confirmations.json`; the order helper targets
`/webapisp/stockplan/ah/orders.json`. Verify its required payload and account
selection instead of assuming any captured request works for both endpoints.

## Run the bundled helpers

Scripts are included in the installed skill:

- [etrade_download.py](../../scripts/etrade_download.py): confirmation PDFs.
- [etrade_orders.py](../../scripts/etrade_orders.py): original order-history JSON.
- [etrade_common.py](../../scripts/etrade_common.py): shared request/file handling;
  keep it beside both entry points.

From the installed skill directory, replace the example paths and dates with the
user's private workspace and required history:

```sh
python3 scripts/etrade_download.py \
  --start-date 2019-01-01 --end-date 2025-12-31 \
  --output-dir /path/to/private-tax-records/confirmations \
  --request-file /path/to/private-confirmations-request.txt

python3 scripts/etrade_orders.py \
  --years 2024 2025 \
  --output-dir /path/to/private-tax-records/orders \
  --request-file /path/to/private-orders-request.txt
```

Both accept a start/end date range; orders also accepts explicit `--years` instead.
Dates accept YYYY-MM-DD or MM/DD/YYYY. There is no default year or history cutoff.
The confirmation request must come from confirmations.json; the order request
must come from orders.json. Preserve the account selection and use the matching
capture, rather than assuming the two request bodies are interchangeable.

`--request-file` consumes and removes the temporary capture after reading, even if
parsing fails. Capture afresh for a retry. If no request file is supplied, the helper
reads stdin; the caller must remove any file redirected into stdin. Clean up unused
captures after argument errors, cancellation or host failures. Never paste the
captured request into chat, print it, or shell-execute its cURL text.

Use private outputs outside the skill/repository. Credentials are used only for
HTTPS requests to E*TRADE's stock-plan endpoints, and redirects are rejected. The
helpers use bounded responses/timeouts and static error messages; they never print
employee IDs, cookies or response bodies. Invalid PDFs are rejected by basic
signature/trailer checks. JSON must have a recognized record envelope. Known
pagination/count gaps produce a failure instead of a completeness claim. New
response formats may need a script update; do not weaken validation to force success.

Partial download failures return a nonzero exit code. Successful files remain;
rerunning may fetch them again but leaves identical originals unchanged and refuses
to overwrite different bytes. There is no resumable manifest, inventory-only mode,
automatic retry/pagination or upload helper yet. Save progress using
[progress guidance](../run-state.md) and verify actual broker coverage before import.
Zero selected confirmations or order records is not proof that all required
history was obtained. Separate trade confirmations and cash activity still need
their documented browser routes.

## Reconcile orders and PDFs

Preserve original PDFs and JSON, hashes, requested/observed coverage and account
reference. Validate PDF structure and JSON envelope/application errors. Check
pagination/truncation; no guarantee of complete history follows from one response.
Report each source category as collected, missing or not applicable.

Treat order exports as reconciliation and execution evidence. Check the live
service's supported format and document context before import. If the service
supports evidence-only imports, verify reconciliation counts and contents rather
than expecting new stock events. Confirm which order statuses are included and
report exclusions. Uploading JSON does not prove timestamps were applied to the
canonical journal.

Match by account and stable broker IDs when available, then symbol, date,
transaction type, quantity and amounts. Do not equate all identifier fields or
match solely by date. Preserve ambiguity, partial fills and linked exercise/sale
groups. Compare order inventory with PDFs to find separate historical sales.
Option confirmations and trade confirmations may describe the same sale; review
duplicate results without deleting original evidence automatically.

Execution timestamps can resolve same-day acquisitions and disposals. Preserve
the original timestamp, explicit timezone/offset and provenance. A timezone-free
value is not UTC. Compare with expanded Orders → Order History “Order Executed”
records if needed; do not use order-placement time as execution time. Apply
America/New_York daylight-saving rules only when the source timezone is established.
Do not invent seconds to order linked exercise and sale events sharing a timestamp.

Use [MCP review](../mcp-review.md) to preview supported corrections. Linked-group
writes and evidence verification may be unavailable; report exactly what remains
unsaved. Never mark an order verified merely because its JSON parsed successfully.

## Guides

- [Required documents](https://www.skatteguru.se/help-center/import/etrade-documents)
- [Execution times](https://www.skatteguru.se/help-center/import/etrade-documents/execution-time)
- [Cash activity](https://www.skatteguru.se/help-center/import/etrade-documents/cash-management-activity)
- [Parsing](https://www.skatteguru.se/help-center/how-it-works/etrade-parsing)
