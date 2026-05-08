# Flow: Ozu-1 property rendering, decoupled

> Just the look-and-feel story for the Ozu-1 property: materials, lighting, textures, glass, post-processing across exterior + interior. No placement, no geometry. For where things sit see `flow-ozu-1-layout.md`. For end-to-end see `flow-ozu-1-full.md`. The standalone room-1 sandbox rendering flow lives at `../flow-room-1/flow-room-1-rendering.md`.

> See `glossary.md` in this folder for definitions of `MeshStandardMaterial`, `MeshPhysicalMaterial`, clearcoat, transmission, emissive, PBR, env map, PMREM, the four light types, and hex colour syntax.

## 1. We started flat-colour for everything except room-1

In the early Ozu-1 build, only the room-1 standalone sandbox had cinematic rendering (ACES tone mapping, PMREM env map, post-processing). The exterior registerScene block and the multi-room interior registerScene block used plain `MeshStandardMaterial` with flat colours and the renderer's default tone mapping (source: `ozu-test/master-plan.md`, "Phase 7.5" section, "ACES filmic tone mapping applied globally (was room-1 only)").

This was deliberate: room-1 was a sandbox for cutting-edge experiments, the rest of the property was production at "good enough" quality.

## 2. We unified the wall geometry, which forced shared materials

Commit 0046b8b ("unify exterior + interior wall geometry, add cladding split") merged the exterior and interior wall builders (source: git short-sha 0046b8b). Once geometry was shared, the materials had to be shared too. A `wallMat` constant (`0xeeeae3`, cream) became the single source for outer walls' inner finish across both scenes.

## 3. We added two-layer cladding with the brown panel inset

Commit 4e735e7 ("2-layer outer walls, brown panel inset, LDK polish, room-4 build") added the outer cladding face plus the inner finish face for outer walls (source: git short-sha 4e735e7). The brown wood panel ground-floor inset uses its own `matLower` material against the cream `matUpper` for the upper section.

## 4. We worked through master-plan phases 1 to 6 with mostly-flat materials

Through phases 1 to 6 of the master plan, rendering stayed mostly flat-colour. Ceilings were added (Phase 1) but as flat plaster. Doorways got the right shape (Phase 2) but generic `doorMat` colour. The genkan, 2F toilet, stairs, and exterior polish (Phases 3 to 6) shipped on flat materials. Phase 4 added a frosted-privacy-window detail in the 2F toilet (source: `ozu-test/master-plan.md`, phases 1 through 6 sections, all done).

The materials at this stage were chosen to read well against the panoramas but with no PBR maps and no global env map.

## 5. We ran a multi-agent audit and applied presentation-fidelity quick wins

On 2026-05-06 a deep multi-agent audit ran against 2026 architectural-visualisation standards. Phase 7.5 applied the wins (source: `ozu-test/master-plan.md`, "Phase 7.5" section).

The wins, in order of impact on the rendered look:

