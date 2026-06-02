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

AC_STATUSES = {"pending", "pass", "fail", "blocked", "skipped", "not-applicable"}
GATE_DECISIONS = {"pending", "approved", "approved-with-risk", "blocked", "not-applicable"}
VAGUE_TERMS = (
    "improve",
    "improves",
    "improved",
    "improving",
    "optimize",
    "optimizes",
    "optimized",
    "optimization",
    "better",
    "faster",
    "reduce",
    "reduces",
    "reduced",
    "decrease",
    "decreases",
    "decreased",
    "increase",
    "increases",
    "increased",
    "enhance",
    "quality",
    "提升",
    "优化",
    "减少",
    "降低",
    "提高",
    "更快",
    "更好",
    "改善",
    "改进",
)
CHECKABLE_MARKERS = (
    "scenario",
    "test",
    "command",
    "manual",
    "profile",
    "log",
    "telemetry",
    "trace",
    "fixed",
    "same-scene",
    "before/after",
    "steps",
    "reproduce",
    "reproducible",
    "invariant",
    "without",
    "does not",
    "must not",
    "exactly",
    "at least",
    "no more",
    "less than",
    "greater than",
    "under",
    "within",
    "baseline",
    "threshold",
    "场景",
    "测试",
    "日志",
    "指标",
    "固定",
    "复现",
    "不超过",
    "不少于",
    "至少",
    "小于",
    "大于",
    "基线",
    "阈值",
)
MEASUREMENT_PATTERN = re.compile(
    r"\d+(?:\.\d+)?\s*(?:%|ms|s|sec|seconds|m|min|minutes|x|kb|mb|gb|fps|qps|rps|items|rows|requests|errors|crashes|次|秒|毫秒|分钟|倍)\b",
    flags=re.IGNORECASE,
)


def section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    next_match = re.search(r"^##\s+", text[start + len(heading):], flags=re.MULTILINE)
    if not next_match:
        return text[start:]
    return text[start:start + len(heading) + next_match.start()]


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_rows(section_text: str, prefix: str | None = None) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section_text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = table_cells(line)
        if not cells or not cells[0] or cells[0].lower() in {"id", "time", "gate"}:
            continue
        if set(cells[0]) <= {"-"}:
            continue
        if prefix and not cells[0].startswith(prefix):
            continue
        rows.append(cells)
    return rows


def has_table_columns(section_text: str, required_columns: set[str]) -> bool:
    for line in section_text.splitlines():
        if not line.strip().startswith("|"):
            continue
        normalized = {cell.strip().lower() for cell in table_cells(line)}
        if required_columns <= normalized:
            return True
    return False


def risk_class(text: str) -> str:
    match = re.search(r"^Risk class:\s*([ABCD])\b", text, flags=re.MULTILINE)
    return match.group(1) if match else ""


def has_checkable_detail(value: str) -> bool:
    lower_value = value.lower()
    return bool(MEASUREMENT_PATTERN.search(value)) or any(marker in lower_value for marker in CHECKABLE_MARKERS)


def criterion_is_vague(criterion: str) -> bool:
    lower_criterion = criterion.lower()
    return any(term in lower_criterion for term in VAGUE_TERMS)


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

    current_risk_class = risk_class(text)
    if not current_risk_class and not allow_placeholders:
        errors.append("risk class must be one of A, B, C, or D")

    matrix = section(text, "## 4. Acceptance Matrix")
    ac_rows = table_rows(matrix, "AC-")
    if len(ac_rows) < (1 if current_risk_class == "A" else 3):
        errors.append("acceptance matrix must contain at least 1 AC-* row for class A and at least 3 AC-* rows for class B/C/D")

    if ac_rows and not has_table_columns(
        matrix,
        {"id", "risk", "criterion", "method", "evidence", "evidence link", "status", "owner/gate"},
    ):
        errors.append("acceptance matrix must include ID, Risk, Criterion, Method, Evidence, Evidence Link, Status, and Owner/Gate columns")

    for row in ac_rows:
        if len(row) < 8:
            errors.append(f"{row[0]} acceptance row must include evidence link and status columns")
            continue
        ac_id, _risk, criterion, method, evidence, evidence_link, status = row[:7]
        if not allow_placeholders and status not in AC_STATUSES:
            errors.append(f"{ac_id} status must be one of: {', '.join(sorted(AC_STATUSES))}")
        if not allow_placeholders and status in {"pass", "fail", "blocked", "skipped"} and not evidence_link:
            errors.append(f"{ac_id} must include an evidence link when status is {status}")
        if not allow_placeholders and status == "skipped" and "why" not in " ".join(row).lower():
            errors.append(f"{ac_id} skipped status must explain why")
        if not allow_placeholders and criterion_is_vague(criterion):
            combined_check = " ".join([criterion, method, evidence, evidence_link])
            if not has_checkable_detail(combined_check):
                errors.append(f"{ac_id} criterion is vague; add a threshold, invariant, or reproducible scenario")

    lower_matrix = matrix.lower()
    if current_risk_class != "A":
        for risk_name, aliases in REQUIRED_ACCEPTANCE_RISKS.items():
            if not any(alias.lower() in lower_matrix for alias in aliases):
                errors.append(f"acceptance matrix must include {risk_name} risk coverage for class B/C/D")

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

    gates = section(text, "## 7. Human Gates")
    gate_rows = table_rows(gates)
    lower_gates = gates.lower()
    if not any(decision in lower_gates for decision in GATE_DECISIONS):
        errors.append("human gates must contain a recognizable decision state")
    if not allow_placeholders:
        for row in gate_rows:
            if len(row) < 4:
                errors.append(f"gate row '{row[0]}' must include required flag, owner, and decision")
                continue
            decision = row[3].lower()
            if decision not in GATE_DECISIONS:
                errors.append(f"gate '{row[0]}' decision must be one of: {', '.join(sorted(GATE_DECISIONS))}")

    evidence = section(text, "## 8. Evidence Log")
    evidence_rows = table_rows(evidence)
    if not allow_placeholders and "skipped" in evidence.lower() and "why" not in evidence.lower():
        errors.append("skipped evidence should include why it was skipped")
    if current_risk_class in {"B", "C", "D"} and not evidence_rows:
        errors.append("class B/C/D plans must include at least one evidence log row")

    if current_risk_class in {"C", "D"}:
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
        if not any(len(row) >= 4 and row[1].lower() in {"yes", "true", "required"} for row in gate_rows):
            errors.append("class C/D plans must include at least one explicit required human gate")
        residual_risk = section(text, "## 9. Residual Risk").lower()
        if not any(term in residual_risk for term in ("remaining risk", "residual", "accepted", "blocked", "残余", "剩余")):
            errors.append("class C/D plans must include a residual risk statement")

    if current_risk_class == "D":
        d_record = "\n".join([section(text, "## 1. 任务与风险分级"), gates]).lower()
        if not any(term in d_record for term in ("owner approval", "owner gate", "security", "privacy", "payment", "legal", "高影响", "安全", "隐私", "支付", "法务")):
            errors.append("class D plans must document separate owner approval or high-impact review")
        if not any(term in text.lower() for term in ("rollback drill", "fallback drill", "回滚演练", "回退演练")):
            errors.append("class D plans must document a rollback or fallback drill")

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
