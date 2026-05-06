# What we need to create this quality render

A team brief for everyone touching room-1.

**Audience:** CEO, CTO, devs, designer, photographer, videographer.
**Goal:** photoreal, interactive 3D of a real Japanese bedroom, viewable in any browser, optionally in AR.
**Date:** 2026-05-06.

---

## TL;DR (read this even if you read nothing else)

- The path to "indistinguishable from the photos" exists in 2026 and is called **Gaussian splatting**. It's the technique behind Apple Vision Pro spatial scenes and Niantic Scaniverse. A neural network turns photos into a 3D cloud of millions of coloured dots; rendered in a browser, the result looks like the photos themselves projected into space.
- We are blocked on **three** things:
  1. **Photographer/videographer:** the 4 corner panoramas we have are not enough input. We need a 1–2 minute video walkthrough OR 12–20 overlapping panoramas on a 1.5m grid.
  2. **CEO:** iPhone Safari does not support browser AR (and Apple has shown no signal it ever will). Decision: drop AR on iPhone, OR fund a separate native iOS module.
  3. **CTO:** room-1 currently lives as one inlined `<script>` block in `ozu-test.html`. The modern stack (Three.js r184, Spark 2.0 splat library, WebGPU) needs a real build setup. Approve a small Vite project for room-1, keep the rest of the property on the existing setup.
- **Total cost:** $5–50 in cloud GPU (we already own a powerful local GPU; cloud is a backup). 4–5 weeks of focused engineering work.
- **Total result:** browser URL that opens the room as if you're standing inside the photo, click the light switch and it toggles, look out the window and see the real outside, optionally enter AR on Quest/Android and the room appears in your living room.

---

## What "this quality" looks like

| What we have today | What we're building |
|---|---|
| Hand-modeled boxes coloured to match the photos | A direct visual reconstruction from the photos themselves |
| Edges and corners always look like a 3D model | Looks like the actual room because the source data IS the room |
| Walls are flat colour with PBR textures we hunt for | Walls are the real photographed walls, with their actual paint, marks, light |
| Curtain folds, pillow shapes are approximations | Curtain folds and pillow shapes are the real ones, frozen in 3D |
| AR experience is a visualization | AR experience drops the real captured room into the user's space |

The bar is **photoreal at the capture points, recognizable everywhere else**. No 3D technique in 2026 — including this one — can fully fabricate views the photographer never captured. So capture density determines quality.

---

## The technique (Gaussian splatting), in plain language

1. The photographer captures the room (video walkthrough or many panoramas).
2. A neural network is trained on those frames using a free CUDA tool called **PostShot** or **gsplat**. Training takes 20–60 minutes on a modern GPU.
3. The output is a `.ply` file: a list of millions of tiny coloured "splats" (think Gaussian dots) floating in 3D space.
4. The browser library **Spark 2.0** (Three.js plugin) renders those splats at interactive framerates on desktop, mobile, and AR headsets.
5. We hand-build a small interactive layer on top: clickable light switch, glass mesh over the window opening, HDRI sky behind the glass.

No special licenses. No proprietary tools. Pipeline runs entirely on free / CC0 software. Outputs are static files served from any web host.

---

## What we already have

- Blueprint of the room (PDF, dimensions accurate to ~1cm).
- 4 panoramas, one from each corner, at `ozu-test/interior-images/room-1/corner-*/`. **Not enough input on their own** — see "blocking truth #1".
- Hand-modeled three.js scene of the room (current state, ozu-test.html). This becomes the **fallback** if splatting can't be tried, and the **collision layer** under the splat once it can.
- Powerful Linux GPU box. Used as a workstation for splat training and shader experiments. No cloud spend needed for training.
- This research report (49 sources, 2026-05-06).

## What we don't have

- A capture sufficient to train a high-quality splat. **Recapture is the single biggest gating decision.**
- A small build/deploy setup for room-1 (Vite + ESM modules + Three.js r184). Currently everything is inlined in one HTML file.
- A decision on AR scope: do iPhones get AR or not.

---

## What each role does

### Photographer / videographer (capture lead)

You are the most important role on this project. The visual ceiling of the final render is set entirely by how the room is captured. **The current 4-panorama capture won't get us where we want to go.** Two options:

**Option A — video walkthrough (fastest, cheapest)**

- Slow walking pace (5 seconds per metre).
- Phone or camera with **locked exposure, locked white balance, locked focus**. iPhone 15 Pro+ ProRes, any modern Android in pro mode, or a small mirrorless camera in manual.
- 4K resolution minimum, 30fps, ideally 60fps.
- Cover the full room: walk in, around the bed, behind furniture, near each window, and out. 1–2 minutes of footage total.
- **Even motion** — no jerks, no rapid pans. Imagine a robot dollying.
- **Lights on, blinds in their everyday position.** Curtains drawn the way they normally hang.
- **No people in shot.** No moving objects.
- Capture twice: once with all lights on, once with daylight only. Two splats, two moods, same room.

