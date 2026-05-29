#!/usr/bin/env python3
"""Render a project's knowledge index as an interactive graph + integrity QA.

Reads the project's terse index (node metadata) + detail index (typed related[] edges
+ supersession), adds directory-containment edges for research trees, computes
integrity findings (3-way dangling classification, orphans, superseded), and emits a
self-contained cytoscape.js HTML that opens in a browser. Sibling to agile-workflow:board.

Usage: render.py [PROJECT_ROOT] [OUT_HTML]
  PROJECT_ROOT defaults to the current working directory.
  OUT_HTML defaults to a temp file path (printed on completion).

QA classes for an unresolved related[] target:
  unindexed   — file exists on disk under a scanned root but isn't in the index (FIX: re-index / repair its frontmatter)
  broken      — target does not exist on disk at all (FIX: correct the related[] slug)
  out-of-scope— target outside the indexed roots (e.g. src/), expected; not a defect
"""
import sys, json, html, tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("render.py requires PyYAML (pip install pyyaml)")

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(tempfile.gettempdir()) / "knowledge-graph.html"
SCOPE = ("docs/", ".research/")  # roots the index scans; refs elsewhere are out-of-scope by design

terse_path = ROOT / "docs/knowledge-index.yaml"
detail_path = ROOT / "docs/knowledge-index-detail.yaml"
if not terse_path.exists():
    sys.exit(f"no knowledge index at {terse_path} — run /research-pipeline:knowledge-index first")
terse = yaml.safe_load(terse_path.read_text())
detail = yaml.safe_load(detail_path.read_text()) if detail_path.exists() else {"documents": {}}

nodes = {}
for e in terse.get("documents", []):
    p = e["path"]
    nodes[p] = {"title": e.get("title") or p.rsplit("/", 1)[-1], "type": e.get("type") or "?",
                "kind": e.get("kind") or "?", "nav": e.get("nav_priority") == "high",
                "summary": "", "superseded": False}

def group_of(path):
    if path.startswith(".research/programs/"): return "prog:" + path.split("/")[2]
    if path.startswith(".research/briefs/"): return "brief:" + path.split("/")[2]
    if path.startswith(".research/"): return "research-other"
    if path.startswith("docs/architecture/history"): return "history"
    if path.startswith("docs/architecture"): return "architecture"
    parts = path.split("/"); return "/".join(parts[:2]) if len(parts) > 1 else parts[0]

# --- semantic edges (related[]) + supersession from detail ---
edges, dangling, seen = [], [], set()
for p, entry in detail.get("documents", {}).items():
    if not isinstance(entry, dict): continue
    if p in nodes:
        nodes[p]["summary"] = (entry.get("summary") or "").strip()[:280]
        if entry.get("supersession_note"): nodes[p]["superseded"] = True
    for r in entry.get("related") or []:
        if not isinstance(r, dict): continue
        tgt, rel = r.get("slug"), (r.get("relationship") or "related").strip()
        if not tgt or (p, tgt, rel) in seen: continue
        seen.add((p, tgt, rel))
        dgl = tgt not in nodes
        if dgl: dangling.append({"source": p, "target": tgt, "rel": rel})
        edges.append({"source": p, "target": tgt, "rel": rel, "kind": "related", "dangling": dgl})

# --- directory-containment edges: connect each research subtree's root (super-parent.md /
#     parent.md) to the other docs beneath it. Kills false-positive "orphans" for sub-docs
#     that are structurally children but carry no explicit related[]. ---
def subtree_root(path):
    # the program/brief container directory, e.g. .research/programs/<X> or .research/briefs/<X>
    if path.startswith(".research/programs/"):
        return "/".join(path.split("/")[:3])
    if path.startswith(".research/briefs/"):
        return "/".join(path.split("/")[:3])
    return None
roots = {}  # container dir -> root doc path (super-parent.md preferred, else parent.md)
for p in nodes:
    base = subtree_root(p)
    if not base: continue
    name = p.split("/")[-1]
    if name == "super-parent.md" or (name == "parent.md" and base not in roots):
        roots[base] = p
cont_seen = set()
for p in nodes:
    base = subtree_root(p)
    if not base or base not in roots: continue
    root = roots[base]
    if p == root: continue
    key = (root, p)
    if key in cont_seen: continue
    cont_seen.add(key)
    edges.append({"source": root, "target": p, "rel": "contains", "kind": "containment", "dangling": False})

def classify(tgt):
    if not tgt.startswith(SCOPE): return "out-of-scope"
    return "unindexed" if (ROOT / tgt).exists() else "broken"
dcls = {"out-of-scope": [], "unindexed": [], "broken": []}
for d in dangling:
    dcls[classify(d["target"])].append(d)

