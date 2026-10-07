"""Offline tests for scripts/check_catalog.py, run against a saved catalog response."""
import copy
import io
import json
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import check_catalog  # noqa: E402

with open(os.path.join(HERE, "fixtures", "catalog_2026-10-07.json"), encoding="utf-8") as handle:
    ITEMS = json.load(handle)["items"]
with open(check_catalog.DATA, encoding="utf-8") as handle:
    LOCAL = json.load(handle)


def test_documented_facts_match_the_saved_catalog():
    assert check_catalog.compare(LOCAL, ITEMS) == []


def test_price_change_is_reported():
    items = copy.deepcopy(ITEMS)
    items[0]["pricing"]["effective"]["input_per_million"] = 0.5
    problems = check_catalog.compare(LOCAL, items)
    assert problems == ["deepseek-v4-pro: gateway_usd_per_million.input is 0.5 live, 0.528 here"]


def test_removed_and_new_models_are_reported():
    items = [i for i in copy.deepcopy(ITEMS) if i["id"] != "deepseek-v4.1-flash"]
    items.append({"id": "deepseek-v5", "provider_id": "deepseek"})
    problems = check_catalog.compare(LOCAL, items)
    assert "deepseek-v4.1-flash: no longer in the catalog" in problems
    assert "deepseek-v5: new DeepSeek model in the catalog, not documented here" in problems


def test_peak_note_change_is_reported():
    items = copy.deepcopy(ITEMS)
    items[1]["note"] = None
    assert any("peak-hour note" in p for p in check_catalog.compare(LOCAL, items))


def test_main_exit_code_and_user_agent(monkeypatch, capsys):
    seen = {}

    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            pass

    def urlopen(request, timeout=None):
        seen["ua"] = request.get_header("User-agent")
        return Response(json.dumps({"items": ITEMS}).encode())

    monkeypatch.setattr(check_catalog.urllib.request, "urlopen", urlopen)
    assert check_catalog.main([]) == 0
    assert "OK: 2 models" in capsys.readouterr().out
    assert not seen["ua"].startswith("Python-urllib")
