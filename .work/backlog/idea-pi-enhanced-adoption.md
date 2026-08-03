---
id: idea-pi-enhanced-adoption
created: 2026-08-02
updated: 2026-08-02
tags: [pi, plugins, models, workflow, security, upstream]
---

Resume the investigation into adopting Nathan Klisch's `@nklisch/pi-enhanced`
as the third driver harness for skills-v2, especially for Z.AI GLM and Kimi.
This is related to, but broader than,
`idea-pi-plugin-apfs-lock-probe`: the lock probe blocks plugin loading; this
capture preserves the harness, model-mode, safety, and peer-review findings.

## Operator context

- Andrew has Claude and Codex subscriptions and wants either host to drive while
  the other performs cross-model review.
- A friend supplied authorized GLM 5.2 and Kimi API keys for experimentation and
  recommended `pi-enhanced`, `pi-model-modes`, and Clearance.
- Claude authentication was refreshed successfully on 2026-08-02.
- Do not record provider keys in the repository, chat, or shell history; enter
  them through Pi's interactive `/login` flow.

## Verified local state

- Project: `/Users/andrewclark/dev/skills-v2`.
- Pi `0.83.0` is installed.
- Pi currently lists only `npm:@nklisch/pi-plugins`; no default provider,
  model, or thinking level is configured.
- Installed `@nklisch/pi-plugins` is `0.2.4` and fails its Darwin filesystem-lock
  capability probe before `/plugins` becomes available. See the related parked
  item for the exact `statfs` evidence.
- The completed cross-host defaults feature is archived at
  `.work/archive/feature-cross-host-model-defaults-2026-08.md`; its full body is
  recoverable from Git ref `c3795a52`.

## Source findings

- `pi-enhanced` is a one-install bundle containing Clearance, the `pi-plugins`
  Claude/Codex-compatible marketplace, subagents, background tasks,
  `pi-model-modes`, research/search tools, and UX extensions. It deliberately
  does not configure personal API keys, provider/model defaults, theme, or
  editor bindings.
  - https://github.com/nklisch/pi-extensions/tree/main/packages/pi-enhanced
- Published `@nklisch/pi-enhanced@0.1.1` bundles
  `@nklisch/pi-plugins@0.1.21`. Inspection of the published tarball found the
  same Darwin filesystem allowlist and failure message as the installed bridge,
  so the bundle does not currently solve the local lock-probe blocker and would
  replace the newer standalone bridge with an older affected copy.
- `pi-model-modes` is a behavioral prompt layer, not a model/effort selector.
  It composes base voice plus agency, quality, scope, and modifiers; provider,
  model, and thinking level remain separate Pi settings. It transforms the main
  session prompt while preserving tools, skills, project context, date, and cwd.
  Specialist subagent definitions are appended later and win conflicts.
  - https://github.com/nklisch/pi-extensions/tree/main/packages/pi-model-modes
- The durable default recommendation during evaluation was `none` for
  workflow-bound skills-v2 sessions, with explicit experiments such as
  `extend` for implementation, `create` for greenfield work, `methodical` for
  narrow careful work, and `explore` for read-only investigation/review.
- Clearance structurally classifies calls into allow, review, or deny. Its
  global `off | ask | auto` mode changes only the review bucket; the sealed deny
  floor remains active even when Clearance is off. `/clearance tune` can use
  captured history, replay, and adversarial checks to propose static rules, but
  writes require explicit approval.
  - https://github.com/nklisch/pi-extensions/tree/main/packages/pi-clearance
- Clearance is marked work-in-progress. Its README says unknown tools default
  to review, while current configuration documentation and source resolve an
  omitted `unknownToolPosture` to `allow`. The conservative evaluation posture
  is therefore explicit `unknownToolPosture: "review"`, mode `ask`, and project
  scope before considering `auto`.
- Clearance's model reviewer authorizes an uncertain tool call; it is not the
  substantive cross-model reviewer supplied by peeragent.

## Cross-model implications

- The existing provider-relative model/effort matrix remains useful.
  `pi-model-modes` adds a separate behavioral-mode dimension rather than
  replacing driver model or effort defaults.
- Intended peers remain Claude driver to Codex, Codex driver to Claude, and
  GLM/Kimi Pi driver to Claude or Codex once plugin-backed workflows operate.
- GLM is available through peeragent's Z.AI adapter. Kimi is currently a Pi
  driver only, not a peeragent target.
- Do not install `pi-enhanced` alongside the standalone `pi-plugins` entry;
  duplicate plugin-manager extension registration should be avoided. If a
  fixed bundle is adopted later, remove the standalone source first.

## Questions to resume with

- Has Nathan released a `pi-enhanced` bundle whose embedded `pi-plugins` fixes
  the Darwin filesystem probe, or provided an unreleased fixed build?
- After the bridge works, can skills-v2 install and exercise Claude/Codex-shaped
  plugins under GLM and Kimi without host-specific path or hook failures?
- Which Pi mode and thinking combinations perform best for implementation,
  design, research, and review under GLM and Kimi?
- Should the shared model matrix document a Pi behavioral-mode column, keeping
  model, reasoning effort, workflow role, and Clearance reviewer selection
  explicitly separate?
