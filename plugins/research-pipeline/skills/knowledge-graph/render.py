#!/usr/bin/env python3
"""Render a project's knowledge index as an interactive doc-corpus graph (v2).

This is a deterministic ADAPTER: it reads the project's terse index (node metadata) + detail index
(typed related[] edges, summaries, decisions, supersession) and emits ONE `DATA` view-model object
serialized into a self-contained HTML. The DATA contract is renderer-agnostic; two views consume it:
the default 3D view (template-3d.html, 3d-force-graph/three.js) and the 2D view (template.html,
cytoscape.js — search/expand DOI + QA lenses + table). render.py contains no view logic and no
runtime sub-agents.

Usage: render.py [PROJECT_ROOT] [OUT_HTML] [--2d] [--communities] [--print-data]
  PROJECT_ROOT defaults to the current working directory.
  OUT_HTML defaults to a temp file path (printed on completion).
  --2d           emit the 2D cytoscape view (search/expand DOI + QA lenses + table). Default is 3D.
  --communities  compute Louvain communities (pure-stdlib; off by default). Enables the 3D
                 community Z-axis option.
  --print-data   dump the DATA JSON to stdout (for tests) instead of/in addition to writing HTML.

QA classes for an unresolved related[] target:
  unindexed   — file exists on disk under a scanned root but isn't in the index (FIX: re-index / repair frontmatter)
  broken      — target does not exist on disk at all (FIX: correct the related[] slug)
  out-of-scope— target outside the indexed roots (e.g. src/), expected; not a defect
"""
import sys, json, html, tempfile, re
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("render.py requires PyYAML (pip install pyyaml)")

SCOPE = ("docs/", ".research/")  # roots the index scans; refs elsewhere are out-of-scope by design
PALETTE = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1", "#ff9da7",
           "#9c755f", "#bab0ac", "#86bcb6", "#d37295", "#a0cbe8", "#8cd17d", "#499894", "#79706e",
           "#fabfd2", "#d4a6c8", "#b6992d", "#d7660e", "#5b8ff9", "#61ddaa", "#f6bd16", "#7262fd"]
GHOST_COLOR = {"out-of-scope": "#888", "unindexed": "#ff9f1c", "broken": "#ff0033"}
SUPERSEDE_RELS = {"supersedes", "superseded-by", "superseded", "superseded_by"}
# ARD evidence overlay: attestations are a distinct node class, NOT doc nodes (they're
# excluded from the index by design — see ard-adoption-plan.md D2). Resolved = an attestation
# file backs a cited [handle]{N}; unresolved = a [handle]{N} cited with no attestation (a broken
# citation chain — the same defect /citation-lint + gate-citations flag, made visible here).
EVIDENCE_COLOR = {"resolved": "#2f9e80", "unresolved": "#ff0033"}
CITATION_RE = re.compile(r"\[([\w-]+)\]\{(\d+)\}")   # same wire-form the lint resolves
ATTEST_DIR = ".research/attestation"


# ---------------------------------------------------------------------------
# load
# ---------------------------------------------------------------------------
def load_index(root: Path):
    """Return (terse, detail). Exit if terse is missing; detail defaults to empty (degraded input)."""
    terse_path = root / "docs/knowledge-index.yaml"
    detail_path = root / "docs/knowledge-index-detail.yaml"
    if not terse_path.exists():
        sys.exit(f"no knowledge index at {terse_path} — run /research-pipeline:knowledge-index first")
    terse = yaml.safe_load(terse_path.read_text()) or {}
    detail = (yaml.safe_load(detail_path.read_text()) if detail_path.exists() else None) or {"documents": {}}
    return terse, detail


# ---------------------------------------------------------------------------
# grouping (unchanged semantics)
# ---------------------------------------------------------------------------
def group_of(path: str) -> str:
    if path.startswith(".research/programs/"):
        return "prog:" + path.split("/")[2]
    if path.startswith(".research/briefs/"):
        return "brief:" + path.split("/")[2]
    if path.startswith(".research/"):
        return "research-other"
    if path.startswith("docs/architecture/history"):
        return "history"
    if path.startswith("docs/architecture"):
        return "architecture"
    parts = path.split("/")
    return "/".join(parts[:2]) if len(parts) > 1 else parts[0]


