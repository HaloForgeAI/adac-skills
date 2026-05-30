# ADAC Skills Distribution

ADAC Skills is designed as a portable package, not a single-agent feature. The canonical content is:

- `spec/ADAC-0001.md`: normative mechanism;
- `spec/templates/`: human and agent-facing templates;
- `skills/adac/SKILL.md`: portable skill instructions;
- `scripts/validate_adac_plan.py`: deterministic validation helper;
- `.claude-plugin/plugin.json`: Claude Code plugin manifest;
- `.claude-plugin/marketplace.json`: Claude Code marketplace catalog;
- `.codex-plugin/plugin.json`: Codex plugin manifest;
- `package.json`: npm distribution metadata and CLI entrypoint.

## Names

Recommended public names:

- GitHub repo: `HaloForgeAI/adac-skills`
- npm package: `adac-skills`
- optional scoped npm package: `@haloforgeai/adac-skills`
- skill name: `adac`
- method name: `Acceptance-Driven Agentic Coding`

`adac-skills` and `@haloforgeai/adac-skills` were not found in the npm registry during the 2026-05-30 check. Publishing still requires an authenticated npm account with permission to publish the chosen scope.

## Claude

Claude Skills use a `SKILL.md` file with frontmatter and progressively disclosed resources. ADAC provides that portable skill at `skills/adac/SKILL.md`.

Claude Code plugins can package skills and can be distributed through plugin marketplaces. Claude Code marketplace sources can include GitHub, Git URLs, git subdirectories, and npm packages, so ADAC can be distributed from this repo or from a future npm package.

This repository includes a marketplace catalog at `.claude-plugin/marketplace.json`. Once the repository is accessible to the user or team, it can be registered from inside Claude Code:

```bash
/plugin marketplace add HaloForgeAI/adac-skills
/plugin install adac-skills@haloforgeai-skills
```

The installed Claude command is namespaced:

```text
/adac-skills:adac
```

GitHub plugin entry shape:

```json
{
  "name": "adac-skills",
  "source": {
    "source": "github",
    "repo": "HaloForgeAI/adac-skills"
  }
}
```

If the marketplace expects npm source, publish the package first and point the marketplace entry at `adac-skills`.

npm plugin entry shape:

```json
{
  "name": "adac-skills",
  "source": {
    "source": "npm",
    "package": "adac-skills",
    "version": "^0.1.0"
  }
}
```

## Codex

Codex can consume `skills/adac/SKILL.md` directly or through `.codex-plugin/plugin.json`. The Codex wrapper is a compatibility package; it is not the identity of ADAC.

## npm

The npm package provides:

- portable skill and spec files;
- `adac-skills validate <plan.md>`;
- `adac-validate <plan.md>`;
- package metadata for registry discovery.

The names `adac-skills` and `@haloforgeai/adac-skills` were not found on npm during the local check, but publishing cannot be completed until an npm account is authenticated and the public/private distribution decision is explicit.

Before publishing:

```bash
npm login
npm run validate
npm pack --dry-run
npm publish --access public
```

For a scoped package:

```bash
npm pkg set name=@haloforgeai/adac-skills
npm publish --access public
```

Do not publish until the repo license, visibility, package ownership, and intended public/private distribution model are explicitly decided.

## Recommended First Registration Path

1. Keep the GitHub repo canonical as `HaloForgeAI/adac-skills`.
2. Publish npm only after deciding whether ADAC should be public.
3. Use unscoped `adac-skills` if public discoverability matters most.
4. Use `@haloforgeai/adac-skills` if publisher identity and namespace control matter more.
5. Register Claude/Codex marketplace entries from the npm package once package ownership is secured.

## Reference Notes

- Claude Agent Skills are directories with `SKILL.md` plus optional supporting files; Claude discovers them by description and loads supporting files progressively: <https://docs.claude.com/en/docs/claude-code/skills>
- Claude Code plugin marketplaces use `.claude-plugin/marketplace.json`; plugin sources include relative paths, GitHub repositories, Git URLs, git subdirectories, and npm packages: <https://docs.claude.com/en/docs/claude-code/plugin-marketplaces>
- npm package names checked locally on 2026-05-30: `adac-skills` and `@haloforgeai/adac-skills` returned `E404 Not Found`, while `npm whoami` returned unauthenticated.
