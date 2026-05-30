---
name: knowledge-graph
description: >
  Render the project's knowledge index as an interactive, search-first browser graph + integrity QA.
  Reads docs/knowledge-index.yaml (nodes) + docs/knowledge-index-detail.yaml (typed related[] edges,
  summaries, decisions, supersession), adds directory-containment edges for research trees, and emits
  a self-contained cytoscape.js HTML. The graph opens in "type to explore" mode (Search → Show Context
  → Expand on Demand) with a stable, persisted layout — not a hairball. Doubles as a knowledge-index
  LINTER: classifies unresolved related[] targets (unindexed-on-disk / broken-ref / out-of-scope) and
  surfaces orphans + superseded chains, embedded directly in the graph and as one-click QA lenses plus
  a sortable table. Sibling to agile-workflow:board (board = work substrate; this = knowledge corpus).
  Use when the user asks to "visualize the knowledge graph", "show the doc graph", "graph the research",
  "find orphan docs", or "audit the knowledge index integrity".
user-invocable: true
allowed-tools: Bash, Read
model: haiku
---

# Knowledge Graph

You render a project's knowledge corpus as an interactive graph and surface index-integrity findings.
This is a deterministic renderer — run the script, report the QA summary, open the HTML. No judgment
calls, no sub-agents.

## What it produces

A self-contained HTML (cytoscape.js, opened in the browser) built on the **DOI model** (van Ham &
Perer — *Search → Show Context → Expand on Demand*). It opens **empty** with a "🔎 type to explore"
prompt rather than dumping the whole corpus:

- **Search-first** — type a doc title; matching nodes + their N-hop neighborhood appear (depth 1/2/3
  selectable). The rest stays hidden, so there's no hairball. **Show all** renders the full corpus.
- **Expand on demand** — click a node to grow its neighborhood; **already-placed nodes don't move**.
  Right-click for a radial menu (open / expand / dependents / pin / hide).
- **Stable layout** — positions persist to `localStorage` per project; reopening restores the same
  arrangement. Newly-revealed nodes get a local layout; existing ones stay put. Toggle organic
  (fcose) vs. hierarchy (dagre).
- **Nodes** = indexed docs, colored by group, **sized by in-link degree** (how referenced),
  white-bordered if `nav_priority: high`, dashed if orphan, purple-ringed if superseded.
- **Edges** = typed `related[]` (reference vs. supersession) + directory-**containment**. Each edge
  category has an independent **show/hide toggle** in the toolbar.
- **Right panel — Detail | Table | QA** (brushing & linking; selecting in any one syncs the others):
  - **Detail** — click a node for its card: kind/status, summary, decisions, key_findings, with
    **in-links above / out-links below** (Roam-style), each clickable to re-focus.
  - **Table** — every doc as a sortable row (title / kind / status / in / out / flags); click a row to
    focus the node. The audit surface.
  - **QA** — one-click **lenses** (highlight-mode) for each integrity class + a "next" stepper that
    centers each finding in turn:
    - 🟠 **unindexed** — a `related[]` target on disk but not in the index → repair/re-index it.
    - 🔴 **broken** — a `related[]` target that doesn't exist on disk → fix the slug.
    - ⚫ **out-of-scope** — target outside the indexed roots (e.g. `src/`); expected, not a defect.
    - ⚪ **orphans** — docs with zero edges (after containment); a cross-reference gap worth backfilling.
    - 🟣 **superseded** — docs carrying a `supersession_note`.

## Workflow

### Step 1: Ensure the index exists

The renderer reads `docs/knowledge-index.yaml` + `docs/knowledge-index-detail.yaml`. If the terse
index is missing or stale, run `/research-pipeline:knowledge-index` first. (A terse-only project still
renders — nodes just have empty summaries/decisions.)

### Step 2: Render

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/knowledge-graph/render.py" "$PWD"
```

- First positional arg = project root (defaults to CWD).
- Optional second arg = output HTML path (defaults to a temp file; the path is printed).
- `--communities` — compute Louvain communities (pure-stdlib; off by default).
- `--3d` — emit a **3D** view (`3d-force-graph`/three.js) instead of the 2D cytoscape graph, from the
  same `DATA`. Nodes are stacked into **vertical layers by `kind`** (historical → research → brief →
  architecture → planning, bottom→top) so the third dimension carries real signal; x/z are
  force-driven. Left-drag orbits, right-drag pans, scroll zooms; a gentle auto-spin stops on first
  interaction. Includes search-to-focus, hover cards, a click→detail panel (in/out links), and
  edge-type toggles. Use for spatial exploration; the 2D view remains the surface for QA/audit.
- `--print-data` — dump the `DATA` JSON to stdout (used by the test suite).
- Requires `python3` + PyYAML (already a knowledge-index dependency).

### Step 3: Report + open

Print the QA summary line the script emits (node/edge/group counts + the 5 QA classes). Call out
**unindexed** and **broken** counts explicitly — those are actionable index bugs. Then open the HTML:

```bash
open "<printed-path>"        # macOS
# xdg-open / wslview on Linux/WSL
```

Tell the user: whether it opened automatically, the HTML path (so they can re-open without
re-rendering), that it opens in **type-to-explore** mode (search a doc or click **show all**), and
that re-running regenerates from the current index.

## Notes

- **It's a linter, not just a picture.** The `unindexed` / `broken` classes catch frontmatter bugs
  that silently drop docs from the index — surface them prominently; they often warrant a
  `/research-pipeline:knowledge-index` re-run or a frontmatter fix.
- **Orphans are a curation signal, not an error.** A planning doc with zero `related[]` edges is valid
  but disconnected — flag it; don't auto-edit.
- **Layout is persisted** to the browser's `localStorage` (keyed by project name). The **relayout**
  button clears it and re-runs from scratch.
- **Determinism.** Same index → byte-identical HTML (`generated_at` is read from the index, not the
  wall clock). The DATA-contract renderer is covered by `tests/test_render.py`
  (`python3 -m pytest .../knowledge-graph/tests/ -q`).
- Throwaway HTML: it pulls cytoscape + extensions from a CDN (needs network) and is safe to
  delete/regenerate.
