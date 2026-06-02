# ADAC Reference

## Compact Checklist

Use this checklist before and during AI-assisted implementation.

1. What real user or engineering risk is this task trying to reduce?
2. What source paths, docs, logs, metrics, and prior incidents have been verified?
3. What must not change?
4. What acceptance evidence will prove the behavior is acceptable?
5. What practical user verification scenario can the user or reviewer run?
6. What historical regression must stay fixed?
7. What pressure, performance, or lifecycle scenario matters?
8. What logs, telemetry, profile, trace, or dump entry will diagnose failure?
9. What rollback or fallback exists?
10. Which decisions require human approval?
11. What reusable asset should survive this task?

## Recommended Acceptance Categories

| Category | Use for | Good evidence |
|---|---|---|
| behavior | user-visible or business-visible result | scenario, screenshot, video, manual script, end-to-end test |
| regression | previous bug or fragile invariant | regression test, pressure case, incident replay |
| lifecycle | ownership, allocation, release, callback order | stress log, leak check, code review, trace |
| performance | latency, throughput, CPU/GPU, memory, frame time | before/after profile, fixed-scenario timing |
| observability | ability to debug failures | log fields, telemetry, dump, trace, dashboard |
| rollout | release safety | feature switch, fallback test, canary plan |
| security | auth, privacy, secrets, trust boundaries | security review, threat note, audit log |

## User Verification Scenarios

Use these when the change has user-facing or business-visible behavior. A good scenario includes `UV-*` ID, linked `AC-*` item, persona, preconditions, concrete steps, expected visible result, evidence to capture, and owner/gate.

Prefer scenarios that a real user, QA owner, reviewer, or product owner can run without reading implementation details.

## Phrasing Guide

Prefer:

- "accepted when AC-01 through AC-06 have evidence and G-02 is approved";
- "UV-01: as an admin reviewer, select three eligible rows, click Archive, confirm, and verify only those rows move to Archived with an audit entry";
- "same scenario, same machine tier, same measurement method";
- "agent prepares evidence; human owner approves the gate";
- "test coverage is supporting evidence, not the acceptance claim";
- "residual risk remains in concurrency and is accepted only with fallback."

Avoid:

- "AI completed this independently";
- "tests prove there are no bugs";
- "coverage is high, therefore accepted";
- "make it better";
- "refactor while we are here";
- "fallback removed because new path works."
