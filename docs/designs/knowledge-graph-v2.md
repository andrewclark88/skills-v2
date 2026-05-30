# Design: knowledge-graph skill v2 (interactive doc-corpus graph)

## Overview

A **bold rebuild** of the `research-pipeline:knowledge-graph` skill's interface, grounded in
`plugins/research-pipeline/docs/scout-landscape-knowledge-graph.md`. The current skill renders the
whole corpus at once into a static cytoscape.js graph — the scout's convergent finding is that this
*show-everything-passively* model is the root cause of "clunky / not interactive."

v2 reconceives the interface around **van Ham & Perer's DOI model** (Search → Show Context →
Expand-on-Demand), a **deterministic/stable layout**, **diagnostics embedded in the graph**,
**brushing-and-linking** between graph / detail card / table / QA, **typed-edge toggles**, and stretch
differentiators (breadcrumb trail, semantic zoom, Louvain coloring).

### Architectural stance (Ports & Adapters + Generated Contract)

- **`render.py` is the adapter**: it reads the two index YAMLs and emits **one `DATA` JSON object** —
  a complete view-model. It contains *no view logic* and *no runtime sub-agents*; it stays a
  deterministic renderer.
- **`template.html` is the view**: pure client-side logic that reads `DATA` and nothing else. All
  interaction (search, expand, layout, card, table, lenses, toggles) lives here.
- **The `DATA` object is the generated contract** between them (Unit 1 defines it exactly). Every
  other unit consumes a slice of it. This is the single source of truth; the HTML never recomputes
  what `render.py` already derived (degree, QA classes, adjacency, communities).

Stay on **cytoscape.js** (scout verdict: WebGL buys nothing at our scale; the missing piece is the
extension layer). CDN-loaded, self-contained throwaway HTML, opens in the browser. Inputs unchanged:
`docs/knowledge-index.yaml` + `docs/knowledge-index-detail.yaml`.

### Test fixtures (real corpora on disk)
- `~/dev/ds-engine` — 484 docs, schema_version 2, has detail layer → **scale/stress fixture**
- `~/dev/grimoire`, `~/dev/legacy-engine` — mid-size, both layers present
- `~/dev/edh-engine`, `~/dev/choice-specs` — terse only (no detail) → **degraded-input fixture**

---

## Implementation Units

### Unit 1: `render.py` — view-model adapter & the `DATA` contract

**File**: `plugins/research-pipeline/skills/knowledge-graph/render.py` (rewrite of the data layer; CLI
signature unchanged: `render.py [PROJECT_ROOT] [OUT_HTML]`)

The emitted `DATA` object (serialized into `__DATA__`):

