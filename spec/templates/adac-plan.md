# ADAC Plan: <task name>

Status: draft  
Risk class: <A | B | C | D>  
Owner: <human owner>  
Agent role: <implementation | verification | planning | mixed>  
Target repo/module: <path or system>

## 1. 任务与风险分级

- User/business goal:
- Engineering deliverable:
- Risk class and reason:
- Out of scope:

## 2. Context Pack

### Verified Facts

- <source path, doc, metric, log, incident, or observed behavior>

### Assumptions

- <assumption and how to verify or gate it>

### Known Unknowns

- <unknown that may require a gate>

## 3. Spec Boundary

- Target behavior:
- Interfaces that may change:
- Interfaces that must stay stable:
- Ownership/lifecycle boundaries:
- Rollback or fallback path:

## 4. Acceptance Matrix

| ID | Risk | Criterion | Method | Evidence | Owner/Gate |
|---|---|---|---|---|---|
| AC-01 | behavior | <externally meaningful behavior> | <scenario or command> | <artifact/result> | <agent/human> |
| AC-02 | regression | <invariant that must not regress> | <test/log/manual check> | <artifact/result> | <agent/human> |
| AC-03 | observability | <diagnosis requirement> | <log/telemetry/dump check> | <artifact/result> | <agent/human> |

## 5. Agent Work Plan

1. Context reading:
2. Exploration:
3. Implementation steps:
4. Verification steps:
5. Documentation or assetization:

## 6. Human Gates

| Gate | Required? | Decision owner | Decision |
|---|---|---|---|
| Scope and non-goals | yes | <owner> | pending |
| Architecture/interface boundary | <yes/no> | <owner> | pending |
| Concurrency/data/resource risk | <yes/no> | <owner> | pending |
| Release/rollback | <yes/no> | <owner> | pending |

## 7. Evidence Log

| Time | Check | Result | Artifact |
|---|---|---|---|
| <timestamp> | <command/scenario/review> | <pass/fail/blocked/skipped> | <path/link/log> |

## 8. Residual Risk

- Remaining risk:
- Why acceptable or blocked:
- Follow-up owner:

## 9. Reusable Assets

- Context to preserve:
- Tests/checks to preserve:
- Scripts/tools/docs/skills to update:

