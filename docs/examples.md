# ADAC Skills Examples

These examples show how ADAC changes the way an AI coding agent helps. The point is not to make the agent slower; it is to make the work reviewable before it becomes large.

## Example 1: Async Resource Loading Refactor

User request:

```text
Use ADAC to plan and implement a safer async resource loading path for the avatar system.
```

Without ADAC, the agent may start by refactoring queues, moving callbacks, and adding tests after the fact.

With ADAC, the agent should first produce:

- risk class: C, because the task touches async execution and resource lifecycle;
- context pack: current loading code paths, ownership rules, historical crashes, profiling entry points, and existing tests;
- spec boundary: no direct render resource creation outside approved thread/RHI boundaries;
- acceptance matrix:
  - `AC-01 behavior`: avatar enters scene with body, clothing, effects, and materials eventually complete;
  - `AC-02 regression`: missing asset and cancel paths do not deadlock;
  - `AC-03 lifecycle`: repeated enter/exit does not leak or double-release resources;
  - `AC-04 performance`: same-scene load timing is recorded before and after;
  - `AC-05 observability`: logs or telemetry expose queue depth, task latency, and completion failures;
- user verification scenarios:
  - `UV-01`: as a QA reviewer, enter the same avatar scene with a fixed account and verify visible resources complete while timing and logs are captured;
  - `UV-02`: trigger cancel or missing-asset behavior and verify the visible flow does not hang while diagnostic logs identify the failed task;
- gates: concurrency ownership review and release fallback review.

Useful prompt:

```text
Use ADAC for this async resource loading task. Before editing code, classify risk, build a context pack from the repo, and propose an acceptance matrix plus user verification scenarios covering behavior, regression, lifecycle, performance, observability, and rollback.
```

## Example 2: Payment Flow Change

User request:

```text
Use ADAC to add a new coupon validation path to checkout.
```

Expected ADAC shape:

- risk class: D, because the task touches payment and money;
- context pack: checkout flow, pricing rules, fraud/abuse notes, tests, logs, and current coupon behavior;
- spec boundary: final charged amount must come from trusted server-side calculation;
- acceptance matrix:
  - valid coupon applies exactly once;
  - expired coupon returns a user-safe error;
  - discount cannot exceed allowed bounds;
  - retries do not double-apply discounts;
  - audit log records coupon decision and pricing result;
- user verification scenarios:
  - shopper applies a valid coupon, refreshes or retries once, and confirms the visible discount appears once while the final charged amount matches the server result;
  - shopper applies an expired coupon and sees a safe, non-leaking error without changing the final charged amount;
- gates: product rule approval, security review, rollout/rollback decision.

Useful prompt:

```text
Use ADAC for this checkout change. Treat it as high-impact unless evidence says otherwise. Do not implement until the acceptance matrix and human gates are explicit.
```

## Example 3: UI Feature With Business Behavior

User request:

```text
Use ADAC to add a bulk archive action to the admin dashboard.
```

Expected ADAC shape:

- risk class: B or C depending on reversibility;
- context pack: list selection behavior, permission model, archive API, undo/restore rules, analytics events;
- spec boundary: bulk action must respect per-item permission and partial failure behavior;
- acceptance matrix:
  - selected rows archive only after confirmation;
  - unauthorized items remain unchanged and are reported;
  - partial failures show item-level result;
  - undo/restore path is available if required;
  - analytics records count and failure reason without private data;
- user verification scenarios:
  - admin selects eligible and unauthorized rows, confirms archive, and verifies only authorized rows move state while item-level failures are shown;
  - admin uses undo or restore, if required, and verifies restored rows return to the expected list state;
- gates: product behavior review and permissions review.

Useful prompt:

```text
Use ADAC for this admin bulk action. Produce acceptance criteria for partial failure, permissions, undo behavior, and observability before implementation.
```

## Example 4: AI-Generated Test Plan Review

User request:

```text
Use ADAC to review this AI-generated test plan before I let the agent implement it.
```

Expected ADAC review:

- identify whether tests map to real risks or only internal coverage;
- flag missing behavior/regression/performance/observability categories;
- flag missing user verification scenarios for behavior a user or reviewer can actually observe;
- require evidence artifacts for each acceptance item;
- add gates where test interpretation needs human judgment;
- reject tests that only mirror implementation details and would be rewritten with every refactor.

Useful prompt:

```text
Use ADAC to review this test plan. Tell me which acceptance risks are covered, which are missing, and which tests are likely low-value implementation mirrors.
```

## Example 5: Turning a One-Off Workflow Into a Team Skill

User request:

```text
Use ADAC to turn our incident fix workflow into a reusable skill.
```

Expected ADAC shape:

- context pack: incident templates, logs, dashboards, rollback steps, review owners;
- spec boundary: skill guides diagnosis and evidence collection, but does not approve production rollback by itself;
- acceptance matrix:
  - skill asks for incident scope and severity;
  - skill collects logs, metrics, recent deploys, and known incidents;
  - skill produces timeline, suspected cause, rollback options, and residual risk;
  - skill creates human gates for mitigation approval and postmortem signoff;
- assetization: `SKILL.md`, references, scripts, and examples.

Useful prompt:

```text
Use ADAC to design a reusable incident-response skill. Include the context pack, gates, evidence artifacts, and validation examples another agent can run.
```

## Measuring Whether ADAC Helped

A useful ADAC adoption check is not "did the agent write more code?" Instead ask:

- Did review start from acceptance items instead of a raw patch?
- Could a user, reviewer, QA owner, or product owner run the listed behavior scenarios and know what evidence to capture?
- Were non-goals and stable interfaces explicit before coding?
- Did the final answer include evidence, skipped checks, and residual risk?
- Did high-risk decisions stop at human gates?
- Did any reusable context, tests, or scripts survive the task?
