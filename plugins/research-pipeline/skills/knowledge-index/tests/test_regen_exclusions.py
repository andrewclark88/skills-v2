"""Tests for regen.py discovery exclusions.

Run: python3 -m pytest plugins/research-pipeline/skills/knowledge-index/tests/ -q

Builds a throwaway project tree in a tmp dir so the test runs anywhere — no
dependency on real project corpora.
"""
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent
REGEN = HERE.parent / "regen.py"


def _write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _run(root: Path):
    return subprocess.run(
        [sys.executable, str(REGEN), str(root)],
        capture_output=True, text=True,
    )


def _build_project(root: Path):
    # A normal docs/ file — should be indexed.
    _write(root / "docs" / "north-star.md",
           "---\ndescription: vision\ntype: north-star\nupdated: 2026-06-08\n"
           "decisions:\n  - ship it\n---\n\n# North Star\n")
    # A legacy pipeline brief — should remain indexed during coexistence.
    _write(root / ".research" / "briefs" / "auth-providers" / "parent.md",
           "---\ndescription: auth research\ntype: brief\nupdated: 2026-06-08\n"
           "key_findings:\n  - use oauth\n---\n\n# Auth Providers\n")
    # A current Agentic Research analysis artifact uses the ARD schema rather
    # than docs-style description/type fields. It must still be discoverable.
    _write(root / ".research" / "analysis" / "positions" / "auth-direction.md",
           "---\nslug: auth-direction\nprovenance: agent-synthesis\nupdated: 2026-08-01\n"
           "---\n\n# Authentication direction\n")
    # ARD source-record tiers — must be EXCLUDED (non-docs frontmatter schema).
    _write(root / ".research" / "attestation" / "rfc6749.md",
           "---\nsource_handle: rfc6749\nfetched: 2026-06-08\n"
           "source_url: https://www.rfc-editor.org/rfc/rfc6749\nprovenance: fetched\n---\n\n"
           "## Section 1\n> the OAuth 2.0 authorization framework\n")
    _write(root / ".research" / "reference" / "rfcs" / "INDEX.md",
           "# RFC corpus\n\n1. rfc6749 — OAuth 2.0\n")
    _write(root / ".research" / "precis" / "rfc6749.md",
           "---\nsource_handle: rfc6749\n---\n\n# Precis\n")
    _write(root / ".research" / ".import-holding" / "old-auth.md",
           "---\nimport_origin: inferred-from-legacy\n---\n\n# Old auth research\n")
    _write(root / ".research" / "CONVENTIONS.md", "# Research conventions\n")


def _index_paths(root: Path):
    idx = yaml.safe_load((root / "docs" / "knowledge-index.yaml").read_text())
    return [d["path"] for d in (idx.get("documents") or [])]


def test_source_tiers_excluded_from_index(tmp_path):
    _build_project(tmp_path)
    result = _run(tmp_path)
    assert result.returncode == 0, f"regen failed:\n{result.stdout}\n{result.stderr}"

    paths = _index_paths(tmp_path)
    # Analysis-tier brief and the normal doc ARE indexed.
    assert any("briefs/auth-providers/parent.md" in p for p in paths), paths
    assert any("analysis/positions/auth-direction.md" in p for p in paths), paths
    assert any("north-star.md" in p for p in paths), paths
    # ARD source tiers are NOT indexed.
    assert not any("/attestation/" in p for p in paths), paths
    assert not any("/reference/" in p for p in paths), paths
    assert not any("/precis/" in p for p in paths), paths
    assert not any("/.import-holding/" in p for p in paths), paths
    assert ".research/CONVENTIONS.md" not in paths


def test_agentic_analysis_requires_only_ard_provenance(tmp_path):
    _build_project(tmp_path)
    result = _run(tmp_path)
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    assert "analysis/positions/auth-direction.md: missing required field" not in combined


def test_attestation_does_not_trip_docs_lint(tmp_path):
    # An attestation lacks description/type/updated; if it were discovered it would
    # raise "missing required field" lint errors. Excluding it keeps the lint clean.
    _build_project(tmp_path)
    result = _run(tmp_path)
    combined = result.stdout + result.stderr
    assert "attestation/rfc6749.md" not in combined, combined
    assert "missing required field" not in combined, combined


def test_oversized_navigator_fails_generation(tmp_path):
    _build_project(tmp_path)
    # Explicit load-bearing entries are the only unbounded navigator section.
    # Generate enough legitimate docs to cross the 10KB contract.
    for i in range(90):
        _write(tmp_path / "docs" / f"load-bearing-{i:03}.md",
               "---\n"
               f"description: {'x' * 120}{i}\n"
               "type: north-star\n"
               "updated: 2026-08-01\n"
               "nav_priority: high\n"
               "decisions:\n  - retain this document\n"
               "---\n\n"
               f"# Load-bearing document {'x' * 80}{i}\n")
    result = _run(tmp_path)
    assert result.returncode != 0
    assert "EXCEEDS 10KB" in result.stdout
