# ROOM-1 ONLY — v5 feasibility audit (phase 0, audit only, no building)

> **SCOPE: ROOM-1 ONLY.** This document is about **room-1** of the Ozu-1 house, and nothing else. It is **NOT** the master plan for the Ozu-1 project. It does **NOT** cover room-2, room-3, room-4, the exterior, or the property as a whole. Do not extrapolate.

## Key principle (read twice)

Phase 0 audits viability for 7 specific user requests against a proposed cutting-edge stack. It produces a feasibility report. It does NOT build. It does NOT install. It does NOT modify any existing variant. Once Riaan reads the report, he picks which phases to fund and I will write each one as a separate prompt.

Scope is room-1 only. Do NOT touch unified-building, room-2-3d, room-3-3d, room-4-3d, ozu-test.html, or v1-v4 of room-1-3d.

## The 7 user requests this audit must answer

| # | User request | Audit task | Green/yellow/red verdict required |
|---|---|---|---|
| 1 | Functional light switch | Task 8 | Yes |
| 2 | Glass windows with outside view | Task 9 | Yes |
| 3 | Match panorama photos exactly | Task 5 | Yes |
| 4 | Hard and soft textures (PBR materials) | Task 10 | Yes |
| 5 | Keyshot library help | Answered upfront: NO. Keyshot is licensed and has no Three.js path. Polyhaven (CC0) replaces it for any hand-built parts. | N/A |
| 6 | AR | Task 11 | Yes |
| 7 | Adapt to mobile | Task 12 | Yes |

## Proposed cutting-edge stack (audit each, do NOT install)

| Layer | Candidate | Source |
|---|---|---|
| Renderer | Three.js WebGPU renderer (r171+, September 2025) | https://threejs.org/docs/pages/WebGPURenderer.html and https://www.utsubo.com/blog/threejs-2026-what-changed |
| Splats (visual layer) | Spark 2.0 by World Labs | https://sparkjs.dev/ and https://github.com/sparkjsdev/spark and https://sparkjs.dev/docs/new-features-2.0/ |
| Path tracing (cinema mode) | three-gpu-pathtracer | https://github.com/gkjohnson/three-gpu-pathtracer |
| Splat training from panos | Splatter-360 (designed for wide-baseline 360 input) | https://3d-aigc.github.io/Splatter-360/ |
| AR | WebXR Device API with Three.js | https://developers.google.com/ar/develop/webxr/hello-webxr |
| AR occlusion | enva-xr | https://github.com/tentone/enva-xr |
| Shaders | TSL (Three Shader Language) | https://blog.maximeheckel.com/posts/field-guide-to-tsl-and-webgpu/ |
| PBR textures | Polyhaven (CC0) | https://polyhaven.com |

NOT Keyshot.

## Inputs (verify each path; if any missing, stop and report)

| Item | Path |
|---|---|
| Panoramas, room-1 | /Users/riaan/3d-vertical-test/ozu-test/interior-images/room-1/corner-*/ |
| Existing v4 reference | /Users/riaan/3d-vertical-test/room-1-3d/src/variants/v4/ |
| package.json | /Users/riaan/3d-vertical-test/room-1-3d/package.json |

## Tasks

TodoWrite: create checklist with the following 13 items. Mark each done as it completes.

1. Bash: `cd /Users/riaan/3d-vertical-test/room-1-3d && npm list three`. Write to chat: installed Three.js version + whether < r171 (means renderer upgrade needed).

2. Bash: `cd /Users/riaan/3d-vertical-test/room-1-3d && cat package.json | grep -E "spark|pathtracer"`. Write to chat: install status of @sparkjsdev/spark and three-gpu-pathtracer. Do NOT install.

3. Bash: `ls /Users/riaan/3d-vertical-test/ozu-test/interior-images/room-1/corner-*/*.webp | wc -l` and `ls -d /Users/riaan/3d-vertical-test/ozu-test/interior-images/room-1/corner-*/`. Write to chat: total .webp count + per-corner directory list.

4. Read: one .webp per corner-*/ folder (4 reads total). Write: room-1-3d/notes/v5-pano-audit.md with resolution, exposure consistency observation, visible features per corner.

5. Read web docs at https://3d-aigc.github.io/Splatter-360/ and the gsplat baseline at https://github.com/graphdeco-inria/gaussian-splatting. Then evaluate against the 4 panos audited in task 4:
   - Is 4 wide-baseline 360 panoramas enough input?
   - If not, propose minimum additional capture (positions, count).
   - Preferred method: Splatter-360 vs baseline gsplat with cubemap unwrap.
   - Where training runs: Claude Code sandbox (almost certainly no GPU access), Riaan's machine (has powerful GPU), or cloud.
   
   Write: room-1-3d/notes/v5-splat-options.md. Cite each claim with a docs link.

6. Read web docs at https://sparkjs.dev/docs/ and https://github.com/gkjohnson/three-gpu-pathtracer. Then evaluate composition:
   - Can a Spark SplatMesh and a three-gpu-pathtracer mesh coexist in one render pass? Cite specific docs or open issues.
   - If not, is a mode toggle (splat for walkthrough, path tracer for cinema render) the viable pattern?
   - What is the path tracer's support status under the new WebGPU compute backend per https://discourse.threejs.org/t/three-gpu-pathtracer-a-modular-shader-based-path-tracing-extension-for-three-js/36903/51
   
   Write: room-1-3d/notes/v5-composition.md. Cite each claim.

