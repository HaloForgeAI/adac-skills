---
name: adac
description: "Use this skill when planning, executing, reviewing, or formalizing AI-assisted coding work that needs acceptance-first delivery controls: complex module changes, production behavior changes, performance work, concurrency/resource lifecycle work, regression-sensitive refactors, release/rollback decisions, or requests to turn an AI coding method into a reusable spec, skill, or engineering workflow."
---

# ADAC

## Purpose

Use Acceptance-Driven Agentic Coding (ADAC) to make AI coding work verifiable before it becomes large. The core rule is:

`Context + Spec + Evals + Gates` before broad implementation.

ADAC is not ordinary TDD. Prefer behavior checks, regression checks, performance/pressure evidence, observability, and human decision gates over coverage targets.

## Default Workflow

1. **Classify risk**: assign risk class A, B, C, or D.
   - A: local isolated change.
   - B: shared or user-facing change.
   - C: critical path, concurrency, resource lifecycle, performance, release path, or broad integration.
   - D: security, privacy, irreversible data, payment, legal, or high-impact rollout.
2. **Build Context Pack**: list verified facts, source paths, docs, tests, incidents, metrics, logs, assumptions, and known unknowns.
3. **Define Spec Boundary**: write target behavior, non-goals, changed/stable interfaces, ownership boundaries, compatibility, and rollback/fallback.
4. **Create Acceptance Matrix**: convert real risks into checkable AC items with method, evidence, and owner/gate.
5. **Write User Verification Scenarios**: for user-facing or business-visible behavior, list practical scenarios a user, reviewer, QA owner, or product owner can run, with steps and expected visible results.
6. **Plan Agent Work**: decompose implementation into small steps; tie each step to acceptance items.
7. **Execute and Verify**: implement, test, profile, inspect logs, collect evidence, and update the matrix when new risk appears.
8. **Run Human Gates**: stop for human approval where judgment is required.
9. **Assetize**: preserve reusable context, checks, scripts, runbooks, specs, or skill updates.

## Risk Scaling

- For class A, keep the ADAC record short: context, acceptance checklist, verification.
- For class B, produce a full plan and evidence log.
- For class C, require explicit human gates and independent verification when possible.
- For class D, require owner approval before implementation and release; document rollback.

If risk is unclear, classify upward.

## Acceptance Matrix Rules

Each acceptance item must include:

- stable ID, for example `AC-01`;
- risk category;
- externally meaningful criterion or invariant;
- verification method;
- evidence artifact or result;
- owner or gate.

Behavior and regression items that a user can observe should link to a user verification scenario, for example `UV-01`.

Include relevant categories:

- behavior;
- regression;
- integration/lifecycle;
- performance/resource usage;
- observability/diagnosis;
- rollout/fallback;
- security/privacy when applicable.

Reject vague criteria such as "improve quality" or "make it faster" until they become checkable.

## User Verification Scenario Rules

When behavior is user-facing or business-visible, include a short scenario list for the user. Each scenario should include:

- stable ID, for example `UV-01`;
- linked AC item, for example `AC-01`;
- persona or reviewer perspective;
- preconditions, environment, fixture, or test data;
- exact steps the user can perform;
- expected visible result;
- evidence to capture, such as screenshot, video, log, metric, or written observation;
- owner or gate if interpretation needs human judgment.

Use these scenarios to give the user practical validation information. Do not replace automated tests, performance evidence, observability checks, or required human gates with scenarios alone.

## Human Gate Rules

Create a human gate when work touches:

- API or module contracts;
- threading, async, locking, scheduling, lifecycle, or resource ownership;
- data migrations or irreversible state;
- secrets, auth, security, or privacy;
- release switches, rollback, canary, or operational response;
- business behavior that cannot be judged from code alone;
- unknowns the agent cannot verify from available context.

Agents may prepare evidence for gates. Do not silently approve a gate.

## Output Patterns

When the user asks for a plan, produce an ADAC plan using `spec/templates/adac-plan.md` if available.

When the user asks to implement, first do a compact ADAC pass before editing:

- risk class;
- context sources read;
- acceptance items;
- user verification scenarios when applicable;
- required gates;
- implementation steps.

Then proceed with implementation unless a required gate blocks progress.

When the user asks to formalize a mechanism, produce:

- canonical spec;
- templates;
- skill instructions;
- validation or checklist tooling when useful;
- one worked example.

## References

- Read `../../spec/ADAC-0001.md` for the canonical mechanism when working inside this repository or plugin.
- Read `references/adac-reference.md` for a compact checklist and phrasing guide.
