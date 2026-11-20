# Nordnet

Status: guide-based stub. Browser automation has not been validated for this package.
Read the [current guide](https://www.skatteguru.se/help-center/import/nordnet-csv).

Choose the **aktie- och fondkonto (AF) → Transaktioner**, set the period to include
required acquisition history, then **Exportera → CSV**. Exclude ISK/KF/pension
history from this K4 calculation. Do not let transaction/instrument filters remove
necessary buys or transfers. Record the actual exported dates and account.

Preserve the original CSV and inspect accepted events and currencies. Relevant
holdings at other brokers may require additional acquisition evidence. Use
[browser preflight](../browser.md) and [MCP review](../mcp-review.md).
Future acceptance: populated AF export with earlier acquisitions and account
selection/exclusion checks; no supported coverage claim based on headers alone.
