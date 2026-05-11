# Interior render recipe — the laundry-test playbook

> **What this is.** A step-by-step recipe for taking a Japanese-house interior room from "photo evidence + folder of references" to a high-fidelity three.js render with Cycles-baked lightmaps. Distilled from the laundry-test rebuild (2026-05-11) — every knob, every value, every reason — so any future room (living-dining, washroom, room-1..4, corridor, etc.) can follow the same path.
>
> **Authority.** This recipe operationalizes the **CLAUDE.md "Interior-render daylight rule — Kumamoto, sunny spring, 11:00 AM JST"** and the memory rules under `~/.claude/projects/-home-moha-Project-3d-vertical-test/memory/`. When this doc conflicts with those, those win. When this doc conflicts with intuition, the rules still win — every value below is tied to a reason; don't change values without updating the reason.
>
> **Scope.** "Interior render" = camera placed INSIDE a room looking at walls / floor / ceiling / fixtures. Exterior shots (facade, garden) are NOT covered.

---

## 0. The room sandbox pattern

Every interior render in this repo lives in its own self-contained sandbox HTML file, paired with a folder for bakes and textures. This isolates rendering work from the master `ozu-test.html` and lets each room be tuned without breaking another.

```
<room>-test.html                # single-file ESM project — three.js inlined via import map
<room>-test/
  bake/
    bake_room_lightmap.py       # Cycles A6000 bake script — Sky Texture (Nishita) + Light Portal
    bake_room_ao.py             # optional separate AO bake (corner darkening)
    bake_<product>_ao.py        # per-featured-product AO bake
  textures/
    lightmap/                   # output PNGs from bake_room_lightmap.py — UV2 lightmaps per face
    ao/                         # output PNGs from bake_*_ao.py
```

**Reference patterns:** `laundry-test.html` + `laundry-test/` (washing-machine showcase) and `kitchen-test.html` + `kitchen-test/` (kitchen surfaces). Read those before starting a new room — they are the templates.

**Index card:** every sandbox gets a card in `index.html` so the project hub lists it.

---

## 1. Phase 0 — Photo audit (mandatory)

Before ANY code, audit the room's reference photos. Skipping this is the #1 cause of rework later.

### Inputs
- **Photos:** `ozu-test/interior-images/<room>/` — usually structured as 4 corner sweeps (`a/`, `b/`, `c/`, `d/`) plus an optional `close-up/` folder. Some rooms have sub-zones (e.g. `living-dining/` has `living/{a,b,c}` + `dining/{a,b,c}`).
- **Map:** `ozu-test/interior-images/<room>/room-map.md` — wall names by feature (NEVER by compass), exterior-vs-interior wall flags, fixture anchors, corner-id conventions.
- **Photo→wall index:** `ozu-test/interior-images/<room>/room-map-photos.md` if present.
- **Featured products:** `appliances-and-furniture/<room>-appliances/<product>/` — curated reference photos + a `<product>-dimensions.md`.
- **Master plan:** `ozu-test/master-plan.md` — the broader context for what's done elsewhere in the house.

### Audit checklist (apply to every room)
1. **Read the room-map carefully.** Note the 4 wall names (feature-based, NEVER directional), which walls are EXTERIOR vs INTERIOR, where each window and door sits, what's mounted on each wall.
2. **Read 2-3 representative frames per corner.** Pick frame 01 of each corner first (canonical orientation), then 1-2 more if anything is unclear. Don't speed-skim — actually look at each photo.
3. **Catalog discrepancies BEFORE writing code.** Build a table: photo evidence | room-map claim | what to model. Examples from laundry-test:
   - room-map said "drying rails on window-wall" → photos showed them on the brick vanity-wall
   - room-map said "Sharp ES-11K1 front-loader" → photos showed a top-loader
