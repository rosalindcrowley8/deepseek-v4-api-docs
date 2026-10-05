#!/usr/bin/env bash
set -euo pipefail
: "${ARGOLINK_API_KEY:?set ARGOLINK_API_KEY first}"
BASE_URL="${ARGOLINK_BASE_URL:-https://api.argolink.io}"
curl -sS "$BASE_URL/v1/chat/completions" \
  -H "Authorization: Bearer ${ARGOLINK_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{"model":"deepseek-v4-pro","messages":[{"role":"user","content":"Give one practical idempotency rule"}],"reasoning_effort":"low"}'