def subtree_root(path: str):
    """The program/brief container directory for containment edges, e.g. .research/programs/<X>."""
    if path.startswith(".research/programs/") or path.startswith(".research/briefs/"):
        return "/".join(path.split("/")[:3])
    return None


def classify_target(tgt: str, root: Path) -> str:
    if not tgt.startswith(SCOPE):
        return "out-of-scope"
    return "unindexed" if (root / tgt).exists() else "broken"


def classify_relationship(rel: str) -> str:
    return "supersession" if (rel or "").strip().lower() in SUPERSEDE_RELS else "reference"


# ---------------------------------------------------------------------------
# nodes
# ---------------------------------------------------------------------------
def build_nodes(terse: dict, detail: dict) -> dict:
    nodes = {}
    for e in terse.get("documents", []) or []:
        p = e["path"]
        nodes[p] = {
            "id": p,
            "label": e.get("title") or p.rsplit("/", 1)[-1],
            "kind": e.get("kind") or "?",
            "type": e.get("type") or "?",
            "status": "",
            "nav": e.get("nav_priority") == "high",
            "consumer_hint": e.get("consumer_hint") or "",
            "updated": str(e.get("updated") or ""),
            "summary": "", "decisions": [], "key_findings": [],
            "supersession_note": None, "superseded": False,
            "deg": 0, "indeg": 0, "outdeg": 0, "orphan": True,
            "community": None,
        }
    for p, entry in (detail.get("documents", {}) or {}).items():
        if not isinstance(entry, dict) or p not in nodes:
            continue
        n = nodes[p]
        n["summary"] = (entry.get("summary") or "").strip()
        n["decisions"] = [str(d).strip() for d in (entry.get("decisions") or []) if d]
        n["key_findings"] = [str(k).strip() for k in (entry.get("key_findings") or []) if k]
        if entry.get("status"):
            n["status"] = str(entry["status"]).strip()
        if entry.get("supersession_note"):
            n["supersession_note"] = str(entry["supersession_note"]).strip()
            n["superseded"] = True
    return nodes


# ---------------------------------------------------------------------------
# edges
# ---------------------------------------------------------------------------
def build_edges(detail: dict, nodes: dict, root: Path):
    """Return (edges, dangling). Semantic edges from related[]; containment edges from research trees."""
    edges, dangling, seen = [], [], set()
    for p, entry in (detail.get("documents", {}) or {}).items():
        if not isinstance(entry, dict):
            continue
        for r in entry.get("related") or []:
            if not isinstance(r, dict):
                continue
            tgt = r.get("slug")
            rel = (r.get("relationship") or "related").strip()
            if not tgt or (p, tgt, rel) in seen:
                continue
            seen.add((p, tgt, rel))
            ecat = classify_relationship(rel)
            dcls = classify_target(tgt, root) if tgt not in nodes else ""
            if dcls:
                dangling.append({"source": p, "target": tgt, "rel": rel, "dclass": dcls})
            edges.append({"id": f"{p}__{tgt}__{ecat}", "source": p, "target": tgt, "rel": rel,
                          "ekind": "related", "ecat": ecat, "dclass": dcls})

    # containment edges: connect each research subtree's root (super-parent.md / parent.md) to its sub-docs
    roots = {}
    for p in nodes:
        base = subtree_root(p)
        if not base:
            continue
        name = p.split("/")[-1]
        if name == "super-parent.md" or (name == "parent.md" and base not in roots):
            roots[base] = p
    cont_seen = set()
    for p in nodes:
        base = subtree_root(p)
        if not base or base not in roots:
            continue
        rt = roots[base]
        if p == rt or (rt, p) in cont_seen:
            continue
        cont_seen.add((rt, p))
        edges.append({"id": f"{rt}__{p}__containment", "source": rt, "target": p, "rel": "contains",
                      "ekind": "containment", "ecat": "containment", "dclass": ""})
    return edges, dangling


