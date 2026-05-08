# Flow: room-1 rendering, decoupled

> Just the look-and-feel story for room-1: materials, lighting, textures, glass, post-processing. No placement, no geometry. For where things sit in space see `flow-room-1-layout.md`. For the end-to-end picture see `flow-room-1-full.md`. The whole-property rendering flow lives at `../flow-ozu-1/flow-ozu-1-rendering.md`.

> See `glossary.md` in this folder for definitions of `MeshStandardMaterial`, `MeshPhysicalMaterial`, transmission, clearcoat, emissive, anisotropy, PBR, env map, PMREM, `EffectComposer`, the post-processing pass types, and hex colour syntax.

## 1. We started with flat colours and nothing else

The earliest version of the registerScene('room-1') block used plain `MeshStandardMaterial` with flat colours, no textures (source: `ozu-test/room-1-ONLY-rendering-plan.md`, "Walls + materials" section). Walls were a warm neutral grey `0xa9a59f` matching the real photos. There was no env map, no tone mapping, no shadow setup, no post-processing.

## 2. We turned on tone mapping

ACES filmic tone mapping was enabled when room-1 was the visible scene. ACES is a global brightness/contrast curve that compresses bright highlights so cream walls don't blow out white. Initial exposure was 0.85. That was washing colours out, so in a later session it was dropped to 0.55 (source: `room-1-ONLY-rendering-plan.md`, "Lighting + colour" section, exposure 0.55 noted).

The pipeline runs only while room-1 is the visible scene; the exterior and interior scenes fall back to the plain `renderer.render()` path (source: same plan, "Post-processing pipeline" section).

## 3. We built the indirect light from a procedural cube

Indirect light came from a procedural inside-out coloured cube baked into a cube-map via `THREE.PMREMGenerator`, used as `scene.environment` (source: same plan, "Lighting + colour" section). The cube provides realistic indirect bounce-light and reflections, fully offline. The procedural builder is a function called `buildRoom1EnvMap` (find it in `ozu-test.html` by searching for `buildRoom1EnvMap`).

This is what the cutting-edge plan plans to replace with a real HDRI in Phase 2b (source: `room-1-ONLY-cutting-edge-plan.md`, "2b" section).

## 4. We turned on max anisotropy on every PBR texture

All PBR textures (floor, dark wood, the procedural ceiling plank texture) were set to `renderer.capabilities.getMaxAnisotropy()`, which queries whatever the GPU's maximum anisotropy is (usually 16x). Without this, distant floor planks blur to mush at glancing angles (source: `room-1-ONLY-rendering-plan.md`, "Lighting + colour" section).

## 5. We added the sun and the fill light

A directional sun light (think: light coming from one direction, like the sun) was placed at the window direction, intensity 0.85, casting shadows with `shadow.radius = 6` for soft edges. A cool-tinted fill light (a second directional light, no shadows, dimmer, on the opposite side) was added on the cabinet-wall side, intensity 0.22 (source: `room-1-ONLY-rendering-plan.md`, "Lighting + colour" section).

## 6. We turned shadow casting off on the walls and ceiling

Walls and ceiling were excluded from shadow casting and receiving. This prevents x-ray silhouettes of furniture bleeding through the thin walls when the scene is viewed from outside the room cube (source: same plan, "Walls + materials" section). The floor still receives shadows so the sun beam visibly lands on it.

## 7. We added the ceiling

The ceiling got a weathered whitewashed plank texture, generated procedurally: wider shade variance, knots, grain, dark plank seams. Plus white crown moulding (source: same plan, "Walls + materials" section).

## 8. We added the glass on the windows

Real refractive glass via `MeshPhysicalMaterial` with `transmission` was put on the sliding window. Refractive means the light bends slightly as it passes through, so you can see what's beyond and the glass picks up the env map and gives proper specular highlights. Frosted glass (different roughness, different transmission settings) went on the narrow ac-wall privacy window (source: same plan, "Glass + windows" section).

The walls had been split into segments around each window hole during layout (see `flow-room-1-layout.md` step 6) so the glass would actually look through to what's beyond instead of looking at the wall behind it.

## 9. We added the backdrop planes outside the windows

Procedural Japanese-suburban backdrop planes were placed outside both windows so the windows had something to look at. A vertical mullion (the strip where two sliding panels of a hikichigai meet) was added on the sliding window. Glass and backdrop planes were excluded from shadow casting and receiving so the glass doesn't drop a hard shadow and the backdrops don't block the sun (source: same plan, "Glass + windows" section).

## 10. We polished the room one pass at a time

Commit 4367d66 ("ozu-test: room-1 polish: closed door, smooth walls, sunlight + shadows, light ceiling") was a polish pass that closed the entrance door, smoothed the wall geometry, tuned the sunlight and shadow setup, and lightened the ceiling colour (source: git short-sha 4367d66).

## 11. We rebuilt the pendant lamps

