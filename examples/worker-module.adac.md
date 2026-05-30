# ADAC Plan: WorkerModule AI-assisted delivery

Status: accepted-example  
Risk class: C  
Owner: engine module owner  
Agent role: implementation and verification support  
Target repo/module: Engine IO and multi-thread task progression paths

## 1. 任务与风险分级

- User/business goal: reduce community enter and exit waiting time without breaking resource lifecycle behavior.
- Engineering deliverable: introduce a WorkerModule path for background task progression, completion queue handling, instrumentation, and fallback comparison.
- Risk class and reason: C. The work touches long-evolved engine paths, async execution, resource lifecycle, render/RHI boundaries, performance, and release rollback.
- Out of scope: not a full engine streaming rewrite, not a direct replacement for all asset loading systems, and not a claim that AI independently owns correctness.

## 2. Context Pack

### Verified Facts

- The target experience includes community enter loading and community exit waiting.
- Existing investigation points to old IO and multi-thread task progression paths as the relevant engineering surface.
- The new path must return completion to controlled main-thread callback/RHI flow instead of crossing render boundaries directly.
- Acceptance must include same-scene performance comparison, pressure scenarios, logs, telemetry, and dump entry points.
- Supporting source and reference materials include engine IO code, WorkerTaskRouter, WorkerModule implementation files, and architecture comparison notes.

### Assumptions

- Same-scene measurements are comparable only when machine tier, scene, account state, and measurement method are kept stable.
- Some lifecycle correctness cannot be proven by unit tests alone and requires pressure or manual review evidence.

### Known Unknowns

- Remaining data race risk requires human review at the concurrency gate.
- Release readiness requires a human decision about fallback configuration and acceptable residual risk.

## 3. Spec Boundary

- Target behavior: background IO/CPU task progression is more continuous, completion returns through a controlled queue, and user-visible waiting decreases in community enter/exit scenarios.
- Interfaces that may change: internal task routing and WorkerModule integration points.
- Interfaces that must stay stable: caller-facing behavior, render/RHI ownership boundary, existing fallback path, and release switch behavior.
- Ownership/lifecycle boundaries: WorkerModule does not directly own render resource creation or destruction outside approved boundaries.
- Rollback or fallback path: keep configuration switch to compare or return to old path during diagnosis.

## 4. Acceptance Matrix

| ID | Risk | Criterion | Method | Evidence | Owner/Gate |
|---|---|---|---|---|---|
| AC-01 | behavior | Community enter eventually loads characters, clothing, effects, actions, makeup, and related visible resources without long stalled waiting. | Same-scene manual scenario plus logs/profile. | Timing record, profile snapshot, and visual confirmation. | agent prepares, human reviews |
| AC-02 | behavior | Community exit wait time is reduced without leaving visible stale resources or blocked wait pages. | Same-scene before/after scenario. | Exit timing record and release log. | agent prepares, human reviews |
| AC-03 | regression | Reference counting and resource release paths do not regress under random outfit and effect switching. | Regression test or pressure scenario. | Test output, pressure log, or dump absence record. | agent plus reviewer |
| AC-04 | regression | Missing resource, failed load, callback failure, and cancel/wait paths do not deadlock or crash. | Fault scenario and log inspection. | Error-path log and dump check. | human gate |
| AC-05 | performance | Same-scene measurements show the new path improves observed waiting time on high and mid tier machines. | Before/after timing with fixed scenario. | Example observation: enter 34.4s to 17.2s on high tier, 70s to 31s on mid tier; exit 7s to about 1s on high tier, 8s to 2s on mid tier. | human reviews interpretation |
| AC-06 | observability | WorkerModule activity can be diagnosed through stats, telemetry, logs, profile, and dump entry points. | Inspect instrumentation and run a scenario. | WorkerStats/telemetry/log/profile artifacts. | agent |
| AC-07 | rollout | New path can be switched or compared against the old path when diagnosing release issues. | Configuration or startup switch check. | Switch documentation and smoke check. | release owner gate |

## 5. Agent Work Plan

1. Context reading: inspect old IO/task progression path, WorkerModule files, WorkerTaskRouter, comparison notes, and test entry points.
2. Exploration: map blocking/waiting behavior to task progression, completion callback, resource lifecycle, and render/RHI boundaries.
3. Implementation steps: implement in small patches tied to AC items; preserve caller behavior and fallback path.
4. Verification steps: run functional scenarios, pressure cases, same-scene timing, instrumentation checks, and targeted review of concurrency/lifecycle boundaries.
5. Documentation or assetization: preserve context notes, acceptance cases, instrumentation entry points, and release switch instructions.

## 6. Human Gates

| Gate | Required? | Decision owner | Decision |
|---|---|---|---|
| Scope and non-goals | yes | module owner | approved |
| Architecture/interface boundary | yes | engine owner | approved |
| Concurrency/data/resource risk | yes | engine reviewer | approved-with-risk |
| Release/rollback | yes | release owner | approved-with-risk |

## 7. Evidence Log

| Time | Check | Result | Artifact |
|---|---|---|---|
| 2026-05-30 | same-scene enter/exit comparison record | pass | timing notes and demo videos |
| 2026-05-30 | resource lifecycle pressure coverage review | pass | regression scenario list |
| 2026-05-30 | observability entry review | pass | telemetry/log/dump entry list |
| 2026-05-30 | release fallback gate | approved-with-risk | configuration switch note |

## 8. Residual Risk

- Remaining risk: complex concurrency and lifecycle behavior cannot be proven absent by tests alone.
- Why acceptable or blocked: accepted only with human review, pressure coverage, logs/dump entry points, and fallback switch.
- Follow-up owner: module owner.

## 9. Reusable Assets

- Context to preserve: architecture notes, source path index, known risk list, and comparison facts.
- Tests/checks to preserve: enter/exit scenarios, random outfit pressure, missing resource and callback failure cases, same-scene timing method.
- Scripts/tools/docs/skills to update: WorkerModule troubleshooting notes, telemetry field list, and ADAC acceptance template.