4. **Identify which exterior wall facings the room has** (north / south / east / west). This determines the lighting rig — see phase 4.
5. **Featured product dimensions** — read `<product>-dimensions.md` for the showcased item. If absent, measure from the photo against known references (door height = 2 m, counter height = 0.85 m).

### Output
A short written audit (in the handoff or as a comment in the new sandbox HTML) listing:
- Room dimensions (from blueprint or room-map)
- Each wall's identity (feature name + interior/exterior + which window/door it carries)
- Window facings (N/S/E/W) — this is the most important output for lighting
- Featured products + which corner they appear in + their dimensions
- Any room-map-vs-photo conflicts and the resolution

---

## 2. Phase 1 — Sandbox scaffold

### File creation
Create `<room>-test.html` by copying `laundry-test.html` (or `kitchen-test.html` if the room has more variety than laundry-test offers). Either is a valid starting point; pick whichever matches the eventual complexity.

### Imports (line ~160 in the laundry-test pattern)
```js
import * as THREE from 'three';
import { HDRLoader }                from './vendor/three/examples/jsm/loaders/HDRLoader.js';
import { RoundedBoxGeometry }       from './vendor/three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { RectAreaLightUniformsLib } from './vendor/three/examples/jsm/lights/RectAreaLightUniformsLib.js';
import { EffectComposer }           from './vendor/three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass }               from './vendor/three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass }          from './vendor/three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { OutputPass }               from './vendor/three/examples/jsm/postprocessing/OutputPass.js';
RectAreaLightUniformsLib.init();
```
> WebGL renderer uses `RectAreaLightUniformsLib`. If you switch to `WebGPURenderer` you MUST swap to `RectAreaLightNode.setLTC(RectAreaLightTexturesLib.init())` — they are not interchangeable.

### Renderer
```js
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.68;        // Kumamoto 11 AM clear sky — sweet spot
renderer.outputColorSpace = THREE.SRGBColorSpace;
```
> **Exposure 0.68 is load-bearing.** 0.62 was too dim ("window blocked" bug). 0.78–0.82 was too bright (washing machine blew out). 0.68 is the tested value for Kumamoto 11 AM spring after going both directions.

### HDRI + scene environment (the IBL backbone)
```js
const pmrem = new THREE.PMREMGenerator(renderer);
pmrem.compileEquirectangularShader();

new HDRLoader().load('ozu-test/hdri/kloppenheim_06_puresky_2k.hdr', (hdr) => {
  const envMap = pmrem.fromEquirectangular(hdr).texture;
  scene.environment = envMap;
  scene.environmentIntensity = 0.60;                       // r163+ scene-level IBL gain
  scene.environmentRotation = new THREE.Euler(0, 0.80, 0); // align HDRI sun with azimuth 160° SSE
  hdr.dispose();
});
```
> `scene.environmentRotation` was added in r163. The yaw value (+0.80 rad ≈ +46°) is specific to **kloppenheim_06_puresky_2k.hdr** — it puts that HDRI's bright sun zone over the SSE direction in world coords. For other HDRIs the value is different; check the equirect and re-pick.

---

## 3. Phase 2 — Room shell (walls / floor / ceiling)

### Constants
Define room dimensions FIRST, from the blueprint or `room-map.md`. Don't eyeball.

```js
const ROOM_W = 1.80;   // E-W (along +X)
const ROOM_D = 2.70;   // N-S (along +Z)
const ROOM_H = 2.50;   // up (along +Y)
const WALL_T = 0.05;
```

> **Coord convention** in this repo: +X east, +Y up, +Z north. Always. NEVER use compass-named variables — use the feature-named wall identifiers from `room-map.md`.

### Walls — one `wallBox` per face, distinct material per face
This is critical for lightmaps to work. Each wall is its own mesh with its own material clone, so the lightmap's UV1 override targets one face at a time.

