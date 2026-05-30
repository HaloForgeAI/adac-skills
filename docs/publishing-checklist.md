# Publishing Checklist

Use this before making ADAC Skills public or registering it in a marketplace.

## Brand Assets To Upload

Minimum viable public release:

- repository README;
- `docs/brand.md`;
- `docs/examples.md`;
- `docs/distribution.md`;
- GitHub Pages site from `docs/index.html`;
- one square icon, 512 x 512 PNG;
- one social preview image, 1280 x 640 PNG;
- npm package metadata;
- Claude plugin manifest and marketplace catalog;
- Codex plugin manifest.

Recommended later:

- short demo video showing ADAC turning a vague task into an acceptance matrix;
- example PR description generated with ADAC;
- before/after agent transcript;
- docs site custom domain;
- public changelog and release tags.

## npm

Current candidate package names:

- `adac-skills`
- `@haloforgeai/adac-skills`

Local availability check on 2026-05-30 returned npm `E404` for both names. Publishing requires npm authentication:

```bash
npm login
npm run validate
npm pack --dry-run
npm publish --access public
```

Use the scoped package if you want publisher identity first. Use the unscoped package if you want the cleanest install command.

## npx skills

The repository works with the Vercel Labs `skills` CLI:

```bash
npx skills add HaloForgeAI/adac-skills --skill adac
```

For local validation:

```bash
npx skills add . --list
```

Expected result: the CLI discovers one skill named `adac`.

## Claude

Claude Code can consume the portable skill through the Claude plugin manifest/marketplace files:

```text
/plugin marketplace add HaloForgeAI/adac-skills
/plugin install adac-skills@haloforgeai-skills
```

Expected command after installation:

```text
/adac-skills:adac
```

## GitHub Pages

Recommended source:

- branch: `main`;
- folder: `/docs`.

If using GitHub CLI/API, enable Pages after pushing the `docs/` folder. If the repo stays private, Pages availability depends on the GitHub plan and organization policy.
