<!--
BRIEF (pinned per prose-draft)
Audience: developers evaluating or installing plugins from this skills
  marketplace. They know their AI coding host (Claude Code, Codex, or Pi) and
  what plugins and skills are; they have not read the prose-craft source.
Venue: README — Diátaxis hybrid: pitch (what and why) + install how-to +
  pointers to deeper docs.
Purpose: after reading, the reader knows what prose-craft does, whether they
  want it, and how to install it.
Must-keeps: the three skill names (prose-draft, prose-review, prose-refine)
  and what each does; the six lens names (audience, structure, clarity,
  accuracy, voice, accessibility); the prose-refine round cap of 3;
  "no substrate dependency"; the Pi install command
  `pi install -l ./plugins/prose-craft`.
Out of scope: the full style contract and lens checklists (linked instead);
  version, author, and license (kept in plugin metadata).
-->

# prose-craft

Three skills for documentation meant to be read by humans — READMEs,
foundation docs, web articles, guides. Draft under a plain-language style
contract, review through editorial lenses, and refine with a multi-model
rewrite-and-weave loop until the changes dwindle.

The skills are prose workflow only. They don't read or write a `.work/`
ledger or any other planning substrate, so they fit any repo regardless of
how it tracks work — agile-workflow, Workbench, or nothing at all.

## What each skill does

- **prose-draft** — Draft or rewrite a document to a plain-language style
  contract. Pins a five-field doc brief (audience, venue, purpose,
  must-keeps, scope) before writing, so later review judges against intent
  instead of taste.
- **prose-review** — One-pass editorial review through up to six lenses:
  audience, structure, clarity, accuracy, voice, accessibility. The default
  selection is four (audience, structure, clarity, accuracy); ask for all
  six on a thorough pass. Each finding is tagged `material` or `polish` with
  a concrete fix, and is a proposal for the author to adjudicate — not a
  verdict.
- **prose-refine** — The multi-model cycle. Each round, fresh-context
  re-writer sub-agents — a different model class each, where the host
  allows — rewrite the draft in parallel, and the orchestrator weaves the
  strongest sections into one voice. Scope shrinks each round: full
  rewrite, then machine-prose tell hunting, then micro-edits. Stops when a
  round yields only micro-edits; the cap is 3 rounds. Closes with a single
  proofread pass. Needs a host that can spawn sub-agents.

Each skill stands alone. Use `prose-draft` to start a draft, `prose-review`
for a quick read on an existing one, or `prose-refine` for the full path to
publication quality. The brief that `prose-draft` pins is what keeps the
`prose-refine` loop honest — carry it along when you hand off.

## Install

The plugin ships for three hosts: Claude Code, Codex, and Pi.

```sh
# Pi — from a clone of this repo, run at the repo root:
pi install -l ./plugins/prose-craft
```

For Claude Code or Codex, install through the marketplace catalogs at the
repo root: `.claude-plugin/marketplace.json` (Claude Code) and
`.agents/plugins/marketplace.json` (Codex). Each lists `prose-craft` with a
local source pointing at `./plugins/prose-craft`.

## Read more

- Style contract — `skills/prose-draft/references/style-contract.md`
- Document types and Diátaxis mode obligations — `skills/prose-draft/references/doc-types.md`
- The six review lenses — `skills/prose-review/references/lenses.md`

Source: <https://github.com/nklisch/skills>
