"""Small Argolink DeepSeek V4 Pro client."""
from __future__ import annotations
import os
from typing import Any, Dict, Optional, Sequence
import requests

MODEL_ID = "deepseek-v4-pro"
DEFAULT_BASE_URL = "https://api.argolink.io"
EFFORTS = {"low", "high", "max"}

class DeepSeekAPIError(RuntimeError):
    def __init__(self, message: str, *, status_code: Optional[int] = None, payload: Any = None):
        super().__init__(message); self.status_code = status_code; self.payload = payload

class DeepSeekAPI:
    def __init__(self, api_key: Optional[str] = None, *, base_url: Optional[str] = None, session: Optional[requests.Session] = None, timeout: float = 60):
        self.api_key = api_key or os.getenv("ARGOLINK_API_KEY")
        if not self.api_key: raise DeepSeekAPIError("ARGOLINK_API_KEY is required")
        self.base_url = (base_url or os.getenv("ARGOLINK_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.session = session or requests.Session(); self.timeout = timeout

    def chat(self, messages: Sequence[Dict[str, Any]], *, reasoning_effort: str = "high", stream: bool = False) -> Dict[str, Any]:
        if not messages: raise DeepSeekAPIError("messages must not be empty")
        if reasoning_effort not in EFFORTS: raise DeepSeekAPIError("reasoning_effort must be low, high, or max")
        body = {"model": MODEL_ID, "messages": list(messages), "reasoning_effort": reasoning_effort, "stream": stream}
        try:
            response = self.session.post(f"{self.base_url}/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, json=body, timeout=self.timeout)
        except requests.RequestException as exc: raise DeepSeekAPIError(f"network error: {exc}") from exc
        try: payload = response.json()
        except ValueError: payload = response.text
        if response.status_code >= 400: raise DeepSeekAPIError(f"Argolink returned HTTP {response.status_code}", status_code=response.status_code, payload=payload)
        if not isinstance(payload, dict): raise DeepSeekAPIError("expected a JSON object", payload=payload)
        return payload
