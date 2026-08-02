---
id: feature-cross-host-model-defaults-2026-08
kind: feature
stage: implementing
tags: [claude, codex, workflow, prompt-ware]
parent: null
depends_on: []
release_binding: null
gate_origin: null
created: 2026-08-02
updated: 2026-08-02
---

# Make workflow model defaults host-aware

Preserve the existing role-based model and effort guidance while making every
cross-model workflow work symmetrically when either Claude Code or Codex is the
driver. Remove stale Claude-only skill metadata from portable Research Pipeline
skills, route concrete model choices through Agile Workflow's shared model
matrix, and make peer-readiness diagnostics validate the opposite host rather
than assuming Codex is always the peer.

This is related to, but does not absorb,
`cross-model-review-prompt-ware`: that backlog item decides when foundational
prompt-ware should trigger review; this feature decides how an already-required
peer is selected.

## Acceptance

- Claude-driven workflows select an explicit Codex model and effort appropriate
  to the role; Codex-driven workflows select an explicit Claude model and effort.
- Shared skill prose does not describe Claude as the assumed driver.
- Research Pipeline portable skill frontmatter contains only `name` and
  `description`; Codex invocation policy remains in `agents/openai.yaml`.
- The SessionStart peer preflight detects the active host and checks the
  opposite subscription-backed CLI without producing noise when peer review is
  unavailable by design.
- Tests cover both Claude-to-Codex and Codex-to-Claude readiness paths, including
  missing CLI and unauthenticated CLI behavior.
- The older Claude-only model-selection guidance is replaced by or redirected
  to the shared cross-host decision matrix.

## Simplification opportunities

- Consolidate concrete model mappings in one shared reference instead of
  maintaining a second Claude-only role table in Research Pipeline.
- Replace repeated host-specific advisory wording with one shared policy link.
- Remove portable frontmatter keys that only one harness understands.

## Design decisions

- **Driver selection**: Skills inherit the interactive host/session model. They
  do not force Claude or Codex as the driver.
- **Peer selection**: Concrete peer model and effort are resolved explicitly
  from Agile Workflow's host-to-peer matrix whenever cross-model work is
  required.
- **Unknown hook host**: The preflight remains silent rather than guessing and
  warning about the wrong peer.
- **Installed-peer detection**: Recognize a PATH override or an enabled plugin
  in the host's standard installation registry; do not require a global
  `peeragent` executable.

## Architectural choice

Use the existing Agile Workflow model matrix as the single source of truth and
make Research Pipeline consume it by role. This preserves the intelligent
defaults already present and limits host-specific logic to the adapter boundary:
the peer preflight and peeragent invocation.

Two alternatives were rejected. Keeping parallel Claude and Codex tables in
Research Pipeline would drift as model generations change. Relying on each peer
CLI's global default would be symmetric but nondeterministic and could silently
select a model or effort inappropriate for the review role.

## Implementation Units

### Unit 1: Cross-host model policy consumption

**Files**:
- `plugins/research-pipeline/skills/feature-design/SKILL.md`
- `plugins/research-pipeline/skills/epic-design/SKILL.md`
- `plugins/research-pipeline/docs/model-selection-pattern.md`

**Interface**: Shared prose names role/capability requirements and delegates
concrete host-to-peer resolution to
`plugins/agile-workflow/skills/principles/references/models.md`.

**Acceptance Criteria**:
- [ ] Neither advisory design skill assumes Claude is the host.
- [ ] Research Pipeline does not maintain a competing Claude-only model table.

### Unit 2: Host-aware readiness adapter

**Files**:
- `plugins/research-pipeline/hooks/scripts/session-start-peer-preflight.sh`
- `plugins/research-pipeline/hooks/scripts/test_peer_preflight.sh`

**Interface**:

```text
stdin: SessionStart JSON with model, transcript_path, cwd, hook_event_name
stdout: empty on ready/inactive/unknown; actionable warning on missing peer CLI
        or failed peer authentication
exit: always 0
```

**Acceptance Criteria**:
- [ ] Claude host checks Codex CLI and `codex login status`.
- [ ] Codex host checks Claude CLI and `claude auth status`.
- [ ] Missing, unauthenticated, ready, inactive, and unknown-host cases are
      covered without invoking real CLIs.

### Unit 3: Portable Research Pipeline skill metadata

**Files**:
- `plugins/research-pipeline/skills/*/SKILL.md`
- `plugins/research-pipeline/skills/*/agents/openai.yaml` where explicit Codex
  picker or implicit-invocation metadata is needed

**Interface**: Portable `SKILL.md` frontmatter contains only `name` and
`description`; Codex-specific presentation and invocation policy uses the
standard `agents/openai.yaml` schema.

**Acceptance Criteria**:
- [ ] No Research Pipeline skill frontmatter contains host-only model, effort,
      tool-list, or invocation keys.
- [ ] Existing deliberate manual/implicit routing remains represented in Codex
      metadata where applicable.

## Implementation Order

1. Rewrite the readiness adapter and its fixture tests because host detection is
   the trickiest behavioral unit.
2. Consolidate model-policy prose and advisory routing.
3. Apply the mechanical frontmatter and Codex-metadata projection.
4. Run hook, frontmatter, skill-shape, and cross-host plugin validation.

## Testing

- Shell fixture tests stub `peeragent`, `codex`, and `claude` commands through a
  temporary PATH and assert exact warning/silence behavior.
- Repository scans assert Research Pipeline frontmatter portability and absence
  of stale Claude-driver wording.
- Existing Research Pipeline and marketplace validation suites protect plugin
  shape and host parity.

## Risks

- **Host payload drift**: Claude and Codex hook payloads are similar but not
  identical. Detect from model first, transcript path second, and fail silent.
- **Plugin registry drift**: Installation registries may move. PATH and explicit
  `PEERAGENT_BIN` remain supported; registry parsing is best-effort and silent.
- **Metadata behavior change**: Removing Claude-only frontmatter can change
  automatic routing. Keep descriptions precise and project Codex policy into
  `agents/openai.yaml`; validate rendered skill inventories where available.