```js
const matBathWall   = matWall.clone();      // west wall
const matDoorWall   = matWall.clone();      // south wall
const matVanityWall = matBrick.clone();     // east wall (accent material here)
const matWindowWall = matWall.clone();      // north wall (also wraps the window cutout)

for (const m of [matBathWall, matDoorWall, matVanityWall, matWindowWall]) {
  m.lightMap = loadLightmap(/* slug */, { channel: 1 });
  m.lightMapIntensity = 1.0;
  m.envMapIntensity = 0.15;                 // dampen IBL — lightmap carries GI
  m.needsUpdate = true;
}

scene.add(wallBox(-WALL_T, 0,             0, ROOM_H,    0, ROOM_D, matBathWall));
scene.add(wallBox(0,       ROOM_W,        0, ROOM_H,   -WALL_T, 0, matDoorWall));
scene.add(wallBox(ROOM_W,  ROOM_W+WALL_T, 0, ROOM_H,    0, ROOM_D, matVanityWall));
// Window-wall is built as fragments around the cutout — see phase 3.
```

### Floor + ceiling
```js
// Floor — single plane (lightmapped on the +Y face)
const floor = new THREE.Mesh(
  new THREE.PlaneGeometry(ROOM_W, ROOM_D + 0.4),  // overhang under bath-wall is intentional
  matFloor
);
floor.rotation.x = -Math.PI / 2;
floor.position.set(ROOM_W / 2, 0, ROOM_D / 2 - 0.2);
floor.receiveShadow = true;
scene.add(floor);

// Ceiling — slab with UV1 override on its -Y face (visible from below)
const ceil = new THREE.Mesh(
  new THREE.BoxGeometry(ROOM_W + WALL_T * 2, WALL_T, ROOM_D),
  matCeilingLight
);
ceil.position.set(ROOM_W / 2, ROOM_H + WALL_T / 2, ROOM_D / 2);
ceil.receiveShadow = true; ceil.castShadow = true;
setLightmapUV1(ceil, 'y', -1, (x, y, z) => [x / ROOM_W, z / ROOM_D]);
scene.add(ceil);
```

> `setLightmapUV1(mesh, axis, sign, worldToUv)` is the per-mesh override that lets a single lightmap PNG map to ONE face of a box (the rest of the box's vertices get UV (-1,-1) which clamps to the texture's edge). Helper sits at top of laundry-test.html — copy verbatim.

---

## 4. Phase 3 — Windows + recessed reveals

Most lighting realism failures trace back to a flat window cutout that reads as "a hole in the wall" instead of a deep recess. The recipe is:

### Constants
```js
const WIN_X0 = 0.60, WIN_X1 = 1.20;   // 600 mm wide
const WIN_Y0 = 1.50, WIN_Y1 = 1.80;   // 300 mm tall, sill 1.50 m above floor
const WIN_DEPTH = 0.10;               // 10 cm reveal depth (north wall locally thicker)
```
> These dimensions come from the photo + the room-map's `06003` / `02607` / `16009` sash codes (Japanese window codes: first 2 digits = width × 100 mm, last digits = height × 100 mm).

### Wall fragments around the cutout
```js
const NX0 = 0, NX1 = ROOM_W;
const NZ0 = ROOM_D, NZ1 = ROOM_D + WIN_DEPTH;     // local wall thickness for this wall = WIN_DEPTH
const winWallUv = (x, y, z) => [(ROOM_W - x) / ROOM_W, y / ROOM_H];
const winFragments = [
  wallBox(NX0,    NX1,    0,      WIN_Y0,  NZ0, NZ1, matWindowWall),  // below
  wallBox(NX0,    NX1,    WIN_Y1, ROOM_H,  NZ0, NZ1, matWindowWall),  // above
  wallBox(NX0,    WIN_X0, WIN_Y0, WIN_Y1,  NZ0, NZ1, matWindowWall),  // left jamb
  wallBox(WIN_X1, NX1,    WIN_Y0, WIN_Y1,  NZ0, NZ1, matWindowWall),  // right jamb
];
for (const f of winFragments) { setLightmapUV1(f, 'z', -1, winWallUv); scene.add(f); }
```