**Option B — dense panorama grid**

- 12–20 panoramas instead of 4.
- 360° spherical (Insta360 X4 or Theta Z1, ~$500).
- Place the tripod on a roughly 1.5m grid covering all walkable floor area, including doorways and corners.
- Same exposure / WB / focus lock as above.
- Tripod height: eye level (~160cm).

Either option is **a few hours of on-site work**. Output goes onto a USB drive and arrives at the engineering team.

A future "Phase 2" for this project would be capturing exterior elevations (front facade, garden, street). For now, **room-1 is the pilot.**

### Designer (creative direction)

Your role is to define what "good" looks like and pick the polish layer.

- Decide the **mood**: bright daylight, golden hour, lights-on evening. The photographer captures one or all; you pick which version becomes the default.
- Pick the **outside-the-window HDRI**. Three Polyhaven CC0 candidates from the research:
  - `kloofendal_43d_clear_puresky` — clear blue sky, suburb-friendly latitude.
  - `dikhololo_night` — dusk / lit-window mood.
  - `quattro_canti` — overcast urban courtyard.
  - These are vibe matches, not geo-correct to Kumamoto. Choose by feel.
- Pick **PBR materials** for the small hand-built parts (light switch plate, possibly a window frame): from Poly Haven CC0 only. (Keyshot is replaced — see CTO section.)
- Approve the post-processing look: ACES filmic tonemapping, slight bloom, sharpening, vignetting. Each is a slider; designer picks values.

### CTO (technical lead)

Two architectural decisions that need your sign-off.

**Decision 1: room-1 leaves `ozu-test.html`.**
The single-HTML, no-bundler, three.js-r128-inlined setup served us well for the rest of the property and continues to work fine for those rooms. But it does not support modern browser tech (WebGPU, ESM imports, the splat library). Room-1 (and only room-1) moves to a small Vite + ESM project at `room-1-3d/` with its own `package.json`. The other rooms in `ozu-test.html` are unchanged. The two coexist; users navigate to room-1 via a chip from the existing platform hub.

**Decision 2: forked render path for AR.**
The Three.js WebGPURenderer gives us the highest visual quality (WebGPU compute shaders, TSL, real-time SSGI, MeshPhysicalNodeMaterial). But WebXR over WebGPU is **not yet supported on Quest 3** (the device most likely to be the AR target). So the AR session forces a WebGL2 fallback. Same scene, same code, smaller render feature set inside the AR session. **This is a real architectural cost** — every visual feature has to work on both paths.

**Stack you're approving:**

- **Renderer:** Three.js r184 with WebGPURenderer; WebGL2 fallback for AR sessions.
- **Splat library:** Spark 2.0 (Three.js plugin, MIT license, World Labs).
- **Path tracer (optional cinema render):** three-gpu-pathtracer + oidn-web (denoiser).
- **Build:** Vite (zero-config, hot reload, ESM out of the box).
- **Hosting:** static files on any CDN. No backend needed. Output is `<10 MB compressed`.
- **Splat training:** PostShot or gsplat on the local GPU box. Free.
- **Splat editing/cleanup:** SuperSplat (browser tool, CC0, no install).

**Stack you are NOT approving (rejected after research):**

- Keyshot — no browser-interactive output, paid license, asset library replaced by Poly Haven CC0.
- Babylon.js 9 — viable alternative but porting cost outweighs the gain for one room.
- NeRFs (Instant-NGP) — surpassed by Gaussian splatting for this use case.
- Splatter-360 — research code requiring 8×V100 to train; gsplat covers our needs.

### Devs (implementation)

Phased work, 4–5 weeks. Each phase ends with a demoable output.

1. **Phase 1 — Recapture verification** (1 day). Train a splat from the existing 4 panos. Verify it fails (it will). Decision artifact: side-by-side screenshot of trained splat vs original panos.
2. **Phase 2 — Recapture + train** (gated on photographer). Train a splat from the new capture. Output: a usable `.ply`.
3. **Phase 3 — Web sandbox** (1 week). Stand up `room-1-3d/` Vite project. Render the `.ply` with Spark in WebGPURenderer. Output: viewable URL on three devices.
4. **Phase 4 — Interactive layer** (3 days). Click-to-toggle light switch. Glass window with HDRI behind. Output: clickable demo.
5. **Phase 5 — AR mode** (3 days). WebXR on Quest 3 + Android Chrome. iPhone fallback (orbit-only). Output: live on-device demo.
6. **Phase 6 — Cinema render** (3 days, optional). Path-traced still on a "Render" button. Output: a 4K still rendered in <60 seconds.
7. **Phase 7 — SSGI + post** (3 days). Real-time global illumination. ACES tonemap. SMAA. Output: visual A/B vs Phase 4.
8. **Phase 8 — Mobile / LoD** (2 days). Spark `.RAD` streamed format. Output: mobile loads in <2 seconds on a 50 Mbps link.

