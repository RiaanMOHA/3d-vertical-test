# Flow: room-1 full build, start to finish

> The whole story of how room-1 was built, from raw inputs to current state. Use this when starting a fresh property and you need the end-to-end picture. For just placement work see `flow-room-1-layout.md`. For just look and feel see `flow-room-1-rendering.md`.

## 1. We started with raw inputs

The build began with three kinds of source material on disk before any 3D work happened.

The blueprint PDF of the property landed at `ozu-test/blueprints/ozu-1-blueprint.pdf` (source: CLAUDE.md off-limits-paths list). Then on-site interior panorama photos were organised into one folder per room corner. For room-1 the four corner folders were `corner-ac-entrance`, `corner-ac-window`, `corner-cabinet-entrance`, and `corner-cabinet-window` (source: `ozu-test/interior-images/room-1/` directory listing). Front-facade exterior photos went into `ozu-test/exterior-images/` (source: commit ccd2239 file list).

No code was written in this stage. The inputs were the ground truth that everything later got cross-checked against (source: CLAUDE.md source-of-truth-hierarchy rule).

## 2. We wrote the docs the 3D work would reference

Before any geometry got built, planning artefacts were written down so the 3D work had something to point at.

First the per-room map at `ozu-test/interior-images/room-1/room-map.md` plus a sibling photo index at `room-map-photos.md` (source: directory listing). These named each wall and corner in plain words: window-wall, ac-wall, cabinet-wall, entrance-wall. The naming had to match folder names exactly so chip labels and viewpoint ids would line up later (source: CLAUDE.md naming convention).

Then global coordinates were written at `ozu-test/blueprints/global-coords.md` (source: CLAUDE.md folder map). After that a whole-property master plan was written at `ozu-test/master-plan.md` covering all rooms in phases 1 to 8 (source: CLAUDE.md plans-hierarchy section). A separate room-1 standalone rendering plan was written at `ozu-test/room-1-ONLY-rendering-plan.md` covering the standalone sandbox in phases A to G. A focused cutting-edge sub-plan was written at `ozu-test/room-1-ONLY-cutting-edge-plan.md` for the three live quality issues: pixelation, lighting, real-world textures (source: `room-1-ONLY-cutting-edge-plan.md` problems-we-are-solving section).

The naming convention was strict from the start: chip labels, viewpoint ids, and scene names had to match folder names exactly with no friendly relabeling (source: CLAUDE.md naming section).

## 3. We built room-1 first as a standalone Vite project, versioned v1 through v4

The first 3D build of room-1 lived in its own folder at `room-1-3d/` as a separate project with its own Vite config, and shipped four iterations.

v1 went in with the initial commit ccd2239 on 2026-04-22 as part of "3d-vertical-test project with room-1-3d variant switcher" (source: git short-sha ccd2239). The variant switcher meant several geometry experiments could run side by side under one app.

v2 and v3 were intermediate experiments. A duplicate `room-1-3d-v3/` folder got removed in commit 34c053e (source: git short-sha 34c053e).

Then v4 landed in commit 957810b on 2026-04-22 with a corrected feature-to-wall map (closet on cabinet-wall only, ac unit and frosted window on ac-wall), feel-roomier dimensions (ceiling 2.5 m, walls 0.02 m, fov 70), Polyhaven PBR textures (oak floor, plaster walls and ceiling, dark wood desk and shelf), an openable door as a `THREE.Group` swinging 90 degrees into the room, three-piece door casing, baseboards, and the variant chips were moved out of the room-1 app onto the parent exterior page (source: git short-sha 957810b commit body).

After v4 the standalone folder was retired.

## 4. We dropped the standalone folder and rebuilt room-1 inside ozu-test.html

In commit 4a540b1 the `room-1-3d/` folder was dropped while room-2 was being built with corner viewpoints (source: git short-sha 4a540b1). From that point room-1 lived as a `registerScene('room-1', ...)` block inside `ozu-test.html`, sharing the same HTML file as the exterior facade and the multi-room interior but kept logically separate (source: `ozu-test/room-1-ONLY-rendering-plan.md` scope section, which states ozu-test.html holds two parallel projects and they must never mix).

This "two projects in one file" rule is locked in user memory: the registerScene('room-1') block must not be edited unless the user literally types "room-1" (source: memory file `project_room1_is_separate_project.md`).

## 5. We built the layout next

With the registerScene shell in place, the placement work happened. The full chronological detail is in `flow-room-1-layout.md`. The condensed sequence:

