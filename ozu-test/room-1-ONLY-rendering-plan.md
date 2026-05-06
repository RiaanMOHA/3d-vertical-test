# ROOM-1 ONLY — cutting-edge rendering plan (standalone sandbox)

> **SCOPE: ROOM-1 STANDALONE SANDBOX ONLY.** This plan is for the standalone `room-1` 3D scene at `registerScene('room-1', ...)` inside `ozu-test.html`. It is **NOT** the Ozu-1 master plan (that's `master-plan.md` next to this file). It is **NOT** the room-1 v5 feasibility audit (that lives at `../room-1-ONLY-v5-feasibility/`). "Room-1" here means the standalone single-room sandbox, distinct from the room-1 zone inside the master plan's interior scene.

> **Last updated:** 2026-05-05. Rewritten to match the actual code in
> `ozu-test.html` (the previous version was from before the May 4
> photo-match sessions and before today's SMAA fix — it claimed
> several things were "not done" or "disabled" that are now done +
> running).

## Scope (read first)

This plan applies **only** to the standalone `room-1` 3D scene at
`registerScene('room-1', ...)` inside `ozu-test.html`.

It does **not** apply to the rest of the house (the "ozu-1 property" —
exterior facade + multi-room interior, planned in
[master-plan.md](master-plan.md)).

`ozu-test.html` is one HTML file but holds **two parallel projects**:

- **Project A — ozu-1 property:** the full Japanese house. Has its
  own plan file.
- **Project B — room-1 standalone:** an isolated single-room renderer
  used as a sandbox for cutting-edge rendering experiments.

Work between the two projects must never mix.

## Current actual state of room-1 (verified 2026-05-05)

### Lighting + colour ✅
- ACES filmic tone mapping active when room-1 is the visible scene,
  exposure 0.55 (dropped from 0.85 in prior session — was washing out)
- Procedural inside-out coloured cube baked into a cube-map via
  `THREE.PMREMGenerator`, used as `scene.environment` (provides
  realistic indirect light + reflections, fully offline)
- All PBR textures (floor, dark wood) plus the procedural ceiling
  plank texture are running at the GPU's max anisotropic filtering
- Window-direction directional light, intensity 0.85, casts shadows
  with `shadow.radius = 6` for soft edges
- Cool-tinted fill `DirectionalLight` from the cabinet-wall side,
  no shadow casting, intensity 0.22

### Walls + materials ✅
- Walls are plain `MeshStandardMaterial` (no PBR maps), warm neutral
  grey `0xa9a59f` matching the real photos at
  `interior-images/room-1/`
- Walls + ceiling DON'T receive or cast shadows (prevents X-ray
  silhouettes of furniture bleeding through the thin walls when
  viewed from outside)
- Floor still receives shadows so the sun beam visibly lands on it
- Weathered whitewashed plank ceiling — wider shade variance, knots,
  grain, dark plank seams

### Glass + windows ✅ (added since last plan)
- Real refractive glass (`MeshPhysicalMaterial` with `transmission`)
  on the sliding window — picks up the env map, gives proper specular
- Frosted glass on the narrow ac-wall privacy window
- Walls split into 4 segments around each window hole so the glass
  actually shows what's beyond (instead of looking at the wall behind
  the glass)
- Procedural Japanese-suburban-houses backdrop planes outside both
  windows so the windows have something to look at
- Vertical mullion on the sliding window (panel-meeting point of the
  hikichigai)
- Glass + backdrop planes excluded from shadow casting/receiving so
  glass doesn't drop a hard shadow and backdrops don't block the sun

### Furniture detail ✅
- Iron-frame bed (long side against ac-wall), ball finials on the
  four corner posts, sheet + scaled-`SphereGeometry` ellipsoid
  pillows (white + dark accent)
- Solid wood desk against window-wall
- L-shape shelf with X-bracing at corner-cabinet-window
- Desk chair, chestnut leather seat
- White closet against cabinet-wall, bi-fold pin handle (single
  vertical seam-handle, not 2 horizontal knobs)
- Coat hook rail with two black peg hooks (whitewashed wood plank
  base) on the cabinet-wall near the entrance corner
- White entrance door panel with a chrome round doorknob
  (escutcheon + stem + sphere)
- Light switch plate (white, with rocker button) on the entrance-wall
  next to the door
- Intercom panel below the AC unit (white plate + small dark button)
- Cream curtains either side of the sliding window, hourglass-bunched
  with a tieback ring
- Whitewashed wood-plank ceiling + white crown molding

