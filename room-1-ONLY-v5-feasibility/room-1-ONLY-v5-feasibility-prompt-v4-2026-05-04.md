# ROOM-1 ONLY — v5 feasibility audit (phase 0, audit only, no building)

> **SCOPE: ROOM-1 ONLY.** This document is about **room-1** of the Ozu-1 house, and nothing else. It is **NOT** the master plan for the Ozu-1 project. It does **NOT** cover room-2, room-3, room-4, the exterior, or the property as a whole. Do not extrapolate.

## Verdict definitions (used throughout)

- Green: viable as designed in the proposed stack, no caveats.
- Yellow: viable with caveats, or "needs prototype" to confirm. Specify what's missing.
- Red: not viable as designed; an alternative approach is required. Propose one.

## v5 is a parallel variant (read this; do not violate)

v5 is NOT a replacement for v4. v4 stays exactly where it is and continues to work. When phase 1+ eventually builds v5, it lives at `room-1-3d/src/variants/v5/` as a sibling to v4. Riaan switches between v4 and v5 via the chip switcher in `ozu-test.html` (or the room-1-3d local equivalent), comparing them side by side. Replacing or overwriting v4 is forbidden in every phase, including future ones. This phase 0 audit does not build v5; it only writes notes and a test page. Future phase prompts will build v5 in its own variant folder.

## Machine and structure confirmation (read first, before anything else)

This audit must run on Riaan's Mac. The project root is `/Users/riaan/3d-vertical-test/`.

Bash: `pwd && hostname && whoami`. If the working path doesn't sit under `/Users/riaan/` or you're on Linux at `/home/`, STOP and report. Do not improvise paths. Do not continue.

Then verify all three structural assumptions exist. STOP and report if any are missing:

- `/Users/riaan/3d-vertical-test/room-1-3d/` exists as a folder.
- `/Users/riaan/3d-vertical-test/room-1-3d/src/variants/v4/` exists with files inside.
- `/Users/riaan/3d-vertical-test/room-1-3d/package.json` exists.

If any of the above is missing, STOP and wait for Riaan. Do NOT scaffold v4 from scratch. Do NOT improvise. v4 is the product of prior sessions of careful work and must not be recreated by guessing. Riaan will fix the folder structure and re-run the prompt.

## Two-machine context (relevant to task 5)

Riaan has two machines:

- His Mac (where this audit runs, where the project files live).
- A separate Linux GPU box (specs unknown to Claude Code; Riaan will need to provide them).

The GPU box is NOT where this audit runs. It exists for splat training (task 5) which may need CUDA. Treat it as a future destination for training jobs, not as a source of files for this audit.

## Key principle (read twice)

Phase 0 audits viability for 7 specific user requests against a proposed cutting-edge stack. It produces a feasibility report. It does NOT build. It does NOT install. It does NOT modify any existing variant. Once Riaan reads the report, he picks which phases to fund and I will write each one as a separate prompt.

Scope is room-1 only. Do NOT touch unified-building, room-2-3d, room-3-3d, room-4-3d, ozu-test.html, or v1-v4 of room-1-3d.

## The 7 user requests this audit must answer

| # | User request | Audit task | Verdict required |
|---|---|---|---|
| 1 | Functional light switch | Task 7 | Yes |
| 2 | Glass windows with outside view | Task 8 | Yes |
| 3 | Match panorama photos exactly | Task 5 (with fallback contingency) | Yes |
| 4 | Hard and soft textures (PBR materials) | Task 9 | Yes |
| 5 | Keyshot library help | Tentatively NO (licensed, no Three.js path; Polyhaven CC0 replaces). Riaan to confirm in his read of the report. | Riaan-confirm |
| 6 | AR | Task 10 | Yes |
| 7 | Adapt to mobile | Task 11 | Yes |

## Proposed cutting-edge stack (audit each, do NOT install)

| Layer | Candidate | Source |
|---|---|---|
| Renderer | Three.js WebGPU renderer (r171+, September 2025) | https://threejs.org/docs/pages/WebGPURenderer.html and https://www.utsubo.com/blog/threejs-2026-what-changed |
| Splats (visual layer) | Spark 2.0 by World Labs | https://sparkjs.dev/ and https://github.com/sparkjsdev/spark and https://sparkjs.dev/docs/new-features-2.0/ |
| Path tracing (cinema mode) | three-gpu-pathtracer | https://github.com/gkjohnson/three-gpu-pathtracer |
| Splat training from panos | Splatter-360 (designed for wide-baseline 360 input) | https://3d-aigc.github.io/Splatter-360/ |
| AR | WebXR Device API with Three.js | https://developers.google.com/ar/develop/webxr/hello-webxr |
| AR occlusion | enva-xr | https://github.com/tentone/enva-xr |
| Shaders | TSL (Three Shader Language; ships with WebGPU renderer) | https://blog.maximeheckel.com/posts/field-guide-to-tsl-and-webgpu/ |
| PBR textures | Polyhaven (CC0) | https://polyhaven.com |