```python
# ---- DATA contract (JSON-serializable) ----
# meta: dict
#   root: str               # project dir name
#   generated_at: str       # ISO8601, sourced from terse index 'generated_at' (NOT wall clock — keeps deterministic)
#   total_docs: int
#   schema_version: int
#   has_communities: bool   # whether Louvain ran (Unit 7)
#   scope: list[str]        # SCOPE roots, e.g. ["docs/", ".research/"]
#
# nodes: list[Node]   where Node = {
#   "id": str,              # doc path — primary key
#   "label": str,           # title (fallback: basename)
#   "group": str,           # group_of(path)
#   "kind": str,            # planning|research|brief|historical|... ("?" if absent)
#   "type": str,            # architecture|landscape|... ("?" if absent)
#   "status": str,          # draft|active|superseded|"" 
#   "nav": bool,            # nav_priority == high
#   "deg": int, "indeg": int, "outdeg": int,   # over RESOLVED edges only (excludes dangling)
#   "orphan": bool,         # deg == 0 after containment edges
#   "superseded": bool,     # has supersession_note
#   "supersession_note": str | None,
#   "summary": str,         # from detail layer, "" if none (full, not truncated — view truncates)
#   "decisions": list[str], # from detail layer (may be [])
#   "key_findings": list[str],
#   "community": int | None,    # Louvain community id (Unit 7); None if not computed
#   "color": str,           # hex, by group
#   "consumer_hint": str,   # terse-index consumer_hint, "" if none
#   "updated": str,         # "" if none
# }
#
# ghosts: list[Ghost]  where Ghost = {  # dangling related[] targets, rendered as diamonds on demand
#   "id": str, "label": str, "dclass": "unindexed"|"broken"|"out-of-scope", "color": str
# }
#
# edges: list[Edge]  where Edge = {
#   "id": str,              # f"{source}__{target}__{ecat}"
#   "source": str, "target": str,
#   "rel": str,             # relationship label (e.g. "extends","supersedes","contains")
#   "ekind": "related" | "containment",
#   "ecat": "reference" | "supersession" | "containment",   # the toggle categories (Unit 6)
#   "dclass": "" | "unindexed" | "broken" | "out-of-scope",  # "" when target resolves
# }
#
# adjacency: dict[str, {"in": list[Adj], "out": list[Adj]}]   # resolved edges only, keyed by node id
#   where Adj = {"id": str, "rel": str, "ecat": str}          # powers detail-card in/out lists (Unit 5)
#
# qa: {
#   "unindexed": list[str], "broken": list[str], "out_of_scope": list[str],
#   "orphans": dict[str, list[str]],   # group -> [paths]
#   "superseded": list[str],
# }
#
# groups: list[{"name": str, "color": str}]
#
# stats: {"nodes","related","containment","groups","orphans","unindexed","broken","oos","superseded"}  # all int
```

Required functions (replacing the current flat script body):

```python
def load_index(root: Path) -> tuple[dict, dict]:
    """Return (terse, detail). Exit with a clear message if terse is missing.
    detail defaults to {"documents": {}} when absent (degraded-input fixtures)."""

def group_of(path: str) -> str:
    """UNCHANGED from current logic (.research/programs|briefs, docs/architecture[/history], else first 2 path parts)."""

def build_nodes(terse: dict, detail: dict) -> dict[str, dict]:
    """Merge terse entry + detail entry into the Node shape above. summary/decisions/key_findings/
    status/supersession_note pulled from detail when present."""

def classify_relationship(rel: str) -> str:
    """Map a related[] relationship label to an ecat:
       'supersedes','superseded-by','superseded'        -> 'supersession'
       anything else                                     -> 'reference'
    (containment edges are assigned ecat='containment' at creation, not here)."""

def build_edges(detail: dict, nodes: dict, root: Path) -> tuple[list[dict], list[dict]]:
    """Return (edges, dangling). Semantic edges from detail related[]; containment edges from
    subtree_root() logic (UNCHANGED). Each edge gets ekind + ecat + dclass. dangling = edges whose
    target is not a node (dclass set via classify_target)."""

def subtree_root(path: str) -> str | None:
    """UNCHANGED — .research/programs|briefs container dir."""

def classify_target(tgt: str, root: Path, scope: tuple[str, ...]) -> str:
    """UNCHANGED 3-way: out-of-scope | unindexed (exists on disk) | broken (missing)."""

def compute_degree(nodes: dict, edges: list[dict]) -> None:
    """Set deg/indeg/outdeg per node over RESOLVED edges (dclass==''). Mutates nodes in place."""

def build_adjacency(nodes: dict, edges: list[dict]) -> dict:
    """Build the adjacency map (resolved edges only)."""

def compute_communities(nodes: dict, edges: list[dict]) -> bool:
    """Unit 7. Optional Louvain over the resolved undirected graph. Pure-Python implementation
    (no new deps) OR no-op returning False if --communities flag absent. Sets node['community'].
    Returns has_communities."""

def assemble_data(...) -> dict:
    """Compose the full DATA object."""

def render(root: Path, out: Path, want_communities: bool) -> dict:
    """Orchestrate: load -> build -> assemble -> substitute into template -> write. Return stats for the CLI summary."""
```

**Implementation Notes**:
- `generated_at` is read from the terse index, **not** wall-clock — keeps render deterministic and
  diffable (mirrors the no-`Date.now()` discipline elsewhere in the repo).
