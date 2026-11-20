# Connection

Use this reference after the user chooses connected features. For calculations
without an account, follow [account-free help](account-free.md) instead.

Reuse a matching connection to the production MCP endpoint:
`https://rust.skatteguru.se/mcp`.

If the user already has an account, let them sign in through the supported browser
OAuth flow. If they want account features but have no account, explain the relevant
benefits first and guide them through the public sign-up option on the login page
or [Skatteguru website](https://www.skatteguru.se). The user creates/verifies the
account and approves access. Return to their existing records and task afterward;
do not make them restart completed work. Account creation alone does not establish
paid export access. Explain returned access requirements when relevant.

Connect through the host's supported MCP connector flow using browser OAuth.
The skill cannot create an OAuth grant simply by being installed. Do not ask for
pasted bearer tokens, passwords, administrative identity or account IDs.

Discover tools rather than assuming a host-specific prefix. Verify `ping`, then
`search_documents` with `limit: 1`; ping alone proves no account access. Empty
authenticated results can be valid. Show minimal metadata so the user can
recognize the intended account.

Normal permissions: `documents:read documents:upload tax:read tax:export`.
Use only the scopes needed. Reorder writes also require opt-in `documents:write`
and tax reads; deletion requires `documents:delete`. Missing tools may reflect
scopes or deployment version. Inspect available schemas before promising a write.
Reconnect for required permissions; do not change endpoints to mask errors.

For 401 reauthenticate the same connection. For 403 distinguish scope from product
access. Respect 429/retry guidance. Report persistent errors without secrets.
Browser login to Skatteguru and its MCP OAuth grant are separate sessions.

[Skatteguru setup guide](https://www.skatteguru.se/help-center/integrations/ai-agents)