Pendant lamps were rebuilt as four linen-weave fabric shades on a wood crossbar. The shade material uses a procedural canvas texture: warp threads, weft threads, noise dots. The central hub is brass `MeshStandardMaterial` with metalness 0.85 (i.e. very metallic). Visible bulb spheres sit inside open-ended shade cylinders (the shade bottom is uncapped so the bulb is visible from below). The default state on first room-1 load is lamps off (`S.lampsOn = false`). A Lights button in the dock toggles the shade emissive (the shade glows), the bulb emissive (the bulb glows), and the bloom enabled state (the post-processing pass adds halo around the bright areas) (source: `room-1-ONLY-rendering-plan.md`, "Pendant lamps" section).

## 12. We added the post-processing pipeline

An `EffectComposer` was wired up with three passes in order: `RenderPass` (draws the 3D), then `UnrealBloomPass` (adds glow around bright areas), then `SMAAPass` (smooths jagged edges) (source: same plan, "Post-processing pipeline" section). Bloom is enabled only when the lamps are on. The pipeline runs only while room-1 is the visible scene.

## 13. We hit a blocker: the SMAA shader source was missing

The SMAA pass crashed on construction. The `SMAAPass` class itself had been inlined but the companion shader source (`SMAAEdgesShader`, `SMAAWeightsShader`, `SMAABlendShader`, three small text files of GPU code that the pass reads at startup) was missing.

This was fixed in commit 579f287 ("ozu-test: SMAA shader inlined; room-1 photo-match pass") by inlining the shader source so the constructor stops crashing (source: git short-sha 579f287, also `room-1-ONLY-rendering-plan.md`, "Post-processing pipeline" section).

## 14. We added the AC unit, switches, intercom, doorknob, hooks

Small fixtures got their own materials in pass:

