---
title: Moving between api.deepseek.com and the gateway
checked: 2026-10-07
sources:
  - https://api-docs.deepseek.com/quick_start/pricing
  - https://api-docs.deepseek.com/guides/thinking_mode
  - https://api-docs.deepseek.com/guides/anthropic_api
  - https://argolink.io/en/docs
  - https://argolink.io/en/models/deepseek-v4-pro
---

# Moving between api.deepseek.com and the gateway

Code written for DeepSeek's own API runs on the gateway after two value changes, and one more if you switch thinking off.

```python
import os
from openai import OpenAI

# DeepSeek's API
client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
fast = client.chat.completions.create(
    model="deepseek-flash",
    messages=[{"role": "user", "content": "ping"}],
    extra_body={"thinking": {"type": "disabled"}},
)

# The gateway
client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://argolink.io/v1")
fast = client.chat.completions.create(
    model="deepseek-v4.1-flash",          # Flash has a versioned ID here
    messages=[{"role": "user", "content": "ping"}],
    reasoning_effort="none",              # thinking.type disabled has no effect here
)
```

## What differs

| | api.deepseek.com | Gateway |
|---|---|---|
| OpenAI SDK base URL | `https://api.deepseek.com` | `https://argolink.io/v1` |
| Anthropic SDK base URL | `https://api.deepseek.com/anthropic` | `https://argolink.io` |
| Pro model ID | `deepseek-v4-pro` | `deepseek-v4-pro` |
| Flash model ID | `deepseek-flash` | `deepseek-v4.1-flash` |
| Thinking off | `thinking: {"type": "disabled"}`, both models | Flash: `reasoning_effort: "none"`; Pro: not possible |
| Responses and Anthropic formats | native | converted to Chat Completions |
| Claude model names on the Anthropic endpoint | mapped to DeepSeek models | not mapped; send the DeepSeek ID |
| Price, Pro, off-peak, per 1M in / out | $0.66 / $1.98 | $0.528 / $1.584 |
| Peak hours | 2× on weekdays 01:00–04:00 and 06:00–10:00 UTC, except Chinese public holidays | 2× in the same hours |
| Published concurrency limit | 500 (Pro) and 2,500 (Flash) per account | not published |
| Other models on the same key | DeepSeek only | GLM, Kimi, GPT, Claude, Grok and others in the catalog |

## DeepSeek features the gateway docs don't list

| Feature on api.deepseek.com | On the gateway |
|---|---|
| JSON Output (`response_format: {"type": "json_object"}`) | Chat Completions forwards DeepSeek's fields as sent, so the field reaches the model; the gateway docs do not describe it, so test it on your prompts |
| FIM completion and chat prefix completion (beta, under `https://api.deepseek.com/beta`) | not listed |
| Files API (`file_id` images and documents) | not listed; send images as URLs or data URLs |
| `user_id` for KV-cache and scheduling isolation | not listed |
| `GET /user/balance` | not listed |

If you depend on one of these, keep that call on DeepSeek's API and move the rest.

## Claude Code and other Anthropic clients

Point the client at the bare origin and name the model explicitly; DeepSeek's automatic Claude-name mapping does not exist on the gateway.

```bash
export ANTHROPIC_BASE_URL=https://argolink.io
export ANTHROPIC_AUTH_TOKEN=$DEEPSEEK_API_KEY
export ANTHROPIC_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4.1-flash   # Claude Code's background tasks use the haiku alias
claude
```

The gateway lists no Haiku model, so with `ANTHROPIC_DEFAULT_HAIKU_MODEL` unset, Claude Code's background calls ask for a model the gateway does not serve. Over this route the effort comes from `output_config.effort`; when the client sends none, the gateway uses `medium`, which DeepSeek runs as `high`.

## Checklist

- [ ] Base URL changed, with `/v1` for OpenAI SDKs and without it for Anthropic SDKs
- [ ] `deepseek-flash` renamed to `deepseek-v4.1-flash`
- [ ] `thinking: {"type": "disabled"}` replaced by `reasoning_effort: "none"` (Flash), or removed (Pro)
- [ ] Budgets updated: same peak windows, 20% lower rates
- [ ] Any JSON Output, FIM or Files API call tested or kept on DeepSeek's API
