---
title: DeepSeek V4 thinking mode and reasoning effort
checked: 2026-10-07
sources:
  - https://argolink.io/en/docs
  - https://argolink.io/en/models/deepseek-v4-pro
  - https://argolink.io/en/models/deepseek-v4.1-flash
  - https://api-docs.deepseek.com/guides/thinking_mode
---

# Thinking mode and reasoning effort

Both V4 models think before they answer by default. The controls differ between DeepSeek's own API and the gateway, which is the most common source of "my parameter did nothing" bugs.

## The controls side by side

| | Gateway, `deepseek-v4-pro` | Gateway, `deepseek-v4.1-flash` | api.deepseek.com, both models |
|---|---|---|---|
| Default | thinking on, effort `high` | thinking on, effort `high` | thinking on, effort `high` |
| Set the effort | `reasoning_effort`: `low` · `high` · `max` | `reasoning_effort`: `low` · `high` · `max` | `reasoning_effort`: `low` · `high` · `max` |
| Aliases | `minimal` → `low`; `medium`, `xhigh` → `high` | the same | the same, plus `ultra` → `max` |
| Turn thinking off | not possible: `thinking.type: "disabled"` and `reasoning_effort: "none"` are both ignored | `reasoning_effort: "none"`; `thinking.type: "disabled"` has no effect | `thinking: {"type": "disabled"}` |
| Responses format | `reasoning.effort` | `reasoning.effort` | `reasoning.effort`, where `none` turns thinking off |
| Anthropic format | `output_config.effort`, sent as `medium` when left out | the same | `output_config.effort`; thinking toggled with `thinking` |

An unknown or ignored field still returns HTTP 200, so success does not prove a control worked. Check `usage.completion_tokens_details.reasoning_tokens`, or the length of `reasoning_content`, when it matters.

## Faster answers

```bash
# Flash with thinking off: the cheapest, lowest-latency call
curl https://argolink.io/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "deepseek-v4.1-flash", "reasoning_effort": "none",
       "messages": [{"role": "user", "content": "Classify the sentiment: \"The update broke my login.\""}]}'

# Pro cannot stop thinking; low effort is the shortest it gets
curl https://argolink.io/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "deepseek-v4-pro", "reasoning_effort": "low", "stream": true,
       "messages": [{"role": "user", "content": "Rename these variables to snake_case: userId, createdAt"}]}'
```

Streaming does not shorten the work, but the reasoning tokens arrive as they are produced, so a client can show progress instead of waiting in silence.

## Reading the chain of thought

DeepSeek returns the reasoning in `reasoning_content`, next to `content`:

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://argolink.io/v1")
reply = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": "Is 2^31 - 1 prime?"}],
    reasoning_effort="max",
)
message = reply.choices[0].message
print(getattr(message, "reasoning_content", None))  # the thinking, if present
print(message.content)                              # the answer
```

The OpenAI SDK keeps unknown response fields, so `reasoning_content` is readable as an attribute even though it is not part of OpenAI's schema. In a stream, read `chunk.choices[0].delta.reasoning_content` until `delta.content` starts.

## Multi-turn conversations

DeepSeek's thinking-mode guide sets two rules:

1. **Without `tools`**, earlier `reasoning_content` is not needed. If you send it back it is ignored and not added to the context.
2. **With `tools`**, every earlier assistant turn's `reasoning_content` must be sent back, even on turns without a tool call. If it is missing, DeepSeek returns 400.

The simplest way to satisfy both is to append the assistant message object exactly as you received it:

```python
messages.append(reply.choices[0].message)   # keeps content, reasoning_content and tool_calls
```

## Parameters that stop working in thinking mode

Per DeepSeek's guide: `temperature`, `presence_penalty` and `frequency_penalty` are accepted but have no effect, and `top_p` only applies between 0.95 and 1.0 (lower values are treated as 0.95). On the gateway, V4 Pro always thinks, so these parameters never apply to it. Flash with `reasoning_effort: "none"` runs in non-thinking mode, where DeepSeek fixes `top_p` at 1.0.

## Cost of thinking

Reasoning tokens are billed as output tokens: $1.584 per 1M on V4 Pro and $0.48 on Flash through the gateway. `max_completion_tokens` caps reasoning and answer together, so set it, or a hard prompt at `max` effort can run to the 393,216-token output limit.