### CEO / product

Three decisions. Each blocks downstream work until answered.

1. **Approve recapture.** A few hours of photographer/videographer time + a phone or 360° camera. This is the gating decision; without it, the project plateaus at "decent fake."
2. **Decide AR scope on iPhone.** Apple Safari does not support `immersive-ar` and has shown no signal of changing. Options:
   - **A)** Drop AR for iPhone users entirely. iPhone users get a high-quality 2D-screen orbit view. (Recommended; scope-tight.)
   - **B)** Fund a separate native iOS app using RealityKit + USDZ. Adds significant cost, a separate codebase, App Store review. Only pursue if the parent app on iPhone needs AR specifically for room-1.
3. **Approve the small build setup for room-1.** Costs nothing. Concept: room-1 leaves the single-HTML setup and gets its own Vite project at `room-1-3d/`. Keeps the rest of the property simple.

---

## Capture protocol — full version (for photographer/videographer)

This is the spec. Hand it to whoever does the recapture.

### Equipment

- **Best:** iPhone 15 Pro+ in ProRes mode, OR a mirrorless camera with manual controls (Sony A7C, Fuji X-T5, Canon R7).
- **Acceptable:** any modern Android with a "Pro" video mode + manual focus + manual WB.
- **Tripod or gimbal optional but recommended** for the panorama-grid option.
- **For panorama option:** Insta360 X4, Theta Z1, or equivalent 360° camera.

### Settings (lock all, do not change during capture)

- **Resolution:** 4K minimum, 30fps minimum, 60fps preferred.
- **Codec:** ProRes or H.265 high-bitrate. Avoid HEVC compression artifacts.
- **Exposure:** locked. Pick a value that doesn't blow out the windows or crush the shadows.
- **White balance:** locked. Match the natural daylight feel.
- **Focus:** locked at infinity (or hyperfocal distance for the room — about 2m).
- **ISO:** as low as possible without underexposing. ~ISO 100–400.
- **Stabilization:** off if on a tripod, on if handheld.

### Sequence (video option)

1. **Lights:** all on, blinds in everyday position, curtains as they normally hang.
2. Stand outside the door, looking in. **Start recording.**
3. Walk slowly into the room. **5 seconds per metre.**
4. Move along one wall, then another, then another, then back to the start.
5. Approach each window, both at standing height and crouching height (different parallax).
6. Walk past the bed on both sides. Stop briefly at each side.
7. Look up at the ceiling for 3 seconds. Look down at the floor for 3 seconds.
8. **Total duration: 60–120 seconds.**
9. Stop recording.
10. **Repeat with the lights off, daylight only.** Different mood, same path.

### Sequence (panorama-grid option)

