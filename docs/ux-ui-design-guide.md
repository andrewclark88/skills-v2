# UX/UI Design Guide

How to use the `ux-ui-design` plugin to design a user interface **before**
writing any production code — with throwaway, single-file HTML mockups
that open in any browser.

This guide is for humans collaborating with an agent on visual and
interaction design. The plugin runs on Claude Code, OpenAI Codex, and Pi.
It works on its own, pairs with `workbench` (where `.mockups/` is an
optional UI-alignment layer), and slots most tightly into `agile-workflow`
(see *Plugged into agile-workflow* below).

## What this is

A small plugin that turns your agent into a UI design partner. You ask for
screen options, a flow, or a palette. The agent generates standalone HTML
mocks under `.mockups/`. You open them, compare, pick one (or describe a
hybrid), and the agent iterates. When you sign off, that mock is the
alignment artifact — your implementer later translates it into your real
stack.

**Mocks are throwaway.** They exist for *alignment*, not deployment. No
build step, no React, no Tailwind — a `.html` file with vanilla CSS and JS
that still opens in a browser long after the framework of the moment is
gone.

## Before you start

Install the plugin in the harness you use. You also need a browser that
can open local HTML files. The agent normally opens the review page after
generating one; if that fails, use the `file://` URL it prints.

```bash
# Claude Code
/plugin marketplace add nklisch/skills
/plugin install ux-ui-design@nklisch-skills

# OpenAI Codex
codex plugin marketplace add https://github.com/nklisch/skills
codex plugin install ux-ui-design

# Pi (via the pi-plugins manager)
pi install npm:@nklisch/pi-plugins
# then, inside Pi:
/plugins marketplace add nklisch/skills
/plugins add ux-ui-design@nklisch-skills --scope user
# or, from a local checkout:
pi install -l ./plugins/ux-ui-design
```

All three channels consume the same shared `skills/` directory. On its
first relevant run, `ux-ui-principles` offers to add the mockup-first
convention block to your project's `AGENTS.md` — accept it if you want
later agents to follow the same rule.

## The skills

Seven skills, one shared `skills/` directory across all three harnesses.

| Skill | Use it when you need | What you review |
|---|---|---|
| **`palette`** | Color, typography, and design tokens | Color and type options as HTML previews; your choice locks into `tokens.css` |
| **`components`** | Shared buttons, inputs, cards, modals in every state | A component showcase page, plus a reusable `components.css` |
| **`motion`** | Easing, durations, springs, reduced-motion variants | A playable motion showcase, plus a reusable `motion.css` |
| **`screens`** | Several alternatives for one screen | N distinct HTML options (default 4), plus a comparison grid |
| **`flows`** | One journey that crosses several screens | A multi-page mock whose chrome matches the flow's topology (sequential, hub-and-spoke, or hybrid), plus an index navigator |
| **`adopt`** | An existing UI needs inventory, audit, mocks, or redesign | Scans the codebase, audits every UI surface, then orchestrates the pipeline. Writes `.mockups/adoption-report.md` |
| **`ux-ui-principles`** | Any UI design work (auto-loads) | Reference: storage layout, decision matrix, linking convention, tech rule |

The first six are generator skills. `ux-ui-principles` is the reference
they defer to for where mocks live, when to produce them, and how they
link back to work items.

## The mock-first loop

1. **Choose the starting point.** For a new product or feature, start with
   the design-system ordering below. For a project that already has UI
   code, start with `adopt`.
2. **Ask in plain language.** *"Mock a compact, calm settings screen for
   power users; explore four layouts."* A useful request describes the
   user's goal and the intended feel, not only widgets.
3. **Review the index page.** Screen options appear side by side; flow
   pages appear in a navigator that reflects how people move through the
   journey.
4. **Pick or hybridize.** *"Option 3, but with the nav from option 1."*
   The agent updates the mock, never production code.
5. **Record the decision.** Attached to an `agile-workflow` item, the agent
   records the mock path and chosen direction under `## Mockups`.
   Otherwise, the chosen HTML file is the reference.
6. **Implement from the signed-off mock.** Translate the design into your
   production stack. Do not treat mock HTML or CSS as production
   components.

## The natural ordering

When the product needs a coherent design system, run the design-system
skills in order — each step gives the next one a shared vocabulary:

```
1. palette       → tokens.css      (colors, type)
2. components    → components.css  (uses tokens.css)
3. motion        → motion.css      (uses tokens + components)
4. screens / flows                 (link all three)
```

You don't have to run them all at once. You can also just say "design the
login screen" — the agent checks whether a palette exists and offers to
run it first if not. For a small exploration, `screens` and `flows` work
without the full system; a project with many mocks benefits from the
complete sequence.

## The output layout

Every project that uses the plugin gets the same `.mockups/` shape:

```
.mockups/
├── design-system/
│   ├── palette.html       color + WCAG check
│   ├── typography.html    font scale
│   ├── components.html    every component, every state
│   ├── motion.html        every motion, playable
│   ├── tokens.css         locked-in design tokens
│   ├── components.css     reusable component primitives
│   └── motion.css         reusable easing, durations, springs
├── screens/<feature>/     N option HTMLs + index.html
└── flows/<flow-name>/     numbered sequence + index.html
```

Mocks are plain HTML — open them straight from your file manager. Every
screen and flow links the shared `tokens.css`, `components.css`, and
`motion.css`, so the whole project shares one visual and kinetic voice.
Treat each directory's `index.html` as the review entry point: it holds
the comparison grid or flow navigator, and opening individual files first
loses that context.

## Adopting an existing project

