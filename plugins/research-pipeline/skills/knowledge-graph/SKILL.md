---
name: knowledge-graph
description: >
  Render the project's knowledge index as an interactive browser graph + integrity QA.
  Reads docs/knowledge-index.yaml (nodes) + docs/knowledge-index-detail.yaml (typed
  related[] edges + supersession), adds directory-containment edges for research trees,
  and emits a self-contained cytoscape.js HTML that opens in the browser. Doubles as a
  knowledge-index LINTER: classifies unresolved related[] targets (unindexed-on-disk /
  broken-ref / out-of-scope), surfaces orphans and superseded chains. Sibling to
  agile-workflow:board (board = work substrate; this = knowledge corpus). Use when the
  user asks to "visualize the knowledge graph", "show the doc graph", "graph the research",
  "find orphan docs", or "audit the knowledge index integrity".
user-invocable: true
allowed-tools: Bash, Read
model: haiku
---

# Knowledge Graph

You render a project's knowledge corpus as an interactive graph and surface index-integrity
findings. This is a deterministic renderer — run the script, report the QA summary, open the
HTML. No judgment calls, no sub-agents.

## What it produces

A self-contained HTML (cytoscape.js, opened in the browser) where:

- **Nodes** = indexed docs, colored by group (research program / brief / architecture / etc.),
  sized by edge-degree, white-bordered if `nav_priority: high`.
- **Edges** = typed `related[]` semantic edges + directory-**containment** edges (each research
  subtree's `super-parent.md`/`parent.md` → its sub-docs, so structurally-nested docs aren't
  false-positive orphans). A lens toggle switches between related / containment / both.
- **QA panel** (right side, click a finding to focus its node):
  - 🟠 **unindexed** — a `related[]` target that exists on disk under a scanned root but isn't
    in the index → its frontmatter is broken or missing required fields; re-index / repair it.
  - 🔴 **broken** — a `related[]` target that doesn't exist on disk at all → fix the slug.
  - ⚫ **out-of-scope** — target outside the indexed roots (e.g. `src/`); expected, not a defect.
  - ⚪ **orphans** — docs with zero edges (after containment); a real cross-reference gap worth backfilling.
  - 🟣 **superseded** — docs carrying a `supersession_note`.

## Workflow

### Step 1: Ensure the index exists

The renderer reads `docs/knowledge-index.yaml` + `docs/knowledge-index-detail.yaml`. If the
terse index is missing or stale, run `/research-pipeline:knowledge-index` first.

### Step 2: Render

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/knowledge-graph/render.py" "$PWD"
```

- First positional arg = project root (defaults to CWD).
- Optional second arg = output HTML path (defaults to a temp file; the path is printed).
- Requires `python3` + PyYAML (already a knowledge-index dependency).

### Step 3: Report + open

Print the QA summary line the script emits (node/edge/group counts + the 5 QA classes).
Call out **unindexed** and **broken** counts explicitly — those are actionable index bugs.
Then open the HTML:

```bash
open "<printed-path>"        # macOS
# xdg-open / wslview on Linux/WSL
```

Tell the user: whether it opened automatically, the HTML path (so they can re-open without
re-rendering), and that re-running regenerates from the current index.

## Notes

- **It's a linter, not just a picture.** The `unindexed` / `broken` classes catch frontmatter
  bugs that silently drop docs from the index — surface them prominently; they often warrant a
  `/research-pipeline:knowledge-index` re-run or a frontmatter fix.
- **Orphans are a curation signal, not an error.** A planning doc with zero `related[]` edges is
  valid but disconnected — flag it for the user; don't auto-edit.
- Throwaway HTML: it pulls cytoscape from a CDN (needs network) and is safe to delete/regenerate.
