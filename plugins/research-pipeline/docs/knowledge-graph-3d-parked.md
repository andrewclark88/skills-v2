---
description: "Parked: 3D knowledge-graph view — why it was reverted and the lead to pick up next time."
type: backlog
kind: historical
status: parked
updated: 2026-05-29
---

# Parked: knowledge-graph 3D view

A 3D view (`3d-force-graph` / three.js, `render.py --3d`) with a kind-layered vertical axis was
built and shipped (PRs #17, #18) but **reverted** because it rendered no visible nodes — UI chrome
and the layer legend appeared, but the WebGL canvas stayed empty in real browsers and in headless.

**The lead (verified, worth resuming from):** a *minimal* `3d-force-graph` page — 5 hardcoded nodes
with `fy` set in the node objects, `controlType:'orbit'`, and `onEngineStop(()=>zoomToFit())` —
**renders correctly** (colored spheres in stacked y-layers with edges). The full 485-node template
did **not**, even after removing the auto-spin loop (which was a real bug — it hijacked the camera
every frame) and shortening `cooldownTime`. So the remaining difference is in the full template's
init path, most likely one of:

- `fy` is assigned via `applyZ()` *after* `graphData(...)` + `d3ReheatSimulation()`, rather than
  baked into the node objects before `graphData` (the minimal does the latter). **Try precomputing
  `fy` on the node objects first, like the minimal, then layer the selectable-axis on top.**
- node/link scale (485 / 3011) + the per-node accessors (`nodeLabel`, `linkVisibility`, etc.)
  interacting with the layout — bisect by adding them back one at a time onto the working minimal.

**Next step:** start from the known-good minimal and add real DATA → fy-in-objects → accessors →
selectable axis, screenshotting at each step (headless Chrome `--screenshot`, then inspect center
pixels). Don't rely on headless console logs — force-graph's perpetual render loop keeps the page
from flushing stderr.

The 2D cytoscape view (the supported renderer) is unaffected and remains the QA/audit surface.
