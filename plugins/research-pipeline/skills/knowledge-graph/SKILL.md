---
name: knowledge-graph
description: >
  Render the project's knowledge index as an interactive browser graph + integrity QA. Reads
  docs/knowledge-index.yaml (nodes) + docs/knowledge-index-detail.yaml (typed related[] edges,
  summaries, decisions, supersession), adds directory-containment edges for research trees, and emits
  a self-contained HTML. DEFAULT is a 3D view (3d-force-graph/three.js) where docs are stacked into
  vertical layers by a selectable dimension (kind / group / status / recency / in-degree / community);
  pass --2d for the cytoscape.js view (search-first "type to explore" DOI navigation + QA lenses +
  sortable table). Doubles as a knowledge-index LINTER: classifies unresolved related[] targets
  (unindexed-on-disk / broken-ref / out-of-scope) and surfaces orphans + superseded chains. Sibling to
  agile-workflow:board (board = work substrate; this = knowledge corpus). Use when the user asks to
  "visualize the knowledge graph", "show the doc graph", "graph the research", "find orphan docs", or
  "audit the knowledge index integrity".
user-invocable: true
allowed-tools: Bash, Read
model: haiku
---

# Knowledge Graph

You render a project's knowledge corpus as an interactive graph and surface index-integrity findings.
This is a deterministic renderer — run the script, report the QA summary, open the HTML. No judgment
calls, no sub-agents.

## What it produces

A self-contained HTML opened in the browser. `render.py` is a deterministic adapter that emits one
renderer-agnostic `DATA` view-model; two views consume it.

### Default: 3D view (`3d-force-graph` / three.js)

Docs are stacked into **vertical layers by a selectable dimension** so the third dimension carries
real signal (not random physics); x/z are force-driven within each layer.

- **"Z:" dropdown** — choose what the vertical axis encodes: **kind** (default: historical → research
  → brief → architecture → planning, bottom→top), **group**, **status**, **recency** (by `updated`),
  **in-degree**, **community** (shown only with `--communities`), or **flat** (free 3D). Switching
  re-sorts the layers live and updates the legend.
- **Navigation** — left-drag orbits, right-drag pans, scroll zooms; **space** toggles left-drag
  between rotate and pan. A gentle auto-spin stops on first interaction. **Search** flies the camera
  to a doc; **click** a node for its detail panel (kind/status, summary, decisions, key_findings,
  clickable in/out links). **Edge-type toggles** (reference / supersession / containment) in the
  toolbar. Nodes colored by group, sized by in-link degree; broken refs appear as red links to
  bottom-layer ghost nodes.

### `--2d`: cytoscape.js view (DOI navigation + QA audit surface)

The search-first 2D graph — best for integrity auditing. Built on the **DOI model** (van Ham & Perer
— *Search → Show Context → Expand on Demand*): opens **empty** with a "🔎 type to explore" prompt.

- **Search-first / expand-on-demand** — type a doc title → matching nodes + N-hop neighborhood (depth
  1/2/3); click to grow; **already-placed nodes don't move**. **Show all** for the full corpus.
- **Stable layout** persisted to `localStorage`; organic (fcose) / hierarchy (dagre) toggle.
- **Detail | Table | QA** right panel (brushing & linking): a sortable table of every doc, and
  one-click QA **lenses** + a "next" stepper for each integrity class.

### QA / linter classes (reported on stdout for both views)

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
python3 "${CLAUDE_PLUGIN_ROOT}/skills/knowledge-graph/render.py" "$PWD" --communities
```

This renders the **3D view by default**. Add `--communities` to enable the community Z-axis option
(cheap; recommended). Use `--2d` when the user wants the cytoscape DOI/QA audit surface instead.

- First positional arg = project root (defaults to CWD).
- Optional second arg = output HTML path (defaults to a temp file; the path is printed).
- `--2d` — emit the **2D cytoscape** view (search-first DOI navigation + QA lenses + sortable table)
  instead of the default 3D view. Best for integrity auditing.
- `--communities` — compute Louvain communities (pure-stdlib; off by default). Enables the 3D
  **community** Z-axis option.
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
re-rendering), that the **3D view is the default** (orbit with left-drag, **space** toggles
rotate/pan, the **"Z:"** dropdown changes the vertical dimension) and that `--2d` gives the
search-first cytoscape audit view, and that re-running regenerates from the current index.

## Notes

- **It's a linter, not just a picture.** The `unindexed` / `broken` classes catch frontmatter bugs
  that silently drop docs from the index — surface them prominently; they often warrant a
  `/research-pipeline:knowledge-index` re-run or a frontmatter fix.
- **Orphans are a curation signal, not an error.** A planning doc with zero `related[]` edges is valid
  but disconnected — flag it; don't auto-edit.
- **2D layout is persisted** to the browser's `localStorage` (keyed by project name); the **relayout**
  button clears it. The 3D layout re-settles each load (positions aren't persisted).
- **Determinism.** Same index → byte-identical HTML (`generated_at` is read from the index, not the
  wall clock). The DATA-contract adapter is covered by `tests/test_render.py`
  (`python3 -m pytest .../knowledge-graph/tests/ -q`).
- Throwaway HTML: it pulls its graph library from a CDN — `3d-force-graph`/three.js (3D, default) or
  cytoscape.js + extensions (`--2d`) — so it needs network, and is safe to delete/regenerate.