If you already have UI in code and want mocks — for a redesign, an audit,
or to backfill a design system that drifted from the implementation:

```
/ux-ui-design:adopt
```

`adopt` scans the codebase, inventories every UI surface, and audits for
inconsistencies (duplicate components, hardcoded colors, missing empty
states). The audit always runs, and its findings inform whichever mode
you pick:

- **Mirror** — faithful capture of the current implementation as mocks.
  Audit findings become remediation proposals shown side by side.
- **Reimagine** — a redesign. Existing code informs constraints (data
  shape, audience, copy voice) but the visual direction is open.
- **Diegetic prototype** — a speculative, future-facing concept rather
  than a capture of the present, with fake-OS chrome and fake timestamps.
  Use it for strategy passes, not for bringing an existing codebase into
  the convention.

Output is the same `.mockups/` shape, ready for iteration, plus
`.mockups/adoption-report.md` with the inventory, findings, and decisions.

## The tech rule

The constraint that makes mocks portable:

- One `.html` file per mock. Vanilla CSS in `<style>`, vanilla JS in
  `<script>`.
- No build step, no CDN, no npm, no CSS or JS framework.
- Optional `<link rel="stylesheet" href="../../design-system/tokens.css">` —
  the local shared stylesheets are the only allowed external references.
- If a palette deliberately chooses a hosted font, include a system-font
  fallback; the mock's layout and interaction must still work offline.
- Self-contained, so the file opens in any browser, offline, years from
  now.

The point: mocks survive frameworks. A plain HTML/CSS mock written in 2026
still opens in 2036.

## Plugged into agile-workflow

> `agile-workflow` is stable and **supported in maintenance mode (KTLO)**:
> bug fixes and compatibility work land, but no new feature development is
> planned. This section remains accurate for projects that already use it.
> **New projects** should adopt
> [`workbench`](../plugins/workbench/README.md); on a workbench project,
> use the same skills standalone — see *Pairing with workbench*.

The plugin works standalone, but it clicks most tightly with
`agile-workflow`. Mock at the highest workflow tier where a decision can
land — mocks are cheap; re-aligning implemented code because direction
wasn't pinned is not.

### The four tiers

| Tier | When | What gets mocked |
|---|---|---|
| **`scope`** | Large UI scope, cross-feature journeys already clear at scope time | `palette` + `flows` (greenfield), or `adopt` for an existing project |
| **`epic-design`** | The primary tier — net-new screens and multi-screen journeys across an epic | The full pipeline: palette → components → motion → screens + flows. `--only-questions` always runs this pass |
| **`feature-design`** | The fallback — small, genuinely new surfaces the parent epic didn't cover | Inherits parent mocks; adds only what's missing |
| **`ideate`** | A UI-bearing project right after foundation work | Recommends `palette` so the visual identity precedes scope and epic work |

### How the linking works

When a mock is generated against a substrate item, the agent adds a
`## Mockups` section to the item's body pointing at the relevant paths,
and may set an optional `mockups:` frontmatter field. There is no schema
coupling — `agile-workflow` doesn't parse the field, so the path
convention is the real link. The implementer reading the item sees the
mock alongside the design and uses it as ground truth.

### Why this is the alignment habit

The killer move with `agile-workflow` is the `--only-questions` pass —
interactive Q&A across the drafting queue *before* autopilot starts. Adding
mocks to that pass means autopilot inherits **both**:

- Directional answers captured under `## Design decisions` in each item
  body.
- Visual alignment captured under `## Mockups` in each item body.

Autopilot then designs and implements with no autonomous guessing on either
front. See [agile-workflow-guide.md](agile-workflow-guide.md) for the full
loop.

## Pairing with workbench

On a `workbench` project, the same generator skills run standalone.
Workbench treats `.mockups/` as an optional UI-alignment layer: a work
item can keep a small walkthrough under `.mockups/<item-id>/index.html`
and reference it from the item through `mock_refs`. Mockups there are
requirements evidence, not production components — the same throwaway
posture as everywhere else.

Run `palette`, `components`, and `motion` once to seed a design system,
then invoke `screens` and `flows` per work item as its UI warrants.
`adopt` applies when the project already has UI code.

## When NOT to use this

- **Production code generation.** These are alignment artifacts, not
  components — your implementer translates the chosen mock into your real
  stack.
- **Highly interactive prototypes** with real state, fetches, or routing —
  use a real stack for those.
- **Pixel-perfect handoff comps** for a separate visual designer — use
  Figma for that.
- **A change with no UX surface.** Backend work, copy-only edits, and
  non-visual fixes don't need mockups.

This plugin sits in the gap: more structured than whiteboard sketches,
less work than a real prototype, opens-in-any-browser portable.

## Tips

- **Mock big decisions first.** The scope and epic-design tiers cover the
  most ground per minute spent.
- **Describe taste, not specs.** *"Feels like Linear meets Stripe, weighted
  toward minimal"* gets better options than *"use #5B6CFF and Inter."*
- **Hybridize freely.** When option 3 is mostly right but option 1's nav
  is better, say so. The agent merges and re-renders.
- **Throw mocks away when shipped.** Once the real UI ships, delete the
  mock directory or keep it as a frozen reference. Git holds the history
  either way.
- **Open the index, not individual files.** Every mock directory has an
  `index.html` with the comparison grid or flow navigator — that's the
  intended entry point.

## Where to read more

- `plugins/ux-ui-design/README.md` — plugin reference, decision matrix,
  and install details
- Each skill's `SKILL.md` under `plugins/ux-ui-design/skills/<name>/` —
  per-skill triggers, exact output contract, and examples