1. Place a 1.5m × 1.5m grid covering the floor (use chalk, painter's tape, or a measuring tape).
2. At each grid intersection, set tripod, eye-level. Capture a full 360°.
3. Each panorama: 4–8 second exposure, locked settings.
4. Result: 12–20 panoramas covering the room.

### Don'ts

- Don't capture with people in shot.
- Don't capture with moving objects (curtains blowing, plants moving).
- Don't change focus mid-capture.
- Don't change exposure mid-capture.
- Don't capture with auto-WB.
- Don't compress / re-encode the footage before handing it to engineering.

---

## Asset library (for designer + devs)

All from Poly Haven (CC0, no attribution required) unless noted.

- **HDRIs (outside-the-window):**
  - `kloofendal_43d_clear_puresky` — clear sky.
  - `dikhololo_night` — dusk.
  - `quattro_canti` — urban overcast.
- **Hard surfaces (light switch, frame, etc.):**
  - `metal_plate_02` — switch plate.
  - `painted_metal_02` — window frame.
- **Soft surfaces (only if splat fails on bedding):**
  - `fabric_pattern_05`, `fabric_pattern_07`, `fabric_pattern_09`.
- **Wood (if needed):**
  - `wood_planks_grey` or use Three.js r180+ TSL Procedural Wood Material (no texture download).

Designer reviews and locks final list before Phase 4.

---

## Timeline + cost

### Cost

- **Software:** $0. Everything is free or CC0.
- **Cloud GPU (backup if local GPU is busy):** ~$5 per training iteration, $20–50 total over the project. Using RunPod A100 80GB at $1.29/hr or Vast.ai A100 80GB at $0.67/hr (as of 2026-05-06).
- **Equipment (if 360° camera not owned):** ~$500 for an Insta360 X4 or Theta Z1.
- **Total external cost ceiling:** ~$550.

### Time

- Recapture: a few hours of photographer time (one site visit).
- Engineering: 4–5 weeks of focused work assuming Phase 1 verifies recapture is needed.
- + 1 week if iPhone gets a separate native AR module.

### Critical path

```
[CEO approves recapture] ─┐
                          ├──► [Photographer captures] ──► [Phase 2 train splat] ──► [Phases 3–8]
[CTO approves Vite setup]─┤
[CTO approves WebGPU+AR fork]
```

Until the first three approvals land, engineering is on Phase 1 (training a verification splat from the current 4 panos) and a parallel Phase 3 (standing up the new build setup).

---

## Risks

1. **Recapture quality.** Even with a perfect protocol, the first capture might have issues (motion blur, exposure shift, lighting changes). Plan for one re-shoot.
2. **Glass window through a splat.** Manual workflow per window: cut splats around the window in SuperSplat, place a glass mesh, place HDRI behind. 30–60 minutes per window.
3. **iOS users get a downgraded experience.** Non-AR view is still high quality, but the AR pillar is dead on Apple's mobile platform until Apple changes course.
4. **WebGPU + WebXR is bleeding edge.** Quest 3 specifically does not implement WebXR over WebGPU. Forced WebGL2 fallback in AR mode is the architectural cost.
5. **The path-traced cinema render mode is optional.** Worth doing for marketing assets and high-end stills, not required for the core experience.
6. **Long-term maintenance.** Each major Three.js release (r184 → r185 → ...) requires re-testing. Plan for ~4 hours of upkeep per quarter.

---

## Open questions (for CEO before kickoff)

1. **Do iPhones need AR for this?** If yes, separate iOS native track. If no, simpler scope.
2. **Which mood is the default?** Lights-on evening, bright daylight, golden hour, or all three on a toggle.
3. **Does the experience need audio?** Ambient room tone, click feedback on the light switch, etc. Marginal scope.
4. **Where does this live?** Standalone URL or embedded in the parent gktk-prototype mobile app?
5. **Future rooms.** Once room-1 ships, the same pipeline applies to room-2, room-3, room-4, the LDK, the bathroom, etc. Each new room is ~2 weeks once the pipeline is built.

---

## Glossary (so any role can read this)

- **Gaussian splat / splatting** — a 2026 technique where photos are turned into a 3D cloud of millions of coloured ellipsoids ("Gaussians") that, viewed together, look photoreal. Apple Vision Pro spatial scenes use the same idea.
- **Three.js** — the open-source library most browser-based 3D experiences are built on. Free, MIT license.
- **WebGPU** — the new high-performance graphics API in browsers (replaces WebGL). Available on Chrome, Edge, Safari iOS 26+, Chrome Android. ~85% of the world has it.
- **WebGL2** — the older API. Slower but universal. Fallback path.
- **WebXR** — the browser standard for VR/AR. Works on Quest 3, Android Chrome. Not on iPhone Safari.
- **HDRI** — a high-dynamic-range environment image used as the "sky" or out-the-window scenery. Free from Poly Haven.
- **PBR** — physically based rendering. The way materials work in modern 3D: defined by colour, roughness, metalness, normal map, etc.
- **MeshPhysicalMaterial** — Three.js's high-end material with sheen, transmission (glass), clearcoat, etc.
- **TSL** — Three.js Shader Language. The new way to write custom material code; works on both WebGPU and WebGL2.
- **PostShot** — desktop tool that trains a Gaussian splat from a video or photo set. Free.
- **gsplat** — the open-source CUDA library underneath PostShot. Free.
- **SuperSplat** — browser-based editor for cleaning up trained splats. Free, no install.
- **Spark 2.0** — Three.js plugin that renders splats in a browser. Free.
- **Polyhaven** — CC0 asset library: HDRIs, PBR textures, models. Free, no attribution required.
- **`.ply`** — file format for the trained splat. Single file, ~50–500 MB depending on splat density.
- **`.RAD`** — Spark's streaming-LoD splat format. Splits the splat into HTTP-rangeable chunks for fast mobile loading.

---

*This brief was written 2026-05-06 from a research report citing 49 live sources. Re-validate cloud pricing if reading more than 30 days later. Re-validate Apple's WebXR stance if reading more than 6 months later.*
