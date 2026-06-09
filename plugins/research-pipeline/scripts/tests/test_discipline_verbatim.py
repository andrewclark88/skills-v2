"""Verbatim guard for the vendored ARD discipline bundle.

Run: python3 -m pytest plugins/research-pipeline/scripts/tests/ -q

The six numbered sections of skills/research-discipline/SKILL.md ARE ARD's
kernel/discipline.md, vendored verbatim — the anti-fabrication floor that gets
inlined into every research-authoring sub-context. ard.json asserts they're
byte-identical to the pinned release; the conformance suite only checks LINT
behavior, not this text. This test makes the verbatim guarantee enforceable: a
stray edit or an unreviewed re-sync that mutates the floor fails CI/local tests.

The deployment WRAPPER above '## 1. Source-bound' is intentionally ours (it names
our orchestrators + paths) and is NOT covered — only the kernel sections are.

On an intentional ARD bump: re-copy the sections verbatim, then update
adopts.discipline_sha256 in ard.json (the failure message prints the command).
"""
import hashlib
import json
import re
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
SKILL = PLUGIN / "skills" / "research-discipline" / "SKILL.md"
ARD = PLUGIN / "ard.json"
SECTION_1 = re.compile(r"^## 1\. Source-bound", re.M)


def _discipline_sections(text: str) -> str:
    """The six numbered sections: from the '## 1. Source-bound' heading to EOF.
    Mirrors `awk '/^## 1\\. Source-bound/{p=1} p'` so the recorded hash is reproducible."""
    m = SECTION_1.search(text)
    assert m, "could not locate '## 1. Source-bound' heading in research-discipline/SKILL.md"
    return text[m.start():]


def test_discipline_sections_match_pinned_hash():
    recorded = json.loads(ARD.read_text())["adopts"]["discipline_sha256"]
    body = _discipline_sections(SKILL.read_text())
    actual = hashlib.sha256(body.encode("utf-8")).hexdigest()
    assert actual == recorded, (
        "research-discipline's six sections drifted from the pinned ARD kernel "
        f"(recorded {recorded[:12]}…, got {actual[:12]}…).\n"
        "If this was an intentional ARD re-sync, update adopts.discipline_sha256 in "
        "ard.json to:\n  " + actual + "\n"
        "Regenerate with: awk '/^## 1\\. Source-bound/{p=1} p' "
        "skills/research-discipline/SKILL.md | shasum -a 256"
    )