### Four reveal faces (the inside of the recess)
```js
const matReveal = new THREE.MeshPhysicalMaterial({
  color: 0xfafaf6, roughness: 0.55, metalness: 0,
  clearcoat: 0.25, clearcoatRoughness: 0.40,
  envMapIntensity: 0.55,
});
// sill (+Y face into pocket), head (-Y), left jamb (+X), right jamb (-X)
const sill = new THREE.Mesh(new THREE.PlaneGeometry(winW, WIN_DEPTH), matReveal);
sill.rotation.x = -Math.PI / 2;
sill.position.set(winCx, WIN_Y0, (NZ0 + NZ1) / 2);
sill.receiveShadow = true;
scene.add(sill);
// (head, leftJamb, rightJamb — same pattern, see laundry-test.html ~717-755)
```

### Frosted glass
```js
const frostNoiseCanvas = (() => { /* 3-octave value-noise into a 256² canvas */ })();
const frostRoughnessTex = texFromCanvas(frostNoiseCanvas);
frostRoughnessTex.colorSpace = THREE.NoColorSpace;
const frostNormalTex = deriveNormalFromCanvas(frostNoiseCanvas, 0.10);

const matGlassFrosted = new THREE.MeshPhysicalMaterial({
  color: 0xf4f7fa,
  roughness: 0.62,                          // sweet spot of the true-frosted band (0.60–0.85)
  metalness: 0,
  roughnessMap: frostRoughnessTex,          // procedural micro-pebble noise
  normalMap: frostNormalTex,
  normalScale: new THREE.Vector2(0.06, 0.06),
  transmission: 1.0,                        // full transmission
  ior: 1.50,
  thickness: 0.005,
  attenuationColor: new THREE.Color(0xeef2f8),  // cool tint per Kumamoto rule
  attenuationDistance: 0.10,
  envMapIntensity: 2.5,                     // backlit-glow trick
});
```
> **Roughness sweet spots are bimodal:** 0.05–0.15 (clear) or 0.65–0.85 (true frosted). The middle 0.3–0.6 produces pixelated transmission samples. **0.62 is intentionally at the low end of the frosted band** — high enough to obscure, low enough to read bright.
>
> `envMapIntensity: 2.5` is the "backlit glow without emissive" trick from May-2026 frosted-glass research — boosts IBL specular on the glass plane so it reads as a glowing pane.

### Casing + sill ledge + sky proxy
```js
// White picture-frame casing — 4 strips on the inside wall face, ~2.5 cm wide × 1.5 cm proud
// Sill ledge — thin shelf at bottom of opening, ~1 cm proud
// (See laundry-test.html ~775-810 for exact geometry.)

// Sky proxy — HDR-bright panel 30 cm OUTSIDE the wall
const skyMat = new THREE.MeshBasicMaterial({ color: 0xeaf2ff, toneMapped: false });
skyMat.color.multiplyScalar(2.4);          // lift above bloom threshold 1.0
const sky = new THREE.Mesh(new THREE.PlaneGeometry(winW * 1.8, winH * 1.8), skyMat);
sky.position.set(winCx, winCy, NZ1 + 0.30);
sky.rotation.y = Math.PI;
scene.add(sky);
```
> **The `multiplyScalar(2.4)` is non-negotiable.** Without HDR (>1.0 linear) brightness on the sky proxy, the frosted glass samples a non-bright color and the window reads as a colored tile, not a window. We learned this the hard way: setting just `MeshBasicMaterial({ color: 0xeaf2ff, toneMapped: false })` capped at 1.0 (since the hex is below pure white), so the window appeared "blocked".

---

## 5. Phase 4 — Lighting rig (KUMAMOTO 11 AM RULE)

This is the rule's enforcement layer. Per CLAUDE.md the sun is at azimuth ≈ 160° (SSE), elevation ≈ 60°, color ~5500 K. EVERY interior render uses this — only the per-window directions vary.

