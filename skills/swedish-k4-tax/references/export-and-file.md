# SRU export, PDF audit report and approved filing

For account-free calculations, use [account-free help](account-free.md). Manual K4
entry can proceed without MCP or Skatteguru SRU export. Apply the approval and
verification rules below to any real filing, including manual browser entry.

## Review and export

For the connected route, read [MCP review](mcp-review.md). Confirm income year, taxpayer, source coverage
and unresolved issues before calling the result ready. Distinguish the supported
investment/K4 calculation from unrelated parts of the whole declaration.

Use `get_tax_year_access`, then `prepare_tax_export` with the actual required
identity fields from the live schema. Obtain the user's name and personal number
only when needed; do not infer them from another person's documents or store them
in skill files. If access requires a seasonal pass, open the returned purchase URL
for the user, recheck access afterward, and retry only after confirmation.

Handle `input_required` as unresolved input. For `ready`, save the returned original
file resources. If the response exposes only structured artifact text, preserve
its exact content using the contract's ISO-8859-1/Latin-1 encoding; do not silently
substitute UTF-8 or replace characters. Preserve `INFO.SRU` and `BLANKETTER.SRU`.
Reject unencodable content instead of transliterating identity. If the host cannot
save files, provide the returned document/download route without claiming a save.

Record private artifact paths, SHA-256 hashes, income year, reviewed totals and
analysis revision if provided. If the ledger or export changes afterward, re-review
the files before filing. Never claim revision binding is server-enforced unless
the deployed tools establish that fact.

## Save a PDF audit report

Offer the report when the user wants a lasting record of the calculations and
supporting evidence. Discover `prepare_tax_report_pdf` and `get_tax_report_pdf`
and their live schemas. Call preparation for the chosen income year; select the
user's language and detail level. Minimal detail contains essential calculation
support. Ask before selecting full detail or notes, since full reports may include
detailed journals and original source documents.

Poll with the returned report ID and retry guidance. When ready, save the exact
PDF from its private download URL without forwarding OAuth credentials to storage.
Request a fresh URL if it expires. Report generation errors and review issues;
do not claim a complete evidence package when source material was unavailable.
If tools/access are missing, explain the limitation and offer the public product
workflow where supported. Do not promise a price or access level absent evidence.

Record the report's income year, generation time, local file/hash and its relation
to the reviewed calculation. Regenerate if the financial records change. Explain
that users can retain it for future reference or supply it to Skatteverket if asked
how amounts were calculated. It does not replace K4/SRU, establish authority approval,
or authorize sending source records. Sharing the report with Skatteverket requires
the user's approval for the actual report and intended recipient.

## Choose the current Skatteverket route

Run [browser preflight](browser.md), including file-selection/upload capability.
Read the current [Skatteguru filing guide](https://www.skatteguru.se/help-center/filing/uploading-sru-files)
and [Skatteverket technical requirements](https://www.skatteverket.se/foretag/inkomstdeklaration/forredovisningsbyraer/tekniskinformationomfiloverforing.4.13948c0e18e810bfa0cca8.html).
Use the official site for login and verify the requested income year is supported
by the live service. Older-year corrections can require a different procedure;
do not assume today's regular return accepts every prior year.

The Skatteguru guide describes direct K4 import and Filöverföring, with a stated
300-sales limit on direct import. Check current limits and actual UI before choosing
the route. Do not hardcode the limit as a permanent rule. Filöverföring requires
both INFO.SRU and BLANKETTER.SRU; Skatteverket currently documents a 5.0 MB bound
and validates the received form blocks. Do not split, aggregate or modify financial
rows locally to get around a service limit; request a supported export solution.

Do not promise that a K4 sent through Filöverföring automatically appears as editable
rows in the ordinary declaration service. Verify the receipt and any required
follow-up for the chosen route; imported attachments, transferred attachments
and a signed whole declaration are different states.

## Approval before sending

Prepare everything reviewable before asking for approval. Present:

- Intended taxpayer (mask the personal number in chat), income year and purpose.
- Exact reviewed files/hashes or manual K4 entries, supported totals and unresolved issues.
- Target Skatteverket service, whether the action imports into a draft or sends
  attachments, and what signing/follow-up remains.

Obtain explicit approval for sending these files or entering/submitting the reviewed K4 data. Installing the skill, approving
CDP, uploading to Skatteguru or asking for an SRU download does not grant filing
approval. Honor a clear existing approval for the same unchanged files and action;
do not ask repeatedly. Changed files/year/taxpayer require fresh approval. If a
file-upload control itself sends the tax data, obtain approval before selecting it.

## Transfer and verify

User handles e-identification, BankID and signing. Use supported browser controls
for approved uploads; inspect displayed validation results, taxpayer/year and totals.
Do not overwrite existing draft data silently. Explain any replacement/duplicate
warning and resolve it within the approved action before proceeding.

On an uncertain response, check receipts/current state before retrying; never
blindly submit the same return again. Save the acceptance receipt privately, noting
accepted/rejected form blocks, time and the artifact hashes associated with it.
Transfer acceptance is established by the observed receipt, not a button click.

If the task includes completion of the return, help the user review remaining
steps and hand over signing. Observe the final confirmation after their handoff.
Report exactly whether SRU was exported, imported into a draft, transferred and
accepted, and whether signing was verified. Preserve an explicit pending state
if the service is closed, files are rejected, signing is unfinished or the host
cannot upload. No live Skatteverket submission is authorized by package tests.