NOT Keyshot.

## Inputs (verify each path; if any missing, stop and report)

| Item | Path |
|---|---|
| Panoramas, room-1 | /Users/riaan/3d-vertical-test/ozu-test/interior-images/room-1/corner-*/ |
| Existing v4 reference | /Users/riaan/3d-vertical-test/room-1-3d/src/variants/v4/ |
| package.json | /Users/riaan/3d-vertical-test/room-1-3d/package.json |

## Tasks

TodoWrite: create checklist with the following 12 items. Mark each done as it completes.

1. Renderer audit. 
   - Bash: `cd /Users/riaan/3d-vertical-test/room-1-3d && npm list three`. Report installed Three.js version.
   - Bash: `cd /Users/riaan/3d-vertical-test/room-1-3d && grep -rE "WebGLRenderer|WebGPURenderer" src/variants/v4/`. This catches both `new THREE.WebGLRenderer()` and destructured `import { WebGLRenderer } from 'three'; new WebGLRenderer()`. Read the matching lines to determine which renderer class is actually instantiated. Report findings to chat.
   - Note that being on r171+ does NOT mean WebGPU is in use; the project may still instantiate WebGLRenderer on a recent Three.js version. Both facts (version + actual renderer class) are needed to answer "is a renderer migration needed".
   - Note also that TSL shipping status follows the WebGPU renderer; the TSL verdict in section 6 of the consolidated report inherits from this task's findings (no separate audit task).
   - Then write `room-1-3d/test-webgpu.html`: standalone HTML page that calls `navigator.gpu.requestAdapter()`, reports `adapter.info` to a div, and falls back gracefully if undefined. Instruct Riaan in chat to open it in Chrome and paste the adapter info. Do NOT block on his reply; continue.

2. Bash: `cd /Users/riaan/3d-vertical-test/room-1-3d && cat package.json | grep -E "spark|pathtracer"`. Write to chat: install status of @sparkjsdev/spark and three-gpu-pathtracer. Do NOT install.

3. Bash: `ls -d /Users/riaan/3d-vertical-test/ozu-test/interior-images/room-1/corner-*/` to list all corner folders. Then for each folder, list its contents: `ls /Users/riaan/3d-vertical-test/ozu-test/interior-images/room-1/corner-*/`. Write to chat: actual folder count, actual file extensions (do NOT assume `.webp`), per-folder file count.

4. Pano content + cross-folder exposure check.
   - Read: one image file per corner folder found in task 3 (whatever the actual extension is, however many folders exist). For each image, note resolution, visible features, and any subjective exposure observation (bright, dark, blown highlights, crushed shadows).
   - Cross-folder exposure consistency: compare the per-image observations across all folders. Flag any folder that looks materially brighter or darker than the others. Exposure mismatch across corner panoramas is a real risk for splat training; the comparison must happen across folders, not within one image.
   - Write: `room-1-3d/notes/v5-pano-audit.md` with per-folder observations, the cross-folder exposure consistency verdict, and a note on whether folder names match expected room corners or whether any of the deferred mis-named folders (`corner-cabinet-window`, `corner-ac-entrance` per memory) are present.

