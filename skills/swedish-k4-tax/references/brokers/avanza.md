# Avanza

Status: guide-based stub. Browser automation has not been validated for this package.
Read the [current guide](https://www.skatteguru.se/help-center/import/avanza-csv).

In the browser, open **Min ekonomi → Transaktioner**, choose the taxable depå/AF
account, include relevant acquisition history through the income year, and select
**Exportera transaktioner → Excel-format (.csv)**. Exclude ISK/KF/pension records
from this K4 workflow. If filtering, retain buys, sells and relevant securities
transfers. Check that the export actually covers the selected period.

Preserve the original bytes. The guide describes buys, sells and securities
transfers; do not assume other CSV rows are included in tax analysis. Gather
records from other taxable accounts holding the same instruments when relevant.
Use [browser preflight](../browser.md) and [MCP review](../mcp-review.md).
Future acceptance: original CSV, transfer history, account exclusions and a
populated buy/sell example with acquisition history.
