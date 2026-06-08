"""Conformance test for the vendored ARD citation lint.

Run: python3 -m pytest plugins/research-pipeline/scripts/tests/ -q

Asserts the vendored lint-citations.py reproduces ARD's canonical verdicts across
the golden fixtures (all citation statuses + the thin flag + every pattern
category). This is the drift guard: if a future ARD re-sync changes behavior, or
the vendored copy is accidentally edited, this fails. See ard.json.
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
RUN = SCRIPTS / "conformance" / "run.py"


def test_vendored_lint_passes_ard_conformance():
    result = subprocess.run(
        [sys.executable, str(RUN)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        "vendored citation lint failed ARD conformance — the vendored copy may have "
        f"drifted or been edited (pin, don't fork):\n{result.stdout}\n{result.stderr}"
    )
    assert "conformance:" in result.stdout, result.stdout
