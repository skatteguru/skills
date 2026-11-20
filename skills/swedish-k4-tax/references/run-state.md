# Track progress and resume work

Use this guidance when a task spans many files, is interrupted, or needs a handoff.
The purpose is to remember what has actually finished and what remains. This skill
has no automatic checkpoint or resume tool yet; do not claim progress was saved
unless you created a record the host can retrieve.

## Keep a short progress note

If the host can save files, keep a private progress note beside the user's working
files, outside the installed skill and its repository. If it cannot, give the user
a concise handoff summary. Do not create a formal manifest just to follow this
reference; there is no required file format today.

Record only what is needed to continue:

- The income year, brokers, account references and chosen account-free or connected
  route. Note the Skatteguru connection only when one is used.
- What history was requested, what was collected and any missing periods.
- Files still needing transfer, processing or review, with Skatteguru file IDs
  where available. Keep checksums when computed for upload or export.
- Unresolved review issues and the next useful action.
- Exported SRU files, whether filing was approved, and any observed receipt or
  signing status. Preserve enough detail to identify the exact approved files.

For example, a progress note might say:

| Item | Confirmed status | Next action |
| --- | --- | --- |
| IBKR 2025 Activity Statement | Downloaded; not uploaded | Prepare and transfer the original CSV |
| E*TRADE confirmations | Uploaded; two still processing | Check those document IDs |
| Earlier acquisition history | 2022 records missing | Collect the missing report |
| SRU and filing | Not started | Finish import review first |

Keep these distinctions clear: downloaded is not uploaded; upload preparation is
not a completed transfer; processed is not reviewed; SRU export is not filing; a
transfer receipt is not proof that the whole declaration was signed.

## Before continuing an interrupted task

1. Read the note and confirm that it belongs to the intended taxpayer, accounts,
   income year and chosen route. For connected work, verify the account and endpoint.
   Do not infer identity from a folder name.
2. Check the local files and current Skatteguru document statuses. Use the existing
   file IDs to investigate pending work instead of uploading everything again.
3. Reconcile uncertain transfers before retrying. Preserve originals and do not
   overwrite a file whose contents differ from the saved copy.
4. Recheck the current analysis before relying on an earlier review. If financial
   records or SRU files changed, review again and obtain approval for the changed
   filing artifacts. Reuse an existing approval only for its unchanged scope.
5. Update the note with confirmed outcomes and the next action. Distinguish facts
   you checked now from earlier notes that still need verification.

The progress note itself contains private financial information. Keep passwords,
cookies, bearer tokens, captured requests and signed URLs out of it. Authentication
captures and temporary transfer instructions need separate private handling and
cleanup as described in [browser preflight](browser.md).
