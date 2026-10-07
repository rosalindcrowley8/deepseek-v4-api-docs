---
title: DeepSeek V4 models, IDs and limits
checked: 2026-10-07
sources:
  - https://argolink.io/en/models/deepseek-v4-pro
  - https://argolink.io/en/models/deepseek-v4.1-flash
  - https://argolink.io/en/docs
  - https://api-docs.deepseek.com/quick_start/pricing
  - https://api-docs.deepseek.com/quick_start/rate_limit
---

# DeepSeek V4 models, IDs and limits

Two DeepSeek V4 models are served: **V4 Pro**, the strongest, and **V4.1 Flash**, the fast, cheap one that also reads images.

| | DeepSeek V4 Pro | DeepSeek V4.1 Flash |
|---|---|---|
| Model ID on the gateway | `deepseek-v4-pro` | `deepseek-v4.1-flash` |
| Model name on api.deepseek.com | `deepseek-v4-pro` | `deepseek-flash` |
| Version DeepSeek serves | DeepSeek-V4-Pro-0813 | DeepSeek-V4.1-Flash |
| Context window | 1,048,576 tokens | 1,048,576 tokens |
| Max output | 393,216 tokens (DeepSeek writes "384K") | 393,216 tokens |
| Input | text | text and images |
| Output | text | text |
| Thinking on the gateway | always on | on by default; `reasoning_effort: "none"` turns it off |
| `reasoning_effort` | `low` · `high` · `max`, default `high` | `low` · `high` · `max` (+ `none`), default `high` |
| Tools / function calling | yes | yes |
| Concurrency at DeepSeek (per account) | 500 | 2,500 |
| Gateway price, input / output per 1M | $0.528 / $1.584 | $0.12 / $0.48 |

Prices and the peak-hour rule are on the [pricing page](pricing.md); thinking controls on [reasoning](reasoning.md).

## Retired and alias IDs

| You send | What happens |
|---|---|
| `deepseek-v4-pro-0813` | replaced on the gateway by `deepseek-v4-pro`; use the new ID |
| `deepseek-v4-flash-vision-exp` | replaced on the gateway by `deepseek-v4.1-flash` |
| `deepseek-v4-flash`, `deepseek-v4-flash-vision-exp` on api.deepseek.com | still accepted by DeepSeek; served by V4.1 Flash at the Flash price |
| `claude-opus-*` on DeepSeek's Anthropic endpoint | DeepSeek maps it to `deepseek-v4-pro`; `claude-sonnet-*` / `claude-haiku-*` map to `deepseek-flash` |
| any unknown name on DeepSeek's Anthropic endpoint | DeepSeek maps it to `deepseek-flash` |

On the gateway, send the catalog ID itself on every protocol, `/v1/messages` included. The Messages endpoint takes any text model ID; it does not have to start with `claude`.

## List the IDs yourself

The model list is public, no key needed:

```bash
curl -s https://argolink.io/v1/models | jq -r '.data[] | select(.owned_by == "deepseek") | .id'
# deepseek-v4-pro
# deepseek-v4.1-flash
```

The richer catalog entry, with limits and both price sets, comes from the catalog API:

```bash
curl -s 'https://argolink.io/api/catalog/v1/models?category=chat&sort=provider&page_size=100' \
  | jq '.items[] | select(.provider_id == "deepseek") | {id, text, pricing}'
```

`scripts/check_catalog.py` in this repo runs that query and fails if any number on these pages has drifted.

## Which one to use

| Workload | Pick | Why |
|---|---|---|
| Agentic coding, multi-step tool use, hard reasoning | `deepseek-v4-pro` | strongest model; always thinks |
| Chat, classification, extraction, summaries at volume | `deepseek-v4.1-flash` | 23% of Pro's input price and 30% of its output price; thinking can be switched off for speed |
| Screenshots, charts, scanned pages | `deepseek-v4.1-flash` | the only V4 model that reads images |
| Very long inputs | either | both take 1,048,576 tokens; Flash costs $0.12 per 1M input tokens against Pro's $0.528 |