Room bounds were set from the blueprint at `x=[3.60, W], z=[4.50, D]` for the 2F (source: ozu-test.html line 889 and line 1662). Outer wall geometry was unified in commit 0046b8b and split into two layers with cladding inset in commit 4e735e7 (source: git short-shas 0046b8b, 4e735e7). Window openings were defined as numbered ranges in F2_WIN_FRONT and F2_WIN_RIGHT arrays. For room-1 these were the front sliding window (引違 11909) at `a=4.105, b=5.795, y0=1.10, y1=2.00` and the side narrow privacy window (縦すべり 02609) at `a=5.720, b=5.980, y0=1.10, y1=2.00` (source: ozu-test.html lines 1359 and 1371). Walls got cut into 4 segments around each window hole so the glass actually shows what's beyond instead of the wall behind it (source: `room-1-ONLY-rendering-plan.md` glass-and-windows section). Door positions and entrance were placed: bi-fold closet door on the west wall, hinged entrance door on the south wall (source: ozu-test.html lines 1502 and 1507). Furniture was placed by reading the four corner panoramas and matching positions against blueprint dimensions: bed long-side against ac-wall, desk on window-wall, L-shape shelf at corner-cabinet-window, closet against cabinet-wall, coat hook rail near entrance corner (source: `room-1-ONLY-rendering-plan.md` furniture-detail section). A chip-driven viewpoint named `room-1` was registered at camera position `[5.8, 4.1, 4.7]` looking at `[4.0, 3.5, 7.0]` (source: ozu-test.html line 911).

Every furniture placement was anchored to a panorama view, never eyeballed, because the visual source of truth for room-1 is the photos (source: memory file `project_room1_visual_source_of_truth.md`).

## 6. We built the rendering on top of the layout

Once geometry was solid, the look got built in passes. The full chronological detail is in `flow-room-1-rendering.md`. The condensed sequence:

Started with plain `MeshStandardMaterial` flat colours (source: `room-1-ONLY-rendering-plan.md` walls-and-materials section). ACES filmic tone mapping was turned on with exposure 0.55 (originally 0.85 but was washing out, was dropped in a later session). A procedural inside-out coloured cube was baked into a cube-map via `THREE.PMREMGenerator` and used as `scene.environment` for indirect light. Anisotropic filtering was set to `renderer.capabilities.getMaxAnisotropy()` for all PBR textures.

Window-direction directional sun light went in at intensity 0.85 with soft shadows (`shadow.radius = 6`). A cool-tinted fill light went on the cabinet-wall side at intensity 0.22 with no shadows. Walls and ceiling were excluded from shadow casting to prevent x-ray silhouettes bleeding through the thin walls when viewed from outside.

Real refractive glass via `MeshPhysicalMaterial` with transmission went on the sliding window. A frosted variant went on the narrow ac-wall privacy window. Procedural Japanese-suburban backdrop planes were placed outside both windows so the windows had something to look at. Room-1 polish landed in commit 4367d66: closed door, smooth walls, sunlight and shadows, light ceiling (source: git short-sha 4367d66).

Pendant lamps were rebuilt with linen-weave shades, brass hub, visible bulb spheres, off by default with a Lights toggle in the dock (source: `room-1-ONLY-rendering-plan.md` pendant-lamps section).

An `EffectComposer` post-processing pipeline was added: `RenderPass` then `UnrealBloomPass` then `SMAAPass` (source: same, post-processing-pipeline section). The pipeline crashed because the SMAA shader source was missing. The shader source was inlined as a fix in commit 579f287 on a photo-match pass (source: git short-sha 579f287).

Jaggy edges were addressed and Phase 3 textures landed in commit 4756f6e: wood_floor and dark_wood PBR sets at `ozu-test/room-1-textures/` got wired into floor, desk, and beam materials (source: git short-sha 4756f6e and `room-1-ONLY-cutting-edge-plan.md` audit-findings section). The `painted_plaster_wall` PBR set was tried and rejected: too bumpy, walls in the photos are smooth modern paint, walls are now intentionally flat colour (source: `room-1-ONLY-cutting-edge-plan.md` audit-findings section).

## 7. We audited what room-1 v5 should look like before building it

On 2026-05-04 a feasibility audit ran for a future v5 of the standalone room-1 project. The audit was read-only research, no build (source: `room-1-ONLY-v5-feasibility/room-1-ONLY-v5-feasibility-prompt-v1-2026-05-04.md` key-principle section).

