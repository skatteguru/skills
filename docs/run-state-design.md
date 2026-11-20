# Proposed run-state format

Development proposal for future download/import helpers. This is not an implemented
schema or a requirement for agents using the current skill. Define and validate
the actual schema before implementing helpers that depend on it.
Current agents should follow the [progress guidance](../skills/swedish-k4-tax/references/run-state.md).

Keep the workspace outside the skill/repository. It contains financial records
and is private even when it excludes authentication secrets. Reuse it only for the
same taxpayer and requested environment; do not infer identity from the folder name.

## Run fields

- `schema_version`, random `run_id`, package/helper versions and timestamps.
- Environment, income year, filing year and pseudonymous taxpayer/account references.
- Requested brokers, account types, periods, source roles and discovered capability
  results. Separate requested range from actual observed coverage.
- Inventory completeness per source/account/period: unknown, partial, complete or
  not applicable, with reasons and expected/observed counts where available.
- Review baseline, unresolved issues, export metadata and filing outcomes.

## Document fields

Stable local key, broker/account reference, source document ID/type/date, role(s),
relative original file path, MIME type, byte size, SHA-256, requested/observed period,
Skatteguru file ID, duplicate-of ID, download/transfer/processing outcomes, parsed
financial/evidence counts, and redacted retry/error details. Validate paths stay
within the run workspace before helpers read or write them. Do not overwrite an
existing original whose bytes differ.

Document stages are independent: inventoried → downloaded → validated → prepared
→ transferred → processed → reconciled. Record failures and pending stages without
erasing prior success. Prepared does not mean uploaded; processed does not mean
reviewed. Do not derive cross-account identity from filename or checksum alone.

## Export and filing fields

Reviewed analysis revision or explicit lack of one, year, totals, artifact paths
and hashes, review time, approval scope/time, target service and receipt reference.
Track exported, draft-imported, transfer-accepted and signed separately. Mark review
and filing approval stale when underlying records/artifacts change. On resume,
revalidate file hashes, current ledger state and prior outcomes before mutations.

Never persist broker cookies, bearer tokens, passwords, cURL captures or signed
upload URLs in the durable manifest. Store short-lived request/transfer instructions
separately with private access and remove them after use, including failure exits.
Atomic updates/checkpointing and a schema validator are planned acceptance criteria,
not guarantees supplied by this prose contract.
