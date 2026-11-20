# Charles Schwab

Status: guide-based stub; limited import examples and no validated package browser route.
Read the [current guide](https://www.skatteguru.se/help-center/import/schwab-csv).

Use the website: **Accounts → History → account/date range → Search → Export →
CSV**. The guide says mobile has no CSV export. Split long history into complete
year/quarter chunks if results are limited. Verify boundaries and expected rows.

Expected original columns include Date, Action, Symbol, Description, Quantity,
Price, Fees & Comm and Amount. Preserve dates, signs and currencies. Ask separately
for stock-plan acquisitions, transfers or corporate actions missing from the CSV.
Do not infer support for all short-sale or derivative events from a successful upload.
Use [browser preflight](../browser.md) and [MCP review](../mcp-review.md).
Future acceptance: overlapping date chunks, fees, original currencies and missing
stock-plan history detection.
