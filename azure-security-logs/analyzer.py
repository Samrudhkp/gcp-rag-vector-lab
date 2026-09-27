"""Analyze fictional login logs for failed-login thresholds.

Pure Python — no Azure SDK required. Used by the Function and by local tests.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any


FAILURE_THRESHOLD = 5


def analyze_login_log(payload: dict[str, Any], *, source_blob: str = "") -> dict[str, Any]:
    """Count failed logins and flag accounts at or above the threshold.

    Expected input shape::

        {
          "source": "...",
          "generated_at": "...",
          "events": [
            {"timestamp": "...", "username": "...", "result": "success"|"failure", "ip": "..."}
          ]
        }
    """
    events = payload.get("events") or []
    if not isinstance(events, list):
        raise ValueError("payload['events'] must be a list")

    failure_counts: Counter[str] = Counter()
    success_counts: Counter[str] = Counter()
    usernames: set[str] = set()

    for i, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError(f"events[{i}] must be an object")
        username = event.get("username")
        result = (event.get("result") or "").strip().lower()
        if not username or not isinstance(username, str):
            raise ValueError(f"events[{i}] missing username")
        usernames.add(username)
        if result == "failure":
            failure_counts[username] += 1
        elif result == "success":
            success_counts[username] += 1
        else:
            raise ValueError(f"events[{i}] result must be 'success' or 'failure'")

    flagged = sorted(
        [
            {
                "username": user,
                "failed_logins": failure_counts[user],
                "reason": f">= {FAILURE_THRESHOLD} failed logins",
            }
            for user, count in failure_counts.items()
            if count >= FAILURE_THRESHOLD
        ],
        key=lambda row: (-row["failed_logins"], row["username"]),
    )

    return {
        "report_type": "failed_login_summary",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_blob": source_blob,
        "threshold": FAILURE_THRESHOLD,
        "total_events": len(events),
        "unique_accounts": len(usernames),
        "failed_login_counts": dict(sorted(failure_counts.items())),
        "success_login_counts": dict(sorted(success_counts.items())),
        "flagged_accounts": flagged,
        "flagged_count": len(flagged),
    }
