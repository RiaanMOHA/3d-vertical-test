# Sinyi experiment — Phase 1 audit prompt (ozu-1)

Paste the block below into a fresh Claude Code window when you're ready to run the audit. It is read-only — Claude Code is told not to change any files. The output is a Markdown report with nine numbered sections.

After the report comes back and you approve it, you'll start a new Phase 2 message that includes the three Sinyi extraction docs.

---

Role: senior three.js engineer doing a read-only audit of this repo.

Stack: vanilla HTML + native browser ESM + three.js r184 (vendored at `vendor/three/`). No React, no bundler, no TypeScript, no JSX. Package manager: npm, single devDep `concurrently`. Dev runtime: `python3 -m http.server 8080`. Node is not used at app runtime. Convention: one HTML file per project with an inlined `<script type="module">`; the canonical entry is `ozu-test.html`. Controls: a custom inlined OrbitControls class inside `ozu-test.html`, plus the vendored official r184 OrbitControls available under `vendor/three/`. Animation: raw `requestAnimationFrame` with hand-rolled easing — no gsap, no framer, no tween lib of any kind.

Mode: Phase 1 — discovery and proposal only. Do not edit, create, run, install, or format any files. Do not start the dev server. Do not run npm. If you feel the urge to write code, stop and add the question to the "Open questions" section instead.

Context: I want to add three features later, modeled on Sinyi DiNDON's 3D viewer. Exact constants, eases, and shader details are out of scope for this phase — they live in three extraction docs I will paste at the start of Phase 2. For now, treat the features as named intents:

  F1. Floorplan ↔ 3D camera transition. A 2D top-down plan view that the user can switch into and out of, with an animated camera fly between the two views.

  F2. In-pano hotspot rings. Floor-level ring meshes at predefined positions inside the house; clicking one moves the camera to that spot. Optional text labels.

  F3. Smooth walk between hotspots. Animated camera translation + yaw alignment between any two hotspots.

Target: the **ozu-1 master plan** (the whole property — exterior + multi-room interior). This is the main scene work inside `ozu-test.html`. F1/F2/F3 are scoped to the ozu-1 scenes; section 6 must pick which scene(s) each feature belongs in.

The **room-1 zone that exists as part of ozu-1's multi-room interior** is in scope (it is part of ozu-1).

Hard exclusions — do not study, modify, propose changes to, or cross-reference findings from:
- the standalone room-1 sandbox `registerScene('room-1', ...)` block inside `ozu-test.html` (this is a separate, locked project that happens to share the file)
- the `room-1-3d/` separate Vite workshop folder
- the `room-1-ONLY-v5-feasibility/` research folder
- the `ozu-test/room-1-ONLY-rendering-plan.md` and `ozu-test/room-1-ONLY-cutting-edge-plan.md` plan docs

`ozu-test.html` holds two parallel projects — ozu-1 (this audit) and the standalone room-1 sandbox (out of scope). Same file, not the same project.

Deliverable: a single Markdown report with exactly these sections, in this order. No code blocks. No implementation. No "I'll start by…" — just findings.

  1. Repo map. Top-level folders and the 5–15 files most relevant to scene, camera, modes, and UI for the ozu-1 scenes. One line each. Note which file is the canonical entry. Identify the line ranges inside `ozu-test.html` for: (a) the ozu-1 exterior block, (b) the ozu-1 multi-room interior block, (c) the standalone room-1 sandbox `registerScene('room-1', ...)` block — only so the boundary is clear; do not propose edits to (c).

  2. Mode-switching pattern. How the existing Exterior / Room 1 / Interior / Lights bar in `ozu-test.html` works today: where state lives (module-scoped variable, dataset attribute, CSS class, etc.), how the bar dispatches, how scene content reacts. The existing "Room 1" chip points at the standalone room-1 sandbox (out of scope) — it must keep working unchanged. Where a new "Plan" mode would slot in for the ozu-1 scenes, and what type of state change it implies — same shape as existing modes, or different (camera-level vs content-level vs both). Also: name the level the new "Plan" mode should live at — a new top-level chip (alongside the existing four, not replacing any of them), or a sub-toggle internal to an ozu-1 scene (content-level switch within one scene), or a hybrid. Pick one and justify in one sentence based on F1's intent.

  3. Geometry (ozu-1 only). For each ozu-1 scene (exterior + multi-room interior): file and variable names of the principal meshes. Origin location in world space. Units (m or cm — check against any explicit dimensions in the source). Y-up or Z-up. Any existing world-space anchors I can reuse for hotspot positions. If geometry differs between exterior and interior, note both.

  4. Camera and controls (ozu-1 only). Per ozu-1 scene: camera type, fov, near/far, initial position and target. Which OrbitControls is actually wired up in the ozu-1 scenes — the inlined custom class or the vendored r184 one. Whether the controls own the camera target or the scene does. Note any custom damping, polar limits, or zoom clamps already set.

  5. Animation stack. Confirm there is no tween library. Identify the existing `requestAnimationFrame` loop used by the ozu-1 scenes (file + approximate location), how it's started/stopped, and any easing helper functions already defined that camera-fly logic could reuse. Note whether the loop is shared with the standalone room-1 sandbox or separate.

  6. Proposal — placement only, no code:
     - Which ozu-1 scene(s) each of F1, F2, F3 belongs in (exterior, interior, or both). Justify in one sentence each.
     - Where the floorplan sprite/plane belongs in the chosen scene's scene graph and which existing variable would parent it.
     - Where hotspot data should live. Given the one-HTML-file convention, options are: (a) a new sibling ES module like `hotspots.js` imported by `ozu-test.html`, (b) inline as a const at the top of the ozu-1 module script, (c) a JSON file fetched at startup. Pick one and justify in one sentence. Propose a schema with field names only — modeled on Sinyi's: `id`, `position`, `rotation`, `bestCameraView`, `visibleHotSpotIds`, `label`. Hotspots are new metadata layered on the existing ozu-1 meshes; geometry is not changing.
     - Where camera-fly tween logic belongs. Given there are no React hooks and no manager classes, the honest options are: (a) a plain function inside the existing ozu-1 module script, (b) a small new ES module under a new `lib/` or `vendor/`-adjacent path imported by the HTML. Pick one and justify in one sentence based on what's already in the repo.

  7. Files to create / files to modify. Two bullet lists, paths only, one-line reason each. Default assumption: new code lands inside the ozu-1 blocks in `ozu-test.html` unless there's a strong reason to split into a separate ES module — if you propose a split, name the reason. Hard exclude: do not propose edits to the standalone room-1 sandbox block, `room-1-3d/`, or any `room-1-ONLY-*` folder/doc.

  8. Conflicts.
     - Code conflicts. Specific things in the existing Exterior / Room 1 / Interior / Lights pattern, the inlined custom OrbitControls, or the existing rAF loop that the new "Plan" mode, hotspot system, or camera-fly tween would step on. The smallest reconciliation for each. Required — at least name the candidates even if you conclude "no conflict." Also required: confirm the existing "Room 1" chip → standalone room-1 sandbox flow keeps working unchanged.
     - Plan conflicts. Read `ozu-test/master-plan.md`. Name any phase, milestone, or commitment in that doc that F1/F2/F3 would supersede, duplicate, or reorder, and propose the smallest reconciliation for each. Do not consider the `room-1-ONLY-*.md` plans — they are out of scope.

  9. Open questions. Anything you would need from me before Phase 2.

Stop after section 9. Wait for my approval before any code.
