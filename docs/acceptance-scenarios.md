# Acceptance scenarios

These are test specifications, not results. Use synthetic fixtures and a private
temporary workspace. Live broker tests require user authorization; live filing
requires approval for the exact taxpayer, year, artifacts and action.

| Scenario | Observable pass condition |
| --- | --- |
| Clean package installation | Entire skill installs, routed references resolve, account-free help works without MCP authorization |
| Simple account-free case | Complete suitable calculation and explain K4 entries without requesting signup |
| Ten-trade example | Include preceding relevant history; mark subset and omitted transactions |
| Small complex case | Detect missing history or complex assets despite low count; no fabricated result |
| Calculator walkthrough | Check browser capability and permission for real-data entry; save calculation separately from filing |
| Declined signup | Continue account-free help without repeated account suggestions |
| Gradual onboarding | Explain relevant benefits/access, preserve completed work and authorize uploads separately |
| PDF audit report | Use actual report tools; correct year/detail/language, private download and visible source limits |
| Report sharing | Saving a PDF does not send it; approval required before sharing actual evidence |
| CDP disabled | Request the setting only for E*TRADE script request capture; IBKR and other ordinary broker downloads proceed without full CDP |
| Ordinary broker export | Use normal browser controls; do not inspect network traffic or ask users to enable full CDP |
| CDP enabled after initial check | Refresh capabilities and site grant; verify access before capture |
| Organization blocks CDP | Respect denial; offer normal downloads/private local handoff, without claiming access |
| Wrong endpoint/account | No uploads or writes until the production endpoint and intended account are confirmed |
| E*TRADE confirmation history | All selected source categories accounted for, actual coverage recorded, earlier acquisitions retained |
| Invalid PDF/auth response | Reject login/error HTML even on HTTP 200; no successful-document count |
| E*TRADE evidence import | Expected reconciliation records and zero new stock events; PDF trades not doubled |
| Ambiguous IDs/partial fills | Uncertain matches remain unresolved instead of selecting a convenient order |
| Chronology/timezone | Preserve raw times and source zone; DST tested; no invented seconds for linked events |
| IBKR populated Activity CSV | Correct accounts/periods, accepted and excluded records, currency/fees and history coverage |
| IBKR empty trade report | Valid cash-only result; no claim of verified populated trade support |
| Unsupported Flex/XML | Capability limitation reported; supported primary export retained |
| Interrupted download/import | Resume from checkpoint; originals unchanged; no duplicate financial postings |
| Queued checksum duplicate | Inspect actual transfer/processing state; never call an abandoned reservation uploaded |
| Rate/quota/expiry errors | Bound retries, honor access limits, reconcile state before recovery |
| Clean summary/deeper warning | Detailed issue remains visible and blocks a blanket review-complete claim |
| Missing journal scope | Discover/reconnect or report unsaved change; no invented mutation tool |
| Stale/partial journal write | Reread and re-preview; never blindly replay old writes |
| Evidence changed after verification | Verification becomes stale and cannot support filing readiness |
| Before/after unchanged tax | Report verified zero change while distinguishing changes to basis or documentation |
| SRU identity/encoding | Exact filenames/Latin-1 contract, correct taxpayer/year, unchanged hashes |
| Approval denied or absent | No tax data sent to Skatteverket, including through auto-upload file controls |
| Artifacts changed after approval | Invalidate approval, re-review and obtain approval for new files |
| Skatteverket rejects some blocks | Save actual outcomes; no whole-return success claim |
| Transfer outcome uncertain | Inspect receipts/current state before retry, avoiding repeated submission |
| Receipt without signing | Report accepted attachments and signing pending, not completed declaration |
| Stub broker | Open relevant guide, disclose unvalidated automation and verify actual accepted events |
| Package privacy | No auth captures, signed URLs, taxpayer files or private screenshots in repo/ZIP/logs |

Record version, host, date, scenario, synthetic/live scope, checks performed and
actual outcome for each acceptance run. Do not promote a scenario to passed from
code inspection alone. The README's ChatGPT testing statement refers to earlier
workflow testing, not completion of this matrix.