### Hemisphere fill (always present, every room)
```js
scene.add(new THREE.HemisphereLight(
  0xc8d6e8,   // sky — clear-day cool blue
  0xa89878,   // ground — warm pine-floor bounce
  0.55
));
```

### Per-window window rig

The decision is: **which way does the window face?** This determines whether direct sun streams in or only diffuse sky.

#### Case A — North-facing window (the laundry-test scenario)
No direct sun at 11 AM. Cool diffuse skylight only. BUT — still needs a shadow-caster, otherwise geometry floats and the room reads flat.

```js
// 1. Sky proxy — HDR-bright, cool tint (see phase 3)

// 2. Diffuse area fill — RectAreaLight at window plane, cool
const winLight = new THREE.RectAreaLight(0xdde6f0, 22.0, winW, winH);
winLight.position.set(winCx, winCy, NZ1 - 0.005);
winLight.lookAt(winCx, winCy, NZ0 - 5);
scene.add(winLight);

// 3. Shadow-caster — DirectionalLight at window, cool, soft, low intensity
const winSky = new THREE.DirectionalLight(0xe0e8f4, 0.95);
winSky.position.set(winCx, winCy + 0.6, NZ1 + 1.5);
winSky.target.position.set(winCx - 0.2, 0.30, 0.80);
winSky.castShadow = true;
winSky.shadow.mapSize.set(2048, 2048);
winSky.shadow.camera.near = 0.5;
winSky.shadow.camera.far  = 9;
winSky.shadow.camera.left = -2.5; winSky.shadow.camera.right = 2.5;
winSky.shadow.camera.top  =  2.5; winSky.shadow.camera.bottom = -1.5;
winSky.shadow.bias       = -0.00015;
winSky.shadow.normalBias =  0.025;
winSky.shadow.radius     =  10;    // VERY soft — frosted-glass scatter
scene.add(winSky, winSky.target);
```
> **The shadow-caster is mandatory even for a north window.** Removing it kills all cast shadows. Pretend you're modeling the directional component of the sky-bounce, not a sun.

#### Case B — South-facing window
Direct sun streams in at ~60° elevation, ~160° azimuth. ONE DirectionalLight in warm-neutral does double-duty: light + shadow.

```js
const winLight = new THREE.RectAreaLight(0xfff5e8, 18.0, winW, winH);  // warm-neutral fill
winLight.position.set(winCx, winCy, NZ0 + 0.005);
winLight.lookAt(winCx, winCy, NZ0 + 5);                                 // pointing OUT (sun comes from outside)
scene.add(winLight);

// Real sun position — azimuth 160°, elevation 60° from the room's window
const sunDir = new THREE.Vector3(0.171, 0.866, -0.470).normalize();    // = (sin(160°)·cos(60°), sin(60°), cos(160°)·cos(60°))
const winSun = new THREE.DirectionalLight(0xf6f5ec, 3.0);              // 5500 K neutral-cool
winSun.position.copy(sunDir).multiplyScalar(6);                        // 6 m out along sun direction
winSun.target.position.set(ROOM_W / 2, 0, ROOM_D / 2);                 // point at room center
winSun.castShadow = true;
// shadow camera same pattern as above; radius 3 (crisper, no frosted glass)
scene.add(winSun, winSun.target);
```

#### Case C — East-facing window
Sun is past peak-east but still streams in at a steep oblique angle. Same rig as south, just rotate the sun direction.

#### Case D — West-facing window
No direct sun in the morning. Same rig as north — cool diffuse + low-intensity cool DirectionalLight for shadows.

### Ceiling lights (optional)
Real interior photos at 11 AM clear sky often show ceiling lights either OFF or just barely contributing. If you include them, keep intensity ≤ 0.7 each so daylight stays dominant:
```js
const sl = new THREE.SpotLight(0xffe1b0, 0.7, 4.5, Math.PI / 4.2, 0.6, 1.6);
sl.castShadow = true;
sl.shadow.bias = -0.0008;
sl.shadow.normalBias = 0.01;
// visible disc — emissiveIntensity 0.45 (fixture reads as "fixture", not "lights on")
```

