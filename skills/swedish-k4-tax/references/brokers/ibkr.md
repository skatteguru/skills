# Interactive Brokers

Use this workflow to collect an original **Activity Flex XML** report and import
it when the connected Skatteguru service supports that format. Activity Statement
CSV is the simpler whole-account export and the fallback when XML support is
unconfirmed. Read the [current Skatteguru import guide][sg-guide] and use any
available production evidence for the exact format, such as an existing document
with verified IBKR XML parser results. A file picker accepting XML or an MCP
schema listing its MIME type only verifies upload admission. Explain any gap in
deployment evidence before uploading. If the user requested Flex only, preserve
the downloaded XML and ask before substituting a different export.

## Sign in and choose the account

Start with the user's existing files or saved query, if available. For new
downloads, follow the [browser preflight](../browser.md) and honor the chosen
collection method. Use the built-in browser when available and permitted. If
authenticated automation is unavailable, open IBKR's official Client Portal for
the user or provide the same steps for their usual browser. Check applicable
IBKR terms for the account and region. IBKR's [AI integration][ibkr-ai] authorizes
specific MCP tools, and its [Flex Web Service][flex-api] retrieves saved reports
via a separate API. Assess permission to operate the signed-in browser
separately.

Hand the browser to the user for sign-in, verification and any consent screens.
The user can use their password manager locally. Keep credentials, verification
codes and Flex Web Service tokens out of chat. Resume browser control only when
the user has returned it and the authorized method permits it. Stay in reporting
screens and use normal controls and the host's download interface. This flow
requires no full CDP, authenticated request capture or trading permissions.

Choose the account and period the user intends to import. Use one account per
XML file and include relevant earlier history if needed to establish acquisition
cost or opening cash. Record the actual exported dates. If a period exceeds the
portal's available range, use contiguous supported periods and disclose any gaps.

## Run or configure Activity Flex

1. In **Performance & Reports → Flex Queries**, use the **Activity Flex Query**
   panel. Run a suitable saved query. If the saved query lacks relevant fields,
   create a separate template when authorized. Leave the original template
   intact unless the user asks to edit it.
2. Use the section profile below for a new template or to check a saved one.
   Choose **XML** under **Delivery Configuration**, keep IBKR's default date
   and time settings, then review and save the template.
3. Click **Run** beside the Activity query. Select the intended period and
   **XML**. For custom dates, set the start first, then verify both dates before
   running because IBKR can adjust the end date. Select one account and avoid
   symbol filters for a whole-account import.
4. Save the download. If delivered as a ZIP, extract only the intended report
   and use the unchanged XML entry. Use the host's actual download result or
   obtain the file from the user. A click or report preview does not verify
   that the file was downloaded.

For the selected financial sections, choose all fields within the intended
detail level when available, then leave optional personal fields out. The table
highlights fields that need particular attention.

| Section | What to select |
| --- | --- |
| Account Information | **Currency** for the account base currency. Leave personal profile fields such as name, address and birth date unselected. |
| Trades | **Execution** detail. Keep original currencies, timestamps, instrument and execution IDs, quantities, signed proceeds/net cash, commissions and their currencies, taxes, **FX Rate to Base**, and opening/closing indicators. |
| Cash Transactions | **Detail** and the relevant categories for dividends, interest, withholding, fees, deposits and withdrawals. Field selection and category selection are separate. Keep transaction IDs, currencies, dates, signed amounts and **FX Rate to Base**. |
| Transfers and Cash Report | Include both for cash reconciliation. Internal cash movements may appear only under **Transfers**. Keep transfer direction, date, ID and signed cash amount, and per-currency starting and ending trade-date balances. Leave optional personal fields out. |
| Securities Info and option lifecycle | Include **Securities Info** and **Option Exercises, Assignments and Expirations** for option activity. Keep underlying, strike, expiry, put/call and multiplier. |
| Other applicable activity | Include relevant **Corporate Actions**, **Transaction Fees**, and **Transaction Taxes**. Keep transaction/trade IDs that link related records. |
| Conversion Rates | Omit the full catalogue for all-SEK activity. Include it when dated cross-currency quotes are needed and retain row-level **FX Rate to Base** for relevant foreign-currency activity. |

Select relevant sections and detail levels. A mixed Activity Flex CSV or a
Trade Confirmation Flex export is a different format. Specific stock-lot
exports can be supplemental evidence when their schema is supported. Leave
unrelated sections out and flag unsupported events such as security transfers
or corrections for review. Cash balances, lot summaries and broker tax basis are
evidence. Use Swedish acquisition-cost rules in the tax workflow.

## Verify and upload to Skatteguru

- Check the file is original UTF-8 Activity Flex XML with a
  `FlexQueryResponse` of type `AF`, a `FlexStatements` envelope, the expected
  account and dates, base currency and relevant activity. Reject sign-in/error
  HTML and Trade Confirmation XML. Cash-only activity can have zero executions.
  Identify any missing coverage before choosing the file to upload.
- Use [Skatteguru setup](../setup.md) and [MCP transfer and review](../mcp-review.md).
  Check the intended production account and the user's authorization for this
  transfer. With the original bytes and HTTP upload capability ready, use
  `prepare_document_upload` with the XML filename, `application/xml`, original
  byte count, SHA-256 and a UUID. Follow the live schema and the 32 MiB XML
  limit. If necessary, export shorter periods from IBKR.
- Follow the returned transfer mode. For `async_upload`, send the byte-for-byte
  XML using the returned signed PUT and required headers. If the host cannot
  transfer the original, skip preparation and offer the Skatteguru Files page
  when the user permits that route. Keep the original file and receipts private.
- Track the document ID through processing. Verify the actual parser result,
  security executions and cash postings against the source. Report unsupported
  records, review issues, and any uncovered period. For overlapping reports,
  check duplicates and evidence roles before uploading another file. Never
  count summaries or uploaded bytes as additional executed trades.

## Collect Activity Statement CSV when appropriate

Open **Performance & Reports → Statements → Activity Statement → Run**.
Choose **Annual** and the income year, or an available custom date range, then
**Download CSV**. Keep the original sectioned CSV and review its account,
dates and expected activity. Use the same [MCP upload workflow](../mcp-review.md)
if the user authorizes the CSV import.

[sg-guide]: https://www.skatteguru.se/help-center/import/ibkr-csv
[ibkr-ai]: https://www.interactivebrokers.ie/en/trading/ai-integrations.php
[flex-api]: https://www.interactivebrokers.com/docs/web-api/flex-web-service/client-portal-configuration

[Create an Activity Flex Query](https://www.ibkrguides.com/clientportal/performanceandstatements/activityflex.htm) ·
[Run a Flex Query](https://www.ibkrguides.com/clientportal/performanceandstatements/runflex.htm) ·
[IBKR Activity Flex section reference](https://www.ibkrguides.com/reportingreference/reportguide/activity%20flex%20query%20reference.htm).
