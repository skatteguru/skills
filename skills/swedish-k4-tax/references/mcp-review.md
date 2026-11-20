# Import and review through MCP

Discover actual tools, schemas, scopes and environment first. Names below are
unprefixed examples of the known surface, not promises about a connection.

## Inspect the account

Use `search_documents`/`list_documents` to establish relevant existing imports.
Follow pagination with the tool that returned the token. Use `get_document` for
metadata/status, and `get_document_context` with extracted text/parsed data only
for relevant evidence. Respect truncation and request a full read when necessary.
Do not dump whole ledgers or personal documents into output.

## Transfer original files

Prepare only files authorized for upload and only when exact bytes and HTTP PUT
are available. Otherwise explain the limitation and offer Skatteguru's document
page on the connected environment. Respect a user request for MCP-only operation;
do not silently replace it with browser upload.

1. Read original bytes, compute SHA-256/size, identify MIME type and allocate a
   stable UUID for the file. Use `application/pdf`, `text/csv`, `application/json`
   or the appropriate spreadsheet MIME type according to the live schema.
2. Call `prepare_document_upload` with the required identity, name, type, size
   and checksum. Inspect tool errors and per-file errors. Batch preparation is
   planned; use it only if actually exposed. Prepare small chunks ready to transfer.
3. For `async_upload`, send the same bytes immediately using the returned method
   and every required header. The host performs this transfer; MCP prepares it.
   Do not attach broker cookies or Skatteguru OAuth credentials to storage URLs.
   Keep signed URLs private and require a successful HTTP result.
4. For `duplicate`, inspect `original_file_id` and status. A queued duplicate can
   be an abandoned preparation, not a completed upload. For `inline_ingest`, inspect
   the actual result rather than claiming an unperformed transfer.
5. Retry a failed transfer with its same valid instructions when safe. Do not
   allocate new IDs or change bytes to evade deduplication. If instructions expire
   or the outcome is unknown, reconcile status before a documented recovery action.
6. Poll status conservatively, respecting rate limits and Retry-After. Finish on
   `done`, `manual_review` or `error`; persist pending work and resume without
   re-uploading. Initial observation can stop after about two minutes with explicit
   pending IDs; when asked to watch completion, continue bounded checks and report
   meaningful changes rather than abandoning the requested monitoring.

Quota/access errors should present the returned upgrade link for user action.
Recheck confirmed access after payment; do not make purchases or infer success
from a checkout redirect. No bundled transfer helper exists in this release.

## Small inline canonical CSV

For CSV text up to the live inline limit (currently 8,000 UTF-8 bytes), read
[Canonical CSV v1](canonical-csv-v1.md), preview with `preview_csv_import` if
exposed, then pass exact unchanged content to `import_csv_document`. Larger CSV
and original broker files use prepared uploads. Do not gzip text to fit the limit.

Reuse an idempotency key only for an exact retry with unchanged content and
interpretation. Changed content conflicts with an existing key; validation failures
can also bind the key, so corrected content needs a new key. The same CSV with a
different key creates another document and does not repair the earlier one. Inspect
accepted/event counts, status and duplicate outcomes before claiming success.

## Financial and evidence review

Use `get_processing_issues`, `get_symbol_summary`, `get_tax_year_summary` and
`analyze_tax_year` as available. Also run `list_trade_order_issues`; a clean compact
summary does not imply there are no chronology issues. Explain tools unavailable
because of permissions or deployment rather than claiming a clean review.

Reconcile source inventory, imported documents, parsed financial events and evidence
records separately. Inspect dates, quantities, gross/net amounts, fees, currencies,
account identity, acquisition history, transfers, corporate actions, duplicates
and negative holdings. A processed trade file with zero events is not a successful
financial import. E*TRADE orders or supported IBKR supplemental lot evidence can
correctly produce zero stock events: verify reconciliation counts and contents.

If the broker evidence disagrees with parsed events, retain the original and
identify the exact discrepancy. Do not silently repair originals or delete a
duplicate document merely because it overlaps. Use a documented correction path.

## Chronology and corrections

Capture a canonical baseline before changes: year, analysis revision when exposed,
realized gains/losses, calculated tax, closing basis/positions, warnings and issues.
Use `preview_trade_reorder` and actual source evidence for the full ordered event
sequence. Preserve linked exercise/sale groups and distinguish source order from
comparable execution times. A cost-basis range is not a tax range.

Show the proposed sequence, evidence and any timestamp edits. `apply_trade_reorder`
requires tax reads, opt-in document-write permission and a matching preview token
under the current contract. Honor its confirmation requirements and existing user
authorization. If linked groups are rejected or the write is not exposed, report
the correction as unsaved. Do not invent artificial times to force acceptance.
If a write partially succeeds, reread current state and obtain a fresh preview
before retrying. Do not replay the old proposal blindly.

After a confirmed change, rerun canonical analysis and compare before/after gains,
tax and carry-forward basis, including later affected years where supported.
State zero monetary change explicitly if verified. An expected zero change is not
a verified post-change result. Formal evidence attachment/verification and frozen
comparison APIs require supported backend capabilities; do not pretend they
exist or label agent review as verification by Skatteverket.

[K4 review](https://www.skatteguru.se/help-center/filing/k4-guide)
and [duplicate review](https://www.skatteguru.se/help-center/filing/deduplication).
