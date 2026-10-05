# Checked Argolink facts

Checked 2026-10-04 against the Argolink catalog and the current model page.

- Model ID: `deepseek-v4-pro`; endpoint: `POST /v1/chat/completions`.
- Context window: 1,048,576 tokens; maximum output: 393,216 tokens.
- `reasoning_effort`: `low`, `high`, or `max`; default `high`. `minimal` maps to `low`; `medium` and `xhigh` map to `high`.
- Thinking cannot be disabled; `thinking.type=disabled` and `reasoning_effort=none` are ignored.
- Pricing is token based: input $0.66/M, output $1.98/M, cached input $0.022/M. Weekday 09:00–12:00 and 14:00–18:00 Beijing time are billed at twice the listed rates.
- The model page also accepts Responses and Messages shapes; this repository uses Chat Completions when effort control matters.
