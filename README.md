# DeepSeek V4 API docs — from $0.12 per 1M input tokens

**DeepSeek V4 Pro and V4.1 Flash are live on [ArgoLink](https://argolink.io/gh-deepseek-v4-api-docs)**: Pro at $0.528 / $1.584 and Flash at $0.12 / $0.48 per 1M input / output tokens, 20% below DeepSeek's own price.
Both have a 1,048,576-token context, up to 393,216 output tokens, thinking mode and tool calls; Flash also reads images. Call them through OpenAI Chat Completions, Responses or Anthropic Messages.

[Models](content/en/models.md) · [Pricing](content/en/pricing.md) · [Endpoints](content/en/endpoints.md) · [Reasoning](content/en/reasoning.md) · [Vision](content/en/vision.md) · [Migrate](content/en/migrate.md) · [FAQ](content/en/faq.md)

<sub>Last checked: 2026-10-07. Every page lists its sources in its front matter, and `python scripts/check_catalog.py` re-checks the numbers against the live catalog. Unofficial; not affiliated with DeepSeek.</sub>

## At a glance

| | DeepSeek V4 Pro | DeepSeek V4.1 Flash |
|---|---|---|
| Model ID | `deepseek-v4-pro` | `deepseek-v4.1-flash` (`deepseek-flash` on api.deepseek.com) |
| Context / max output | 1,048,576 / 393,216 tokens | 1,048,576 / 393,216 tokens |
| Input | text | text, images |
| Thinking | always on | on by default, `reasoning_effort: "none"` turns it off |
| `reasoning_effort` | `low` · `high` · `max`, default `high` | `low` · `high` · `max`, default `high` |
| Endpoints | `/v1/chat/completions` (native) · `/v1/responses` · `/v1/messages` | the same |
| Price per 1M, input / cached / output | $0.528 / $0.0176 / $1.584 | $0.12 / $0.0024 / $0.48 |
| Peak hours | 2× on weekdays 01:00–04:00 and 06:00–10:00 UTC | the same |

## First request

```bash
export DEEPSEEK_API_KEY=your-key   # a key for the endpoint you call
curl https://argolink.io/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-v4-pro", "reasoning_effort": "high",
       "messages": [{"role": "user", "content": "Explain write-ahead logging in three sentences."}]}'
```

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://argolink.io/v1")
reply = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    reasoning_effort="none",                    # Flash only: skip thinking for speed
    messages=[{"role": "user", "content": "Translate to French: the build is green."}],
)
print(reply.choices[0].message.content)
```

```js
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.DEEPSEEK_API_KEY, baseURL: "https://argolink.io/v1" });
const stream = await client.chat.completions.create({
  model: "deepseek-v4-pro",
  stream: true,
  messages: [{ role: "user", content: "Review this regex for catastrophic backtracking: (a+)+$" }],
});
for await (const chunk of stream) process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
```

[Create a key](https://argolink.io/gh-deepseek-v4-api-docs). The same requests work against `https://api.deepseek.com` with a DeepSeek key once Flash is renamed `deepseek-flash` and thinking is switched off with `thinking: {"type": "disabled"}` instead; [migrate](content/en/migrate.md) lists every difference.

## What each page answers

The pages say "the gateway" for ArgoLink's API at `https://argolink.io/v1` and "api.deepseek.com" for DeepSeek's own.

| Page | Questions it settles |
|---|---|
| [models.md](content/en/models.md) | Which ID do I send? Which version does DeepSeek serve? What replaced `deepseek-v4-pro-0813`? |
| [pricing.md](content/en/pricing.md) | What does a 400K-token repo review cost? When do peak rates apply? What do other routes charge? |
| [endpoints.md](content/en/endpoints.md) | Which base URL goes in which SDK? Which fields survive the Responses and Messages conversions? |
| [reasoning.md](content/en/reasoning.md) | How do I turn thinking off, and why didn't `thinking.type: "disabled"` work? What about `reasoning_content` and tools? |
| [vision.md](content/en/vision.md) | How do I send a screenshot to Flash on each format, and how large can it be? |
| [migrate.md](content/en/migrate.md) | What changes between api.deepseek.com and the gateway? How do I run Claude Code on V4 Pro? |
| [faq.md](content/en/faq.md) | 403 `error code: 1010`, a 400 on the second tool turn, JSON Output, billing of failed calls |

## Price snapshot

USD per 1M tokens, off-peak, checked 2026-10-07.

| Model | ArgoLink | DeepSeek official | Lowest-price route listed on OpenRouter |
|---|---:|---:|---:|
| V4 Pro, input / output | **$0.528 / $1.584** | $0.66 / $1.98 ([pricing](https://api-docs.deepseek.com/quick_start/pricing)) | $0.66 / $1.98, DeepSeek itself ([routes](https://openrouter.ai/deepseek/deepseek-v4-pro-0813)) |
| V4.1 Flash, input / output | **$0.12 / $0.48** | $0.15 / $0.60 | $0.09 / $0.18, an fp4 route ([routes](https://openrouter.ai/deepseek/deepseek-v4.1-flash)) |

"Lowest-price" here means the lowest output price among the routes OpenRouter listed that day. All DeepSeek prices double in the peak windows; [pricing](content/en/pricing.md) has peak rates and worked examples.

## Point an agent at it

The pages are plain Markdown with stable paths, and [llms.txt](llms.txt) indexes them. Clone the repo and ask your coding agent:

```bash
git clone https://github.com/rosalindcrowley8/deepseek-v4-api-docs
cd deepseek-v4-api-docs
claude "Which request turns off thinking on deepseek-v4.1-flash, and does the same work on deepseek-v4-pro?"
claude "Estimate the monthly cost of 2,000 RAG calls a day at 50k input, 40k of it cached, 1k output"
```

## Keeping it current

| File | Role |
|---|---|
| `data/deepseek-v4.json` | the numbers used on these pages: IDs, limits, efforts, both price sets |
| `scripts/check_catalog.py` | fetches the public catalog (no key) and exits 1 if anything in the JSON is stale or a new DeepSeek model appeared |
| `tests/` | offline tests of the checker against a saved catalog response |

```bash
python scripts/check_catalog.py     # OK: 2 models match the live catalog (facts dated 2026-10-07)
pip install pytest && pytest tests/
```

DeepSeek-side facts (peak windows, limits, thinking rules) come from api-docs.deepseek.com and are re-read by hand; the `sources:` list on each page says where.

## FAQ

**Is this DeepSeek's documentation?**
No. It is an unofficial reference for one way of calling DeepSeek V4, written against DeepSeek's docs and the gateway's pages. DeepSeek's own docs are at [api-docs.deepseek.com](https://api-docs.deepseek.com/).

**Why is the price lower than DeepSeek's?**
The gateway sells DeepSeek V4 at 80% of DeepSeek's list price on every line, cache hits included, and applies the same peak-hour doubling.

**Can I keep using DeepSeek's own API for some calls?**
Yes. The request formats are the same, so you can mix both: keep FIM, prefix completion or Files API calls on DeepSeek's API and send the rest through the gateway.

**Which format should I use?**
Chat Completions, unless your client only speaks Responses (Codex) or Anthropic Messages (Claude Code). It is DeepSeek's native format and the one where every thinking control is documented to take effect.

## License

MIT for this repository's text and code. DeepSeek is a trademark of its owner.