### AC unit ✅
- White body
- Bottom louver flap hanging slightly below + forward
- Recessed darker grille on the front face
- Dark vent slit
- Standby LED removed (the real Toshiba in the photo doesn't show one)

### Pendant lamps ✅ (rebuilt since last plan)
- 4 linen-weave fabric shades (procedural canvas texture: warp +
  weft threads + noise dots) on a wood crossbar
- Brass central hub (`MeshStandardMaterial`, metalness 0.85)
- Visible bulb spheres inside open-ended shade cylinders (the shade
  bottom is uncapped so you can see the bulb from below)
- `S.lampsOn = false` by default — lamps off on first room-1 load
- Toggle in the dock ("Lights" button) flips the shade emissive +
  bulb emissive + bloom enabled state

### Post-processing pipeline ✅ ACTIVE (fixed today 2026-05-05)
- `EffectComposer` with `RenderPass` → `UnrealBloomPass` → `SMAAPass`
- Today's fix: the SMAAPass class was inlined but its companion
  shader source (`SMAAEdgesShader` + `SMAAWeightsShader` +
  `SMAABlendShader`) was missing — SMAAPass constructor was crashing.
  Inlined the shader source so it constructs without crashing.
- Bloom enabled only when lamps are on
- Pipeline runs only while room-1 is the visible scene; exterior +
  interior fall back to the plain `renderer.render()` path

### Outside-the-box look ✅ (changed since last plan)
- The room is NO LONGER a closed white box from outside. Walls cut
  around window holes; glass + backdrop planes visible through them.
- From outside, you see the room cube with two painted backdrop
  panels flanking it (intentional — the panels are the "view through
  the windows" assets)

---

## What's actually left, in phases

### Phase A — Real lamp glow ✅ DONE (2026-05-05)
Originally blocked because the composer crashed. Today's SMAA fix
unblocked it. Lights toggle now works: clicking "Lights" turns the
bulb emissive on, the shade emissive on, and the bloom pass on, so
the lamps visibly glow.

### Phase B — Window-shaped sunbeam (RectAreaLight)
Replace the current point-direction sun with a rectangular soft area
light matched to the window pane size. Patch of sunlight on the
floor/bed becomes a softer rectangle instead of a hard wedge.

What we'd do:
- Inline `RectAreaLightUniformsLib` (small ~200-line vendor file from
  three.js r128, no shader compilation issues)
- Replace the existing `DirectionalLight` at the window position
  with a `RectAreaLight` matched to the sliding-window pane size

Independent of the post-processing pipeline.

**Status:** not started.

### Phase C — Photographic depth-of-field + vignette
Cinematic camera focus — what the orbit is centred on stays sharp,
further objects gently blurred. Plus subtle screen-corner darkening.

Now technically possible since the composer is working. Adds two
more passes (Bokeh DoF + a vignette shader) to the pipeline.

**Status:** not started.

### Phase D — Backdrop polish (the "view out the windows")
The current backdrop is a hand-drawn cartoon canvas — flat from any
angle, looks painted. Options:
- Bigger plane (current 8×4 m may be too small at steep viewing
  angles)
- Multiple parallax layers (sky / mid-distance houses / foreground
  house) so the view has depth as you move
- A real photograph (rejected today: the user's own exterior photo
  was tried but landed wrong — needs different reference imagery)
- A real HDRI

**Status:** parked — needs user direction on what "good" looks like.

### Phase E — Frosted glass that reads as frosted
Current frosted glass parameters give a clear-ish window. Pushing
roughness to 1.0 and thickness to 0.25 was tried today; user said
it overshot ("heavy fog"). The sweet spot is somewhere in between
and is unverified.

**Status:** parked — needs user-visible reference for the right
amount of blur.

### Phase F — More accurate furniture from photos
Pieces that don't yet match the panorama photos at
`interior-images/room-1/`:
- Curtains: currently a single tapered cylinder + tieback ring.
  Real curtains have folds. The 7-fold bundle attempt today was
  rejected as "weird".
- Desk colour: current vs photo's reddish-brown stained wood with
  visible grain (UNVERIFIED — needs visual compare).
- Wall plaster texture: currently plain colour. Past PBR plaster
  map was rejected as too bumpy. A SOFTER plaster could be tried.

**Status:** partial — most photo-match pieces done, a few rejected
today, a few not yet attempted.

### Phase G — Door + door-frame detail
Current entrance door is a flat white box with a chrome doorknob.
Real photos show: hinged white door with possibly recessed paneling
+ an architrave moulding around the frame.

**Status:** not started.

---

## Trade-off / decision matrix

| What you get | Status |
|---|---|
| Realistic light + colour (env map, ACES, anisotropic, soft shadows, fill, neutral wall colour, AC redesign, no-shadow-bleed walls) | ✅ applied |
| Real refractive glass (clear + frosted) with walls cut around the windows + backdrop visible through them | ✅ applied |
| Pendant lamps actually glow (bulbs visible, bloom around shades, toggle in the dock) | ✅ applied |
| Soft rectangular sunbeam through window | not started, Phase B |
| Cinematic depth of field + vignette | not started, Phase C |
| Backdrop view out the windows looks like a real place | parked, Phase D |
| Frosted window reads as frosted (right amount of blur) | parked, Phase E |
| More accurate curtains / desk / wall plaster | parked or unverified, Phase F |
| Detailed door + frame | not started, Phase G |

## Strict rules during all of this

- Touch only the `registerScene('room-1', ...)` block in
  `ozu-test.html`, plus the small per-scene pipeline switch in
  `switchScene` (which leaves all non-room-1 scenes on their
  existing pipeline).
- Do not touch the exterior or interior scenes.
- Stay on three.js r128, keep it inlined, keep it working offline.
- Pause for review after each phase.
- Plain language status reports.
