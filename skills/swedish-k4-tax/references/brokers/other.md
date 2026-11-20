# Cobra and other CSV sources

Status: guide-based stub. No broker downloader or validated browser automation.
Read the [generic CSV guide](https://www.skatteguru.se/help-center/import/csv-format).

Try the broker's original transaction-level export first. The guide describes
Cobra columns including Date, Quantity, Symbol, Description, Price, Amount, Type
and commissions, but does not prescribe a download menu. Inspect the user's actual
portal if browser collection is requested. Preserve original short-sale signs and
borrow/locate fees; identify unsupported cash or mark-to-market rows explicitly.

Generic uploaded CSV and strict canonical CSV v1 have different coverage. Do not
assume the strict inline tools support the generic guide's short sales, transfers,
dividends, corporate actions or fees as standalone events. Strict v1 supports
positive Buy/Sell trades for equity/ETF/fund and fiat-priced crypto, with gross
Total and explicit currencies. If generating canonical CSV, use the live schema
and [canonical format reference](../canonical-csv-v1.md), preview exact content
first, then import unchanged. Never fabricate values to fit a supported format.

Record source provenance for any reconstruction and keep unknowns unresolved.
Use [browser preflight](../browser.md) and [MCP review](../mcp-review.md).
Future acceptance: original export recognition and safe rejection of unsupported
operations, with evidence-backed conversion only for supported events.
