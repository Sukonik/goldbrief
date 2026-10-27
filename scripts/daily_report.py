#!/usr/bin/env python3
"""Merge structural + browser QA into reports/daily-site-check.json and a review note.

Usage: daily_report.py structural.json browser.json
Exit 0 always; the workflow reads the `result` field to decide whether to open an issue.
"""
import datetime as dt, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
load = lambda p: json.loads(Path(p).read_text())
def safe(path):
    try: return load(path)
    except Exception: return None
struct, browser = load(sys.argv[1]), safe(sys.argv[2])
browser_ran = isinstance(browser, dict) and "failures" in browser
browser = browser if browser_ran else {"failures": []}
prev = {}
try: prev = json.loads((ROOT / "reports/daily-site-check.json").read_text())
except Exception: pass
PRIORITY = {"js-error": "P1", "console-error": "P2", "horizontal-overflow": "P2", "drawer": "P1"}
findings = [{"check": "structure", "page": "-", "detail": e, "priority": "P1"} for e in struct.get("errors", [])]
findings += [{**f, "priority": PRIORITY.get(f["check"], "P3")} for f in browser.get("failures", [])]
key = lambda f: (f["check"], f["page"], f["detail"])
old = {key(f) for f in prev.get("findings", [])}
for f in findings: f["new_regression"] = key(f) not in old
report = {"result": "FAIL" if findings else ("PASS" if browser_ran else "PARTIAL"),
          "browser_checks": "ran" if browser_ran else "unavailable (tooling error); structural checks only",
          "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
          "scope": "Structural + headless-browser checks (overflow at 320-1920px, JS errors, mobile drawer). Visual quality is not judged automatically.",
          "pages_checked": browser.get("pages"), "widths": browser.get("widths"),
          "findings": findings,
          "new_regressions": sum(f["new_regression"] for f in findings),
          "human_review_required": True,
          "human_review_note": "Any visual or editorial change proposed by these results must be reviewed by a person and shipped through a pull request."}
(ROOT / "reports/daily-site-check.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: report[k] for k in ("result", "new_regressions")}), len(findings), "findings")
