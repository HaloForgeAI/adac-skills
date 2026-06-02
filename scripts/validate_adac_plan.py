#!/usr/bin/env python3
"""Validate a Markdown ADAC plan for required sections and acceptance rows."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = [
    "## 1. 任务与风险分级",
    "## 2. Context Pack",
    "## 3. Spec Boundary",
    "## 4. Acceptance Matrix",
    "## 5. User Verification Scenarios",
    "## 6. Agent Work Plan",
    "## 7. Human Gates",
    "## 8. Evidence Log",
    "## 9. Residual Risk",
    "## 10. Reusable Assets",
]

REQUIRED_ACCEPTANCE_RISKS = {
    "behavior": ("behavior", "行为"),
    "regression": ("regression", "回归"),
    "observability": ("observability", "排障", "可观测"),
}


def section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    next_match = re.search(r"^##\s+", text[start + len(heading):], flags=re.MULTILINE)
    if not next_match:
        return text[start:]
    return text[start:start + len(heading) + next_match.start()]


def validate(path: Path, allow_placeholders: bool) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if not text.startswith("# ADAC Plan:"):
        errors.append("document must start with '# ADAC Plan:'")

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing required heading: {heading}")

    if not allow_placeholders and re.search(r"<[^>\n]+>", text):
        errors.append("document contains angle-bracket placeholders")

    matrix = section(text, "## 4. Acceptance Matrix")
    rows = [line for line in matrix.splitlines() if re.match(r"^\|\s*AC-[0-9]{2,}\s*\|", line)]
    if len(rows) < 3:
        errors.append("acceptance matrix must contain at least 3 AC-* rows")

    lower_matrix = matrix.lower()
    for risk_name, aliases in REQUIRED_ACCEPTANCE_RISKS.items():
        if not any(alias.lower() in lower_matrix for alias in aliases):
            errors.append(f"acceptance matrix must include {risk_name} risk coverage")

    user_scenarios = section(text, "## 5. User Verification Scenarios")
    user_scenario_rows = [
        line
        for line in user_scenarios.splitlines()
        if re.match(r"^\|\s*UV-[0-9]{2,}\s*\|", line)
    ]
    lower_user_scenarios = user_scenarios.lower()
    if not user_scenario_rows and not any(
        marker in lower_user_scenarios
        for marker in ("not applicable", "not-applicable", "n/a", "不适用")
    ):
        errors.append("user verification scenarios must include at least one UV-* row or a not-applicable reason")

    gates = section(text, "## 7. Human Gates").lower()
    if "pending" not in gates and "approved" not in gates and "blocked" not in gates:
        errors.append("human gates must contain a recognizable decision state")

    evidence = section(text, "## 8. Evidence Log")
    if not allow_placeholders and "skipped" in evidence.lower() and "why" not in evidence.lower():
        errors.append("skipped evidence should include why it was skipped")

    risk_match = re.search(r"^Risk class:\s*([ABCD])\b", text, flags=re.MULTILINE)
    if risk_match and risk_match.group(1) in {"C", "D"}:
        high_risk_record = "\n".join(
            [
                section(text, "## 3. Spec Boundary"),
                section(text, "## 6. Agent Work Plan"),
                section(text, "## 7. Human Gates"),
                section(text, "## 8. Evidence Log"),
                section(text, "## 9. Residual Risk"),
            ]
        ).lower()
        if not any(term in high_risk_record for term in ("rollback", "fallback", "回滚", "回退")):
            errors.append("class C/D plans must document rollback or fallback readiness")
        if not any(term in high_risk_record for term in ("independent", "review", "human", "人工", "审查", "复核")):
            errors.append("class C/D plans must include independent or human verification evidence")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Markdown ADAC plan path")
    parser.add_argument("--allow-placeholders", action="store_true", help="Allow template placeholders")
    args = parser.parse_args()

    if not args.plan.exists():
        print(f"error: file not found: {args.plan}", file=sys.stderr)
        return 2

    errors = validate(args.plan, args.allow_placeholders)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"ok: {args.plan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