- Degree/orphan computed over **resolved** edges only — a node whose only edge is a broken ref is
  still an orphan (matches current behaviour).
- Louvain (Unit 7) must add **no new pip dependency** — implement the modularity-greedy pass in
  ~40 lines of stdlib Python, gated behind a `--communities` flag (off by default). If skipped,
  `community=None` and the view hides the community-color toggle.
- Keep the existing CLI summary prints (nodes/edges/QA, UNINDEXED/BROKEN call-outs) — the SKILL.md
  workflow depends on them.
- New optional flag parsing: positional args unchanged; add `--communities` as an opt-in keyword.

**Acceptance Criteria**:
- [ ] `python3 render.py ~/dev/ds-engine /tmp/kg.html` exits 0 and writes valid HTML.
- [ ] `DATA` validates against the contract above (a `--print-data` debug mode dumps JSON to stdout for assertion in tests).
- [ ] Every node has `indeg`/`outdeg`/`deg` consistent with `adjacency` (in-count == indeg, out-count == outdeg).
- [ ] Every resolved edge carries a non-empty `ecat` ∈ {reference, supersession, containment}; every dangling edge has `dclass` ≠ "".
- [ ] Running against a terse-only fixture (edh-engine) yields nodes with `summary=""`, `decisions=[]` and does not crash.
- [ ] Same input → byte-identical output (determinism).

---

### Unit 2: `template.html` — shell, DOI loop, stable layout

**File**: `plugins/research-pipeline/skills/knowledge-graph/template.html` (rewrite)

CDN additions (alongside cytoscape 3.30.2 + fcose): `dagre` + `cytoscape-dagre`, `@popperjs/core` +
`tippy.js` + `cytoscape-popper`, `cytoscape-cxtmenu`, `cytoscape-expand-collapse`,
`cytoscape-navigator`. (Extensions wired in Units 3–5; loaded here.)

Core view module (vanilla JS, no build step). Single `__DATA__` placeholder; no other substitution
tokens except `__ROOT__` in `<title>` and a `__BUILD_STATS__` line for the header bar.

```javascript
const DATA = __DATA__;           // the only data source
const LSKEY = 'kg-pos:' + DATA.meta.root;   // localStorage namespace for positions/pins

// ---- view state ----
const view = {
  visible: new Set(),            // node ids currently shown
  focusHistory: [],              // breadcrumb stack (Unit 7)
  depth: 1,                      // neighborhood hop depth for showContext
  mode: 'graph',                 // 'graph' | 'table'
  ecatOff: new Set(),            // edge categories hidden (Unit 6)
  pinned: new Set(),             // pinned node ids (persisted)
  lens: null,                    // active QA lens or null
};

// ---- DOI core (Unit 2) ----
function search(query)        // match nodes by label/id (case-insensitive contains); returns matched ids
function showContext(focalIds, depth)  // visible = focal ∪ N-hop resolved neighbors; render, hide rest
function expandNode(id)       // add id's resolved neighbors to visible; local layout on newcomers only
function collapseNode(id)     // remove id's leaf neighbors not reachable another way
function resetView()          // clear visible; show empty "type to explore" state
function neighbors(id, depth) // BFS over resolved adjacency to `depth`, both directions

// ---- layout (Unit 2) ----
function backboneLayout()     // dagre over containment+supersession edges (deterministic), then place
                              //   reference-only nodes via fcose(randomize:false, quality:'proof')
function localLayout(newNodes)// preset existing positions as fixedNodeConstraint; layout only newNodes
                              //   in a boundingBox around their parent; existing nodes never move
function persistPositions()   // write {id: {x,y}} + pinned[] to localStorage (debounced on dragfree/layoutstop)
function restorePositions()   // load + apply saved positions; return true if any restored
function pinNode(id) / unpinNode(id)   // toggle, persisted; pinned nodes excluded from re-layout
```

**Implementation Notes**:
- **Empty-state first**: on load the canvas is empty with a centered "🔎 Type to explore your corpus
  — or press *Show all*" prompt. This is the DOI inversion; it is the single highest-leverage change.