---

## 6. Phase 5 — Postprocessing

### EffectComposer setup
```js
const composer = new EffectComposer(renderer);
composer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
composer.setSize(window.innerWidth, window.innerHeight);
composer.addPass(new RenderPass(scene, camera));

const bloom = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  /* strength */ 0.16,
  /* radius   */ 0.70,
  /* threshold*/ 1.00         // only HDR-bright stuff (sky proxy ×2.4, emissive LEDs) triggers
);
composer.addPass(bloom);
composer.addPass(new OutputPass());

function tick() {
  composer.render();
  projectHotspots();
  requestAnimationFrame(tick);
}
```

> `renderer.toneMapping = ACESFilmicToneMapping` AND `OutputPass` together — OutputPass reads the renderer's tone mapping setting. Do NOT set `renderer.toneMapping = NoToneMapping` (it breaks OutputPass).
>
> **Bloom strength 0.16 is the tested value.** 0.22 looked like a soap-opera filter. 0.10 didn't read at all.

### Optional GTAO (for screen-space contact shadows)
Kitchen-test has it; laundry-test doesn't. Worth adding to bigger rooms (living-dining, room-1..4). See `kitchen-test.html:~2730+` for the pattern.

---

## 7. Phase 6 — Featured product / fixtures

### Approach
- Build the featured product mesh per the `<product>-dimensions.md` in `appliances-and-furniture/<room>-appliances/<product>/`.
- Use `MeshPhysicalMaterial`. CONSERVATIVE `envMapIntensity` — chrome 0.40-0.50, white paint 0.30-0.40, plastic 0.20-0.30. **Cranking these blew out the washing machine in laundry-test until we capped them.**
- Add `clearcoat: 0.10–0.30` + `clearcoatRoughness: 0.20–0.30` for painted surfaces.
- Roughness for paint: **0.62 minimum** (anything lower reads as showroom-fresh; eggshell is the goal).
- 4 leveling feet, hardware details, brand label as canvas-text plane.

### Hotspot
One product = one hotspot. World position points at the most identifiable feature (the lid/control panel on the washer; the screen on a TV).

```js
const PRODUCTS = {
  'product-001': {
    name: '<plain-language name>',
    meta: '<class + key spec>',
    spec: [['Width', '...'], ['Depth', '...'], ['Height', '...'], ['Brand', 'TBD']],
    refUrl: '#',
    pos: [/* x, y, z in world coords */],
  },
};
```

---

## 8. Phase 7 — Cycles A6000 bake pipeline

**Per CLAUDE.md "A6000 bake for every object" rule — runtime-only tweaks are never the end state.** Lightmap baking captures all the GI the runtime can't simulate.

### bake_room_lightmap.py — the canonical bake script

Use `laundry-test/bake/bake_room_lightmap.py` as the template. The key parameters (Kumamoto 11 AM rule):

