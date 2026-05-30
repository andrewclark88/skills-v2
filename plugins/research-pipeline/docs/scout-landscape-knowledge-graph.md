---
description: "Prior-art landscape for rebuilding the knowledge-graph skill's interface — PKM graph views, JS render ecosystems, code-graph viewers, InfoVis UX canon, and the eye-candy critique. Read before designing the v2 interactive doc-corpus graph."
type: landscape
kind: research
research_method: /scout
updated: 2026-05-29
summary: |
  Scout of interactive knowledge-graph / doc-corpus visualization UIs to inform a bold rebuild of
  the research-pipeline knowledge-graph skill (a cytoscape.js static-HTML renderer that users find
  "clunky / not interactive"). Five vectors — PKM incumbents, the JS render ecosystem, code/dependency
  graph viewers, the InfoVis UX canon, and the "graph view is eye-candy" critique — converge on one
  diagnosis and one fix.
key_findings:
  - "Root cause of 'clunky' is interaction model, not rendering: the graph dumps the whole corpus at once with no entry point. Every other complaint flows from this."
  - "Highest-leverage change: adopt van Ham & Perer's Search → Show Context → Expand-on-Demand (DOI) model. Independently corroborated by Obsidian local-graph+depth, Juggl expand-from-seed, Nx focus mode, dependency-cruiser --focus --focus-depth."
  - "Stay on cytoscape.js — at dozens-to-low-hundreds of nodes, WebGL (sigma.js) buys nothing; the missing layer is the extension ecosystem (popper, cxtmenu, expand-collapse, dagre, navigator)."
  - "Layout instability is the #1 universal complaint across every PKM tool — force layouts scatter on relayout and destroy the user's mental map (Archambault & Purchase 2013). Fix: layout once, persist positions, deterministic hierarchy backbone."
  - "Embed QA diagnostics into the graph (Madge/Understand: orphan fill, broken-ref badge, cycle ring) and make the QA panel one-click lenses + a linked table view, not a passive list."
  - "Brushing & linking: node click ↔ inline detail card (summary, in/out-links, open-file) ↔ QA finding focus. Bidirectional coupling is what separates a tool from a picture."
  - "Six-point bar to not be eye-candy: scoped/clustered default, visual metadata encoding, one-click QA lenses, inline detail card, local zoom, deterministic layout."
status: draft
---

# Scout Landscape: Knowledge-Graph Skill Rebuild

*Scouted: 2026-05-29*

## Context

The `research-pipeline:knowledge-graph` skill renders a project's document/research corpus as an
interactive browser graph. Today it's a deterministic Python renderer (`render.py`) that reads
`knowledge-index.yaml` + `knowledge-index-detail.yaml`, builds nodes (docs) and edges (typed
`related[]` + directory-containment), and string-substitutes into a `template.html` that draws a
**static cytoscape.js fcose graph** with a right-side QA/linter panel (unindexed / broken / orphan /
superseded). The user's verdict: **"clunky and not that useful or interactive."**

We scouted prior art to inform a **bold rebuild** of the interface. The five real jobs this view
serves, decomposed first-principles: **orient** (what clusters exist), **navigate** (find a doc,
follow a thread), **QA/lint** (broken / orphan / superseded), **drill-down** (the rich detail layer —
summaries, decisions, key_findings — currently barely surfaced), and **bridge to reading** (open the
actual doc).

## Search Vectors

**Direct:** Obsidian graph view (+ Juggl / Extended Graph plugins) · Logseq / Roam / Foam / org-roam-ui / Dendron graph views · cytoscape.js vs sigma.js vs d3-force vs vis-network vs G6 ecosystem
**Adjacent:** layout stability & deterministic layouts · code/dependency-graph viewers (dependency-cruiser, Madge, Nx, CodeSee, SciTools Understand, Emerge) · the hairball problem & remedies · detail-on-demand / brushing & linking
**Analogous:** bio/ontology network tools (Gephi, Cytoscape desktop) · TheBrain / Tinderbox / MOCs · the "graph view is useless eye-candy" critique discourse

---

## Landscape

### Theme A — The interaction model is the problem (the convergent finding)

Every vector arrived at the same root cause: **showing the entire corpus at once, by default, with no
entry point.** The graph is passive — it waits to be navigated by physics-placed edges instead of
responding to user intent.

