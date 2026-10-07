---
title: Image input with DeepSeek V4.1 Flash
checked: 2026-10-07
sources:
  - https://argolink.io/en/models/deepseek-v4.1-flash
  - https://argolink.io/en/docs
  - https://api-docs.deepseek.com/guides/vision
  - https://api-docs.deepseek.com/guides/responses_api
---

# Image input (V4.1 Flash only)

`deepseek-v4.1-flash` reads images; `deepseek-v4-pro` reads text only. How an image is accepted depends on the request format:

| Format | How to send an image | Accepted sources |
|---|---|---|
| Chat Completions | a content part `{"type": "image_url", "image_url": {"url": ...}}` in a user turn | public HTTPS URL or `data:` URL |
| Responses | a content part `{"type": "input_image", "image_url": ...}` | public HTTPS URL or `data:` URL |
| Anthropic Messages | an `image` block with a base64 `source` | base64 only: image URLs are dropped on the gateway |

## Chat Completions

```bash
curl https://argolink.io/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4.1-flash",
    "reasoning_effort": "low",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "List every error message visible in this screenshot."},
        {"type": "image_url", "image_url": {"url": "https://example.com/screenshot.png"}}
      ]
    }]
  }'
```

A local file goes in as a data URL:

```python
import base64
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://argolink.io/v1")
with open("invoice.png", "rb") as f:
    data_url = "data:image/png;base64," + base64.b64encode(f.read()).decode()

reply = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Return the invoice number, date and total as JSON."},
        {"type": "image_url", "image_url": {"url": data_url}},
    ]}],
)
print(reply.choices[0].message.content)
```

## Anthropic Messages

Only base64 images carry over through the gateway's conversion:

```json
{
  "model": "deepseek-v4.1-flash",
  "max_tokens": 1000,
  "messages": [{
    "role": "user",
    "content": [
      {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "<BASE64>"}},
      {"type": "text", "text": "What does this chart show?"}
    ]
  }]
}
```

## Limits DeepSeek documents

These are DeepSeek's own limits for `deepseek-flash`. The gateway's pages do not publish separate numbers.

| Limit | Value |
|---|---|
| Formats | JPEG, PNG, GIF, WebP, detected from the file content |
| One image, base64 or URL | 32 MiB; a URL must download within 60 seconds |
| Image URL length | 8,192 characters |
| Request body, base64 images included | 48 MiB |
| Images per request | 600, at most 64 MiB in total |
| Image size | 8,192 px per side, 4,096 px when a request has 15 or more images |
| Where images may appear | user messages (Chat Completions); user and developer items and tool outputs (Responses); never system or assistant, which returns 400 |

## Image or text-only model?

If a request with image parts reaches `deepseek-v4-pro`, the model cannot see the image. Route image requests to Flash explicitly. In a fallback chain, skip text-only models for them, or describe the image with Flash first and pass the text to Pro.