# ---------------------------------------------------------------------------
# ARD evidence overlay (attestations + [handle]{N} citation edges)
# ---------------------------------------------------------------------------
def _attestation_frontmatter(text: str) -> dict:
    """Minimal `---`-fenced frontmatter scan — the few fields the overlay surfaces. No YAML dep
    (the renderer's PyYAML is for the index; attestations are read straight from disk)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    body = text[3:end] if end != -1 else ""
    fm = {}
    for line in body.splitlines():
        k, sep, v = line.partition(":")
        if sep and k.strip():
            fm[k.strip()] = v.strip()
    return fm


def build_evidence(root: Path, nodes: dict):
    """Return (evidence, citations) — the ARD overlay. Evidence nodes are read DIRECTLY from
    `.research/attestation/*.md` (they're not in the index), keyed by source handle; citation
    edges come from scanning each indexed `.research/` doc body for `[handle]{N}`. Evidence is
    deliberately kept OUT of `nodes` so doc-corpus degree/communities/QA are unaffected (ARD D2:
    visible in the graph without being schema-linted as docs). A cited handle with no attestation
    becomes an `unresolved` evidence node (a broken citation chain, surfaced visually)."""
    evidence, citations, cit_seen = {}, [], set()
    att_dir = root / ATTEST_DIR
    if att_dir.is_dir():
        for f in sorted(att_dir.glob("*.md")):
            fm = _attestation_frontmatter(f.read_text(encoding="utf-8", errors="ignore"))
            handle = fm.get("source_handle") or f.stem
            evidence[handle] = {
                "id": "att:" + handle, "handle": handle, "label": handle, "kind": "evidence",
                "resolved": True, "provenance": fm.get("provenance", ""),
                "fetched": fm.get("fetched", ""),
                "source": fm.get("source_url") or fm.get("source_path") or "",
                "color": EVIDENCE_COLOR["resolved"], "cited_by": 0,
            }
    for p in sorted(nodes):
        if not p.startswith(".research/"):
            continue
        fp = root / p
        if not fp.is_file():
            continue
        for m in CITATION_RE.finditer(fp.read_text(encoding="utf-8", errors="ignore")):
            handle, n = m.group(1), int(m.group(2))
            if (p, handle) in cit_seen:
                continue
            cit_seen.add((p, handle))
            resolved = handle in evidence
            if not resolved:
                evidence[handle] = {
                    "id": "att:" + handle, "handle": handle, "label": handle, "kind": "evidence",
                    "resolved": False, "provenance": "", "fetched": "", "source": "",
                    "color": EVIDENCE_COLOR["unresolved"], "cited_by": 0,
                }
            evidence[handle]["cited_by"] += 1
            citations.append({"id": f"{p}__att:{handle}", "source": p, "target": "att:" + handle,
                              "handle": handle, "n": n, "resolved": resolved})
    return [evidence[h] for h in sorted(evidence)], citations


def compute_degree(nodes: dict, edges: list):
    for e in edges:
        if e["dclass"]:
            continue  # resolved edges only
        s, t = e["source"], e["target"]
        if s in nodes:
            nodes[s]["outdeg"] += 1
            nodes[s]["deg"] += 1
        if t in nodes:
            nodes[t]["indeg"] += 1
            nodes[t]["deg"] += 1
    for n in nodes.values():
        n["orphan"] = n["deg"] == 0


def build_adjacency(nodes: dict, edges: list) -> dict:
    adj = {p: {"in": [], "out": []} for p in nodes}
    for e in edges:
        if e["dclass"]:
            continue
        s, t = e["source"], e["target"]
        if s in adj and t in nodes:
            adj[s]["out"].append({"id": t, "rel": e["rel"], "ecat": e["ecat"]})
        if t in adj and s in nodes:
            adj[t]["in"].append({"id": s, "rel": e["rel"], "ecat": e["ecat"]})
    return adj


# ---------------------------------------------------------------------------
# communities (optional, pure stdlib — one Louvain-style greedy pass)
# ---------------------------------------------------------------------------
def compute_communities(nodes: dict, edges: list) -> bool:
    """Greedy modularity local-moving over the resolved undirected graph. No new deps. Best-effort."""
    ids = list(nodes.keys())
    if not ids:
        return False
    nbrs = {p: {} for p in ids}
    m = 0
    for e in edges:
        if e["dclass"]:
            continue
        s, t = e["source"], e["target"]
        if s in nbrs and t in nbrs and s != t:
            nbrs[s][t] = nbrs[s].get(t, 0) + 1
            nbrs[t][s] = nbrs[t].get(s, 0) + 1
            m += 1
    if m == 0:
        return False
    deg = {p: sum(w for w in nbrs[p].values()) for p in ids}
    comm = {p: i for i, p in enumerate(ids)}
    two_m = 2.0 * m
    improved, passes = True, 0
    while improved and passes < 20:
        improved = False
        passes += 1
        for p in ids:  # deterministic order
            cur = comm[p]
            # sum of weights to each neighboring community
            wc = {}
            for q, w in nbrs[p].items():
                wc[comm[q]] = wc.get(comm[q], 0) + w
            best, best_gain = cur, 0.0
            for c, w_in in wc.items():
                if c == cur:
                    continue
                # modularity delta (local approximation): w_in - deg[p]*sigma_tot[c]/2m
                sigma = sum(deg[q] for q in ids if comm[q] == c)
                gain = w_in - deg[p] * sigma / two_m
                if gain > best_gain:
                    best, best_gain = c, gain
            if best != cur:
                comm[p] = best
                improved = True
    # renumber compactly
    relabel, nxt = {}, 0
    for p in ids:
        c = comm[p]
        if c not in relabel:
            relabel[c] = nxt
            nxt += 1
        nodes[p]["community"] = relabel[c]
    return True


# ---------------------------------------------------------------------------
# assemble
# ---------------------------------------------------------------------------
def assemble_data(root, terse, nodes, edges, dangling, adjacency, has_communities,
                  evidence=None, citations=None) -> dict:
    evidence = evidence or []
    citations = citations or []
    groups = sorted({group_of(p) for p in nodes})
    gcolor = {g: PALETTE[i % len(PALETTE)] for i, g in enumerate(groups)}
    for p, n in nodes.items():
        n["group"] = group_of(p)
        n["color"] = gcolor[n["group"]]

    # ghosts (dangling targets), deduped by target
    ghosts = {}
    for d in dangling:
        t = d["target"]
        if t not in ghosts:
            ghosts[t] = {"id": t, "label": t.rsplit("/", 1)[-1], "dclass": d["dclass"],
                         "color": GHOST_COLOR[d["dclass"]]}

    orphan_groups = {}
    for p, n in nodes.items():
        if n["orphan"]:
            orphan_groups.setdefault(n["group"], []).append(p)

    qa = {
        "unindexed": sorted({d["target"] for d in dangling if d["dclass"] == "unindexed"}),
        "broken": sorted({d["target"] for d in dangling if d["dclass"] == "broken"}),
        "out_of_scope": sorted({d["target"] for d in dangling if d["dclass"] == "out-of-scope"}),
        "orphans": orphan_groups,
        "superseded": sorted(p for p, n in nodes.items() if n["superseded"]),
        "unresolved_citations": sorted(e["id"] for e in evidence if not e["resolved"]),
    }
    stats = {
        "nodes": len(nodes),
        "related": sum(1 for e in edges if e["ekind"] == "related"),
        "containment": sum(1 for e in edges if e["ekind"] == "containment"),
        "groups": len(groups),
        "orphans": sum(len(v) for v in orphan_groups.values()),
        "unindexed": len(qa["unindexed"]), "broken": len(qa["broken"]),
        "oos": len(qa["out_of_scope"]), "superseded": len(qa["superseded"]),
        "evidence": len(evidence),
        "citations": len(citations),
        "unresolved_citations": sum(1 for c in citations if not c["resolved"]),
    }
    return {
        "meta": {"root": root.name, "root_abs": str(root), "generated_at": str(terse.get("generated_at") or ""),
                 "total_docs": terse.get("total_docs") or len(nodes),
                 "schema_version": terse.get("schema_version") or 0,
                 "has_communities": has_communities, "scope": list(SCOPE)},
        "nodes": list(nodes.values()),
        "ghosts": list(ghosts.values()),
        "edges": edges,
        "evidence": evidence,
        "citations": citations,
        "adjacency": adjacency,
        "qa": qa,
        "groups": [{"name": g, "color": gcolor[g]} for g in groups],
        "stats": stats,
    }


def render(root: Path, out: Path, want_communities: bool, want_3d: bool = True):
    terse, detail = load_index(root)
    nodes = build_nodes(terse, detail)
    edges, dangling = build_edges(detail, nodes, root)
    compute_degree(nodes, edges)
    adjacency = build_adjacency(nodes, edges)
    has_comm = compute_communities(nodes, edges) if want_communities else False
    evidence, citations = build_evidence(root, nodes)
    data = assemble_data(root, terse, nodes, edges, dangling, adjacency, has_comm, evidence, citations)

    tpl = "template-3d.html" if want_3d else "template.html"
    template = (Path(__file__).parent / tpl).read_text()
    stats = data["stats"]
    evid = (f' · <b>{stats["evidence"]}</b> evidence/<b>{stats["citations"]}</b> cites'
            if stats["evidence"] else "")
    build_stats = (f'<b>{stats["nodes"]}</b> docs · <b>{stats["related"]}</b> related · '
                   f'<b>{stats["containment"]}</b> containment · <b>{stats["groups"]}</b> groups · '
                   f'QA <b>{stats["unindexed"]}</b>u/<b>{stats["broken"]}</b>b/'
                   f'<b>{stats["orphans"]}</b>o/<b>{stats["superseded"]}</b>s{evid}')
    data_json = json.dumps(data, sort_keys=True)  # sort_keys for byte-stable output
    out_html = (template
                .replace("__ROOT__", html.escape(root.name))
                .replace("__BUILD_STATS__", build_stats)
                .replace("__DATA__", data_json))
    out.write_text(out_html)
    return data, stats


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    root = Path(args[0]).resolve() if len(args) > 0 else Path.cwd()
    out = Path(args[1]) if len(args) > 1 else Path(tempfile.gettempdir()) / "knowledge-graph.html"

    if "--print-data" in flags and len(args) < 2:
        # data-only mode for tests: build but don't require writing HTML to a real target
        terse, detail = load_index(root)
        nodes = build_nodes(terse, detail)
        edges, dangling = build_edges(detail, nodes, root)
        compute_degree(nodes, edges)
        adjacency = build_adjacency(nodes, edges)
        has_comm = compute_communities(nodes, edges) if "--communities" in flags else False
        evidence, citations = build_evidence(root, nodes)
        data = assemble_data(root, terse, nodes, edges, dangling, adjacency, has_comm, evidence, citations)
        print(json.dumps(data, sort_keys=True))
        return

    data, stats = render(root, out, want_communities="--communities" in flags, want_3d="--2d" not in flags)
    qa = data["qa"]
    print(f"nodes={stats['nodes']} related_edges={stats['related']} "
          f"containment_edges={stats['containment']} groups={stats['groups']}")
    print(f"QA: unindexed={stats['unindexed']} broken={stats['broken']} out-of-scope={stats['oos']} "
          f"orphans={stats['orphans']} superseded={stats['superseded']}")
    if stats["evidence"]:
        print(f"evidence: {stats['evidence']} attestation node(s) · {stats['citations']} citation edge(s) · "
              f"{stats['unresolved_citations']} unresolved [handle]{{N}} (broken chains)")
    print(f"wrote {out}")
    if qa["unindexed"]:
        print("  UNINDEXED (on disk, fix index):", ", ".join(qa["unindexed"][:8]))
    if qa["broken"]:
        print("  BROKEN refs:", ", ".join(qa["broken"][:8]))
    if "--print-data" in flags:
        print(json.dumps(data, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1:])
