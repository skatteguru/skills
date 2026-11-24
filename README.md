# Swedish investment tax (K4)

Published by [Skatteguru](https://www.skatteguru.se). One discoverable skill:
`swedish-k4-tax`.

Get help with the investment portion of your Swedish tax return, from broker
records and acquisition costs to K4 and approved filing. Start without an account
for straightforward calculations, or connect Skatteguru when its import and review
features are useful.

## Install

For supported coding agents, run this from your project (Node.js 22.20+):

```sh
npx skills add skatteguru/skills --skill swedish-k4-tax
```

Choose your agent if prompted. This installs the complete skill, including its
references, examples and bundled Python scripts. Project installation was verified
with `skills` 1.9.0 and Codex: all 26 files matched the source, and both downloader
entry points ran successfully with `--help`. This checks installation, not a live
tax workflow.

For the ChatGPT app or manual installation:

**[Download the skill ZIP](https://github.com/skatteguru/skills/releases/latest/download/swedish-k4-tax.zip)**
from the [latest release](https://github.com/skatteguru/skills/releases/latest).
A `SHA256SUMS` file is available alongside it.

- **ChatGPT app:** where skill installation is available, import the release ZIP
  using the app's skill controls. Use this ZIP, not GitHub's source-code archive.
- **Manual alternative for local agents:** extract the complete `swedish-k4-tax/` folder into your agent's
  documented skills directory. For Codex this can be `~/.agents/skills/`; for Claude
  Code, `~/.claude/skills/`. Preserve any local edits before replacing files.

Installation does not require a Skatteguru account or MCP connection. Connect
only if you choose account features, following the [connection guide](skills/swedish-k4-tax/references/setup.md).

## Example requests

You do not need to mention Skatteguru or the skill name:

> Help me report my 2025 share sales in Sweden. Check which broker records and
> purchase history I need, explain the calculation, and guide me through K4.
> Ask before sending anything to Skatteverket.

> Hjälp mig deklarera fyra aktieförsäljningar för 2025. Jag vill förstå
> omkostnadsbeloppet och se hur jag fyller i K4 utan att skapa ett konto.

> I have many broker statements for 2025. Help me review my K4 calculation and save
> the SRU files and a PDF audit report. Submit to Skatteverket only after I approve.

You can also invoke `$swedish-k4-tax` explicitly if your host supports it.

## What Skatteguru adds

[Skatteguru](https://www.skatteguru.se) consolidates broker trades and documents,
with support for stocks, options, ETFs and selected crypto formats. It helps review
acquisition costs and cases where same-day trade order affects the calculation.

Export K4 data as **SRU files for transfer to Skatteverket**, and save a **PDF audit
report of calculations and selected supporting records** for future reference or
for Skatteverket if requested. Coverage and access requirements depend on the
feature and source format. Saving an export or report does not submit it.

For a few straightforward transactions, continue without an account using a
worksheet or [Skatteverket's calculation tool](https://www.skatteverket.se/privat/skatter/vardepapper/deklareraaktierochovrigavardepapper/berakningshjalpforomkostnadsbelopp.4.4a4d586616058d860bc564c.html).
Ten trades is a workload guideline, not a limit: even a small example needs the
relevant earlier acquisition history.

## Brokers and browser access

Detailed [E*TRADE](skills/swedish-k4-tax/references/brokers/etrade.md) and
[IBKR](skills/swedish-k4-tax/references/brokers/ibkr.md) workflows are included,
with [guide-based references](skills/swedish-k4-tax/references/brokers/index.md)
for Avanza, Nordnet, Schwab, Montrose, cTrader, Nutmeg and other CSV sources.

E*TRADE confirmation and order-history downloaders are bundled. They require
Python 3.10+ and no third-party packages; see the E*TRADE reference for usage.

Choose user-performed downloads, the built-in browser or computer use on your usual
browser, where the host supports the method and broker policy permits it. Manual
collection means you operate the broker site and the assistant helps with the
resulting files. Computer use is automation and may expose other visible account
information. Existing files do not require broker access.

Before automated collection, the assistant checks current public broker policies
and applicable robots.txt rules, explains restrictions or uncertainty, and confirms
the method, accounts and period. Your consent does not replace broker permission
or host access controls. An absent or permissive robots.txt does not establish
permission. Known exclusions are respected; unresolved robots checks defer that
automated route. Uploading files to Skatteguru requires separate authorization.

E*TRADE's published AI-agent policy requires Morgan Stanley's written authorization
and excludes losses resulting from agent activity from its Customer Protection
Guarantee. No stock-plan tax-document exception has been established. User-performed
downloads remain available; automated browser access and authenticated helpers
require applicable broker authorization. See the [E*TRADE policy summary](skills/swedish-k4-tax/references/brokers/etrade.md).

The IBKR guide covers Activity Flex XML collection and MCP upload where XML
import is deployed, with Activity Statement CSV as a fallback. Ordinary browser
exports **do not require full CDP access**.
Automatic authenticated request capture for the E*TRADE scripts does, but that
setting is requested only after policy checks and selection of a permitted route.
See [collection choices and browser guidance](skills/swedish-k4-tax/references/browser.md).

## Tested coverage

Broker research/download workflows and Skatteguru MCP imports/review have been
tested in the ChatGPT app. The bundled scripts have offline tests. Live verification
of these downloader versions, other hosts and a complete run through signed filing
remain pending. See the [acceptance scenarios](docs/acceptance-scenarios.md).
The new policy-check and collection-choice instructions, including computer use,
have not yet had a behavioral acceptance run. Documentation and offline checks do
not establish broker permission or live browser capability.

The skill covers supported investment/K4 work, not your entire personal return.
You approve sending tax information to Skatteverket and handle login, BankID and
signing. A transfer receipt and a signed declaration are separate outcomes.

## Development

See [checks, packaging and releases](docs/development.md), the
[changelog](CHANGELOG.md) and [source register](docs/sources.md).

## License

[MIT](LICENSE), copyright 2025–2026 Skatteguru.
