# ROOM-1 ONLY — cutting-edge rendering plan (focused quality pass)

> **SCOPE: ROOM-1 ONLY.**
>
> This plan applies **only** to the standalone `room-1` 3D scene at
> `registerScene('room-1', ...)` inside `ozu-test.html`, plus the
> `buildRoom1Composer` function and the renderer-bootstrap step where
> the RectAreaLight uniforms library has to be initialised.
>
> The exterior facade scene and the multi-room interior scene are
> **off-limits** during this work, even on a sweep.
>
> See [room-1-ONLY-rendering-plan.md](room-1-ONLY-rendering-plan.md) for the
> broader room-1 roadmap. This plan is the focused cutting-edge
> quality pass that fixes the three current problems below.
>
> **Last updated:** 2026-05-05.

## Problems we are solving

1. **Pixelation / jagged edges.** Even after MSAA 8× + SMAA, the
   edges on bed rails, AC unit, window mullion, and closet seams
   still look jagged.
2. **Natural and artificial light.** The room reads "lit from
   everywhere" rather than from a clear sun direction. Lamp toggle
   works but does not sell as real glow.
3. **Real-world textures (hard and soft).** Walls, floor, desk,
   pillows, sheet, and curtains are mostly flat colours or weak
   procedural textures.

## Constraints (must hold)

- Three.js r128, inlined into `ozu-test.html`. No bundler, no
  build step.
- Works fully offline once any external assets are saved into
  `ozu-test/`.
- Only the `registerScene('room-1', ...)` block, the
  `buildRoom1Composer` function, and one line in the renderer
  bootstrap may change.

## Audit findings (verified by reading the actual file 2026-05-05)

**Already inlined and working:**
- `EffectComposer`, `ShaderPass`, `RenderPass`, `UnrealBloomPass`,
  `SMAAPass`, `SMAAShader`, `PMREMGenerator`.

**Current room-1 post-processing pipeline:**
- MSAA 8× WebGLMultisampleRenderTarget → RenderPass →
  UnrealBloomPass → SMAAPass.

**Important catch we missed before:**
MSAA 8× only helps the RenderPass output. After MSAA resolves,
bloom and SMAA run on a single-sample buffer. Bloom on bright edges
introduces fresh sub-pixel variance that SMAA alone cannot fully
remove. This is the likely root cause of the "still jagged" report.

**Texture assets** at `ozu-test/room-1-textures/`:
- `wood_floor/` — diffuse + roughness + normal (floor) — ✅ wired
- `dark_wood/` — diffuse + roughness + normal (desk / beam) — ✅ wired
- ~~`painted_plaster_wall/`~~ — REMOVED. Tried 2026-05-05; the bumpy
  plaster look did not match the room-1 photos (real walls are smooth
  modern painted finish). Walls are intentionally flat color — see
  Phase 3a below.

**No HDRI files** in the project — Phase 2b would need a one-time
download into `ozu-test/hdri/`.

**Cross-file dependencies (the trap that bit us with SMAAShader):**
- `TAARenderPass` extends `SSAARenderPass`, which depends on
  `CopyShader`. Three files must be inlined in order:
  `CopyShader.js` → `SSAARenderPass.js` → `TAARenderPass.js`.
- `RectAreaLightUniformsLib.init()` must run **after** the renderer
  exists but **before** any material the light touches is built.
  The previous attempt failed because the order was wrong.

---

## Phase 1 — Anti-aliasing upgrade (TAA)

**Goal:** edges look effectively perfect on a still orbit camera.

**Plain language:** the current edge-smoothing is two layers but
the second layer is doing all the work alone. Add a third layer
(TAA) that takes ~8 ever-so-slightly-shifted snapshots over 8
frames and averages them. On a still scene the result is near-perfect
edges, beyond what MSAA 32× would give.

**What we change:**
1. Splice 3 vendor files into `ozu-test.html` as a new `<script>`
   block in dependency order: `CopyShader.js` →
   `SSAARenderPass.js` → `TAARenderPass.js`. Place between the
   existing inlined `SMAAShader` block and the project script.
2. In `buildRoom1Composer` (lines 3161-3187):
   - Keep the MSAA 8× WebGLMultisampleRenderTarget.
   - Drop `SMAAPass` from the composer.
   - Replace it with `new THREE.TAARenderPass(scene, camera)`,
     `unbiased = true`, `sampleLevel = 2` (= 4 jittered samples).
   - Keep `RenderPass` first, `UnrealBloomPass` second.
