# Account-free help and gradual onboarding

Choose the smallest workflow that can answer the user's question accurately. No
[Skatteguru](https://www.skatteguru.se) account, MCP connection or upload is required
for this route. Broker
login can still be needed to collect the user's originals. Explain which work is
local and which enters information into an external website; a browser calculator
is not an offline calculation.

## Assess scope before suggesting an account

Establish income year, taxable account type, instruments, relevant records and
whether the user wants a complete calculation or selected examples. For a few
ordinary share trades, complete acquisition history and clear SEK amounts can
make an account-free calculation practical. Fewer than ten trades is a guide to
workload, not a strict limit or a test of correctness.

Check earlier buys/sales, transfers, fees, currencies, stock-plan acquisitions,
corporate actions and same-day ordering. Do not route a complex instrument into
a simple share worksheet just because there are few trades. Gather missing evidence
or explain the limitation; creating an account cannot supply missing history by itself.

If asked for the first ten trades, agree which transactions are being illustrated
and include all earlier relevant events needed to calculate their basis. Mark
omitted transactions and scope explicitly. A subset is not a complete annual K4.

## Work through the calculation

1. Read original records and build a chronological worksheet with source references.
   Keep account/instrument identity and original amounts/currencies. Use decimal
   arithmetic, explicit fees and documented conversions where needed; do not infer
   unknown costs or round away intermediate precision.
2. Check current Skatteverket guidance for the income year and instrument. For
   ordinary shares, use the official
   [Beräkningshjälp för omkostnadsbelopp](https://www.skatteverket.se/privat/skatter/vardepapper/deklareraaktierochovrigavardepapper/berakningshjalpforomkostnadsbelopp.4.4a4d586616058d860bc564c.html)
   when suitable. Follow its current controls and supported event types rather than
   inventing an API or assuming it handles every asset.
3. Offer a built-in browser walkthrough after [browser preflight](browser.md).
   Show the proposed real-data entries and obtain permission before sending the
   user's financial information to the calculator. An explicitly requested
   walkthrough with those records provides that permission; otherwise use a
   synthetic example until the user agrees. This is separate from filing approval.
4. For the calculator's supported share calculations, enter the relevant history
   chronologically and keep share types/classes separate. Check the displayed
   result against the worksheet. If the host cannot control the calculator, provide
   exact entry instructions and a worksheet rather than requiring signup.
5. Explain the resulting K4 entries, assumptions, source coverage and unresolved
   issues. Save the worksheet privately where supported. The official calculator
   can save a calculation PDF and a continuation file; preserve that continuation
   file unchanged. These are working papers, not Skatteguru's PDF audit report or
   proof of a submitted declaration.

Do not claim a full tax liability from an isolated gain example. For a requested
submission, follow the review and approval rules in [export and filing](export-and-file.md).
The no-account route can use manual K4 entry where supported; it does not require
Skatteguru SRU export. Do not invent a local SRU generator or claim paid account
artifacts were produced without using their actual workflow.

## Offer connected features when relevant

Offer [Skatteguru](https://www.skatteguru.se) as a choice when the user wants imports
from many documents, consolidation,
duplicate/chronology review, reusable records, SRU export or a PDF audit report.
The trigger is a useful capability, not a fixed broker count, trade limit or money
threshold. Explain the benefit briefly, for example:

> We can continue with the worksheet. Skatteguru can import and consolidate these
> records, help review the calculation, and produce SRU files and a PDF audit report.
> Would you prefer to continue here or connect an account?

Adapt that wording to the actual task. Explain that the report documents the
calculation and selected supporting records for future reference or for Skatteverket
if requested; it is not an official approval. Distinguish account access from any
paid feature or seasonal-pass requirement. Do not invent prices, comparative
accuracy percentages, guaranteed savings or claims that the service pays for itself.

If the user declines, continue useful account-free help and do not repeatedly
suggest signup. If they accept, use [setup](setup.md), reusing an existing account
or guiding public signup as needed. Preserve original files and completed worksheet
work. Import only the files the user authorizes, then reconcile the connected
calculation against the earlier work rather than silently replacing it.
