# Browser and CDP preflight

Use the host's supported browser interface, preferably the built-in browser.
Follow that interface's current documentation rather than inventing CDP commands.

Before a collection task, check only the capabilities needed for its chosen route:
ordinary broker downloads do not require full CDP. Check full CDP only when
capturing authenticated requests for the E*TRADE scripts.

| Capability | Why it matters |
| --- | --- |
| Browser navigation and site access | Open broker pages and verify exports |
| Browser login handoff | User supplies credentials and verification |
| Download/save and local file access | Preserve exact original files for import |
| HTTP/file transfer | Send bytes returned by prepared-upload instructions |
| Full CDP/network inspection and site approval | Capture authenticated requests for E*TRADE helpers |

The presence of browser tools does not establish full CDP access. Check exposed
capabilities and the site's grant before attempting network capture. A denied
operation is a reason to explain and stop that route, not to try hidden browser
state, cookies through another API, or another browser without authorization.

If the chosen E*TRADE script route needs request capture and CDP is missing,
explain the task-specific need: the bulk helper requires the
authenticated broker request, which ordinary page interaction may not expose.
Ask the user to open **Settings → Browser → Developer mode → Enable full CDP
access**, then approve the relevant site. Refresh the browser connection or tool
documentation after they change it, and verify again. An organization may disable
the setting. CDP means Chrome DevTools Protocol, sometimes called “CDT” by users.

IBKR Activity Statement CSV and ordinary exports from other brokers do not require
full CDP. Use normal browser controls for these routes and do not request the CDP
setting. Continue independently useful work while waiting for E*TRADE request-capture
access. If CDP remains
unavailable, offer a normal browser download or user-created private local request
capture; never ask for session cookies in chat. Respect a request to demonstrate
manual downloads even when a bulk route exists.

When capturing an authorized request, restrict capture to the required broker
endpoint. Keep captured headers/payload out of output and logs. A helper must
parse the request as data, restrict credential-bearing requests/redirects to
approved broker origins, and clean up private authentication files on every exit.
Do not send broker credentials to Skatteguru or its signed upload destination.

For Skatteverket, check file-selection/upload support before promising completion.
Hand over login, BankID and signing to the user; observe the returned state and
receipt after they finish. Do not claim that enabling CDP bypasses these steps.

[Official browser developer-mode instructions](https://learn.chatgpt.com/docs/browser#developer-mode)
