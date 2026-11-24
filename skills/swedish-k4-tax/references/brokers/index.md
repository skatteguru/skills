# Broker routing

Read only the modules for the user's sources. Status describes these instructions,
not a guarantee of deployed parser coverage or a successful live download.
For every broker, offer the [collection choice and policy check](../browser.md)
before automated access. Manual instructions remain available; a documented route
or bundled helper does not establish broker authorization.

| Broker | Reference | Collection status |
| --- | --- | --- |
| E*TRADE / Morgan Stanley stock plans | [E*TRADE](etrade.md) | Manual route; automated routes require applicable written authorization; bundled helpers tested offline |
| Interactive Brokers | [IBKR](ibkr.md) | Browser collection and MCP import for Activity Flex XML where deployed; Activity Statement CSV fallback |
| Avanza | [Avanza](avanza.md) | Guide-based stub |
| Nordnet | [Nordnet](nordnet.md) | Guide-based stub |
| Charles Schwab | [Schwab](schwab.md) | Guide-based stub |
| Montrose | [Montrose](montrose.md) | Guide-based stub |
| cTrader | [cTrader](ctrader.md) | Guide-based stub |
| Nutmeg | [Nutmeg](nutmeg.md) | Guide-based stub |
| Cobra and other CSV sources | [Other sources](other.md) | Guide-based stub |

Obtain the income year's disposals plus the acquisition/vesting/exercise and
transfer history required to substantiate them. Do not hardcode a universal first
year. Preserve account identity, original currency and source ordering. If a report
extends beyond the requested year, record its actual coverage and analyze the
intended year explicitly. Never imply that a current-year sales report is complete
acquisition evidence.

Source roles are independent: transaction input, reconciliation/completeness,
execution chronology, and supporting exhibit. One file can serve several roles.
Document those roles before importing overlapping sources. Match records across
sources without creating extra trades just to attach evidence.

For each module, read the linked current help guide before detailed navigation.
Use observed page labels if menus differ. Identify guide/parser conflicts and
verify accepted events; do not resolve a conflict by assuming an unsupported format.
