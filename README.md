# Acceptance-Driven Agentic Coding

Acceptance-Driven Agentic Coding, abbreviated **ADAC**, is a formal delivery mechanism for AI-assisted software engineering. It turns "let AI write code" into a controlled workflow: define context, scope, acceptance evidence, and human gates before expanding implementation work.

This repository contains the canonical ADAC specification, reusable delivery templates, a Codex skill, and lightweight validation tooling.

## Repository Layout

```text
acceptance-driven-agentic-coding/
├── .codex-plugin/plugin.json
├── README.md
├── examples/
│   └── worker-module.adac.md
├── schemas/
│   └── adac-plan.schema.json
├── scripts/
│   └── validate_adac_plan.py
├── skills/
│   └── acceptance-driven-agentic-coding/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/adac-reference.md
└── spec/
    ├── ADAC-0001.md
    └── templates/
        ├── adac-gate-record.md
        └── adac-plan.md
```

## Mechanism Summary

ADAC is built on four required controls:

1. **Context**: make the system, business rules, history, and known risks available before coding.
2. **Spec**: define the target behavior, non-goals, interfaces, and boundaries before implementation.
3. **Evals**: turn real user and engineering risks into executable acceptance checks.
4. **Gates**: reserve architecture, concurrency, security, release, and rollback decisions for human review.

The mechanism is intentionally stricter than ordinary prompt guidelines and broader than TDD. It prioritizes behavior tests, regression checks, pressure/performance evidence, observability, and rollout safety over coverage theater.

## Adoption Path

1. Read [ADAC-0001](spec/ADAC-0001.md).
2. Start each non-trivial AI coding task from [the ADAC plan template](spec/templates/adac-plan.md).
3. Use [the Codex skill](skills/acceptance-driven-agentic-coding/SKILL.md) when asking an agent to plan or execute work under ADAC.
4. Record release decisions with [the gate record template](spec/templates/adac-gate-record.md).
5. Validate a completed plan:

```bash
python3 scripts/validate_adac_plan.py examples/worker-module.adac.md
```

## Design References

The repo structure borrows from several formal mechanisms:

- RFC-style normative language and requirement levels: [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).
- Proposal lifecycle and template discipline: [PEP 1](https://peps.python.org/pep-0001/) and [PEP 12](https://peps.python.org/pep-0012/).
- Machine-readable contract thinking: [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).
- Agent capability packaging: [Model Context Protocol specification](https://modelcontextprotocol.io/specification/) and Codex skill/plugin conventions.

