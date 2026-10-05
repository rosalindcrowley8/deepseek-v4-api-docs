# DeepSeek V4 Pro API Docs

A searchable Argolink guide for **DeepSeek V4 Pro**: the chat-compatible chat contract, reasoning controls, pricing units, operational errors, and a small offline content tree.

[DeepSeek V4 Pro model page →](https://argolink.io/gh-deepseek-v4-api-docs) · [Argolink API docs →](https://argolink.io/gh-unified-api-docs)

The model page is authoritative for live availability and pricing. This repository makes the integration details easy to search and review; it is not a second catalog.

## Contents

- `content/en/quick-start.md` and `content/zh-CN/quick-start.md`: the first request in two languages.
- `content/en/api-contract.md`: endpoint, request, response, reasoning, and error rules.
- `content/en/faq.md`: questions that repeatedly cause integration mistakes.
- `llms.txt`: a small machine-readable index for agents.
- `deepseek_api.py`: a dependency-light synchronous client.
- `examples/chat.sh`: a safe curl request that does not retry submission.

## Quick start

```bash
export ARGOLINK_API_KEY='your-key'
./examples/chat.sh
```

The endpoint is `POST /v1/chat/completions`; set `model` to `deepseek-v4-pro`. The normal response is JSON. For exact reasoning control use `low`, `high`, or `max`. Thinking is always on for this model, so attempts to disable it are ignored.

## Facts used by this draft

- Context: 1,048,576 tokens; maximum output: 393,216 tokens.
- Default reasoning effort: `high`; `minimal` maps to `low`, while `medium` and `xhigh` map to `high`.
- Input price: $0.66 per million tokens; output: $1.98; cached input: $0.022. Weekday peak windows are billed at twice the listed rates.

See [`argolink/FACTS.md`](argolink/FACTS.md) and [`content/en/api-contract.md`](content/en/api-contract.md) for the complete checked table.

## Safety

Never put a key in a Markdown example, shell history committed to the repository, or an issue. A network timeout is not proof that a job was rejected; chat callers should decide whether a request is safe to repeat.