```python
# Bake settings (May 2026 best practices per Agent 1 research)
RES         = 1024              # sufficient for interior surfaces; 2048 is ceiling
SAMPLES     = 512               # OIDN converged sweet spot
MARGIN      = 12

# Cycles config
scene.cycles.device = 'GPU'
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'           # static lightmaps: OIDN beats OptiX
scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
scene.cycles.denoising_prefilter = 'ACCURATE'
scene.cycles.bake_type = 'COMBINED'                  # Direct + Indirect + Diffuse in one pass

# World: Sky Texture (Nishita) for physically-grounded daylight
sky.sky_type = 'NISHITA'
sky.sun_elevation = math.radians(60.0)               # Kumamoto 11 AM spring elevation
sky.sun_rotation  = math.radians(-20.0)              # Blender's south-relative azimuth 160° → -20°
sky.sun_intensity = 1.0
sky.dust_density = 0.3
bg.inputs['Strength'].default_value = 1.2

# Light Portal at the window aperture — biggest single quality lever
light_data = bpy.data.lights.new(name='win_portal', type='AREA')
light_data.shape = 'RECTANGLE'
light_data.size = win_w
light_data.size_y = win_h
light_data.cycles.is_portal = True                   # the magic flag — MIS-samples world through aperture
light_data.energy = 0.0
# Position at the window's outer face, normal pointing into the room

# SUN lamp at the real sun position (independent of window facing — it lights the building exterior)
sun_data.energy = 3.5
sun_data.color = (1.0, 0.985, 0.96)                  # ~5500 K neutral-cool daylight
sun_data.angle = math.radians(0.5)                   # crisp disc — clear sky
sun_dir = mathutils.Vector((0.171, 0.866, -0.470))   # azimuth 160°, elevation 60°
sun.location = sun_dir * 6.0
sun.rotation_euler = (-sun_dir).to_track_quat('-Z', 'Y').to_euler()
```

> **Critical:** swap the frosted glass mesh to a **Translucent BSDF** during the bake. Glass BSDF blocks/refracts light in ways that defeat portals and inflate noise. The runtime keeps the real frosted shader; the bake just needs the light to pass through.

### Per-face bake targets
Build one bake-target image per surface (floor, ceiling, each wall fragment), assign each its own UV2 channel laid out for the lightmap. Save PNGs to `<room>-test/textures/lightmap/<slug>.png`. Wire each runtime material's `lightMap` to its slug.

### Running the bake
```bash
blender --background --python <room>-test/bake/bake_room_lightmap.py
```
On the A6000 with OptiX/OIDN, expect 10-30 min per surface depending on complexity. Total for a 6-surface room: ~1-3 hours.

---

## 9. Phase 8 — Verification + tuning

### Visual verification checklist
1. **Hard-reload** (`Ctrl+Shift+R` or cache-bust). Don't trust a soft reload — Three.js caches geometry.
2. **Orbit camera through each photo-corner viewpoint.** For each corner, compare against the photo. Look for:
   - Wall colors / patterns match?
   - Window glow has right intensity + color temperature?
   - Featured product reads correctly (not blown out, not floating, soft contact shadow)?
   - Floor + ceiling + walls have visible cast shadows from the directional shadow-caster?
   - Bloom only on bright zones (window, emissive LEDs) — NOT on chrome highlights?
3. **Common failure modes & their fixes:**
   - **Window reads as blocked / dark tile** → bump sky proxy `multiplyScalar` to 2.4+ AND make sure `toneMapped: false` is set
   - **Washer / TV blowing out** → cap material `envMapIntensity` (chrome 0.45 max, white 0.35 max)
   - **Room reads flat / no contact shadows** → DirectionalLight `castShadow: true` AND check it's positioned outside the window
   - **Whole image too dim** → bump exposure to 0.70-0.78, NOT higher (0.82 was tested = washer blew out)
   - **Whole image too bright** → drop exposure to 0.65-0.68
   - **Halos on everything (soap-opera filter)** → drop bloom strength to ≤0.16
   - **Sun-through-window reads wrong color** → check window facing vs CLAUDE.md rule (north = cool, south = warm-neutral)

### Iteration loop
After fixing → hard-reload → re-compare. NEVER claim "done" without comparing every photo-corner against the render. This is `feedback_no_phase_done_without_reference`.

---

## 10. Phase 9 — Commit + handoff

Commit in logical chunks per `feedback_review_before_continuing` — no monster "everything" commits.

**Suggested chunks for a new room:**
1. `<room>-test: scaffold + room shell` — file + walls + floor + ceiling
2. `<room>-test: window + recessed reveal + frosted glass`
3. `<room>-test: Kumamoto 11 AM lighting rig`
4. `<room>-test: postprocessing (bloom + output)`
5. `<room>-test: <featured-product>` — one commit per featured item
6. `<room>-test: A6000 bake script + initial bakes`
7. `<room>-test: visual verification tuning + index card`