- **showContext** is filter-mode (hide non-context), distinct from lenses which are highlight-mode.
- **Layout stability**: `backboneLayout()` runs **once** per corpus (cache key = sorted node-id hash
  in localStorage). On subsequent loads `restorePositions()` short-circuits it. `expandNode` only ever
  calls `localLayout` on the newcomers. There is **no global relayout button that re-randomizes** —
  "relayout" re-runs the deterministic backbone, producing the same result.
- New nodes appearing because the index grew: positions are merged — known ids keep saved positions,
  unknown ids get `localLayout` seeded near their highest-degree resolved neighbor.
- Header bar shows `__BUILD_STATS__` (nodes/related/containment/groups + QA counts) — preserve the
  current at-a-glance summary.

**Acceptance Criteria**:
- [ ] Fresh open shows the empty "type to explore" state, not the full graph.
- [ ] Typing a query that matches ≥1 node renders those nodes + their 1-hop neighborhood and hides the rest.
- [ ] Depth control (1/2/3) changes neighborhood size on the next search/expand.
- [ ] Clicking a node adds its neighbors; **already-visible nodes do not move** (assert positions stable across an expand).
- [ ] Reopening the HTML restores the prior layout from localStorage (no re-scatter).
- [ ] "Show all" renders the full graph using the deterministic backbone (same arrangement every time).

---

### Unit 3: cytoscape extensions — hover/click card, radial menu, compound collapse, minimap

**File**: `template.html` (additive)

```javascript
function initPopper()      // cytoscape-popper + tippy: on 'mouseover node' build a tippy with
                           //   label + kind·status·deg + summary excerpt (≤200 chars). Destroy on mouseout.
function initCxtmenu()     // cytoscape-cxtmenu radial menu on right-click node:
                           //   ['Open doc', 'Expand', 'Show dependents', 'Pin/Unpin', 'Hide']
                           //   'Open doc' -> open file:// path; 'Show dependents' -> reaches() filter
function initCompounds()   // model `group` as compound parent nodes; cytoscape-expand-collapse to
                           //   collapse a group to one node, double-click expands in place
function initNavigator()   // cytoscape-navigator minimap, bottom-right, collapsible
function reaches(id)       // reverse-transitive: all nodes that transitively reference id (impact view)
```

**Implementation Notes**:
- Compound parents are **synthetic** view nodes (one per `group`), not in `DATA.nodes`; created
  client-side from `node.group`. They participate in expand-collapse and dagre but never in QA/degree.
- `Open doc` uses `file://` + absolute path derived from `DATA.meta.root` (best effort; note in card
  if the browser blocks `file://` navigation).
- popper instances are created on demand and destroyed on mouseout (scout perf note — never
  pre-create for all nodes).

**Acceptance Criteria**:
- [ ] Hover shows a tippy card with title/kind/status/degree/summary excerpt; dismisses on mouseout.
- [ ] Right-click opens the radial menu; each action performs its function.
- [ ] A group can be collapsed to a single labeled node and double-click expands it in place.
- [ ] Minimap reflects pan/zoom and is collapsible.

---

### Unit 4: QA embedded in the graph + lenses + navigable findings

**File**: `template.html` (additive) + cytoscape style block

Visual encoding (cytoscape stylesheet, driven by `DATA` node fields):
- `node[?orphan]` → distinct muted fill
- `node[?superseded]` → purple ring (`border-color`)
- ghost `node[dclass="broken"]` → red diamond; `[dclass="unindexed"]` → orange diamond
- `width/height` = `mapData(indeg, …)` (in-link degree = "how referenced", per scout)
- edge `[dclass="broken"]` red, `[dclass="unindexed"]` orange, `[ecat="supersession"]` distinct dashed

```javascript
function lens(name)        // name ∈ 'orphans'|'broken'|'unindexed'|'superseded'|null
                           //   HIGHLIGHT mode: dim all, un-dim + halo the matching set (does NOT filter).
                           //   Ensures the relevant nodes are visible (adds them to view if hidden).
function nextFinding(name) // step through findings of class `name`, centering+selecting each in turn
function qaPanelRender()   // render the QA section: each class = a lens toggle with count + a 'next' stepper
```

