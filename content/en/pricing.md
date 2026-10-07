---
title: DeepSeek V4 API pricing, peak hours and cost examples
checked: 2026-10-07
sources:
  - https://argolink.io/en/models/deepseek-v4-pro
  - https://argolink.io/en/models/deepseek-v4.1-flash
  - https://api-docs.deepseek.com/quick_start/pricing
  - https://openrouter.ai/deepseek/deepseek-v4-pro-0813
  - https://openrouter.ai/deepseek/deepseek-v4.1-flash
---

# DeepSeek V4 API pricing

USD per 1M tokens. "Off-peak" is the rate outside DeepSeek's weekday peak windows (below).

| Model | Where | Input | Cached input | Output |
|---|---|---:|---:|---:|
| `deepseek-v4-pro` | [ArgoLink](https://argolink.io/en/models/deepseek-v4-pro) | **$0.528** | **$0.0176** | **$1.584** |
| | DeepSeek (official, off-peak) | $0.66 | $0.022 | $1.98 |
| | DeepSeek (official, peak) | $1.32 | $0.044 | $3.96 |
| `deepseek-v4.1-flash` | [ArgoLink](https://argolink.io/en/models/deepseek-v4.1-flash) | **$0.12** | **$0.0024** | **$0.48** |
| | DeepSeek (official, off-peak) | $0.15 | $0.003 | $0.60 |
| | DeepSeek (official, peak) | $0.30 | $0.006 | $1.20 |

The gateway's rate is 20% below DeepSeek's off-peak rate on every line, including cache hits. The gateway lists cache writes at $0, and DeepSeek's price list has no cache-write line. Reasoning tokens count as output tokens.

## Peak hours

| | Windows | Rate |
|---|---|---|
| DeepSeek | Monday to Friday, 01:00–04:00 and 06:00–10:00 UTC, except Chinese public holidays | off-peak × 2 |
| Gateway | weekdays 09:00–12:00 and 14:00–18:00 Beijing time (the same hours) | the listed rate × 2 |

So at peak the gateway charges $1.056 / $3.168 for V4 Pro and $0.24 / $0.96 for Flash, still 20% under DeepSeek's own peak rates. The gateway's page does not mention a holiday exception.

## Other routes to the same models

OpenRouter listed 21 provider routes for DeepSeek V4 Pro 0813 and 29 for V4.1 Flash on 2026-10-07 (from its public `/api/v1/models/{id}/endpoints` data). A few of them, USD per 1M tokens:

| Model | Route | Input | Output | Cached input | Notes |
|---|---|---:|---:|---:|---|
| V4 Pro 0813 | DeepSeek (first party) | $0.66 | $1.98 | $0.022 | max output 393,216 |
| | Novita | $0.99 | $2.97 | $0.033 | fp8 |
| | DeepInfra | $1.30 | $2.60 | $0.10 | fp8, max output 16,384 |
| | Together | $1.32 | $3.96 | $0.13 | |
| | Sail Research | $0.40 | $4.30 | $0.033 | fp4 |
| | all 21 routes | $0.40–$1.65 | $1.98–$5.00 | | |
| V4.1 Flash | DeepSeek (first party) | $0.15 | $0.60 | $0.003 | max output 393,216 |
| | Decart | $0.09 | $0.18 | $0.018 | fp4, max output 262,144 |
| | DeepInfra | $0.14 | $0.42 | $0.0042 | fp8, max output 131,072 |
| | Together | $0.30 | $1.20 | $0.006 | |
| | all 29 routes | $0.05–$0.45 | $0.18–$2.40 | | |

For V4 Pro, no listed route undercut the gateway on both input and output. For Flash, a few quantized routes are cheaper, Decart's fp4 route on both; check their output limits before you compare. Prices move often: treat this table as a snapshot and re-check the linked pages.

## What requests cost

Off-peak, both columns. Double every figure for DeepSeek's peak hours.

| Request | V4 Pro (gateway) | V4 Pro (DeepSeek) | Flash (gateway) | Flash (DeepSeek) |
|---|---:|---:|---:|---:|
| Chat turn: 2,000 in / 500 out | $0.0018 | $0.0023 | $0.0005 | $0.0006 |
| RAG answer: 50,000 in (40,000 cached) / 1,000 out | $0.0076 | $0.0095 | $0.0018 | $0.0022 |
| Repository review: 400,000 in / 8,000 out | $0.2239 | $0.2798 | $0.0518 | $0.0648 |
| Agent run: 30 calls × 60,000 in (55,000 cached) / 1,500 out | $0.1795 | $0.2244 | $0.0436 | $0.0544 |

Formula: `(input − cached) × input rate + cached × cached rate + output × output rate`, divided by 1,000,000. The two cached rows show why prompt caching matters more than the per-token discount: on the agent run, cache hits cut the gateway bill from $1.02 to $0.18, 82% less, while the gateway discount alone is 20%.

## Where the money goes on a thinking model

- **Reasoning is output.** A short answer to a hard question can carry thousands of reasoning tokens, all billed at the output rate. V4 Pro always thinks; `reasoning_effort: "low"` reduces it. Flash can stop thinking entirely with `"none"`.
- **`max_completion_tokens` caps the bill**, reasoning included. Without it a single call may use the full 393,216-token output limit.
- **Cache hits need an identical prefix.** DeepSeek's disk cache matches whole stored prefix units; keep system prompts and tool definitions byte-identical and put changing text last. DeepSeek reports hits as `prompt_cache_hit_tokens` and misses as `prompt_cache_miss_tokens` in `usage`.