**Tone mapping went global.** ACES filmic tone mapping had been on for room-1 only. It was extended to the exterior and interior scenes too. Highlights stopped clipping on cream walls. (ACES is a global brightness/contrast curve that compresses bright highlights so cream walls don't blow out white.)

**The PMREM env map went global.** A procedural inside-out coloured cube baked through `THREE.PMREMGenerator` had been room-1 only. It was extended to the exterior and interior scenes as `scene.environment`. Metals now reflect indirect light in every scene.

**Interior shadows turned on.** The `DirectionalLight` casts shadows now. Every solid mesh has `castShadow = true` and `receiveShadow = true`. Plus an indoor `HemisphereLight` was added for sky/floor bounce.

**Ceramics upgraded to clearcoat.** Toilets and basins (the `matToilet` material; find it by searching `ozu-test.html` for `matToilet`) were swapped from `MeshStandardMaterial` to `MeshPhysicalMaterial` with clearcoat. They now render as glazed porcelain instead of matte plaster.

**Whitewashed wood-plank ceiling texture applied.** The flat-plaster ceilings got a procedural whitewashed wood-plank texture matching the photos' dominant ceiling material.

**Two warm-white PointLights at the LDK back-wall windows.** Approximating daylight streaming in. This is a placeholder for proper RectAreaLights, which need an extra inlined uniforms library.

Source: `ozu-test/master-plan.md`, "Phase 7.5" section, all marked status: done.

## 6. We did a photo-fidelity colour pass

Phase 7.6 closed visible mismatches between the build and the room photos. Each item was a small material-level change (source: `ozu-test/master-plan.md`, "Phase 7.6" section).

**Brick recolour.** Brick accent walls went from warm-brown (`0x5e4a3d`) to cool grey-white (`0x9a9a96`). Matches the cool grey-white brick plus white mortar visible in the LDK and 1F-toilet photos.

**Laundry brick removed.** The laundry "brick" feature wall was removed entirely. Photos showed plain painted wall, not brick. The vanity wall reverted to default cream paint.

**Toilet floors changed.** 1F and 2F toilet floors went from lavender-purple flat colour (`0xd6cbe0`) to warm light wood plank (`0xc4a888`) using the same procedural plank texture used in the bedrooms.

**LDK pendants got warm-glow emissive.** The sphere shades over dining and sofa now read as lit pendants instead of cold dark spheres.

**Door hardware upgraded to chrome.** Bi-fold closet door pulls and hinged door handles went from matte grey (`0x9a9a9a`, metalness 0.5) to chrome (`0xc8cdd2`, metalness 0.85, roughness 0.18) per photos.

**Bi-fold seam darkened.** The centre seam went from bronze tone (`0x8a7a66`) to a recessed shadow (`0x4a4a4a`). Was reading as a fake bronze strip, now reads as a real fold line.

## 7. We added the painted trim layer

Phase 7.7 added the trim layer that real JP residential interiors all have. One shared off-white `trimMat` (`0xfafaf6`) for visual consistency (source: `ozu-test/master-plan.md`, "Phase 7.7" section).

The materials covered:

- Door casings (architrave / 飾り枠) on all 14 doors via the upgraded `addDoor` helper. Four trim strips per door (two vertical jambs, one top header, on each face of the wall). 70 mm wide and 12 mm proud (sticking out from the wall surface).
- Baseboards (巾木) in all four 2F bedrooms. 70 mm tall strip along the floor perimeter.
- Crown moulding (回り縁) in the same four bedrooms. 50 mm strip at the ceiling line.
- The shared helper `addRoomTrim(...)` makes the trim material reusable for any future room.

## 8. We painted the bedroom walls a per-room colour

Phase 7.8 fixed the bedroom wall colour. Photos showed all four 2F bedrooms have taupe-grey walls (~`0x8e857a`), not the global cream `wallMat` (`0xeeeae3`) used elsewhere (source: `ozu-test/master-plan.md`, "Phase 7.8" section).

The shared `wallMat` couldn't be tinted per-room without refactoring the wall builders. The fix was a thin paint overlay on the interior face of each bedroom's walls. A new helper called `addRoomPaint2F` (the master plan refers to it as `addBedroomWallPaint`; the actual code calls it `addRoomPaint2F`. Find it by searching `ozu-test.html` for `function addRoomPaint2F`) paints all four interior wall faces with door and window x-ranges punched out. The paint Y range sits between the existing baseboard and crown bands so the trim still reads as a separate layer. Applied to room-1, room-2, room-3, and room-4.

## 9. We rebuilt the front door materials

Phase 7.9 rebuilt the genkan front door materials. The previous version was a flat tan box (`doorMat 0xb89878`). The rebuild has seven elements with their own materials (source: `ozu-test/master-plan.md`, "Phase 7.9" section).

- Lower brown panel.
- Upper charcoal panel.
- Vertical glass slit (transmission glass via `MeshPhysicalMaterial`).
- Chrome grip pull.
- Brushed kickplate.
- Mail slot.
- Transom.
- Casing (matches the shared off-white `trimMat`).

## 10. Where the rendering sits today

What is live and working:

- ACES filmic tone mapping applied globally (exterior + interior + room-1).
- Procedural PMREM environment map applied globally as `scene.environment`.
- Interior shadows enabled. `DirectionalLight` casts. Every solid mesh casts and receives. Plus indoor `HemisphereLight` for sky/floor bounce.
- `MeshPhysicalMaterial` with clearcoat on ceramics (toilets, basins).
- Whitewashed wood-plank procedural ceiling texture.
- Two warm-white `PointLights` at LDK back-wall windows (placeholder for RectAreaLights).
- Brick accent in cool grey-white. Laundry brick removed.
- Toilet floors as warm light wood plank.
- LDK pendants with warm-glow emissive.
- All door hardware in chrome.
- Bi-fold seams as recessed shadow.
- Off-white `trimMat` on door casings, baseboards, and crown moulding (4 bedrooms + 14 doors).
- Bedroom walls painted taupe-grey via overlay (room-1, room-2, room-3, room-4).
- Front door rebuilt with seven distinct materials.
- Smoke detectors on 2F bedroom ceilings and stair top.
- 2F toilet picture frame on the east wall (was west).

Source: `ozu-test/master-plan.md`, phases 7.5 through 7.9 sections, all status: done.

What is still open or deferred:

- LDK and corridor trim: deferred (irregular shapes need a polygon-based perimeter helper).
- Brick texture on brick accent walls: deferred (high risk of looking worse than the current flat colour).
- Kitchen detail materials (sink, faucet, cooktop, range hood, fridge, upper cabinets, subway tile): complex, not started.
- Proper RectAreaLights at the LDK windows to replace the placeholder PointLights: needs an inlined uniforms library.

Source: `ozu-test/master-plan.md`, "Exterior" + "Phase 7.6 Deferred" + "Phase 7.7 Deferred" sections.

## How to repeat this rendering flow on the next property

The repeatable rendering sequence for any whole-property build. Run these in order **after** the layout flow has produced a property full of flat-coloured rooms. Hard-reload after each step. Compare against the panoramas before moving on.

1. Confirm the layout is done. Walls, windows, doors, floors, ceilings, furniture all placed. Materials are still placeholder flat-colour.
2. Define one shared `wallMat` for the global wall finish (cream-ish for JP residential, e.g. `0xeeeae3`).
3. Define one shared `trimMat` for door casings, baseboards, and crown moulding (off-white, e.g. `0xfafaf6`).
4. Define the materials registry. At minimum: `doorMat`, `closetDoorMat`, `matToilet`, `matLower` (cladding lower), `matUpper` (cladding upper), `FLOORS.room`, `FLOORS.room4`, `FLOORS.toilet`, etc. One named material per visually distinct surface family.
5. Apply ACES filmic tone mapping globally to every registerScene block (exterior + interior + any sandbox). Set `renderer.toneMapping = THREE.ACESFilmicToneMapping` and `renderer.toneMappingExposure = 1.0` initially. Tune from there.
6. Bake a procedural PMREM environment map and assign as `scene.environment` on every scene. Or load a Polyhaven HDRI for a more realistic look. Either way, do it globally.
7. Turn on interior shadows. `DirectionalLight.castShadow = true`. Every solid mesh sets `castShadow` and `receiveShadow`. Hard reload, check that shadows fall sensibly.
8. Add an indoor `HemisphereLight` with a sky colour at the top and a floor colour at the bottom for general bounce-fill.
9. Use `MeshPhysicalMaterial` with `clearcoat: 1.0`, `clearcoatRoughness: 0.05` for ceramics (toilets, basins, glazed tile). The base colour is still ceramic-white.
10. Use a procedural whitewashed wood-plank texture for ceilings (matches JP residential photos). The same texture function can be reused for toilet floors.
11. Place warm-white `PointLights` at major windows as a daylight placeholder. Upgrade to `RectAreaLight` later when the inlined `RectAreaLightUniformsLib` is wired.
12. Walk every wall, every accent surface, every fixture against the panoramas. Make a list of mismatches. Fix them one at a time. Compare colours via image-viewer eyedropper if precise; eyeball if approximate.
13. JP-residential conventions to check: brick is usually cool grey-white, not warm-brown. Toilet floors are usually warm wood plank, not lavender. Pendant lights need warm-glow emissive or they read as cold dark spheres. Door hardware should be chrome (`metalness 0.85, roughness 0.18`), not matte grey. Bi-fold seams should be a recessed shadow (`0x4a4a4a`), not a bronze metallic strip. Adjust for non-JP properties as appropriate.
14. Add the trim layer with one `addRoomTrim` helper covering baseboards, crown, and door casings. Apply to every clean rectangular room. Defer irregular rooms until you write a polygon-based perimeter helper.
15. Per-room wall colours that differ from the global `wallMat` need an overlay helper, not a `wallMat` refactor. Use `addRoomPaint2F` for 2F rooms (write `addRoomPaint1F` if needed). Paint sits at Y range `[yFloor + baseboard_height, ceilH - crown_height]` so trim reads as a separate layer.
16. Front doors look bad as flat tan boxes. Rebuild with multiple distinct materials: lower panel, upper panel, glass slit (with transmission), chrome grip pull, brushed kickplate, mail slot, transom, casing.
17. (JP-specific.) Add smoke detectors on bedroom ceilings and stair tops. Mandatory per 消防法.
18. (Optional, when a registerScene block needs cinematic quality.) Wire an `EffectComposer` post-processing pipeline (`RenderPass` then `UnrealBloomPass` then `SMAAPass`) for that scene only. Gate the pipeline so it runs only when that scene is the visible scene; the others fall back to plain `renderer.render()`. See `flow-room-1-rendering.md` for the detailed setup.
19. Pause and judge after each step. Hard reload. No batching.

Steps that are JP-residential-specific (skip or adapt for non-JP properties): step 13's recolour conventions, step 17 smoke detectors. The rest applies to any architectural-visualisation build.

## How this rendering flow relates to the room-1 sandbox rendering flow

The room-1 standalone sandbox at `registerScene('room-1', ...)` uses the same rendering primitives but pushes them harder. Things tried first in room-1 and later promoted to global:

- ACES tone mapping (room-1 only, then global in Phase 7.5).
- PMREM env map (room-1 only, then global in Phase 7.5).
- Anisotropic filtering at max (room-1 has it on every PBR texture; the property-level rendering uses default anisotropy on most surfaces).

Things still room-1 only:

- The full `EffectComposer` post-processing pipeline (`RenderPass` then `UnrealBloomPass` then `SMAAPass`). The exterior and interior scenes use plain `renderer.render()`.
- Refractive `MeshPhysicalMaterial` with `transmission` on every glass surface. The property build uses transmission glass only on the front-door slit (Phase 7.9).
- Per-window backdrop planes outside each window. The property build relies on the env map and the actual exterior geometry instead.
- The lamp toggle (bulb emissive plus shade emissive plus bloom flip).

The cutting-edge plan at `ozu-test/room-1-ONLY-cutting-edge-plan.md` lists what's coming next in the sandbox: TAA anti-aliasing, RectAreaLight window sunbeam, real HDRI environment, god-rays cone, soft cloth shader. If any of these prove out in the sandbox they can be promoted to the property scenes the same way ACES and PMREM were.

## Gaps i could not source

- The exact moment the procedural PMREM env map was first added (whether to room-1 or globally) is not in any commit message I read. It is described as live in the master plan and the room-1 rendering plan but the originating commit is not isolated.
- The exact `clearcoat` parameters on the new ceramic `MeshPhysicalMaterial` are documented in code (`clearcoat: 1.0, clearcoatRoughness: 0.05`) but not in the master plan.
- The "audit fixes" referenced in commit 4756f6e's title are not enumerated in the commit body. They are described at a high level in the master plan but not pinned to specific lines.
- The procedural whitewashed wood-plank ceiling texture's exact construction (warp, weft, knots, grain values) is described for room-1 in `room-1-ONLY-rendering-plan.md` but the property-scene version may differ.
- The exact emissive colour and intensity used on the LDK pendant warm-glow is not in the master plan, only the swap.
- The HemisphereLight intensity and sky/floor colours added in Phase 7.5 are not specified in the master plan.
- The master plan refers to the bedroom wall-paint helper as `addBedroomWallPaint`. The actual code calls it `addRoomPaint2F`. The plan name and the code name differ; the code name is authoritative.
