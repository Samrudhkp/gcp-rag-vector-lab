"""Unit tests for analyzer (no Azure credentials required)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analyzer import FAILURE_THRESHOLD, analyze_login_log  # noqa: E402

SAMPLES = ROOT / "samples"


def test_alice_is_flagged():
    payload = json.loads((SAMPLES / "login-log-alice-flagged.json").read_text())
    report = analyze_login_log(payload, source_blob="samples/login-log-alice-flagged.json")
    assert report["failed_login_counts"]["alice"] == 5
    assert report["flagged_count"] == 1
    assert report["flagged_accounts"][0]["username"] == "alice"
    assert report["threshold"] == FAILURE_THRESHOLD


def test_clean_log_flags_nobody():
    payload = json.loads((SAMPLES / "login-log-clean.json").read_text())
    report = analyze_login_log(payload)
    assert report["flagged_count"] == 0
    assert report["flagged_accounts"] == []
    assert report["failed_login_counts"]["dave"] == 2


def test_multi_flagged_sorted_by_failures():
    payload = json.loads((SAMPLES / "login-log-multi-flagged.json").read_text())
    report = analyze_login_log(payload)
    assert report["flagged_count"] == 2
    assert [row["username"] for row in report["flagged_accounts"]] == ["grace", "heidi"]
    assert report["flagged_accounts"][0]["failed_logins"] == 6
    assert report["flagged_accounts"][1]["failed_logins"] == 5


def test_rejects_bad_result():
    with pytest.raises(ValueError, match="success|failure"):
        analyze_login_log({"events": [{"username": "x", "result": "maybe"}]})
