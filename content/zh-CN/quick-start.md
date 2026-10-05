# 快速开始

```bash
export ARGOLINK_API_KEY='your-key'
curl -sS https://api.argolink.io/v1/chat/completions \
  -H "Authorization: Bearer ${ARGOLINK_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{"model":"deepseek-v4-pro","messages":[{"role":"user","content":"用两句话解释什么是幂等 API"}],"reasoning_effort":"low"}'
```

模型 ID 必须使用 `deepseek-v4-pro`。需要精确控制推理强度时使用 Chat Completions。
