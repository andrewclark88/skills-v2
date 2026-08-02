#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
plugin_root=$(CDPATH= cd -- "$script_dir/../.." && pwd)

python3 - "$plugin_root" <<'PY'
from pathlib import Path
import sys
import yaml

root = Path(sys.argv[1])
allowed = {"name", "description"}

for skill in sorted((root / "skills").glob("*/SKILL.md")):
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"{skill}: missing YAML frontmatter")
    frontmatter = text.split("---\n", 2)[1]
    keys = {
        line.split(":", 1)[0]
        for line in frontmatter.splitlines()
        if line and not line[0].isspace() and ":" in line
    }
    unexpected = keys - allowed
    if unexpected:
        raise AssertionError(f"{skill}: non-portable keys {sorted(unexpected)}")

for skill_name in (
    "architecture",
    "doc-review",
    "engineering-principles",
    "epic-design",
    "epicize",
    "expand",
    "feature-design",
    "ideate",
    "init-project",
    "quality-checkpoint",
    "security-review",
    "test-quality",
    "update-documentation",
    "update-epicize",
):
    metadata = root / "skills" / skill_name / "agents" / "openai.yaml"
    document = yaml.safe_load(metadata.read_text(encoding="utf-8"))
    prompt = document.get("interface", {}).get("default_prompt")
    if not isinstance(prompt, str) or f"${skill_name}" not in prompt:
        raise AssertionError(f"{metadata}: default prompt does not name the skill")
    policy = document.get("policy", {}).get("allow_implicit_invocation")
    if not isinstance(policy, bool):
        raise AssertionError(f"{metadata}: invocation policy must be a boolean")

    expected = skill_name != "expand"
    if policy is not expected:
        raise AssertionError(
            f"{metadata}: invocation policy is {policy!r}, expected {expected!r}"
        )
PY

if grep -q 'host Claude.*Codex' \
  "$plugin_root/skills/feature-design/SKILL.md" \
  "$plugin_root/skills/epic-design/SKILL.md"; then
  printf '%s\n' 'design skill assumes Claude is the driver' >&2
  exit 1
fi

grep -q 'GLM/Kimi Pi host' "$plugin_root/skills/feature-design/SKILL.md"
grep -q 'GLM/Kimi Pi host' "$plugin_root/skills/epic-design/SKILL.md"
grep -q 'Kimi (Moonshot; Pi-native driver)' \
  "$plugin_root/../agile-workflow/skills/principles/references/models.md"

printf '%s\n' 'research-pipeline skill portability: ok'