It evaluated seven user requests (functional light switch, glass windows, photo match, hard and soft textures, AR, mobile, plus an explicit "no Keyshot" decision) against a proposed cutting-edge stack: Three.js WebGPU renderer, Spark 2.0 splats, three-gpu-pathtracer, Splatter-360 for splat training from panos, WebXR for AR, Polyhaven CC0 for any hand-built PBR (source: same prompt, proposed-cutting-edge-stack table).

A v4 prompt iteration of the audit added explicit verdict definitions, a parallel-variant rule (v5 lives at `src/variants/v5/` as a sibling to v4, never a replacement), a two-machine context (Mac for the audit, separate Linux GPU box for splat training), and chain-effect rules for AR forcing WebGL fallback (source: `room-1-ONLY-v5-feasibility/room-1-ONLY-v5-feasibility-prompt-v4-2026-05-04.md`). The audit deliverables were eight markdown notes plus a WebGPU adapter test page, all confined to `room-1-3d/notes/v5-*.md` and `room-1-3d/test-webgpu.html` (source: same prompt, constraints section).

## 8. We restarted the standalone folder as a WebGPU smoke test

After the audit, `room-1-3d/` was re-created from scratch (currently untracked in git, see git status). The new `room-1-3d/src/main.js` is a 78-line WebGPU smoke test using `WebGPURenderer` from `three/webgpu`, three.js r184, ACES tone mapping, OrbitControls, a placeholder ground plane, and a single rotating box. The file's own header comment says "WebGPU first, fall back to WebGL2 automatically" and "the room geometry migration replaces this in the next step" (source: `room-1-3d/src/main.js` lines 1-5 and 38-40).

This is the live current state of the standalone v5 build. Its first job is to confirm WebGPU works end-to-end before any room geometry gets ported in.

## 9. Where the build sits today

The `registerScene('room-1', ...)` block inside `ozu-test.html` is the production room-1, with full layout, lighting, glass, furniture, lamp toggle, and post-processing pipeline working (source: `room-1-ONLY-rendering-plan.md` current-actual-state section). The standalone `room-1-3d/` folder is back, in its earliest possible state, as a WebGPU smoke test waiting for room geometry to be ported in (source: `room-1-3d/src/main.js`). The cutting-edge plan at `room-1-ONLY-cutting-edge-plan.md` lists the next quality passes in order: TAA anti-aliasing, RectAreaLight window sunbeam, real HDRI environment, god-rays cone, soft cloth shader, per-material polish (source: `room-1-ONLY-cutting-edge-plan.md` order section).

## How to repeat this on the next property

If you are starting a new property, the same flow applies in this order:

1. Get the blueprint PDF, the per-room corner panoramas, and the front-facade exterior photos onto disk.
2. Write the per-room map (one file per room, plain-language wall names matching the photo folder names exactly).
3. Write the global coordinates file from the blueprint.
4. Write the master plan (whole property, phased) and any per-room standalone plan.
5. Build a quick standalone sandbox for any room that gets cutting-edge experiments, separate from the master HTML file.
6. Inside the master HTML file, add a `registerScene` block per room. Keep the standalone sandbox and the master scene logically separate, even if they share the file.
7. Build layout first (walls, window openings, doors, floor, furniture). See `flow-room-1-layout.md`.
8. Build rendering on top of layout (env map, tone mapping, lights, glass, post-processing, textures). See `flow-room-1-rendering.md`.
9. When you want to push beyond what the current stack can do, run a feasibility audit before building, not during.

## Gaps i could not source

- The exact dates of the "phase A/B/C blueprints + room maps + collision-box audit" work in commit 4caf784 are not broken out per phase in the commit body. The handoffs from late April 2026 would fill this in.
- The exact ordering of the layout work inside the registerScene block (which wall went first, which furniture piece was placed first) is not recoverable from git alone. The handoffs at `.handoffs/handoff-2026-04-27-*.md` through `.handoffs/handoff-2026-04-30-*.md` would fill this in.
- The "Phase D-1/3/4/5/6" naming in commit 6cbf3de implies a Phase D-2 was either skipped or rolled into another phase. The reasoning is not in the commit body.
- v2 of the standalone `room-1-3d/` folder existed only briefly between v1 and v4 and was not committed under its own commit message. Its content is recoverable only from a partial diff at commit 957810b which mentions "rename variant folders: v2 -> v1, v3-rect -> v2, v3-walls -> v3" implying multiple parallel experiments existed.
