# ADAC Reference

## Compact Checklist

Use this checklist before and during AI-assisted implementation.

1. What real user or engineering risk is this task trying to reduce?
2. What source paths, docs, logs, metrics, and prior incidents have been verified?
3. What must not change?
4. What acceptance evidence will prove the behavior is acceptable?
5. What historical regression must stay fixed?
6. What pressure, performance, or lifecycle scenario matters?
7. What logs, telemetry, profile, trace, or dump entry will diagnose failure?
8. What rollback or fallback exists?
9. Which decisions require human approval?
10. What reusable asset should survive this task?

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

## Phrasing Guide

Prefer:

- "accepted when AC-01 through AC-06 have evidence and G-02 is approved";
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

