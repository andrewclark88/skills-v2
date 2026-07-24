from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "validate-workbench.py"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class ValidateWorkbenchTests(unittest.TestCase):
    def make_project(self) -> Path:
        root = Path(tempfile.mkdtemp())
        write(
            root / ".work/CONVENTIONS.md",
            "---\nowner: workbench\nschema: 1\ncompleted_items: summarize\n---\n",
        )
        for directory in ("active", "backlog", "completed", "releases"):
            (root / ".work" / directory).mkdir(parents=True, exist_ok=True)
            write(root / ".work" / directory / ".gitkeep", "")
        write(
            root / "AGENTS.md",
            "<!-- workbench:start -->\n## Workbench\n<!-- workbench:end -->\n",
        )
        write(
            root / ".work/active/example.md",
            """---
id: example
kind: feature
status: active
tags: [test]
parent: null
blocked_by: []
related_to: []
research_refs: []
mock_refs: []
created: 2026-07-24
updated: 2026-07-24
---

# Example
""",
        )
        return root

    def run_validator(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_project_passes(self) -> None:
        result = self.run_validator(self.make_project())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("validation passed", result.stdout)

    def test_unresolved_dependency_fails(self) -> None:
        root = self.make_project()
        path = root / ".work/active/example.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "blocked_by: []", "blocked_by: [missing]"
            ),
            encoding="utf-8",
        )
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unresolved blocked_by target missing", result.stdout)

    def test_completed_item_cannot_satisfy_active_relationship(self) -> None:
        root = self.make_project()
        write(
            root / ".work/completed/finished.md",
            "---\nid: finished\ncompleted: 2026-07-24\n---\n",
        )
        path = root / ".work/active/example.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "related_to: []", "related_to: [finished]"
            ),
            encoding="utf-8",
        )
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unresolved related_to target finished", result.stdout)

    def test_duplicate_id_across_states_fails(self) -> None:
        root = self.make_project()
        write(
            root / ".work/backlog/example.md",
            "---\nid: example\ntags: []\ncreated: 2026-07-24\nupdated: 2026-07-24\n---\n",
        )
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate id example", result.stdout)

    def test_unresolved_mock_ref_fails(self) -> None:
        root = self.make_project()
        path = root / ".work/active/example.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "mock_refs: []", "mock_refs: [.mockups/example/index.html]"
            ),
            encoding="utf-8",
        )
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unresolved mock ref", result.stdout)

    def test_scan_is_a_tag_not_a_kind(self) -> None:
        root = self.make_project()
        path = root / ".work/active/example.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "kind: feature", "kind: scan"
            ),
            encoding="utf-8",
        )
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid kind 'scan'", result.stdout)

    def test_legacy_substrate_fails(self) -> None:
        root = self.make_project()
        (root / ".work/bin").mkdir()
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("superseded workflow path remains", result.stdout)

    def test_nested_work_directory_fails(self) -> None:
        root = self.make_project()
        (root / ".work/active/phases").mkdir()
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("noncanonical nested work directory", result.stdout)

    def test_gitkeep_is_required_for_clone_stability(self) -> None:
        root = self.make_project()
        (root / ".work/backlog/.gitkeep").unlink()
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing .work/backlog/.gitkeep", result.stdout)

    def test_blocked_item_requires_blocker_evidence(self) -> None:
        root = self.make_project()
        path = root / ".work/active/example.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "status: active", "status: blocked"
            ),
            encoding="utf-8",
        )
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("blocked status requires", result.stdout)

    def test_external_blocker_section_is_valid(self) -> None:
        root = self.make_project()
        path = root / ".work/active/example.md"
        text = path.read_text(encoding="utf-8").replace(
            "status: active", "status: blocked"
        )
        path.write_text(
            text + "\n## Blocker\n\nWaiting for vendor credentials; unblocks on receipt.\n",
            encoding="utf-8",
        )
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unrecognized_root_work_directory_fails(self) -> None:
        root = self.make_project()
        (root / ".work/planning").mkdir()
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("noncanonical work directory", result.stdout)


if __name__ == "__main__":
    unittest.main()
