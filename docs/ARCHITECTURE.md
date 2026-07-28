# Architecture

How this repo is organized and how one git tree resolves into installable
plugins and packages for three agent harnesses. This is the meta map;
plugin-internal architecture lives in each plugin's own `docs/ARCHITECTURE.md`.

## Repo layout

```
.
├── plugins/                 # the shippable plugins (one directory each)
│   ├── workbench/            # centerpiece — requirements-first delivery + research
│   ├── agile-workflow/       # structured substrate work tracking (maintenance mode)
│   ├── ux-ui-design/         # standalone mockup-first UI design
│   ├── code-audit/           # standalone markdown code audits
│   ├── nates-toolkit/        # standalone utility skills
│   ├── agentic-research/     # grounded research discipline + .research substrate
│   ├── agent-coordination/   # sparse cross-agent coordination ledger
│   ├── prose-craft/          # prose drafting, lens review, refine cycle
│   └── workflow/             # DEPRECATED, frozen, kept for existing installs
├── .agents/skills/          # standalone reference-skill library (non-plugin)
├── .claude-plugin/
│   └── marketplace.json     # native Claude Code install index
├── .agents/plugins/
│   └── marketplace.json     # native Codex install index
├── scripts/
│   └── bump-version.sh      # the version gate (bumps channel metadata together)
├── docs/                    # this meta layer (VISION, SPEC, ARCHITECTURE)
├── .claude/                 # repo-level Claude config + instructions
└── README.md
```

`.agents/skills/` holds the curated reference library — library references
(`zod-v4`, `hono-v4`, `drizzle-v0`, the tanstack family, `bun`, `biome-v2`,
`smol-toml`, `citty`, `clack-prompts`, `schemars`, `claude-cli-sdk`),
ecosystem-research skills (`claude-code-marketplace`, `codex-plugin-format`),
and a few standalone workflow skills (`clean-memory`, `design-pages`). These
auto-load on relevant context and are not part of any plugin.

## Plugin anatomy

Each `plugins/<name>/` directory carries channel metadata and a mix of shared
and harness-specific components:

```
plugins/<name>/
├── .claude-plugin/plugin.json   # Claude Code manifest
├── .codex-plugin/plugin.json    # Codex manifest
├── skills/                      # SKILL.md units  — shared
├── commands/                    # slash commands  — Claude-specific
├── hooks/                       # event hooks     — harness-specific
├── docs/                        # plugin foundation docs (optional)
├── CHANGELOG.md
└── README.md
```

The shared/harness-specific split is the rule from `docs/SPEC.md`: skills cross
all three harnesses; command, hook, and agent surfaces are exposed only where
the target harness supports them. Pi-native runtime extensions live in the
`nklisch/pi-extensions` repo, not here.

## Distribution wiring

Two native catalogs carry the same ordered plugin identities with
channel-appropriate source shapes:

- `.claude-plugin/marketplace.json` uses Claude Code's string-path source for
  local plugins (`"./plugins/<name>"`).
- `.agents/plugins/marketplace.json` uses Codex's explicit local source objects.
- External plugins (`krometrail`, `peeragent`, `skilltap`) are federated in both
  catalogs through semantically equivalent `git-subdir` sources pointing at
  their own repositories.
- **Version integrity** flows through `scripts/bump-version.sh`, which keeps a
  plugin's channel metadata in lockstep and refuses to act on a dirty plugin
  directory.

Pi installation flows through the bridge, not through packages published from
this tree. The `@nklisch/pi-plugins` manager (source in `nklisch/pi-extensions`)
registers the same two marketplace catalogs — `/plugins marketplace add
nklisch/skills` — and installs the same plugin entries, including the external
`git-subdir` companions, with `/plugins add <name>@nklisch-skills`. A plugin
that is well-formed for Claude and Codex is well-formed for Pi; the bridge
discovers skills by directory convention. Pi-native tool packages
(`pi-plugins`, `pi-background-tasks`, `pi-zai-research`) publish to npm from
`nklisch/pi-extensions`, which is also where Pi runtime extensions are
developed.

## The substrate-access model

agile-workflow's substrate is plain files: `.work/` items as markdown with YAML
frontmatter, which are the single source of truth. Two surfaces read that one
substrate, each tuned for a different consumer:

- **Agent surface — the `work-view` CLI.** Built for agent ergonomics: terse,
  parseable, scriptable output, and dependency-aware filtering. This is what the
  design, implement, review, and autopilot skills call to decide what to act on.
- **Human surface — the `work-view board` web view.** A live localhost board
  for people to see the substrate at a glance, served by the compiled
  `work-view` adapter over the same `.work/` files.

The shape is deliberate: one substrate, two adapters, distinct ergonomics for
distinct consumers — the Ports & Adapters and Single-Source-of-Truth principles
agile-workflow defines for itself, applied to its own tooling. How those
surfaces are built, and how they evolve, is owned by
`plugins/agile-workflow/docs/ARCHITECTURE.md` and tracked as work in `.work/` —
not pinned here.

## Where internals live

- Requirements-first delivery, research evidence, UI walkthroughs, and
  compact release summaries → `plugins/workbench/docs/{VISION,SPEC}.md`.
- Structured substrate lifecycle, gates, releases, and the work-view query
  model (maintenance mode) →
  `plugins/agile-workflow/docs/{ARCHITECTURE,SPEC,PRINCIPLES}.md`.
- Standalone mockup-first design layout → the `ux-ui-design` plugin.
- Standalone markdown audit reports → the `code-audit` plugin.
- Grounded research substrate and citation discipline → the `agentic-research`
  plugin.
- Sparse cross-agent handoffs and claims → the `agent-coordination` plugin.
- Distribution constraints and versioning rules → `docs/SPEC.md`.
- Purpose and the dogfooding thesis → `docs/VISION.md`.
