# ADAC Skills

**ADAC** stands for **Acceptance-Driven Agentic Coding**: a formal delivery mechanism for AI-assisted software engineering. It turns "let AI write code" into a controlled workflow: define context, scope, acceptance evidence, and human gates before expanding implementation work.

This repository contains the canonical ADAC specification, reusable delivery templates, portable agent skills, and lightweight validation tooling. It is intended to work across Claude, Codex, and other AI coding agents that can consume `SKILL.md`-style guidance.

## Brand Positioning

- **Brand**: ADAC Skills
- **Full name**: Acceptance-Driven Agentic Coding
- **Short invocation**: `adac`
- **Tagline**: Acceptance first. Agents second.
- **Promise**: make AI coding work reviewable, evidence-backed, and safe to ship.

## Repository Layout

```text
adac-skills/
├── .claude-plugin/plugin.json
├── .claude-plugin/marketplace.json
├── .codex-plugin/plugin.json
├── bin/adac-validate
├── docs/
│   ├── brand.md
│   ├── examples.md
│   ├── publishing-checklist.md
│   └── distribution.md
├── README.md
├── examples/
│   └── worker-module.adac.md
├── package.json
├── schemas/
│   └── adac-plan.schema.json
├── scripts/
│   └── validate_adac_plan.py
├── skills/
│   └── adac/
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

Install with the portable skills CLI:

```bash
npx skills add HaloForgeAI/adac-skills --skill adac
```

1. Read [ADAC-0001](spec/ADAC-0001.md).
2. Start each non-trivial AI coding task from [the ADAC plan template](spec/templates/adac-plan.md).
3. Use [the ADAC skill](skills/adac/SKILL.md) when asking an AI coding agent to plan or execute work under ADAC.
4. Record release decisions with [the gate record template](spec/templates/adac-gate-record.md).
5. Validate a completed plan:

```bash
python3 scripts/validate_adac_plan.py examples/worker-module.adac.md
```

Or through the npm package entrypoint after publishing/installing:

```bash
npx adac-skills validate examples/worker-module.adac.md
```

## Distribution

ADAC Skills is prepared for several distribution paths:

- GitHub repository: `HaloForgeAI/adac-skills`
- npm package name: `adac-skills`
- Claude Code plugin manifest: `.claude-plugin/plugin.json`
- Claude Code marketplace catalog: `.claude-plugin/marketplace.json`
- Codex plugin manifest: `.codex-plugin/plugin.json`
- Portable skill folder: `skills/adac/`

See [brand notes](docs/brand.md), [example workflows](docs/examples.md), [publishing checklist](docs/publishing-checklist.md), and [distribution notes](docs/distribution.md) for naming, usage, publishing, and registration options.

## GitHub Pages

The static project page lives in [docs/index.html](docs/index.html). Enable GitHub Pages from the `main` branch and `/docs` folder to publish it.

## Design References

The repo structure borrows from several formal mechanisms:

- RFC-style normative language and requirement levels: [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).
- Proposal lifecycle and template discipline: [PEP 1](https://peps.python.org/pep-0001/) and [PEP 12](https://peps.python.org/pep-0012/).
- Machine-readable contract thinking: [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).
- Agent capability packaging: [Model Context Protocol specification](https://modelcontextprotocol.io/specification/), Claude Skills/Plugins, and portable skill/plugin conventions.
