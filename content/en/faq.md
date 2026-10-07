---
title: DeepSeek V4 API FAQ
checked: 2026-10-07
sources:
  - https://argolink.io/en/models/deepseek-v4-pro
  - https://argolink.io/en/models/deepseek-v4.1-flash
  - https://argolink.io/en/docs
  - https://api-docs.deepseek.com/quick_start/pricing
  - https://api-docs.deepseek.com/guides/thinking_mode
  - https://api-docs.deepseek.com/quick_start/error_codes
---

# DeepSeek V4 API FAQ

### What are the model IDs?
`deepseek-v4-pro` and `deepseek-v4.1-flash` on the gateway. DeepSeek's own API calls the second one `deepseek-flash`. `curl -s https://argolink.io/v1/models` lists the current IDs without a key.

### How much does DeepSeek V4 Pro cost?
On the gateway, $0.528 per 1M input tokens, $0.0176 per 1M cached input tokens and $1.584 per 1M output tokens: 20% below DeepSeek's off-peak $0.66 / $0.022 / $1.98. Both double on weekdays 01:00–04:00 and 06:00–10:00 UTC. Details and worked examples: [pricing](pricing.md).

### And V4.1 Flash?
$0.12 / $0.0024 / $0.48 per 1M on the gateway, against DeepSeek's $0.15 / $0.003 / $0.60 off-peak, with the same peak rule.

### How big is the context window?
1,048,576 tokens for both models, with up to 393,216 output tokens per response.

### Can I turn thinking off?
On V4.1 Flash, yes: send `reasoning_effort: "none"`. On V4 Pro through the gateway, no: it always thinks, and both `reasoning_effort: "none"` and `thinking: {"type": "disabled"}` are ignored. Use `reasoning_effort: "low"` for the shortest reasoning. DeepSeek's own API turns thinking off with `thinking: {"type": "disabled"}` on both models. See [reasoning](reasoning.md).

### Why did my parameter do nothing?
Ignored fields still return HTTP 200. In thinking mode `temperature`, `presence_penalty` and `frequency_penalty` have no effect, `thinking.type: "disabled"` has no effect on the gateway, and V4 Pro ignores `reasoning_effort: "none"`. Check `usage.completion_tokens_details.reasoning_tokens` to see whether reasoning happened.

### My second tool-calling turn fails with 400. Why?
DeepSeek requires the `reasoning_content` of every earlier assistant turn to be sent back when the request carries `tools`. Append the assistant message exactly as you received it instead of rebuilding it with only `content` and `tool_calls`.

### Does V4 Pro read images?
No. Only V4.1 Flash does: `image_url` parts on Chat Completions (HTTPS or data URL), `input_image` on Responses, base64 `image` blocks on Anthropic Messages. See [vision](vision.md).

### Can I use Claude Code or the Anthropic SDK?
Yes. Use the base URL `https://argolink.io` (no `/v1`) and the model ID `deepseek-v4-pro`; the gateway converts Messages requests to Chat Completions. Set `ANTHROPIC_DEFAULT_HAIKU_MODEL` as well, because Claude Code sends background tasks to the `haiku` alias. See [migrate](migrate.md#claude-code-and-other-anthropic-clients).

### What are the rate limits?
DeepSeek publishes 500 concurrent requests per account for V4 Pro and 2,500 for Flash, and answers 429 above that. The gateway does not publish a per-model limit. Either way, treat 429 and 503 as retryable, and 400, 401, 402 and 422 as errors to fix.

### My Python script gets `403` with the body `error code: 1010`.
That is Cloudflare refusing Python's default `Python-urllib/3.x` User-Agent before the request reaches the API. Send any other `User-Agent` header. The OpenAI and Anthropic SDKs, `requests` and `httpx` already do.

### Is JSON Output supported?
DeepSeek supports `response_format: {"type": "json_object"}`; it asks for the word "json" in the prompt and an example of the shape, and warns that the content can occasionally be empty. The gateway forwards Chat Completions fields to DeepSeek as sent but does not document JSON Output itself, so test it with your prompts.

### Are failed requests billed?
A request rejected with an HTTP error has no `usage`. A request that times out on your side may still finish upstream and be billed, so prefer streaming and set `max_completion_tokens` on long jobs.