**Implementation Notes**:
- Lenses are **highlight-mode** (overlay on whatever's visible) per the scout's highlight-vs-filter
  distinction; showContext/expand are the filter-mode counterparts.
- `nextFinding` keeps an index per class in `view`; wraps around; updates the detail card (Unit 5).

**Acceptance Criteria**:
- [ ] Orphan nodes are visually distinct without any interaction.
- [ ] Broken/unindexed refs render as colored diamonds with colored edges.
- [ ] Clicking a lens highlights its set over the current view (does not remove other nodes).
- [ ] "Next broken ref" centers each broken-ref finding in sequence and wraps.

---

### Unit 5: detail card + table view + brushing & linking

**File**: `template.html` (additive) — replaces the passive right panel with a tabbed
**Detail | Table | QA** panel.

```javascript
function showCard(id)      // render detail card for node id:
                           //   header: title, kind, status, group, updated
                           //   body: summary, decisions[], key_findings[]
                           //   IN-LINKS (adjacency.in) rendered ABOVE, OUT-LINKS (adjacency.out) BELOW (Roam model)
                           //   each link is clickable -> focusNode(targetId)
                           //   'Open file' button (file:// path)
function focusNode(id)     // center+select node, ensure visible (expand context if hidden), push breadcrumb, showCard
function renderTable()     // table of ALL DATA.nodes: cols = title, kind, status, indeg, outdeg, broken?, orphan?
function sortTable(col)    // client-side sort, toggling asc/desc
function tableRowClick(id) // -> focusNode(id) and switch to graph tab (brushing & linking)
function syncSelection(id) // single entry point: highlight node + matching table row + open card
```

**Implementation Notes**:
- **Bidirectional coupling is the anti-eye-candy requirement**: `syncSelection(id)` is called from
  node tap, table row click, QA finding step, and card in/out-link click — one code path keeps graph,
  table, and card in lockstep.
- Table is the "users preferred a table for audit" surface — it lists the *full* corpus regardless of
  what's visible in the graph, sortable by the QA-relevant columns. Clicking a row brings that node
  into the graph view.
- Card in/out link lists use `DATA.adjacency`; relationship label shown per link (e.g. "extends →").

**Acceptance Criteria**:
- [ ] Clicking a node opens the card with summary + decisions + key_findings and in-links-above / out-links-below.
- [ ] Clicking an in/out link in the card focuses that target node.
- [ ] Table lists all docs, sorts by each column, and clicking a row focuses the node in the graph.
- [ ] Selecting in any surface (graph/table/QA) highlights the corresponding row/node/card.

---

### Unit 6: edge-type toggles

**File**: `template.html` (additive header control)

```javascript
function toggleEcat(cat)   // cat ∈ 'reference'|'supersession'|'containment'; add/remove from view.ecatOff;
                           //   hide/show edges of that ecat (class 'ecat-hidden'); recompute orphan halo if desired
```

**Implementation Notes**:
- Three checkboxes (default all on). The scout flagged this as a gap no interactive tool ships —
  cheap here because `DATA.edges[].ecat` is precomputed.
- Hiding an ecat only affects edge visibility, not the DOI neighborhood computation (which always uses
  resolved adjacency) — toggles are a *display* filter, documented in a tooltip.

**Acceptance Criteria**:
- [ ] Each checkbox independently shows/hides its edge category.
- [ ] Toggling containment off leaves semantic edges intact and vice versa.

---

### Unit 7 (stretch): breadcrumb trail, semantic zoom, Louvain coloring

**File**: `template.html` (+ `render.py` `--communities`)

```javascript
function pushFocus(id) / popFocus()   // breadcrumb stack; render clickable trail; back navigation
function initSemanticZoom()           // cy.on('zoom'): below z<0.5 hide labels (dots); 0.5–1.0 titles; >1.0 titles+badges
function toggleCommunityColor()       // if DATA.meta.has_communities: recolor nodes by community vs group
```

**Implementation Notes**:
- Breadcrumb is the identified differentiator (no surveyed tool has focus-history).
- Community toggle only appears when `render.py --communities` populated `node.community`.

**Acceptance Criteria**:
- [ ] Navigating between focused nodes builds a clickable breadcrumb; clicking an entry returns to it.
- [ ] Zooming out collapses labels to dots; zooming in restores them.
- [ ] With `--communities`, a toggle recolors nodes by detected community.

---

### Unit 8: `SKILL.md` update

**File**: `plugins/research-pipeline/skills/knowledge-graph/SKILL.md`

**Implementation Notes**:
- Rewrite "What it produces" + "Workflow" for the DOI model: the graph opens in type-to-explore mode;
  document search/expand/depth, the Detail|Table|QA tabs, lenses, edge toggles, layout persistence,
  and the optional `--communities` flag.
- Keep Step 1 (ensure index exists) and the "report the QA summary + open the HTML" steps.
- Note position persistence (localStorage) and that the HTML is still throwaway/CDN-backed.

**Acceptance Criteria**:
- [ ] SKILL.md describes every new interaction and the `--communities` flag.
- [ ] The QA-summary reporting step still matches `render.py`'s stdout.

---

## Implementation Order

1. **Unit 1** — `render.py` view-model + `DATA` contract (everything downstream consumes it; ships with `--print-data` for testing).
2. **Unit 2** — `template.html` shell + DOI loop + stable layout (the core experience; usable on its own).
3. **Unit 3** — cytoscape extensions (hover card, radial menu, compounds, minimap).
4. **Unit 4** — QA embedded + lenses + navigable findings.
5. **Unit 5** — detail card + table + brushing/linking.
6. **Unit 6** — edge-type toggles (small, independent).
7. **Unit 7** — stretch (breadcrumb, semantic zoom, Louvain) — ship if budget allows.
8. **Unit 8** — SKILL.md update (after behavior is final).

Units 1–2 deliver a working, dramatically-better graph; 3–6 layer on the full scout consensus; 7 is
differentiation. Each unit is independently verifiable against a real fixture.

## Testing

### `tests/` (new) — `plugins/research-pipeline/skills/knowledge-graph/tests/test_render.py`
Python tests against the real fixtures (no network; pure data assertions via `--print-data`):
- **Contract**: emitted `DATA` has all required keys; node/edge/adjacency shapes match Unit 1.
- **Degree/adjacency consistency**: `len(adjacency[id].in) == indeg`, `.out == outdeg` for all nodes.
- **Edge classification**: every resolved edge `ecat` ∈ allowed set; supersedes-labelled edges → `supersession`.
- **QA parity**: `stats.broken/unindexed/orphans/superseded` equal the current script's output for ds-engine (golden regression vs. the v1 numbers).
- **Degraded input**: edh-engine (terse-only) → no crash, empty summaries/decisions.
- **Determinism**: two runs on ds-engine produce byte-identical HTML.

### Manual browser verification (checklist in the design — graph behavior can't be unit-tested headless cheaply)
- Open `/tmp/kg.html` for ds-engine, grimoire, edh-engine; walk the Unit 2–7 acceptance criteria.

## Verification Checklist

```bash
# data layer
python3 plugins/research-pipeline/skills/knowledge-graph/render.py ~/dev/ds-engine /tmp/kg-ds.html
python3 plugins/research-pipeline/skills/knowledge-graph/render.py ~/dev/edh-engine /tmp/kg-edh.html   # degraded input
python3 -m pytest plugins/research-pipeline/skills/knowledge-graph/tests/ -q

# determinism
python3 .../render.py ~/dev/ds-engine /tmp/a.html && python3 .../render.py ~/dev/ds-engine /tmp/b.html && diff /tmp/a.html /tmp/b.html

# open + manually verify DOI/layout/card/table/lenses/toggles
open /tmp/kg-ds.html
```