5. Splat training viability + fallback for user request 3. Read web docs at https://3d-aigc.github.io/Splatter-360/ and the gsplat baseline at https://github.com/graphdeco-inria/gaussian-splatting. Then evaluate against the panos audited in task 4:
   - What scene types and input counts was Splatter-360 trained and tested on per its paper/repo? Cite the section. Does that match Riaan's case (residential interior, 4 wide-baseline corner panoramas)?
   - Is the actual pano count from task 3 enough input?
   - If not, propose minimum additional capture (positions, count).
   - Preferred method: Splatter-360 vs baseline gsplat with cubemap unwrap.
   - Splatter-360 turnkey check: does the repo ship a runnable training script with a documented entry point, or is it reference code requiring a port? Cite the repo's README/installation section.
   - Where training runs: Riaan's Mac M-series (likely spotty CUDA-centric pipeline support), his separate Linux GPU box (specs unknown; list the requirements training needs so Riaan can check), or cloud. State requirements like CUDA version, GPU VRAM minimum, RAM, OS.
   - Cloud cost estimate, bounded and dated: specify the GPU class needed (e.g. A100, H100, L4), estimated training duration in hours for one room based on Splatter-360 paper or gsplat baseline benchmarks (cite the source), a current hourly rate from a named provider (RunPod, Lambda, Vast.ai - cite the provider's pricing page), and a total estimate range. Tag the estimate with "as of audit date [YYYY-MM-DD]" so it reads as a snapshot, not an evergreen number. Do NOT give a guess across orders of magnitude.
   - Fallback for user request 3 ("match photos exactly"): if splat is infeasible from the actual pano count and additional capture is not possible, what's the next best path? Hand-modeling cannot match photos pixel-for-pixel by definition, so flag this clearly. Provide a contingency verdict for user request 3 under both scenarios (splat works / splat fails).
   
   Write: `room-1-3d/notes/v5-splat-options.md`. Cite each claim with a docs link.

6. Composition. Read web docs at https://sparkjs.dev/docs/ and https://github.com/gkjohnson/three-gpu-pathtracer. Then evaluate:
   - Can a Spark SplatMesh and a three-gpu-pathtracer mesh coexist in one render pass? Cite specific docs or open issues.
   - If not, is a mode toggle (splat for walkthrough, path tracer for cinema render) the viable pattern?
   - What is the path tracer's support status under the new WebGPU compute backend per https://discourse.threejs.org/t/three-gpu-pathtracer-a-modular-shader-based-path-tracing-extension-for-three-js/36903/51
   - If you cannot determine composition without prototyping, write "needs prototype" and specify what minimal prototype would resolve it.
   
   Write: `room-1-3d/notes/v5-composition.md`. Cite each claim.

7. (User request 1) Light switch interactive layer. First verify Spark API: read https://sparkjs.dev/docs/splat-mesh/ and confirm `raycastable` and `minRaycastOpacity` props actually exist on `SplatMesh` in the current Spark 2.0 release. Cite the exact section. If they don't exist or are deprecated, the entire approach changes; report that clearly. If they exist, evaluate: can an invisible mesh be placed coincident with the splat and used for click-detection on a "light switch" without visual conflict? Write findings + verdict to `room-1-3d/notes/v5-interactive-layer.md`.

8. (User request 2) Glass windows. Critical sub-question: in a splat trained from interior panoramas, the window region already contains baked photo content of whatever was outside on shoot day. To replace that with a transparent glass material + HDRI backdrop, the splat must be masked out at the window region. Evaluate:
   - Can a transparent MeshPhysicalMaterial mesh be placed coincident with the splat's window region while masking out the splat's baked window content? Spark may support this via a per-region opacity mask, a gaussian-trim, or a stencil pass. Cite the Spark mechanism if it exists. If no documented mechanism exists, write "needs prototype" and specify what minimal prototype would resolve it.
   - Once the splat's window content is masked, can the transparent glass + HDRI backdrop render correctly behind it (depth ordering, transparency sort)?
   - Outside HDRI: Polyhaven does NOT tag HDRI by location. The best achievable is a vibes match (Asian residential suburb feel, overcast morning light, similar latitude). Propose 3 candidate slugs that fit the vibe, with slug + URL. Frame these as vibes matches, NOT as geo-accurate to Kumamoto.
   
   Write: `room-1-3d/notes/v5-glass-window.md`. Cite Spark and Polyhaven docs.

9. (User request 4) Hard and soft textures across the whole room. Critical framing first: in a pure-splat scene, photo textures come from the panos automatically for ALL surfaces (floor, walls, furniture, ceiling). PBR materials are NOT needed for any surface the splat covers. PBR slugs apply ONLY to hand-built inserts that sit on top of the splat.
   - The canonical list of hand-built inserts is determined by tasks 7 (light switch) and 8 (glass frame), NOT by this task. Do NOT invent speculative inserts. Read the verdicts from tasks 7 and 8 first, list ONLY the inserts they actually require.
   - For each canonical insert from tasks 7 and 8, classify it as hard surface (e.g. ceramic, metal, glass) or soft surface (e.g. cloth, fabric) and propose Polyhaven slugs with URLs.
   - If tasks 7 and 8 both come back red and no hand-built inserts are required, the verdict for user request 4 is green by default (splat handles everything) with a note that PBR is moot.
   - Do NOT propose slugs for surfaces the splat already handles.
   - The verdict for user request 4 covers texture treatment for the whole room; the answer is that splat handles most surfaces "for free" and PBR fills the gaps for whatever inserts tasks 7 and 8 actually require.
   
   Write: `room-1-3d/notes/v5-textures.md`. Cite Polyhaven slugs.

10. (User request 6) AR viability. Read https://threejsresources.com/blog/best-vr-headsets-with-webxr-support-for-threejs-developers-2026 and https://developers.google.com/ar/develop/webxr/hello-webxr. Evaluate WebXR AR for room-1:
    - Verify current iOS Safari support for `immersive-ar`. Sources from late 2025 say no support; check whether anything has changed by searching for newer references or the official MDN browser-support page. Do not assert; verify.
    - Verify current Android Chrome and Quest 3 browser support for `immersive-ar`.
    - WebXR + WebGPU compatibility: can a WebXR AR session run over a WebGPU-rendered scene? This is a known sticky area. Search Three.js examples, the WebXR Device API spec, and GitHub issues on three.js for evidence. If incompatible, the AR pillar may force a fallback to WebGLRenderer for AR sessions only, which has implications for the path tracer and TSL. Cite findings.
    - Chain-effect handling: if the WebXR + WebGPU check forces a WebGL fallback for AR sessions, this dependency MUST be threaded into section 6 of the consolidated report (task 12). Specifically, downgrade the verdicts on these stack-layer rows: Renderer (WebGPU), Path tracing (three-gpu-pathtracer), Shaders (TSL). Each becomes yellow at minimum, with a note that the pillar works for non-AR sessions but the AR session uses a separate WebGL render path. State this dependency explicitly in `v5-ar-viability.md` so the synthesis step in task 12 cannot miss it.
    - Graceful degradation pattern for iOS users.
    - Whether AR over a gaussian splat is documented or unprecedented (search Spark issues + Three.js examples). If unprecedented and undocumented, write "needs prototype" rather than guessing a verdict.
    - Flag this open question for Riaan: if his parent app ships to iPhone, the iOS limitation matters. He needs to decide whether AR is Android+Quest only, or whether iPhone gets a fallback.
    
    Write: `room-1-3d/notes/v5-ar-viability.md`.

11. (User request 7) Mobile viability. Evaluate:
    - Spark 2.0 mobile streaming claims per https://sparkjs.dev/docs/new-features-2.0/. Cite specific.
    - Touch controls + DeviceOrientationEvent for tilt-to-look. iOS 13+ permission requirement.
    - Performance budget for a splat-based scene (NOT a traditional mesh scene). Relevant metrics:
      - Splat count cap on mid-range mobile (cite Spark 2.0 LoD streaming claims).
      - Texture memory for HDRI backdrop + Polyhaven PBR slugs of any hand-built inserts (env map size + PBR texture size). If task 9's verdict is "no inserts required, PBR moot", the PBR texture memory budget is zero and only the HDRI backdrop counts. State the budget conditionally on task 9's outcome.
      - Frame time budget (target 30fps or 60fps on mid-range mobile).
      - Mobile WebGPU availability vs WebGL2 fallback path.
    - Do NOT include shadow map size as a primary metric; splats don't receive shadows the same way as meshes. Mention shadow map size only if hand-built inserts cast shadows on the splat (which is itself a research question).
    
    Write: `room-1-3d/notes/v5-mobile.md`.

12. Consolidated report. 
    - First, read all 7 notes files written in tasks 4-11: `cat room-1-3d/notes/v5-pano-audit.md room-1-3d/notes/v5-splat-options.md room-1-3d/notes/v5-composition.md room-1-3d/notes/v5-interactive-layer.md room-1-3d/notes/v5-glass-window.md room-1-3d/notes/v5-textures.md room-1-3d/notes/v5-ar-viability.md room-1-3d/notes/v5-mobile.md`. Synthesize from the actual notes content, not from memory of what you wrote.
    - Then write: `room-1-3d/notes/v5-feasibility.md`. Sections:
    - 1: Three.js version + currently-instantiated renderer + WebGPU adapter test instructions for Riaan (where to find the test page, what to paste back).
    - 2: Pano inventory summary (actual folder count, actual extension, per-folder content, cross-folder exposure verdict).
    - 3: Splat training viability + recommended method + Splatter-360 turnkey status + training environment requirements (CUDA version, GPU VRAM, RAM, OS) + bounded cloud cost estimate (with audit-date tag) so Riaan can check his Linux GPU box against them (from task 5).
    - 4: Spark + path tracer composition viability (from task 6).
    - 5: Per-user-request verdict table:

      | User request | Verdict | Notes |
      |---|---|---|
      | 1. Light switch | Green/yellow/red | From task 7 |
      | 2. Glass windows | Green/yellow/red | From task 8 |
      | 3. Match photos (splat works) | Green/yellow/red | From task 5 primary path |
      | 3. Match photos (splat fails) | Green/yellow/red | From task 5 fallback |
      | 4. Hard/soft textures (whole room) | Green/yellow/red | From task 9 |
      | 5. Keyshot | Red (Riaan to confirm) | Polyhaven replaces |
      | 6. AR | Green/yellow/red | From task 10 |
      | 7. Mobile | Green/yellow/red | From task 11 |

      After the table, if the AR verdict and the Mobile verdict disagree on iOS (e.g. mobile is green but iPhone AR is red), summarize the resulting iPhone-user experience in plain language. One paragraph. What can an iPhone user do, what can't they do, and what's the proposed graceful degradation.

    - 6: Per-stack-layer verdict table (all 8 layers from the proposed stack). Apply the WebXR + WebGPU chain-effect from task 10: if AR forces a WebGL fallback for AR sessions, the Renderer (WebGPU), Path tracing, and Shaders (TSL) rows MUST be downgraded to yellow at minimum with the AR dependency noted. Do not skip this if `v5-ar-viability.md` flagged the dependency.

      | Layer | Verdict | Notes |
      |---|---|---|
      | Renderer (WebGPU) | Green/yellow/red | From task 1; downgrade to yellow if task 10 flags AR forces WebGL fallback |
      | Splats (Spark 2.0) | Green/yellow/red | From task 7 + task 6 |
      | Path tracing (three-gpu-pathtracer) | Green/yellow/red | From task 6; downgrade to yellow if task 10 flags AR forces WebGL fallback |
      | Splat training (Splatter-360) | Green/yellow/red | From task 5 |
      | AR (WebXR) | Green/yellow/red | From task 10 |
      | AR occlusion (enva-xr) | Green/yellow/red | From task 10 |
      | Shaders (TSL) | Green/yellow/red | Inherits from renderer (task 1); downgrade to yellow if task 10 flags AR forces WebGL fallback |
      | PBR textures (Polyhaven) | Green/yellow/red | From task 8 + task 9 |

    - 7: Observed repo structure. Report what you actually saw: does `room-1-3d/` exist as a sibling project? Does room-1 also live inside `ozu-test.html` as a registered scene? Are both true? Just describe what's there. Riaan reconciles based on observation.
    - 8: Open questions Riaan must answer before phase 1. Include at minimum:
      - What does "match photos exactly" mean? Pixel-faithful, perceptually close, or recognizably the same room?
      - Does AR need to work on iPhone, or is Android + Quest 3 acceptable?
      - Confirm Keyshot is not desired (Polyhaven CC0 replaces it).
      - Linux GPU box specs (GPU model, VRAM, CUDA version, OS) to verify against splat training requirements from section 3.
      - Any other ambiguities surfaced during the audit.
    - 9: Proposed phase order for phases 1-N based on the verdicts (your roadmap proposal, Riaan can override). Phase 1 starts by creating `room-1-3d/src/variants/v5/` as a fresh sibling to v4. v4 is never modified or replaced. Riaan switches between v4 and v5 via the chip switcher to compare them. State this explicitly in the proposed roadmap.

    Hard stop. Paste the absolute path of `v5-feasibility.md` to chat. Do NOT cp v4 v5. Do NOT install. Do NOT touch ozu-test.html. Wait for Riaan's go.

## Constraints

- Read-only on existing project files. Only allowed writes: 8 markdown files under `room-1-3d/notes/v5-*.md` and 1 test page at `room-1-3d/test-webgpu.html`. Nothing else.
- v5 is a parallel variant. v4 is never modified, copied over, or replaced. Future phases will create `src/variants/v5/` as a sibling to v4.
- If any input path doesn't exist, stop and wait for Riaan. Do not guess. Do not scaffold.
- If a docs source contradicts a claim in this prompt, surface it in the report. Do not silently resolve.
- If you cannot determine viability for a task without prototyping code, write "needs prototype" and explain what would be needed. Do not bluff.
- Do NOT extrapolate to any other room. Scope is room-1 only.
- NOT Keyshot. NOT Babylon.js. NOT a different engine.

## Acknowledge before starting

Reply with:
1. Machine confirmation (path under `/Users/riaan/`, hostname).
2. Structure confirmation (`room-1-3d/`, `src/variants/v4/`, `package.json` all exist).
3. All 3 input paths confirmed reachable.
4. TodoWrite checklist created with 12 items.
5. Any clarifications needed before starting task 1.
