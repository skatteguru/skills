# Collection choice, broker policies and browser preflight

## Choose how to collect records

If the user already has the files, continue with local review or separately
authorized upload; no broker-access warning is needed. Otherwise ask which method
they prefer, offering only methods the current host supports and broker policy
permits. Honor an existing choice rather than asking again:

> How would you like to collect your broker documents?
>
> - Download them yourself: I'll explain which files you need, then help process them.
> - Use the built-in browser: I'll help navigate and download documents with some automation.
> - Use your usual browser through computer use: I'll operate its interface to help collect documents. This may expose other visible account information.
>
> Before automated access, I'll check the broker's published restrictions and explain any limitations. You'll handle login and verification.

Computer use is automation too. Explain unavailable or restricted options; do not
promise unsupported methods or ask users to bypass restrictions. For manual collection, give written navigation
instructions and let the user operate the site; do not inspect their logged-in
pages or capture requests as part of that route. User-supplied files can be
processed regardless of whether broker automation is available.

## Check broker policy before automated access

Before opening authenticated broker pages, using computer use on the account,
capturing authenticated requests or running a credential-bearing helper:

1. Check the broker's current public terms, security/AI-agent policy and relevant
   account or stock-plan conditions. Use official sources, record URLs and check
   date, and separate confirmed restrictions from interpretation or uncertainty.
   Do not enter the account just to research permission.
2. Check robots.txt on each intended broker origin, including any separate host
   used by a helper. Apply the relevant agent group and path rules using
   [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html); do not impersonate another
   agent to obtain a more permissive rule. Treat these rules as a collection policy,
   not proof of legal permission. An Allow rule or absent file grants no account
   access rights. A failed fetch is not evidence that the file is absent: disclose
   unresolved checks and defer that automated route until resolved.
3. Explain material restrictions, uncertainty and any stated guarantee exclusions
   before requesting authenticated access. Follow the decision rules below.

| Finding | Action |
| --- | --- |
| No applicable restriction found | Say which sources were checked, without guaranteeing permission; confirm the collection scope and user's choice. |
| Terms unclear or unavailable, robots check resolved | Offer manual download first. The user may choose automation after the uncertainty is explained if no known restriction or host constraint prevents it. |
| Terms prohibit automation or require written authorization | Explain the condition; use manual collection unless applicable broker authorization permits the proposed access. User risk acceptance alone does not satisfy it. |
| Applicable robots rules disallow the route | Respect the exclusion and offer a permitted route; do not offer a user override. |
| Broker or host blocks access | Stop that route; do not switch browsers, replay requests or use helpers to bypass the block. |

For a broker with no restriction found, a short confirmation is enough:

> I found no explicit restriction in the public policies checked, but that does not guarantee broker permission. May I use [method] to collect [documents] for [accounts/years]? You can also download them yourself.

Consent covers the specified broker, accounts, period and method. Reuse it within
that unchanged task; obtain a new choice before materially changing the method,
such as moving to authenticated request capture. Check the scope of any broker
authorization, including the agent, account surface and retrieval method; do not
assume API approval authorizes browser access. User consent, broker permission and
host capability are separate requirements. No warning or acknowledgment guarantees
protection from liability or transfers all responsibility to the user.

Keep only a short policy/consent summary in private [progress notes](run-state.md),
outside the package. Do not store private authorization correspondence in the
repository. Collection permission does not authorize uploading files to Skatteguru.

## Verify the selected method's capabilities

Use the host's supported interface and current documentation rather than inventing
browser or CDP commands. Check only capabilities needed for the permitted route:
ordinary broker downloads do not require full CDP. Check full CDP only when
capturing authenticated requests for the E*TRADE scripts.

| Capability | Why it matters |
| --- | --- |
| Browser navigation and site access | Open broker pages and verify exports |
| Computer-use access to the selected browser | Operate the user's chosen browser without inspecting unrelated tabs or applications |
| Browser login handoff | User supplies credentials and verification |
| Download/save and local file access | Preserve exact original files for import |
| HTTP/file transfer | Send bytes returned by prepared-upload instructions |
| Full CDP/network inspection and site approval | Capture authenticated requests for E*TRADE helpers |

The presence of browser tools does not establish full CDP access. Check exposed
capabilities and the site's grant before attempting network capture. A denied
operation is a reason to explain and stop that route, not to try hidden browser
state, cookies through another API, or another browser without authorization.

Only after policy checks and the collection choice, if the chosen E*TRADE script
route needs request capture and CDP is missing, explain the task-specific need:
the bulk helper requires the authenticated broker request, which ordinary page
interaction may not expose.
Ask the user to open **Settings → Browser → Developer mode → Enable full CDP
access**, then approve the relevant site. Refresh the browser connection or tool
documentation after they change it, and verify again. An organization may disable
the setting. CDP means Chrome DevTools Protocol, sometimes called “CDT” by users.

IBKR Activity Statement CSV and ordinary exports from other brokers do not require
full CDP. Use normal browser controls for these routes and do not request the CDP
setting. Continue independently useful work while waiting for E*TRADE request-capture
access. If CDP remains unavailable, offer user-performed downloads or another
permitted method the user chooses. A user-created request capture and a helper
using it are still subject to broker policy; they are not workarounds for denied
access. Never ask for session cookies in chat. Respect a preference for manual
instructions even when a bulk route exists.

When capturing an authorized request, restrict capture to the required broker
endpoint. Keep captured headers/payload out of output and logs. A helper must
parse the request as data, restrict credential-bearing requests/redirects to
approved broker origins, and clean up private authentication files on every exit.
Do not send broker credentials to Skatteguru or its signed upload destination.

For Skatteverket, check file-selection/upload support before promising completion.
Hand over login, BankID and signing to the user; observe the returned state and
receipt after they finish. Do not claim that enabling CDP bypasses these steps.

[Official browser developer-mode instructions](https://learn.chatgpt.com/docs/browser#developer-mode)