3. Update `resizeRoom1Composer` to call the TAA pass `setSize`.

**Risk:** TAA shows brief ghosting if the camera moves, then
re-converges within ~8 frames. On orbit-around-a-still-target this
is invisible. On a sudden chip jump there may be a 1-2 frame flicker.

**Rollback:** put `SMAAPass` back in the composer, ~30 seconds.

**Stop, hard reload, judge.**

---

## Phase 2 — Real lighting (sub-steps 2a → 2b → 2c)

**Goal:** it feels like sunlight is streaming through the window
from a clear direction, not glowing from everywhere.

### 2a — Window-shaped sunbeam (RectAreaLight, fixed)

**Plain language:** swap the current "point of sun" for an actual
rectangle the size of the window pane. Soft, accurate sunbeam
shape on the floor.

**What we change:**
1. Inline `RectAreaLightUniformsLib.js` (~52 lines, no extra deps)
   after the SMAAShader block.
2. Call `THREE.RectAreaLightUniformsLib.init()` **immediately
   after** `renderer = new THREE.WebGLRenderer(...)` in the project
   bootstrap, before any `registerScene` runs. This is the order
   fix that the previous attempt got wrong.
3. In room-1's lighting block, add a `RectAreaLight` matched to
   the sliding-window pane (~1.19 m × 0.9 m), positioned just
   outside the window plane, oriented to face the room interior.
   Reduce the existing `DirectionalLight` intensity by ~50% so the
   total light isn't doubled.

**Risk:** if init order is still wrong, same failure as before.
If it works, expect a noticeable rectangle of bright floor where
the window beams in.

**Rollback:** delete the RectAreaLight, restore DirectionalLight
intensity.

**Stop, hard reload, judge.**

### 2b — Real HDRI environment

**Plain language:** replace the procedurally-coloured cube that's
lighting the room with a real photograph of the sky and surroundings.
The same image becomes the view through the windows **and** the
indirect light source — they match because they are literally the
same data.

**What we change:**
1. Download one CC0 HDRI from Poly Haven (suburban afternoon, e.g.
   `kloppenheim_06_puresky_2k.hdr`, ~6 MB) into
   `ozu-test/hdri/`.
2. Inline `RGBELoader.js` (~120 lines) as a new `<script>` block.
3. In the room-1 build, replace the procedural env map IIFE
   (`buildRoom1EnvMap`) with: `RGBELoader → PMREMGenerator →
   scene.environment AND scene.background`.
4. Remove the procedural buildings backdrop planes — the HDRI
   replaces them as the "view through the windows".

**Risk:** the HDRI must be downloaded once; we're not breaking the
offline rule (the asset is local after download). HDRI as
`scene.background` may compete with a future skydome — but room-1
doesn't have one, so this is clean.

**Rollback:** restore `buildRoom1EnvMap` and the buildings backdrop
planes.

**Stop, hard reload, judge.**

### 2c — Visible god-rays through the window

**Plain language:** the sunbeam from 2a hits the floor in a
rectangle, but you don't yet see the *beam* in the air — the
golden-hour haze. Add a soft cone of light streaming from the
window into the room.

**What we change:**
1. In room-1's build, after the RectAreaLight, add a
   `ConeGeometry` sized to the window opening, oriented along the
   sun direction, with `MeshBasicMaterial({ color: 0xfff4d6,
   transparent: true, opacity: 0.10, blending:
   THREE.AdditiveBlending, depthWrite: false })`.
2. Add a soft vertex-colour alpha gradient so the cone fades to
   nothing at its base and tip.
3. Exclude the cone from shadow casting/receiving.

**Risk:** if too opaque, looks like a fog volume. Tunable.

**Rollback:** delete the cone mesh.

**Stop, hard reload, judge.**

---

## Phase 3 — Real-world textures (sub-steps 3a → 3b → 3c)

**Goal:** surfaces look like real materials, not painted plastic.

### 3a — Hard surfaces (floor, desk, beam) ✅ DONE

**Status:** floor (`wood_floor`) and desk (`dark_wood`) wired up.
**Walls intentionally left as flat color** — the painted_plaster_wall
PBR set we had was too rough, did not match the smooth modern
painted finish in the room-1 photos. See audit findings above.

