# Sources and verification context

Reference date: 2026-11-20. Menu paths and parser behavior can change. Read current
guides when performing detailed navigation; verify live schemas/deployment for
account operations. Documentation review is not end-to-end acceptance testing.

## Primary workflow sources

- [Skatteverket calculation helper](https://www.skatteverket.se/privat/skatter/vardepapper/deklareraaktierochovrigavardepapper/berakningshjalpforomkostnadsbelopp.4.4a4d586616058d860bc564c.html)

- [Skatteguru agent setup](https://www.skatteguru.se/help-center/integrations/ai-agents)
- [E*TRADE originals](https://www.skatteguru.se/help-center/import/etrade-documents)
- [E*TRADE execution times](https://www.skatteguru.se/help-center/import/etrade-documents/execution-time)
- [E*TRADE helper repository](https://github.com/skatteguru/download-my-documents-from-etrade)
- [Order downloader](https://github.com/skatteguru/download-my-documents-from-etrade/blob/main/etrade_orders.py)
- [Upstream MIT license](https://github.com/skatteguru/download-my-documents-from-etrade/blob/main/LICENSE)
- [IBKR guide](https://www.skatteguru.se/help-center/import/ibkr-csv)
- [IBKR Flex overview](https://www.ibkrguides.com/clientportal/performanceandstatements/flex.htm)
- [Browser/CDP documentation](https://learn.chatgpt.com/docs/browser#developer-mode)
- [Skatteguru SRU guide](https://www.skatteguru.se/help-center/filing/uploading-sru-files)
- [Skatteverket technical requirements and receipts](https://www.skatteverket.se/foretag/inkomstdeklaration/forredovisningsbyraer/tekniskinformationomfiloverforing.4.13948c0e18e810bfa0cca8.html)

Each broker stub links its specific help-center guide. Avanza/Nordnet/Montrose
account exclusions, Schwab web export, cTrader English XLSX fields, Nutmeg's
Purchase/Sale-only coverage and Cobra's original export fields came from the
corresponding public help-center guides.

Earlier ChatGPT workflows informed the package design: E*TRADE collection/import
with order-history investigation and IBKR export verification. No private account
IDs, financial results, screenshots or session captures from those workflows are
included here. No actual Skatteverket filing was verified for this package.

## Bundled E*TRADE helper provenance

The local scripts were adapted from Skatteguru's public downloader scripts and are
now maintained with this skill. Starting source blob IDs:

- `etrade_download.py`: `9c0ccc1e6867a0459d66f46556da30f9a7c57811`.
- `etrade_orders.py`: `083d0c8e3ba91149ace93522626654b4a8dd9eff`.

The original 2025 Skatteguru copyright and the current copyright are covered by
the repository's 2025–2026 Skatteguru MIT notice, also included in the skill ZIP.
These are adapted helpers, not byte-for-byte copies of the older upstream files.
