"""Local runner: analyze sample login logs without Azure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running as `python scripts/run_local.py` from the project root.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analyzer import analyze_login_log  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a login-log JSON file locally.")
    parser.add_argument(
        "input",
        nargs="?",
        default=str(ROOT / "samples" / "login-log-alice-flagged.json"),
        help="Path to a login-log JSON file",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional path to write the JSON report (default: print to stdout)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    report = analyze_login_log(payload, source_blob=str(input_path))

    text = json.dumps(report, indent=2)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {out}")
    else:
        print(text)

    flagged = report["flagged_accounts"]
    if flagged:
        names = ", ".join(f"{row['username']}({row['failed_logins']})" for row in flagged)
        print(f"\nFlagged: {names}", file=sys.stderr)
    else:
        print("\nFlagged: none", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