**What we change:**
1. Add a small `loadPBR(name)` helper that takes a folder name and
   returns `{ map, roughnessMap, normalMap }` from the matching
   `_diff.jpg`, `_rough.jpg`, `_nor_gl.jpg`.
2. Wire results into the wall materials (`matWall_xW`, `matWall_zD`,
   etc.) using `painted_plaster_wall`.
3. Wire `wood_floor` into the floor material.
4. Wire `dark_wood` into the desk top, beam, and any other dark-wood
   surfaces.
5. Set `texture.repeat` per surface so the texture appears at
   real-world scale (~1.5 m per repeat for plaster, ~0.6 m per
   repeat for floor planks).
6. Set `texture.anisotropy` to
   `renderer.capabilities.getMaxAnisotropy()` for sharpness at
   glancing angles.
7. Make sure `map` uses `sRGBEncoding` and `roughnessMap` /
   `normalMap` use `LinearEncoding` (default).

**Risk:** wrong UV scale looks stretched or tiny. Tuning is fast
and visible immediately.

**Rollback:** clear `map`, `roughnessMap`, `normalMap` on each
material.

**Stop, hard reload, judge.**

### 3b — Soft surfaces (pillows, sheet, curtains, lamp shades)

**Plain language:** cloth has a "velvet edge highlight" you can see
at the rim of any soft pillow under directional light. r128's
materials do not include this by default. Inject it via a small
shader patch on top of the existing pillow / sheet / curtain
materials.

**What we change:**
1. Define `applyClothShader(material, sheenColor, sheenStrength)`
   that uses `material.onBeforeCompile = ...` and injects a sheen
   term (Charlie BRDF, the same model r140+ uses natively) into
   the fragment shader.
2. Apply to: white pillow material, dark accent pillow, sheet,
   left curtain, right curtain, both lamp shade materials.
3. Generate a procedural fabric-weave normal map via canvas (no
   download needed) — fine warp/weft pattern. Apply to all soft
   materials.

**Risk:** sheen too strong = pillows look glittery. Tunable.
`onBeforeCompile` patching of `MeshStandardMaterial` is
well-trodden in r128; low structural risk.

**Rollback:** delete the `onBeforeCompile` assignment, clear
`normalMap`.

**Stop, hard reload, judge.**

### 3c — Final per-material polish

**Plain language:** after 3a + 3b, specific surfaces will look off.
Adjust roughness on the doorknob, intercom, AC unit body, light
switch, etc. Small targeted tweaks, no new technology.

**Stop, hard reload, judge. Done.**

---

## Order

1. Phase 1 — TAA (single change, biggest universal impact)
2. Phase 2a — RectAreaLight (fixes a known prior failure)
3. Phase 2b — HDRI environment
4. Phase 2c — god-rays
5. Phase 3a — hard PBR textures
6. Phase 3b — soft cloth shader
7. Phase 3c — per-material polish

**Hard reload + judge between every step. No batching.**

## Strict rules

- Only touch the `registerScene('room-1', ...)` block, the
  `buildRoom1Composer` function, and the one renderer-bootstrap
  line for `RectAreaLightUniformsLib.init()`.
- Do not touch the exterior or interior scenes.
- Stay on three.js r128. Keep three.js inlined. New vendor files
  are inlined as new `<script>` blocks AFTER the three.js bundle
  and BEFORE the project script.
- Plain language status reports.
- One change at a time. The user reloads, then I move to the next
  step.
- Commit after each phase the user accepts.

## Trade-off matrix

| What you get | Cost | Phase |
|---|---|---|
| Effectively perfect edges on a still scene | TAA 4-frame accumulate, tiny GPU cost | 1 |
| Real-shaped sunbeam patch on the floor | RectAreaLight + uniforms init | 2a |
| Sky and sun visible through windows + matching indirect light | One HDRI download (~6 MB), env-map swap | 2b |
| Visible light shafts streaming through the window | One additive cone mesh | 2c |
| Walls, floor, desk look like real materials | Wire existing texture files | 3a |
| Pillows, sheet, curtains read as cloth | Sheen shader patch + procedural weave | 3b |
| Per-surface fine-tune | Manual roughness/normal-strength adjustments | 3c |
