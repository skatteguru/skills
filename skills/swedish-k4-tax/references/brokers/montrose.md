# Montrose

Status: guide-based stub. Browser automation has not been validated for this package.
Read the [current guide](https://www.skatteguru.se/help-center/import/montrose-csv).

Choose **Depå → Transaktioner** (the guide also documents the G shortcut), select
the longest relevant range, then **Exportera** for CSV. Exclude ISK/KF records
from the ordinary K4 calculation. Verify the earliest available date and identify
missing older purchases rather than treating the available range as complete.

Preserve Datum, Typ, Konto, Värdepapper/Beskr., Antal, Kurs, Totalt and their
original formats/currencies. Gather other brokers' records when required for the
same holdings. Use [browser preflight](../browser.md) and
[MCP review](../mcp-review.md). Future acceptance: original taxable-account CSV,
actual date coverage and transfer/acquisition gaps.