- AC unit: white body, bottom louver flap hanging slightly below and forward, recessed darker grille on the front face, dark vent slit, no standby LED (the real Toshiba in the photo doesn't show one).
- Light switch plate on the entrance-wall: white with rocker button.
- Intercom panel below the AC unit: white plate, small dark button.
- Entrance door: white panel with a chrome round doorknob (escutcheon, stem, sphere).
- Coat hook rail near the entrance corner: two black peg hooks on a whitewashed wood-plank base.
- Curtains either side of the sliding window: cream, hourglass-bunched, with a tieback ring.

Source: `ozu-test/room-1-ONLY-rendering-plan.md`, "AC unit" and "Furniture detail" sections.

## 15. We addressed jaggy edges and wired the PBR textures

Commit 4756f6e ("ozu-test: master plan phases 5–6 + audit fixes; room-1 jaggy fix + Phase 3 textures") did two things for rendering. First, a jaggy-edge fix on room-1 (source: git short-sha 4756f6e). Second, Phase 3a hard-surface textures got wired in (source: `room-1-ONLY-cutting-edge-plan.md`, "3a" section).

The PBR sets at `ozu-test/room-1-textures/` are:

- `wood_floor/`: diffuse (colour image), roughness, normal (surface bump map). Wired into the floor.
- `dark_wood/`: same three image types. Wired into the desk top, beam, and other dark-wood surfaces.

A small `loadPBR(name)` helper reads `_diff.jpg`, `_rough.jpg`, `_nor_gl.jpg` from a folder and returns `{ map, roughnessMap, normalMap }`. `texture.repeat` is set per surface to give real-world scale (e.g. ~0.6 m per repeat for floor planks, so a 6 m-long room shows ~10 visible plank lengths). `map` uses `sRGBEncoding` (the standard format for colour images on the web), `roughnessMap` and `normalMap` use `LinearEncoding` (raw values, not gamma-corrected). `texture.anisotropy` is the GPU's max (source: `room-1-ONLY-cutting-edge-plan.md`, "3a" section).

## 16. We tried PBR walls and rejected them

A third PBR set at `ozu-test/room-1-textures/painted_plaster_wall/` was tried on 2026-05-05 and rejected. The bumpy plaster look did not match the room-1 photos: the real walls are a smooth modern painted finish. The walls are now intentionally flat colour and the painted_plaster_wall folder was removed (source: `room-1-ONLY-cutting-edge-plan.md`, "Audit findings" section).

## 17. Where the rendering sits today

What is live and working:

- ACES filmic tone mapping at exposure 0.55, only when room-1 is visible.
- Procedural cube-map env, used as `scene.environment`, baked via `PMREMGenerator`.
- All PBR textures at max anisotropic filtering.
- Window-direction sun (intensity 0.85, soft shadows radius 6) plus cool-tinted fill (intensity 0.22, no shadows).
- Walls and ceiling don't cast or receive shadows. Floor does.
- Refractive glass on the sliding window. Frosted glass on the privacy window.
- Procedural suburban backdrop planes outside both windows.
- Pendant lamps with linen-weave shades, brass hub, visible bulbs, off by default, toggleable.
- Post-processing: `RenderPass` then `UnrealBloomPass` then `SMAAPass`. Bloom only when lamps are on.
- PBR textures on floor (wood_floor) and desk plus beam (dark_wood).

What is planned next, in order, by the cutting-edge plan:

1. TAA anti-aliasing (Phase 1): replaces SMAA with TAA in the composer. TAA averages multiple slightly-shifted snapshots over 8 frames for effectively perfect edges on a still scene.
2. RectAreaLight window sunbeam (Phase 2a): replaces the directional sun with a rectangle the size of the window pane, giving a soft accurate sunbeam shape on the floor.
3. Real HDRI environment (Phase 2b): downloads a Polyhaven CC0 HDRI into `ozu-test/hdri/`, loads via `RGBELoader` then `PMREMGenerator`, replaces the procedural env map and the backdrop planes with one real photograph.
4. God-rays cone (Phase 2c): adds a soft additive cone of light streaming from the window into the room.
5. Soft cloth shader (Phase 3b): a sheen term injected via `onBeforeCompile` on pillows, sheet, curtains, lamp shades. Plus a procedural fabric-weave normal map. Sheen is the velvet-edge highlight you see at the rim of any soft pillow under directional light.
6. Per-material polish (Phase 3c): final tuning of doorknob, intercom, AC unit, light switch roughness.

Source: `ozu-test/room-1-ONLY-cutting-edge-plan.md`, "Order" section.

## How to repeat this rendering flow on the next property or room

The repeatable rendering sequence. Run these in order, hard-reload after each step, judge against the photos before moving on. No batching (source: `room-1-ONLY-cutting-edge-plan.md`, "Strict rules" section).

1. Start with plain `MeshStandardMaterial` flat colours pulled from the panorama photos (use any image viewer's eyedropper to sample colours from the panorama; or just guess and tune from there).
2. Turn on `ACESFilmicToneMapping` only while the room is the visible scene. Start at exposure 0.55, tune from there. If the cream walls blow out white, drop the exposure further.
3. Bake a procedural env map (or load a Polyhaven HDRI) via `PMREMGenerator`, assign to `scene.environment`. The procedural option is offline-ready; the HDRI option looks more realistic but needs a one-time download.
4. Set every PBR texture's anisotropy to `renderer.capabilities.getMaxAnisotropy()`.
5. Add a directional sun in the window direction with soft shadows. Set `shadow.radius = 6` for soft edges. Add a cool-tinted fill light from the opposite side, no shadows, ~25% of the sun's intensity.
6. Set walls and ceiling to neither cast nor receive shadows (`mesh.castShadow = false`, `mesh.receiveShadow = false`). Keep the floor as a shadow receiver.
7. Add real refractive glass via `MeshPhysicalMaterial` with `transmission: 0.95-1.0`, `roughness: 0.05-0.1` for clear windows. For frosted variants, use `roughness: 0.5-0.7` and adjusted thickness. The exact values for frosted are not pinned in the source; tune by eye.
8. Place backdrop planes outside each window so the glass has something to look at.
9. Add pendant lamps, AC unit, switches, intercom, doorknob, curtains, hooks one fixture at a time. Each fixture gets its own material. Hard reload after each fixture.
10. Add an `EffectComposer` post-processing pipeline: `RenderPass` then `UnrealBloomPass` then `SMAAPass` (or TAA if going cutting-edge). Inline the shader source for any pass that needs companion shaders or it will crash on construction. SMAA needs `SMAAEdgesShader` plus `SMAAWeightsShader` plus `SMAABlendShader`. TAA needs `CopyShader` plus `SSAARenderPass` plus `TAARenderPass`.
11. Wire PBR texture sets folder-by-folder via a small `loadPBR(name)` helper. The texture folder must contain three files matching the names `<name>_diff.jpg`, `<name>_rough.jpg`, `<name>_nor_gl.jpg`. Set per-surface `texture.repeat` to real-world scale. `map` uses `sRGBEncoding`; `roughnessMap` and `normalMap` use `LinearEncoding`.
12. Test PBR on every surface but be willing to reject and stay flat-colour if the PBR set does not match the photo. The `painted_plaster_wall` reject is the worked example: real walls were smooth modern paint, the PBR set was bumpy plaster, the PBR was removed.
13. Pause and judge after each pass. Hard reload. No batching.

## Gaps i could not source

- The exact tone-mapping exposure history (0.85 then 0.55) is summarised in the rendering plan but the per-step intermediate values are not. The handoffs around the "washing out" session would fill this in.
- The exact moment the procedural env map was added is not in any commit message I read. It is described as live in `room-1-ONLY-rendering-plan.md`, "Lighting + colour" section. The original commit that added `buildRoom1EnvMap` was not isolated.
- The frosted-glass roughness and thickness values that landed are not pinned in the rendering plan; only that the "1.0 / 0.25" trial overshot to a "heavy fog" look (source: `room-1-ONLY-rendering-plan.md`, "Phase E" section).
- The exact pendant-lamp commit is not isolated. The rebuild is summarised in the rendering plan but spans more than one commit.