deg = {p: 0 for p in nodes}
for e in edges:
    if e["source"] in deg: deg[e["source"]] += 1
    if e["target"] in deg: deg[e["target"]] += 1
orphans = sorted(p for p, d in deg.items() if d == 0)
orphan_groups = {}
for o in orphans: orphan_groups.setdefault(group_of(o), []).append(o)

groups = sorted({group_of(p) for p in nodes})
palette = ["#4e79a7","#f28e2b","#e15759","#76b7b2","#59a14f","#edc948","#b07aa1","#ff9da7",
           "#9c755f","#bab0ac","#86bcb6","#d37295","#a0cbe8","#8cd17d","#499894","#79706e",
           "#fabfd2","#d4a6c8","#b6992d","#d7660e","#5b8ff9","#61ddaa","#f6bd16","#7262fd"]
gcolor = {g: palette[i % len(palette)] for i, g in enumerate(groups)}

cy_nodes = [{"data": {"id": p, "label": nodes[p]["title"], "group": group_of(p),
    "type": nodes[p]["type"], "kind": nodes[p]["kind"], "deg": deg[p], "nav": nodes[p]["nav"],
    "superseded": nodes[p]["superseded"], "orphan": deg[p] == 0,
    "summary": nodes[p]["summary"], "color": gcolor[group_of(p)]}} for p in nodes]
ghost = {d["target"] for d in dangling}
gclass = {t: classify(t) for t in ghost}
gcol = {"out-of-scope": "#888", "unindexed": "#ff9f1c", "broken": "#ff0033"}
for g in ghost:
    cy_nodes.append({"data": {"id": g, "label": g.rsplit("/",1)[-1], "group": "GHOST", "type": "?",
        "kind": "?", "deg": 0, "nav": False, "superseded": False, "orphan": False, "ghost": True,
        "summary": "(not in index — " + gclass[g] + ")", "color": gcol[gclass[g]]}})
cy_edges = [{"data": {"source": e["source"], "target": e["target"], "rel": e["rel"],
    "ekind": e["kind"], "dclass": (gclass.get(e["target"]) if e["dangling"] else "")}} for e in edges]

qa = {"unindexed": sorted({d["target"] for d in dcls["unindexed"]}),
      "broken": sorted({d["target"] for d in dcls["broken"]}),
      "out_of_scope": sorted({d["target"] for d in dcls["out-of-scope"]}),
      "orphans": orphan_groups, "superseded": sorted(p for p in nodes if nodes[p]["superseded"])}
stats = {"nodes": len(nodes), "related": sum(1 for e in edges if e["kind"] == "related"),
         "containment": sum(1 for e in edges if e["kind"] == "containment"), "groups": len(groups),
         "orphans": len(orphans), "unindexed": len(qa["unindexed"]), "broken": len(qa["broken"]),
         "oos": len(qa["out_of_scope"]), "superseded": len(qa["superseded"])}

legend = "".join(f'<span class="lg"><i style="background:{gcolor[g]}"></i>{html.escape(g)}</span>' for g in groups)
data_json = json.dumps({"nodes": cy_nodes, "edges": cy_edges, "qa": qa})

TEMPLATE = (Path(__file__).parent / "template.html").read_text()
rep = {"__ROOT__": html.escape(ROOT.name), "__N__": stats["nodes"], "__RE__": stats["related"],
       "__CE__": stats["containment"], "__G__": stats["groups"], "__U__": stats["unindexed"],
       "__B__": stats["broken"], "__OOS__": stats["oos"], "__O__": stats["orphans"],
       "__SUP__": stats["superseded"], "__UCLS__": "warn" if stats["unindexed"] else "ok",
       "__BCLS__": "bad" if stats["broken"] else "ok",
       "__GOPTS__": "".join(f'<option value="{html.escape(g)}">{html.escape(g)}</option>' for g in groups),
       "__LEGEND__": legend, "__DATA__": data_json}
out = TEMPLATE
for k, v in rep.items(): out = out.replace(k, str(v))
OUT.write_text(out)

print(f"nodes={stats['nodes']} related_edges={stats['related']} containment_edges={stats['containment']} groups={stats['groups']}")
print(f"QA: unindexed={stats['unindexed']} broken={stats['broken']} out-of-scope={stats['oos']} "
      f"orphans={stats['orphans']} superseded={stats['superseded']}")
print(f"wrote {OUT}")
if qa["unindexed"]: print("  UNINDEXED (on disk, fix index):", ", ".join(qa["unindexed"][:8]))
if qa["broken"]: print("  BROKEN refs:", ", ".join(qa["broken"][:8]))
