"""Tests for the knowledge-graph v2 renderer (the DATA-contract adapter).

Run: python3 -m pytest plugins/research-pipeline/skills/knowledge-graph/tests/ -q

These exercise render.py against a small portable fixture (tests/fixtures/proj) so they run
anywhere — no dependency on ~/dev project corpora.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
RENDER = HERE.parent / "render.py"
FIXTURE = HERE / "fixtures" / "proj"


def data(*extra_flags):
    out = subprocess.run([sys.executable, str(RENDER), str(FIXTURE), "--print-data", *extra_flags],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def by_id(d):
    return {n["id"]: n for n in d["nodes"]}


def test_top_level_shape():
    d = data()
    assert set(d) == {"meta", "nodes", "ghosts", "edges", "adjacency", "qa", "groups", "stats"}
    assert d["meta"]["root"] == "proj"
    assert d["meta"]["root_abs"].endswith("proj")
    assert d["stats"]["nodes"] == 6


def test_node_contract_keys():
    d = data()
    need = {"id", "label", "group", "kind", "type", "status", "nav", "deg", "indeg", "outdeg",
            "orphan", "superseded", "supersession_note", "summary", "decisions", "key_findings",
            "community", "color", "consumer_hint", "updated"}
    for n in d["nodes"]:
        assert need <= set(n), need - set(n)


def test_detail_layer_merged():
    n = by_id(data())["docs/a.md"]
    assert n["summary"] == "A summary."
    assert n["decisions"] == ["Decision one"]
    assert n["key_findings"] == ["Finding one"]
    assert n["nav"] is True


def test_edge_classification():
    d = data()
    cats = {"reference", "supersession", "containment"}
    for e in d["edges"]:
        assert e["ecat"] in cats, e
    # the superseded-by edge becomes ecat=supersession
    sup = [e for e in d["edges"] if e["source"] == "docs/b.md" and e["target"] == "docs/a.md"]
    assert sup and sup[0]["ecat"] == "supersession"
    # extends stays reference
    ext = [e for e in d["edges"] if e["source"] == "docs/a.md" and e["target"] == "docs/b.md"]
    assert ext and ext[0]["ecat"] == "reference"


def test_containment_edges_from_research_subtree():
    d = data()
    cont = {(e["source"], e["target"]) for e in d["edges"] if e["ecat"] == "containment"}
    root = ".research/programs/x/super-parent.md"
    assert (root, ".research/programs/x/sub1.md") in cont
    assert (root, ".research/programs/x/sub2.md") in cont


def test_degree_matches_adjacency():
    d = data()
    adj = d["adjacency"]
    for n in d["nodes"]:
        assert len(adj[n["id"]]["in"]) == n["indeg"]
        assert len(adj[n["id"]]["out"]) == n["outdeg"]
        assert n["deg"] == n["indeg"] + n["outdeg"]


def test_qa_classification():
    d = data()
    qa = d["qa"]
    assert qa["broken"] == ["docs/missing.md"]
    assert qa["unindexed"] == ["docs/unindexed-on-disk.md"]
    assert qa["out_of_scope"] == ["src/foo.py"]
    assert qa["superseded"] == ["docs/b.md"]
    # c.md is the only node with zero resolved edges
    orphan_paths = [p for v in qa["orphans"].values() for p in v]
    assert orphan_paths == ["docs/c.md"]


def test_ghosts_emitted_for_dangling():
    d = data()
    gids = {g["id"]: g for g in d["ghosts"]}
    assert gids["docs/missing.md"]["dclass"] == "broken"
    assert gids["docs/unindexed-on-disk.md"]["dclass"] == "unindexed"
    assert gids["src/foo.py"]["dclass"] == "out-of-scope"


def test_determinism():
    a = subprocess.run([sys.executable, str(RENDER), str(FIXTURE), "--print-data"],
                       capture_output=True, text=True, check=True).stdout
    b = subprocess.run([sys.executable, str(RENDER), str(FIXTURE), "--print-data"],
                       capture_output=True, text=True, check=True).stdout
    assert a == b


def test_communities_flag():
    base = data()
    assert base["meta"]["has_communities"] is False
    assert all(n["community"] is None for n in base["nodes"])
    withc = data("--communities")
    # fixture has resolved edges, so Louvain runs
    assert withc["meta"]["has_communities"] is True
    assert any(n["community"] is not None for n in withc["nodes"])


def test_html_render_substitutes_all_placeholders(tmp_path):
    out = tmp_path / "kg.html"
    subprocess.run([sys.executable, str(RENDER), str(FIXTURE), str(out)], check=True,
                   capture_output=True, text=True)
    html = out.read_text()
    assert "__DATA__" not in html
    assert "__ROOT__" not in html
    assert "__BUILD_STATS__" not in html
    assert "const DATA =" in html
