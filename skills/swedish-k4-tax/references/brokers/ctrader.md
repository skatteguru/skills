# cTrader

Status: guide-based stub. Browser automation has not been validated for this package.
Read the [current guide](https://www.skatteguru.se/help-center/import/ctrader-csv).

Use Desktop or Web, with English headers and Buy/Sell values; mobile export is
not documented. Open **Trade Watch → History**, show closed trades for the period,
then **Statement → Excel → Save**. Preserve the original XLSX rather than changing
its extension to CSV. Use a user handoff if only Desktop can export the account.

Required evidence includes Symbol, Opening direction, Closing time, Entry price,
Closing price, Closing quantity, Gross, Net, Balance, Swap and Commission. Verify
dates, quantity/contract units, currency and fees. This is closed-position/CFD
coverage; do not force it into an ordinary share-acquisition workflow or assume
every instrument has the same K4 treatment.

Use [browser preflight](../browser.md) and [MCP review](../mcp-review.md).
Future acceptance: populated closed trades, commission/swap handling and date
range completeness across multiple chunks.
