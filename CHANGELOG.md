# Changelog

## 0.1.2

- Document IBKR Activity Flex XML collection with browser handoff for sign-in,
  report template selection and a minimal export profile.
- Describe original-file upload and parser verification through Skatteguru MCP,
  including the Activity Statement CSV fallback when XML availability is unconfirmed.

## 0.1.1

- Offer manual downloads, built-in browsing or computer use where supported,
  with separate consent for broker collection and uploads.
- Check broker policies and applicable robots.txt rules before automated access;
  distinguish user consent from broker authorization and respect access restrictions.
- Document E*TRADE's written-authorization requirement and guarantee exclusion.
- Update broker routing, progress guidance and acceptance scenarios. New policy-check
  and collection-choice behaviors await behavioral acceptance testing; no live
  broker, computer-use collection or filing test was performed for this release.

## 0.1.0

- One discoverable Swedish investment tax (K4) skill, published by Skatteguru.
- Account-free calculations and Skatteverket walkthrough guidance, with optional
  Skatteguru onboarding, imports, review, SRU export and PDF audit reports.
- E*TRADE and IBKR workflows, bundled E*TRADE confirmation/order downloaders, and
  guide-based references for other brokers.
- Reproducible installable ZIP, SHA-256 checksum, package validation and offline CI.

Broker research/download workflows and MCP import/review have been tested in the
ChatGPT app. The bundled downloaders have offline tests. Live authenticated
verification of these downloader versions and a complete installation-to-signed-
declaration run remain pending. Filing always requires the user's approval.
