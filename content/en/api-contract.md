# API contract

## Request

`POST https://api.argolink.io/v1/chat/completions` with `Authorization: Bearer $ARGOLINK_API_KEY`. The request must include `model` and `messages`.

| Field | Rule |
|---|---|
| `model` | exactly `deepseek-v4-pro` |
| `messages` | chat-compatible message array |
| `reasoning_effort` | `low`, `high`, or `max`; omitted means `high` |
| `stream` | use only when the caller can consume SSE safely |

Thinking remains enabled at every effort. Do not add a fake `thinking.type=disabled` switch.

## Errors

Treat a 4xx response as a request or authentication problem and fix the payload before retrying. Treat 5xx and transport failures as uncertain completion state; do not blindly repeat a paid call. Preserve `request_id` from the JSON error for support.

## Billing

Count input, output, and cached input separately. The model page is authoritative for current prices and peak-window rules.