7. Write: room-1-3d/test-webgpu.html. A standalone HTML page that calls navigator.gpu.requestAdapter(), reports adapter.info to a div, and falls back gracefully if undefined. After write, instruct Riaan in chat to open it in Chrome and paste the adapter info. Do NOT block on his reply; continue with remaining tasks.

8. (User request 1) Read https://sparkjs.dev/docs/splat-mesh/ for raycastable + minRaycastOpacity props. Then evaluate: can an invisible mesh be placed coincident with the splat and used for click-detection on a "light switch" without visual conflict? Write findings + verdict (green/yellow/red) to room-1-3d/notes/v5-interactive-layer.md. Cite the SplatMesh docs.

9. (User request 2) Evaluate window viability:
   - Can a transparent MeshPhysicalMaterial mesh be placed coincident with the splat's window region, occluding the splat behind the glass while showing an HDRI backdrop beyond?
   - Which Polyhaven HDRI slugs would suit a residential suburb in Kumamoto Prefecture (lat 32.914715, lon 130.85025)? Propose 3 candidates with slug + URL.
   
   Write: room-1-3d/notes/v5-glass-window.md. Cite Spark and Polyhaven docs.

10. (User request 4) Evaluate hard/soft texture treatment:
    - In a pure splat, textures come from the photos automatically (user request 4 is satisfied "for free"). Confirm this against splat docs.
    - For any hand-built mesh in the hybrid (light switch fixture, glass frame, possible architectural baseboards): plan PBR via Polyhaven. Specify hard surface candidates (ceramic switch plate, metal handle, glass) vs soft surface candidates (any visible cloth on the bed if hand-modeled).
    
    Write: room-1-3d/notes/v5-textures.md. Cite Polyhaven slugs proposed.

11. (User request 6) Read https://threejsresources.com/blog/best-vr-headsets-with-webxr-support-for-threejs-developers-2026 and https://developers.google.com/ar/develop/webxr/hello-webxr. Evaluate WebXR AR for room-1:
    - Confirm iOS Safari does NOT support immersive-ar (cite source).
    - Confirm Android Chrome and Quest 3 browser DO support immersive-ar (cite source).
    - Graceful degradation pattern for iOS users.
    - Whether AR over a gaussian splat is documented or unprecedented (search Spark issues + Three.js examples).
    
    Write: room-1-3d/notes/v5-ar-viability.md.

12. (User request 7) Evaluate mobile viability:
    - Spark 2.0 mobile streaming claims per https://sparkjs.dev/docs/new-features-2.0/. Cite specific.
    - Touch controls + DeviceOrientationEvent for tilt-to-look. iOS 13+ permission requirement.
    - Performance budget: env map size, shadow map size, max texture size, splat count cap on mobile.
    
    Write: room-1-3d/notes/v5-mobile.md.

13. Write: room-1-3d/notes/v5-feasibility.md. Consolidated report. Sections:
    - 1: Three.js version status + WebGPU test instructions for Riaan.
    - 2: Pano inventory summary.
    - 3: Splat training viability + recommended method + where it runs (from task 5).
    - 4: Spark + path tracer composition viability (from task 6).
    - 5: Per-user-request verdict table:

      | User request | Verdict | Notes |
      |---|---|---|
      | 1. Light switch | Green/yellow/red | From task 8 |
      | 2. Glass windows | Green/yellow/red | From task 9 |
      | 3. Match photos | Green/yellow/red | From task 5 |
      | 4. Hard/soft textures | Green/yellow/red | From task 10 |
      | 5. Keyshot | Red | Not viable, Polyhaven replaces |
      | 6. AR | Green/yellow/red | From task 11 |
      | 7. Mobile | Green/yellow/red | From task 12 |

    - 6: Per-pillar verdict table (WebGPU renderer, Spark splats, path tracer).
    - 7: Open questions for Riaan.
    - 8: Proposed phase order for phases 1-N based on the verdicts (your roadmap proposal, Riaan can override).

    Hard stop. Paste the absolute path of v5-feasibility.md to chat. Do NOT cp v4 v5. Do NOT install. Do NOT touch ozu-test.html. Wait for Riaan's go.

## Constraints

- Read-only on existing project files. Only allowed writes: 8 markdown files under room-1-3d/notes/v5-*.md and 1 test page at room-1-3d/test-webgpu.html. Nothing else.
- If any input path doesn't exist, stop and report. Do not guess.
- If a docs source contradicts a claim in this prompt, surface it in the report. Do not silently resolve.
- If you cannot determine viability for a task without prototyping code, write "needs prototype" and explain what would be needed. Do not bluff.
- Do NOT extrapolate to any other room. Scope is room-1 only.
- NOT Keyshot. NOT Babylon.js. NOT a different engine.

## Acknowledge before starting

Reply with:
1. All 3 input paths confirmed reachable.
2. TodoWrite checklist created with 13 items.
3. Any clarifications needed before starting task 1.
