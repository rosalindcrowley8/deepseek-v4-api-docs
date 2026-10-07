---
title: DeepSeek V4 endpoints, base URLs and request fields
checked: 2026-10-07
sources:
  - https://argolink.io/en/docs
  - https://argolink.io/en/models/deepseek-v4-pro
  - https://argolink.io/en/models/deepseek-v4.1-flash
  - https://api-docs.deepseek.com/guides/anthropic_api
  - https://api-docs.deepseek.com/guides/responses_api
---

# Endpoints, base URLs and request fields

DeepSeek V4 answers on three request formats. On the gateway, Chat Completions is DeepSeek's native format and the other two are converted to it.

| Format | Gateway | api.deepseek.com |
|---|---|---|
| OpenAI Chat Completions | `POST https://argolink.io/v1/chat/completions`, native: every field is forwarded as sent | `POST https://api.deepseek.com/chat/completions` |
| OpenAI Responses | `POST https://argolink.io/v1/responses`, converted to Chat Completions | `POST https://api.deepseek.com/responses` |
| Anthropic Messages | `POST https://argolink.io/v1/messages`, converted to Chat Completions | `POST https://api.deepseek.com/anthropic/v1/messages` |
| Model list | `GET https://argolink.io/v1/models`, no key | `GET https://api.deepseek.com/models` |

SDK base URLs follow from that. OpenAI SDKs take `https://argolink.io/v1`. Anthropic SDKs and Claude Code take the bare origin `https://argolink.io`, because they append `/v1/messages` themselves. DeepSeek's own values are `https://api.deepseek.com` and `https://api.deepseek.com/anthropic`.

## Authentication

| Format | Header |
|---|---|
| Chat Completions, Responses | `Authorization: Bearer $KEY` |
| Anthropic Messages | `x-api-key: $KEY` (Bearer is accepted too) and `anthropic-version: 2023-06-01` |

## Chat Completions (recommended)

```bash
curl https://argolink.io/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4-pro",
    "messages": [
      {"role": "system", "content": "Answer in at most three sentences."},
      {"role": "user", "content": "When should I use a B-tree index instead of a hash index?"}
    ],
    "reasoning_effort": "high",
    "max_completion_tokens": 4000
  }'
```

| Field | V4 Pro | V4.1 Flash |
|---|---|---|
| `messages` | system, user, assistant and tool turns; text only | the same, plus `image_url` parts in user turns |
| `reasoning_effort` | `low` · `high` · `max` (default `high`) | `none` · `low` · `high` · `max` (default `high`) |
| `thinking` | always on; leave it out | `{"type": "disabled"}` has no effect; use `reasoning_effort: "none"` |
| `max_completion_tokens` | up to 393,216 (`max_tokens` also works) | up to 393,216 |
| `tools`, `tool_choice` | function tools | function tools |
| `stream` | `true` for server-sent events | `true` for server-sent events |
| `service_tier` | not supported; leave it out | not supported; leave it out |

The reply is DeepSeek's: the answer in `choices[0].message.content`, the chain of thought beside it in `choices[0].message.reasoning_content`, and token counts in `usage`. Streamed chunks carry `delta.reasoning_content` first, then `delta.content`.

## Responses (converted)

```bash
curl https://argolink.io/v1/responses \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4-pro",
    "instructions": "Answer in at most three sentences.",
    "input": "When should I use a B-tree index instead of a hash index?",
    "reasoning": {"effort": "high"}
  }'
```

| Field | On the gateway |
|---|---|
| `input` | text; on Flash also `input_image` parts. `input_file` parts are dropped |
| `reasoning.effort` | the same values as `reasoning_effort` |
| web search and other server-side tools | dropped |

Codex CLI uses this format. Read the answer from `output[]` items of type `message`, or `output_text` in the SDKs; don't hard-code an array index, because reasoning and tool-call items can come first.

## Anthropic Messages (converted)

```bash
curl https://argolink.io/v1/messages \
  -H "x-api-key: $DEEPSEEK_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4-pro",
    "max_tokens": 4000,
    "system": "Answer in at most three sentences.",
    "messages": [{"role": "user", "content": "When should I use a B-tree index instead of a hash index?"}],
    "output_config": {"effort": "high"}
  }'
```

| Field | On the gateway |
|---|---|
| `model` | the catalog ID (`deepseek-v4-pro`); no Claude name mapping |
| `max_tokens` | required by the Messages format |
| `messages` | text and tool blocks; on Flash also base64 `image` blocks (image URLs are dropped) |
| `output_config.effort` | the same values as `reasoning_effort`; when left out it is sent as `medium`, which DeepSeek runs as `high` |
| web search and other server-side tools | dropped |

Claude Code uses this format. DeepSeek's own Anthropic endpoint differs in a few places: it maps Claude model names to its models, ignores `anthropic-version`, `top_k` and `cache_control`, and supports `thinking` blocks but not `document` blocks.

## Which format to choose

| You use | Format | Why |
|---|---|---|
| OpenAI SDK, LangChain, most OpenAI-compatible tools | Chat Completions | native; `reasoning_effort` and `thinking` behave exactly as documented |
| Codex CLI or code written for the Responses API | Responses | works, with conversion; the effort control survives |
| Claude Code, Anthropic SDK | Anthropic Messages | works, with conversion; send `output_config.effort` if the default `medium` (= `high`) is not what you want |

Behaviour that has to be exact (thinking on or off, effort level) is documented and tested on Chat Completions; prefer it when you have the choice.
