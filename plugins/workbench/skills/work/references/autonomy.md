# Autonomy and Authority

Resolve one effective autonomy posture from the user's current request, then
`.work/CONVENTIONS.md`, then `adaptive`. Current explicit intent overrides the
repository default.

Semantic request signals:

- “help me think,” “design this with me,” “explore options,” or “grill me” →
  `collaborative`;
- “implement this,” “fix this,” or another bounded delivery request →
  `adaptive`;
- “handle this end to end,” “drive these epics to done,” “finish,” or “do not
  stop” → `autonomous` inside the named boundary;
- a question, explanation, diagnosis, or review remains read-only unless the
  user also requests change.

## Postures

- **Collaborative** — discuss ideal states as well as appropriately scoped
  options. Surface consequential alternatives, trade-offs, and long-term
  direction before binding the design.
- **Adaptive** — ask about consequential human-owned choices; resolve routine,
  reversible decisions with judgment. Escalate when an ideal state materially
  changes scope, product direction, or an external contract.
- **Autonomous** — choose and deliver the strongest maintainable solution
  inside the authorized outcome. Prefer coherent, durable structure over a
  smaller patch that creates foreseeable debt. Park worthwhile improvements
  that exceed the boundary.

Autonomy changes participation and continuation, not quality, permissions, or
scope. Every posture still pauses for missing product direction, material scope
expansion, production or real-data action, irreversible change, credentials,
external coordination, or authority the user has not granted.

## Durable simplicity

Prefer the simplest coherent design that reaches a maintainable intended state.
Measure simplicity in durable concepts, operating cost, and verification cost,
not diff size.

Do not choose a hack merely because it touches fewer files. Use a workaround
only when scope, time, compatibility, missing authority, or another real
constraint requires it. Record the constraint, consequence, and better future
direction.

In collaborative work, discuss the ideal state and the appropriately scoped
option before the user chooses. In adaptive work, recommend the ideal state
when it materially affects the current decision. In autonomous work, implement
the durable solution when it fits the authorized outcome without silently
expanding that outcome.
