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
    # A normal analysis-tier brief — should be indexed.
    _write(root / ".research" / "briefs" / "auth-providers" / "parent.md",
           "---\ndescription: auth research\ntype: brief\nupdated: 2026-06-08\n"
           "key_findings:\n  - use oauth\n---\n\n# Auth Providers\n")
    # ARD source-record tiers — must be EXCLUDED (non-docs frontmatter schema).
    _write(root / ".research" / "attestation" / "rfc6749.md",
           "---\nsource_handle: rfc6749\nfetched: 2026-06-08\n"
           "source_url: https://www.rfc-editor.org/rfc/rfc6749\nprovenance: fetched\n---\n\n"
           "## Section 1\n> the OAuth 2.0 authorization framework\n")
    _write(root / ".research" / "reference" / "rfcs" / "INDEX.md",
           "# RFC corpus\n\n1. rfc6749 — OAuth 2.0\n")
    _write(root / ".research" / "precis" / "rfc6749.md",
           "---\nsource_handle: rfc6749\n---\n\n# Precis\n")


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
    assert any("north-star.md" in p for p in paths), paths
    # ARD source tiers are NOT indexed.
    assert not any("/attestation/" in p for p in paths), paths
    assert not any("/reference/" in p for p in paths), paths
    assert not any("/precis/" in p for p in paths), paths


def test_attestation_does_not_trip_docs_lint(tmp_path):
    # An attestation lacks description/type/updated; if it were discovered it would
    # raise "missing required field" lint errors. Excluding it keeps the lint clean.
    _build_project(tmp_path)
    result = _run(tmp_path)
    combined = result.stdout + result.stderr
    assert "attestation/rfc6749.md" not in combined, combined
    assert "missing required field" not in combined, combined
