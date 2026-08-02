---
id: feature-cross-host-model-defaults-2026-08
kind: feature
stage: review
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
cross-model workflow work symmetrically when Claude Code, Codex, or Pi is the
driver. Pi must support at least Z.AI GLM and Kimi as driver lineages. Remove
stale Claude-only skill metadata from portable Research Pipeline
skills, route concrete model choices through Agile Workflow's shared model
matrix, and make peer-readiness diagnostics validate the opposite host rather
than assuming Codex is always the peer.

This is related to, but does not absorb,
`cross-model-review-prompt-ware`: that backlog item decides when foundational
prompt-ware should trigger review; this feature decides how an already-required
peer is selected.

## Acceptance

- Claude-driven workflows select an explicit non-Claude peer; Codex-driven
  workflows select an explicit non-OpenAI peer; Pi-driven GLM or Kimi workflows
  select an explicit different-lineage peer appropriate to the role.
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
- Driver defaults are documented for Claude, Codex, and Pi without pretending
  that identically named effort levels are equivalent across providers.

## Simplification opportunities

- Consolidate concrete model mappings in one shared reference instead of
  maintaining a second Claude-only role table in Research Pipeline.
- Replace repeated host-specific advisory wording with one shared policy link.
- Remove portable frontmatter keys that only one harness understands.

## Design decisions

- **Driver selection**: Skills inherit the interactive host/session model. They
  do not force Claude, Codex, GLM, or Kimi as the driver.
- **Peer selection**: Concrete peer model and effort are resolved explicitly
  from Agile Workflow's host-to-peer matrix whenever cross-model work is
  required.
- **Unknown hook host**: The preflight remains silent rather than guessing and
  warning about the wrong peer.
- **Pi boundary**: Pi consumes portable skills through the existing plugin
  bridge. Claude/Codex-specific hooks remain absent in Pi, so peer readiness is
  checked when delegation is attempted rather than at SessionStart.
- **Kimi peer scope**: Kimi is supported as a Pi driver. It is not advertised as
  a peeragent target until peeragent gains a Kimi adapter.
- **Installed-peer detection**: Recognize a PATH override or an enabled plugin
  in the host's standard installation registry; do not require a global
  `peeragent` executable.

## Architectural choice

Use the existing Agile Workflow model matrix as the single source of truth and
make Research Pipeline consume it by role. Extend the matrix with Pi/Kimi driver
semantics while preserving the existing GLM card. This preserves the intelligent
defaults already present and limits host-specific logic to adapter boundaries:
native harness settings, the Claude/Codex peer preflight, and peeragent invocation.

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
- `plugins/agile-workflow/skills/principles/references/models.md`

**Interface**: Shared prose names role/capability requirements and delegates
concrete host-to-peer resolution to
`plugins/agile-workflow/skills/principles/references/models.md`.

**Acceptance Criteria**:
- [ ] Neither advisory design skill assumes Claude is the host.
- [ ] Research Pipeline does not maintain a competing Claude-only model table.
- [ ] The shared matrix covers Pi with both GLM and Kimi as drivers and does not
      claim Kimi is an available peeragent target.

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
- **Pi hook mismatch**: Pi does not consume Claude/Codex plugin hooks. Keep the
  preflight explicitly native-host-only and make delegated peer failure
  non-blocking in portable skills.
- **Plugin registry drift**: Installation registries may move. PATH and explicit
  `PEERAGENT_BIN` remain supported; registry parsing is best-effort and silent.
- **Metadata behavior change**: Removing Claude-only frontmatter can change
  automatic routing. Keep descriptions precise and project Codex policy into
  `agents/openai.yaml`; validate rendered skill inventories where available.

## Implementation notes

- Execution capability: quality-first host tier; the change spans portable
  prompt contracts, native hook behavior, and three driver harnesses.
- Review weight: standard, from the project default.
- Files changed: the shared Agile Workflow model matrix; Research Pipeline's
  model-selection pattern, model-assignment prose, portable skill frontmatter,
  Codex metadata, and peer preflight; repo skill-style scope.
- Tests added: `test_peer_preflight.sh` covers inactive, unknown, missing CLI,
  authenticated, and unauthenticated Claude/Codex paths;
  `skill-portability.test.sh` protects portable frontmatter, Codex policy, and
  GLM/Kimi driver wording.
- Simplification: replaced the 274-line Claude-only model table with a compact
  role vocabulary backed by the shared cross-provider decision matrix.
- Discrepancies from design: Pi 0.83.0 installed successfully, but
  `@nklisch/pi-plugins` 0.2.4 fails its macOS/APFS lock-capability probe before
  plugin activation. Pi can drive after provider login, but bridge-backed skill
  activation awaits the upstream fix.
- Adjacent issues parked: `idea-pi-plugin-apfs-lock-probe`.
- Machine setup: Claude peeragent updated from 0.2.4 to 0.5.1; Pi 0.83.0 and
  `@nklisch/pi-plugins` 0.2.4 installed. No provider credentials were read or
  stored.

## Verification evidence

- Research Pipeline shell tests: pass (`resolve-agentic-research`, portability,
  peer preflight, session context).
- Research Pipeline Python suite: 19 passed.
- Every Research Pipeline skill passes the system skill validator.
- Every new `agents/openai.yaml` parses and contains typed invocation policy.
- Host-specific model-name scan and `git diff --check`: clean.
