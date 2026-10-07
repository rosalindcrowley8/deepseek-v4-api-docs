"""Compare data/deepseek-v4.json with the live public model catalog.

    python scripts/check_catalog.py            # exit 1 if any fact here is stale
    python scripts/check_catalog.py --json     # print the live DeepSeek entries

No key is needed: the catalog endpoint is public. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "deepseek-v4.json")
CATALOG_URL = "https://argolink.io/api/catalog/v1/models?category=chat&sort=provider&page_size=100"
# The site answers Python's default "Python-urllib/3.x" agent with 403, so name the script.
USER_AGENT = "deepseek-v4-api-docs/1.0"


def fetch_catalog(url: str = CATALOG_URL) -> list:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())["items"]


def compare(local: dict, items: list) -> list:
    """Return human-readable differences; an empty list means everything matches."""
    live = {item["id"]: item for item in items if item.get("provider_id") == "deepseek"}
    problems = []
    for model_id, facts in local["models"].items():
        item = live.get(model_id)
        if item is None:
            problems.append(f"{model_id}: no longer in the catalog")
            continue
        text, pricing = item.get("text", {}), item.get("pricing", {})
        checks = {
            "context_tokens": (facts["context_tokens"], text.get("context_tokens")),
            "max_output_tokens": (facts["max_output_tokens"], text.get("max_output_tokens")),
            "efforts": (facts["efforts"], text.get("efforts")),
            "default_effort": (facts["default_effort"], text.get("default_effort")),
            "images": (facts["images"], bool(text.get("images"))),
        }
        for side, key in (("gateway_usd_per_million", "effective"), ("official_usd_per_million", "official")):
            price = pricing.get(key, {})
            checks[f"{side}.input"] = (facts[side]["input"], price.get("input_per_million"))
            checks[f"{side}.cached_input"] = (facts[side]["cached_input"], price.get("cached_input_per_million"))
            checks[f"{side}.output"] = (facts[side]["output"], price.get("output_per_million"))
        for name, (ours, theirs) in checks.items():
            if ours != theirs:
                problems.append(f"{model_id}: {name} is {theirs!r} live, {ours!r} here")
        note = (item.get("note") or {}).get("en", "")
        if "twice" not in note:
            problems.append(f"{model_id}: the peak-hour note changed: {note!r}")
    for model_id in sorted(set(live) - set(local["models"])):
        problems.append(f"{model_id}: new DeepSeek model in the catalog, not documented here")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", action="store_true", help="print the live DeepSeek catalog entries")
    args = parser.parse_args(argv)
    items = fetch_catalog()
    if args.json:
        print(json.dumps([i for i in items if i.get("provider_id") == "deepseek"], indent=2, ensure_ascii=False))
        return 0
    with open(DATA, encoding="utf-8") as handle:
        local = json.load(handle)
    problems = compare(local, items)
    for line in problems:
        print("STALE", line)
    if not problems:
        print(f"OK: {len(local['models'])} models match the live catalog (facts dated {local['checked']})")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