Each commit's body should reference this recipe doc + the room-map.md.

### Handoff requirements
Include in the handoff:
- Which phase you finished, which is next
- Any unresolved photo-vs-code conflicts (deferred to next session)
- Any tuning values that diverged from this recipe (and why)
- Whether the A6000 bake has been run (and how many surfaces)

---

## Appendix A — Quick-reference value table

| Knob | Value | Why |
|---|---|---|
| renderer.toneMappingExposure | **0.68** | Sweet spot — 0.62 too dim, 0.82 blows out whites |
| scene.environmentIntensity | **0.60** | IBL bounce strong but not overpowering |
| scene.environmentRotation | `Euler(0, 0.80, 0)` for kloppenheim_06 | Puts HDRI sun at world azimuth 160° |
| HemisphereLight | sky `0xc8d6e8` / ground `0xa89878` / 0.55 | Cool clear-day sky, warm floor bounce |
| Window RectAreaLight (north) | `0xdde6f0` / **22** / winW × winH | Cool diffuse skylight; intensity tested |
| Window DirectionalLight (north) | `0xe0e8f4` / **0.95** / shadow.radius **10** | Cool shadow-caster, frosted-soft edges |
| Window DirectionalLight (south) | `0xf6f5ec` / **3.0** / shadow.radius **3** | Real sun at azimuth 160°, elev 60° |
| Sky proxy material | `MeshBasicMaterial({ color: 0xeaf2ff, toneMapped: false })`, `color.multiplyScalar(2.4)` | HDR-bright above bloom threshold 1.0 |
| Frosted glass | rough **0.62**, transmission **1.0**, attenuationColor `0xeef2f8`, attenuationDistance **0.10**, envMapIntensity **2.5** | Bimodal-roughness bright frosted band + backlit-glow trick |
| Bloom | strength **0.16**, radius **0.70**, threshold **1.00** | Tight halo only on truly bright zones |
| Featured-product white paint | rough **0.62**, metal **0.04**, clearcoat 0.25, envMapIntensity **0.35** | Eggshell paint, won't blow out |
| Featured-product chrome | rough **0.30**, metal 1.0, envMapIntensity **0.45** | Dim chrome — doesn't trigger bloom |
| Ceiling SpotLight | each intensity **0.7** | Daylight-dominant — fixtures barely register |

## Appendix B — Memory rules that informed this recipe

- `feedback_interior_render_daylight_rule.md` — Kumamoto / 11 AM / spring is the strict rule
- `feedback_laundry_test_is_washer_showcase.md` — showcase sandboxes ≠ full room recons (but rooms still need the same lighting recipe)
- `feedback_engage_a6000_by_default.md` — bake step is non-negotiable
- `feedback_cutting_edge_and_a6000_for_every_object.md` — applies to room-1 standalone work; not directly to test sandboxes but the bake-step part applies everywhere
- `feedback_no_phase_done_without_reference.md` — "done" requires every decision verified against photos
- `feedback_review_before_continuing.md` — pause and report after each substantive change
- `feedback_test_suffix_means_full_reconstruction.md` — `*-test` files faithfully build the source data; sub-rule for showcases is in `feedback_laundry_test_is_washer_showcase.md`

## Appendix C — Sources cited

All May 2026 research findings that fed into this recipe are documented in `.handoffs/handoff-2026-05-11-*.md`. Key research:
- Three.js r184 release notes (2026-04-16)
- KHR_materials_transmission spec (Khronos)
- Cycles 5.1 manual on Light Portals (Blender 5.1, 2026-03-17)
- Codrops glass-rendering articles (2025-03-13, 2025-03-10)
- Discourse threads on frosted-glass + emissive-glow patterns
