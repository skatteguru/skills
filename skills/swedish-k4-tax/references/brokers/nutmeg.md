# Nutmeg

Status: guide-based stub. Browser automation has not been validated for this package.
Read the [current guide](https://www.skatteguru.se/help-center/import/nutmeg).

Obtain investment-activity CSV covering required history, separately for each
account/pot. The guide has no precise download menu: inspect the actual browser
instead of inventing one. Preserve semicolon delimiters, any Investment-Activity-
intro line, original dates, account type and GBP columns.

The guide documents Purchase and Sale imports, excluding dividends, fees, interest
and unknown transaction types. Make those exclusions explicit when reviewing the
declaration. A UK ISA label does not establish Swedish ISK treatment. Confirm the
relevant Swedish account treatment before combining holdings.

Use [browser preflight](../browser.md) and [MCP review](../mcp-review.md).
Future acceptance: multiple pots, intro/header detection, purchase/sale mapping
and visible exclusion of unsupported cash rows.
