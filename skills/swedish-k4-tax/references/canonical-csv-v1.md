# Canonical CSV v1

Read this reference before generating or importing `skatteguru_csv`. Canonical
CSV is a strict input contract, not a broker-file recovery format. Validation
never falls back to AI, a provider parser, or the lenient generic parser.

## Workflow

1. Generate UTF-8 CSV with the exact `# skatteguru_csv=1` preamble and supported
   columns below. Keep the source content in memory; do not create a temporary
   file merely to call an inline tool.
2. If `preview_csv_import` is exposed, call it with the proposed file name,
   `format: "skatteguru_csv"`, `format_version: 1`, and exact CSV content. It
   uses the production strict parser without storing a document. Fix every
   reported error. A successful preview is validation, not an import.
3. Call `import_csv_document` with the exact unchanged content and a new stable
   idempotency key. Import validates again. See [MCP review](mcp-review.md) for
   inline limits, retries, duplicate behavior, and prepared uploads.

## Supported rows

Version 1 supports `Buy` and `Sell` for `Equity`, `Stock`, `Listed Share`,
`ETF`, `Fund`, `Mutual Fund`, `Crypto`, and `Cryptocurrency`. Crypto support is
limited to ordinary acquisitions and disposals valued in a supported fiat
currency. Crypto-to-crypto swaps, transfers, staking/mining/reward income,
airdrops, chain splits, token-to-token prices, and crypto-denominated fees are
not canonical v1 rows. Preserve those in their original broker/exchange export
or explain that the canonical route cannot represent them.

The accepted columns are:

| Column | Rule |
| --- | --- |
| `Date` | Required supported date or date-time. |
| `Time` | Optional `HH:MM[:SS]`. |
| `Type` | Required `Buy` or `Sell`. |
| `Symbol` | Required; maximum 64 characters. |
| `Asset Type` | Optional; defaults to `Equity`. Use `Crypto` for a cryptocurrency. |
| `Quantity` | Required positive decimal magnitude. Direction comes from `Type`. |
| `Price`, `Price Currency` | Positive unit price and its currency. |
| `Total`, `Total Currency` | Positive gross consideration before fees and its currency. |
| `Fee`, `Fee Currency` | Optional separate positive fee and its currency. |
| `Currency` | Optional row-level fallback for missing named currency columns. |
| `Account` | Optional account label. |
| `Account Type` | Optional `Standard`, `AF`, `Taxable`, `ISK`, or `KF`. |
| `Description` | Optional evidence text. |

At least one of `Price` or `Total` is required. Every populated monetary value
needs a currency. When both price and total have the same currency,
`Price × Quantity` must match gross `Total` within one unit of total precision.
Use plain positive decimals without grouping separators, symbols, or exponents.
Unknown, empty, or repeated headers fail. The maximum is 2,000 data rows.

## Maintained examples and expected tax outcomes

These synthetic SEK examples are packaged with the skill and exercised by the
parser-to-ledger tax tests. They are templates, not user records:

- [Ordinary stock trades](../examples/canonical-stock-trades.csv): ACME sell
  proceeds after fee `596 SEK`, allocated acquisition cost `404 SEK`, and gain
  `192 SEK`.
- [Fractional ETF trades](../examples/canonical-fractional-stock-trades.csv):
  FRACT sell proceeds after fee `99 SEK`, allocated acquisition cost `81 SEK`,
  and gain `18 SEK`.
- [Fiat-priced crypto trades](../examples/canonical-crypto-trades.csv): BTC sell
  proceeds after fee `5,940 SEK`, allocated acquisition cost `4,040 SEK`, and
  K4 section D gain `1,900 SEK`.

Do not copy an example's symbol, dates, amounts, account type, or currency into
a user's import unless their evidence says so.
