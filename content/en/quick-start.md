# Quick start

```bash
export ARGOLINK_API_KEY='your-key'
curl -sS https://api.argolink.io/v1/chat/completions \
  -H "Authorization: Bearer ${ARGOLINK_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{"model":"deepseek-v4-pro","messages":[{"role":"user","content":"Explain an idempotent API in two sentences"}],"reasoning_effort":"low"}'
```

Use the returned JSON as the request result. Keep the `model` ID exact; the former dated alias is not used by new examples.
