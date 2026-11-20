# Maintaining Skatteguru skills

Keep the main skill short and load broker-specific instructions only when needed.
Publish only public product information. Do not include private repository paths
or implementation inspection notes. Use only the production MCP endpoint
`https://rust.skatteguru.se/mcp` in this repository.
Keep actual tested coverage explicit. Instructions are not proof
that an endpoint, parser, permission or browser capability is deployed.

Do not add real financial records, taxpayer identities, screenshots of private
accounts, tokens, cookies, request captures or signed URLs to this repository.
Use synthetic fixtures for tests. Keep user workspaces outside this checkout.

For documentation changes, verify relative links and consistency between the
README, skill routing, broker status and acceptance scenarios. Validate SKILL.md
frontmatter with the host's skill validator when available and inspect a built
ZIP for complete references and absence of private data. Run the checked-in
`python -B scripts/validate_package.py` and `python -B scripts/build_skill_zip.py`;
see `docs/development.md` for lint, formatting, type checks and offline tests.
Keep the single discoverable skill and its version/changelog consistent.

When executable helpers are introduced, add meaningful offline tests for their
observable behavior and run the relevant lint/type/test checks. Report checks
and limitations. Browser download and filing acceptance tests require separate,
explicit authorization; never submit real tax data as an automated test.

Do not claim future batch tools, journal writes, evidence attachment or export
revision APIs exist. Discover live MCP schemas and treat missing permissions
separately from missing product capabilities. Keep filing approval tied to the
reviewed year, taxpayer and exact exported artifacts.