#### [van Ham & Perer (2009), "Search, Show Context, Expand on Demand"](https://perer.org/papers/adamPerer-DOIGraphs-InfoVis2009.pdf) — assessed
**Key insight:** The empirically validated fix for large-graph navigation. A degree-of-interest
function `DOI(node) = importance(node) − distance(focus, node)` drives a three-phase model: **Search**
(type a keyword → matching nodes become focal), **Show Context** (render only nodes above a DOI
threshold — focal set + 1–2 hop neighborhood), **Expand on Demand** (click to grow). In their legal
citation network a 2-hop neighborhood of 2,345 nodes collapsed to a comprehensible subgraph.
**Relevance:** This is our highest-leverage change. The graph should start minimal (or empty —
"type to explore") and respond to a search box. Builds directly on cytoscape's native
`node.neighborhood()` / `closedNeighborhood()`.

#### [Shneiderman (1996), "The Eyes Have It"](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf) — assessed
**Key insight:** "Overview first, zoom and filter, then details on demand." Our current UI inverts the
mantra — details (the whole graph) come first, filter controls are minimal. **Relevance:** Make
search + type-filters the *primary* interface; the graph is the response surface, and the detail card
is the last step (on click), not a hover afterthought.

#### Corroborating implementations (each independently lands on DOI-style focus):
- **Obsidian local graph + depth slider** — the single most-praised PKM nav feature: anchor on a doc, fan out 1–4 hops. ([help docs](https://obsidian.md/help/plugins/graph))
- **[Juggl plugin](https://github.com/HEmile/juggl)** — local-first, expand-from-seed by design; right-click radial menu (expand/collapse/pin/hide); saved workspaces preserve positions. Hairball is structurally impossible.
- **[Nx project graph](https://nx.dev/docs/features/explore-graph)** — best-in-class dev-tool graph UX: Focus button, composite-node double-click-to-expand-in-place, **trace path between two nodes**, edge-click → "which file caused this edge?"
- **[dependency-cruiser](https://github.com/sverweij/dependency-cruiser)** — `--focus <regex> --focus-depth N` (N-hop bidirectional), `--reaches` (reverse-transitive impact), `--highlight` (mark, don't filter) vs `--focus` (filter). The cleanest formalization of neighborhood scoping.

### Theme B — Stay on cytoscape.js; add the missing extension layer

#### Verdict (from the JS-ecosystem scout): **stay on cytoscape.js.**
At dozens-to-low-hundreds of nodes we're far below the ~3–5k-node threshold where sigma.js's WebGL
matters. Migrating would forfeit cytoscape's extension ecosystem and compound-node support for no
gain. cytoscape core is very healthy (v3.33.4, May 2026, ~11k stars, monthly releases). The "clunky"
feeling is a **missing-UX-layer** problem, and the layer already exists as extensions:

| Extension | Health | Adds | Helps us |
|---|---|---|---|
| [cytoscape-popper](https://github.com/cytoscape/cytoscape.js-popper) + Tippy | v4.0.0, maintained | DOM tooltips/popovers tracking pan/zoom | Hover → rich card (title, kind, status, summary excerpt). Biggest "feels interactive" win. |
| [cytoscape-cxtmenu](https://github.com/cytoscape/cytoscape.js-cxtmenu) | v3.5.0, stable | Radial right-click menu | Per-node: open doc, expand neighbors, show dependents, hide subtree |
| [cytoscape.js-expand-collapse](https://github.com/iVis-at-Bilkent/cytoscape.js-expand-collapse) | v4.1.1, maintenance | Collapse/expand compound nodes | Collapse a directory/epic to one node, double-click to expand |
| [cytoscape-dagre](https://github.com/cytoscape/cytoscape.js-dagre) | v3.0.0, maintained | Deterministic layered DAG layout | Stable hierarchy backbone (north-star → arch → briefs) — no scatter |
| [cytoscape-navigator](https://github.com/cytoscape/cytoscape.js-navigator) | stable | Minimap | Spatial orientation at 100+ nodes |

Other libs assessed and set aside: **sigma.js v3 + Graphology** (WebGL, for 10k+ nodes; no compound
nodes; needs build tooling — overkill), **vis-network** (friendly reactive API, weaker layouts/no
compound), **G6 v5** (powerful but Chinese-docs-first, switching cost), **react-flow** (flowcharts,
not networks), **d3-force** (too low-level — you'd rebuild cytoscape's event layer).

### Theme C — Layout stability (the #1 universal complaint)

Across **every** PKM tool (Obsidian, Logseq, Foam, Dendron, org-roam-ui) the most-cited usability
failure is **scatter on relayout** — every filter change / session restart re-runs the force sim and
destroys spatial memory. [Archambault & Purchase (2013), "The Map in the Mental Map"](https://dl.acm.org/doi/10.1016/j.ijhcs.2013.08.004)
shows empirically that layout stability helps on exactly our tasks ("where is X?", "what connects to
Y?"). Roam is the positive outlier — stable positions between sessions — and users cite it as the
advantage, trading away "dynamic reveal" for a "boring but stable" map.

**Recommended recipe:** deterministic **dagre** for the hierarchy backbone; **fcose with
`randomize:false` + `quality:'proof'`** for the relationship web; **persist node positions to
localStorage**, restore on load, and never globally re-run; for expand-on-demand, run a *local* layout
scoped only to the new nodes (`boundingBox` around the focal node) so existing nodes don't move.
`fcose.fixedNodeConstraint` supports pinning; pin-on-drag + persisted pins is the Juggl/GraphFrontier
pattern.

### Theme D — Diagnostics belong *in* the graph (the QA-panel rethink)

Code-graph tools show a spectrum of diagnostic integration; the best **bake findings into node/edge
rendering** rather than isolating them in a side list:
- **[Madge](https://github.com/pahen/madge)** — tri-color encoding: red = circular, green = leaf, baked into the graph by default. Maps directly: orphan fill, broken-ref badge, supersession-cycle ring.
- **[SciTools Understand](https://scitools.com/)** — Butterfly graph (node + immediate in/out = a *named* focus mode), cluster-boundary edge indicators (filled/empty arrow = "hidden edges beyond this boundary, click to reveal"), 4-quadrant archetype classification.
- **IntelliJ DSM** — the gold standard for *navigable* diagnostics: `F2` → next cycle, jump-to-source. Diagnostics aren't just visible, they're steppable.
- **[Emerge](https://github.com/glato/emerge)** — Louvain community detection + concave-hull cluster outlines + node-size = fan-in/out. Structure *emerges* from data without manual grouping.

**Implication:** node color/size/badge should answer "what's wrong?" and "where am I?" pre-click. The
QA panel becomes (1) one-click **lenses** (orphans / broken / superseded / by-kind), highlight-mode by
default; (2) a **navigable** finding list ("next broken ref" centers it); (3) a **linked table view**
of the same data (sortable: kind, status, in/out-link count, broken-ref flag) — multiple PKM critics
and an academic study found users "preferred a table" for analytical/audit tasks.

### Theme E — Detail-on-demand & brushing-and-linking (don't be eye-candy)

The line between a tool and a picture is **bidirectional coupling** (brushing & linking, Becker &
Cleveland 1987). Borrowed patterns:
- **Inline detail card on click** (Wikipedia "entity hop" model, preferred by study participants over graph nav): title, kind, status, summary, and **clickable in-links / out-links** that re-focus the graph. Never a blind click-through.
- **Roam directional page graph** — in-links rendered *above* the node, out-links *below*. For us: supersedes/cites float above, references/derives float below — role legible without reading edge labels.
- **org-roam-ui / Foam "follow active file"** — clicking a doc in the table/QA list auto-centers + highlights its node, and vice versa.
- **Sourcegraph hover model** — "navigation lives in the hover," with inline "find references / find dependents."
- **Edge-type toggles** (Dendron hierarchy-vs-link separation) — independently show/hide containment vs `supersedes` vs `references`. *Gap:* no interactive graph tool surveyed ships typed-edge filtering as UI toggles — an opportunity, and a natural fit since our edges are already typed.

### Theme F — The eye-candy critique (the inversion: what NOT to do)

The recurring complaints (["Obsidian's Graph View Is Beautiful and Almost Completely Useless"](https://codeculture.store/blogs/developer-culture/obsidian-graph-view-useful),
r/ObsidianMD, [arxiv 2304.01311](https://arxiv.org/html/2304.01311v4)):
1. **Hairball past ~200 nodes** → progressive disclosure by default.
2. **Spatial position carries no meaning but users assume it does** → cluster by real metadata, label clusters, deterministic layout.
3. **Shows connections, not priority/status/"what's next"** → encode status/kind/health visually.
4. **Can't navigate TO something without already knowing it** → search is first-class, result focuses the node.
5. **No saved filter presets** → one-click QA lenses, savable named views.
6. **Flat — all links equal, no hierarchy** → typed edges rendered distinctly.
7. **Passive, no completion semantics** → click closes a loop (opens the card); supports "reviewed / not-yet-visited" for QA sweeps.

**The six-point bar to not be eye-candy:** scoped/clustered default · visual metadata encoding ·
one-click QA lenses · inline detail card · local zoom · deterministic layout. *We currently clear
~1.5 of six.*

---

## Research Recommendations

Mostly **applied/spike** rather than deep-domain — the InfoVis theory is settled; the open questions
are implementation fit:

- **DOI / expand-on-demand in cytoscape.js** — spike the Search → Context → Expand loop against a real
  corpus (this repo has none; use a pipeline-managed project like grimoire/cruxcontrol as a test
  fixture). Validate `neighborhood()` performance and the "type-to-explore" empty state.
- **Layout-position persistence** — design how positions serialize. localStorage works for a throwaway
  HTML, but a regenerated graph (new docs added) needs graceful merge: keep existing positions, local-
  layout only the newcomers. Decide whether to persist into a sidecar file next to the index.
- **Louvain community detection** — evaluate `graphology-communities-louvain` (compute in `render.py`
  via a JS step, or a Python equivalent) vs. just coloring by existing `group`/`kind`. Is data-driven
  clustering better than our metadata grouping for *this* corpus shape?
- **Edge-type toggle UX** — the identified gap; low-cost, high-value since edges are already typed.
- **Table view ↔ graph linking** — the "users preferred a table" finding suggests the table may be the
  primary QA surface, with the graph as orientation. Worth prototyping both as co-equal tabs.

## Gaps

- **No tool ships a navigation breadcrumb trail** (focus history) — unsolved across all interactive
  graph tools surveyed. An easy differentiator.
- **No interactive tool ships typed-edge filtering as UI toggles** — opportunity.
- **Incremental-layout stability when adding nodes** is an open problem in cytoscape.js; the
  persist-and-local-layout workaround is practical but not turnkey.
- **Edge-label readability at scale** — no library auto-manages label visibility by zoom; needs manual
  `cy.on('zoom')` thresholds (semantic zoom).
- We found no prior art for graphing a *build-pipeline doc corpus* specifically (research briefs +
  architecture + substrate items) — closest analogues are code-dependency viewers; the patterns
  transfer but the domain framing is ours to define.

## Sources

Consolidated from five parallel scouts. Highest-value:
- van Ham & Perer (2009) DOI graphs — https://perer.org/papers/adamPerer-DOIGraphs-InfoVis2009.pdf
- Shneiderman (1996) The Eyes Have It — https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf
- Archambault & Purchase (2013) Map in the Mental Map — https://dl.acm.org/doi/10.1016/j.ijhcs.2013.08.004
- cytoscape.js + extensions — https://js.cytoscape.org/ · popper, cxtmenu, expand-collapse, dagre, navigator (repos linked inline above)
- cytoscape-fcose (constraint layout) — https://github.com/iVis-at-Bilkent/cytoscape.js-fcose
- dependency-cruiser — https://github.com/sverweij/dependency-cruiser · Nx graph — https://nx.dev/docs/features/explore-graph · Madge — https://github.com/pahen/madge · SciTools Understand — https://scitools.com/ · Emerge — https://github.com/glato/emerge
- Juggl — https://github.com/HEmile/juggl · Obsidian graph help — https://obsidian.md/help/plugins/graph · org-roam-ui — https://github.com/org-roam/org-roam-ui · Dendron graph — https://wiki.dendron.so
- "Beautiful and Almost Completely Useless" — https://codeculture.store/blogs/developer-culture/obsidian-graph-view-useful
- KGs in Practice (arxiv 2304.01311) — https://arxiv.org/html/2304.01311v4
- Louvain method — https://en.wikipedia.org/wiki/Louvain_method · Gephi communities — https://jveerbeek.gitlab.io/gephi/docs/community.html
- Brushing & linking — https://infovis-wiki.net/wiki/Linking_and_Brushing
- Semantic zoom for ontology graphs (Fraunhofer 2017) — https://publica.fraunhofer.de/entities/publication/d99ba659-2a14-4c86-9228-f8d2c57e23e9
- TheBrain Plex — https://stephenjzeoli.medium.com/the-plex-context-and-meaning-e0eb43498feb · Maps of Content — https://www.dsebastien.net/2022-05-15-maps-of-content/
