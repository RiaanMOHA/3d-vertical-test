# Flow: Ozu-1 property full build, start to finish

> The whole story of how the Ozu-1 property (the Japanese house, exterior plus all interior rooms, plus stairs, plus circulation) was built. Use this when starting a fresh property and you need the end-to-end picture. For just placement work see `flow-ozu-1-layout.md`. For just look-and-feel see `flow-ozu-1-rendering.md`. For the standalone room-1 sandbox flow see `../flow-room-1/`.

> See `glossary.md` in this folder for definitions of three.js terms (PBR, transmission, clearcoat, emissive), light types, F1_WIN/F2_WIN array shape, hex colour syntax, and the JP residential terms used in this doc.

## 1. We started with the same raw inputs as room-1

The Ozu-1 build starts from the same source material that fed the room-1 standalone sandbox. Both projects share the inputs.

The blueprint PDF of the property at `ozu-test/blueprints/ozu-1-blueprint.pdf` is the dimensional source of truth (source: CLAUDE.md off-limits-paths list). The on-site interior panorama photos sit at `ozu-test/interior-images/<room-name>/corner-<corner-id>/`, organised by room and by corner. About 950 panoramas total (source: CLAUDE.md "What this is" section). The front-facade exterior photos sit at `ozu-test/exterior-images/` (source: commit ccd2239).

Anywhere two sources disagree, the blueprint at 400 dpi outranks photos, photos outrank room maps, room maps outrank existing 3D code, and "never eyeball" is the rule of last resort (source: CLAUDE.md source-of-truth-hierarchy rule).

## 2. We wrote the docs the property build would reference

A whole-property master plan was written at `ozu-test/master-plan.md` covering exterior and interior in eight phases plus the 7.x detail passes (source: `ozu-test/master-plan.md`).

A per-room map was written at `ozu-test/interior-images/<room>/room-map.md` for each room. These named the walls in plain language (window-wall, ac-wall, cabinet-wall, entrance-wall) so chip labels and viewpoint ids could later match the photo folders exactly (source: CLAUDE.md naming convention).

Global coordinates were written at `ozu-test/blueprints/global-coords.md` translating blueprint metres into the 3D world's `x` (east-west), `y` (vertical), `z` (north-south) axes (source: CLAUDE.md folder map).

A room-identity reference was written at `ozu-test/blueprints/room-identity.md` (source: CLAUDE.md folder map).

The naming convention was strict: chip labels, viewpoint ids, and scene names had to match folder names exactly with no friendly relabeling. Corner ids list walls in alphabetical order (`corner-cabinet-window`, never `corner-window-cabinet`). Wall names use feature names (`window-wall`, `ac-wall`), never compass directions or coordinates (source: CLAUDE.md naming section).

## 3. We built one HTML file with three layers

The whole property lives in one file at `ozu-test.html` as a `<script type="module">` block (a regular script tag with the `module` attribute, which lets the browser load other JS files via `import`). Three layers stack inside it:

- The platform layer at `index.html` is the project hub.
- The project layer at `ozu-test.html` holds three logical projects: an `exterior` registerScene block (front facade), an `interior` registerScene block (multi-room interior), and a `room-1` registerScene block (standalone sandbox, separate sub-project).
- Inside the project layer, scene-to-scene transitions never spawn a new URL or port. Everything stays in-page.

Source: CLAUDE.md architecture section.

The project script imports three.js r184 and HDRLoader as ESM modules (ES Modules, the modern browser-native way to share code between JS files) from `vendor/`. There is no bundler (a tool that combines many JS files into one), no transpiler (a tool that translates new JS into older JS), no build step (source: CLAUDE.md stack section). To "inline three.js" means: put the actual `three.module.min.js` file on disk under `vendor/` and import it directly, instead of fetching it from a CDN.

The architectural rule: window arrays are the single source of truth. The `F1_WIN_*` and `F2_WIN_*` arrays drive both the exterior scene and the interior scene. Edit the array, both scenes update (source: CLAUDE.md window-arrays-as-single-source-of-truth rule).

## 4. We built the foundation: blueprints, room maps, collision-box audit

Phase A/B/C landed together in commit 4caf784 ("ozu-test: phase A/B/C blueprints + room maps + collision-box audit") (source: git short-sha 4caf784). This was foundational: load the blueprint, write the room maps, audit the collision boxes for the walk-through mode (note: walk mode was later cut entirely, so this audit is no longer load-bearing).

## 5. We unified the wall geometry between exterior and interior

Commit 0046b8b ("ozu-test: unify exterior + interior wall geometry, add cladding split") merged the exterior and interior wall builders so a single geometry source feeds both scenes (source: git short-sha 0046b8b). This is what makes the F1_WIN/F2_WIN arrays a true single source of truth.

## 6. We added the two-layer outer walls and built the LDK and room-4

Commit 4e735e7 ("ozu-test: 2-layer outer walls, brown panel inset, LDK polish, room-4 build") split the outer wall into two layers (outer cladding plus inner finish), inset the brown wood panel on the front facade, polished the LDK (Living / Dining / Kitchen), and built room-4 (source: git short-sha 4e735e7).

## 7. We built the rest of the interior rooms

Commit 6cbf3de ("ozu-test: QA navigation tool + Phase D-1/3/4/5/6 builds + showcase folder") landed the QA chip-navigation tool plus Phase D rooms (room-1 zone inside the interior scene, room-3, room-4, plus wet rooms and circulation) (source: git short-sha 6cbf3de). The "Phase D-2" gap is unexplained in the commit body.

Note on terminology: "room-1 zone" means the room-1 area inside the multi-room `interior` registerScene block. This is **different** from the standalone `registerScene('room-1', ...)` block, which is its own sub-project. They share the property's room-1 photos as evidence, but the code lives in two separate places and the two are never edited together.

By this point the master plan considered all four bedrooms done, all three wet rooms done, and the LDK done (source: `ozu-test/master-plan.md`, "What's actually done" section).

## 8. We worked through the master plan phases 1 to 6

Phases 1 to 6 of the master plan landed across multiple commits, with the bulk in commit 4756f6e ("ozu-test: master plan phases 5–6 + audit fixes; room-1 jaggy fix + Phase 3 textures") (source: git short-sha 4756f6e).

The phases were:

- **Phase 1: add ceilings everywhere.** Most rooms had no ceiling and looking up showed sky. One sweep added ceilings to every room, the corridor, and the entry. Done.
- **Phase 2: fix the doorways.** All 14 doorways had been generic flat panels. Each one got the right type per the blueprint: sliding (Japanese-style), hinged, bi-fold (folding closet doors), open archways. Done.
- **Phase 3: detail the genkan.** Added doormat, shoe storage cabinet (玄関収納, shoe storage), and other entry detail. Done.
- **Phase 4: detail the 2F toilet.** Added hand-wash basin, paper holder, frosted privacy window detail, picture frame on the long wall. Done.
- **Phase 5: real stairs (both staircases).** Replaced each stacked-box step with a real sloped-wedge step, added handrails, added wooden side brackets / carriage. Done for both ground-floor and second-floor staircases.
- **Phase 6: finish exterior polish.** Re-measured the brown panel's exact edges from the front-facade photo, settled the back-of-house door-or-window question, added the frosted privacy window on room-4's outside wall. Done.

Source: `ozu-test/master-plan.md`, "What's actually left" section, all marked status: done.

## 9. We removed walk mode entirely

Phase 7 was originally "fix walk mode". It got cut: walk mode was removed entirely on 2026-05-06 (source: `ozu-test/master-plan.md`, "Phase 7" section). The walk button, WASD/pointer-lock movement, per-scene start positions, and the wall-collision list were all deleted. Orbit became the only camera mode.

## 10. We ran a multi-agent audit and applied presentation-fidelity quick wins

On 2026-05-06 a deep multi-agent audit ran. The findings closed specific gaps between the build and 2026 architectural-visualisation standards. Each item was a small focused edit (source: `ozu-test/master-plan.md`, "Phase 7.5" section).

The Phase 7.5 wins:

- Ceramics upgraded to `MeshPhysicalMaterial` with clearcoat (the `matToilet` material; find it by searching `ozu-test.html` for `matToilet`). Toilets and basins render as glazed porcelain instead of matte plaster.
- ACES filmic tone mapping applied globally (was room-1 only). Highlights stop clipping on cream walls in exterior and interior.
- Procedural PMREM environment map applied globally. Metals reflect indirect light in every scene, not just room-1.
- Interior shadows enabled. `DirectionalLight` casts now, every solid mesh casts and receives. Plus an indoor `HemisphereLight` for sky/floor bounce.
- 2F top-of-stair parapet added. Closes the 1.10 m guard gap at the south edge of the stair shaft.
- Genkan 土間 (the lower step-down floor area at the entrance, 150 mm) plus 上がり框 (the wood lip step that separates 土間 from the rest of the house) added. Proper Japanese front-entry geometry.
- Whitewashed wood-plank ceiling texture applied (was flat plaster). Matches the photos' dominant ceiling material.
- Two warm-white `PointLights` at the LDK back-wall windows approximate daylight streaming in (placeholder for proper RectAreaLights, which need an extra inlined uniforms library).
- Smoke detectors (住宅用火災警報器, residential fire alarm) added on every 2F bedroom ceiling and at the top of the stair. Mandatory per 消防法 (Japanese fire-safety law).
- 2F toilet picture frame moved from west wall to east wall per photo evidence.

Source: `ozu-test/master-plan.md`, "Phase 7.5" section.

## 11. We did a photo-fidelity colour pass

Phase 7.6 closed visible mismatches between the build and the room photos. Each item was a small material-level change (source: `ozu-test/master-plan.md`, "Phase 7.6" section).

- Brick accent recoloured from warm-brown (`0x5e4a3d`) to cool grey-white (`0x9a9a96`). Matches the cool grey-white brick plus white mortar visible in the LDK and 1F-toilet photos.
- Laundry "brick" feature wall removed entirely. Photos showed plain painted wall, not brick. The vanity wall reverted to default cream paint.
- 1F and 2F toilet floors changed from lavender-purple (`0xd6cbe0`) flat colour to warm light wood plank (`0xc4a888`) using the same procedural plank texture used in the bedrooms.
- LDK pendant lights given warm-glow emissive. They now read as lit pendants instead of cold dark spheres.
- Bi-fold closet door pulls plus hinged door handles upgraded from matte grey (`0x9a9a9a`, metalness 0.5) to chrome (`0xc8cdd2`, metalness 0.85, roughness 0.18) per photos.
- Bi-fold centre seam darkened from bronze tone (`0x8a7a66`) to a recessed shadow (`0x4a4a4a`). Was reading as a fake bronze strip, now reads as a real fold line.

Source: same.

## 12. We added the painted trim layer that real JP residential interiors have

Phase 7.7 added the trim layer using one shared off-white `trimMat` (`0xfafaf6`) for visual consistency (source: `ozu-test/master-plan.md`, "Phase 7.7" section).

- Door casings (architrave / 飾り枠, the trim around a door frame) added to all 14 doors automatically. The `addDoor` helper now draws four trim strips per door (two vertical jambs, one top header, on each face of the wall). 70 mm wide and 12 mm proud (sticking out from the wall surface).
- Baseboards (巾木, the strip along the floor) added in all four 2F bedrooms. 70 mm tall strip along the floor perimeter, with door openings punched out so the baseboard doesn't run through the door panels.
- Crown moulding (回り縁, the strip at the ceiling line) added in the same four bedrooms. 50 mm strip at the ceiling line, same perimeter logic.
- Reusable helper `addRoomTrim(x0, z0, x1, z1, yFloor, ceilH, doorList)`. Call it for any clean rectangular room and it handles baseboard, crown, and door cuts. Find it in `ozu-test.html` by searching for `function addRoomTrim`.

Trim was deferred for the LDK (irregular L-shape), the corridors (also irregular), the closets (small enough not to matter), and the wet rooms (JP wet rooms typically don't have wood baseboards) (source: same, "Deferred" section).

## 13. We painted the bedroom walls taupe-grey

Phase 7.8 fixed the bedroom wall colour. Photo evidence showed all four 2F bedrooms have taupe-grey walls (~`0x8e857a`), not the global cream `wallMat` (`0xeeeae3`) used elsewhere. The shared `wallMat` couldn't be tinted per-room without refactoring the wall builders, so a thin paint overlay was added on the interior face of each bedroom's walls (source: `ozu-test/master-plan.md`, "Phase 7.8" section).

A new helper called `addRoomPaint2F` (the master plan refers to it as `addBedroomWallPaint` but the code uses `addRoomPaint2F`; find it by searching `ozu-test.html` for `function addRoomPaint2F`) paints all four interior wall faces with door and window x-ranges punched out. Signature: `addRoomPaint2F(x0, z0, x1, z1, yFloor, ceilH, doorList, gapsBySide)`. The paint Y range sits between the existing baseboard and crown bands so the trim still reads as a separate layer. Applied to room-1, room-2, room-3, and room-4.

## 14. We rebuilt the front door

Phase 7.9 rebuilt the genkan front door. The previous version was a flat tan box (`doorMat 0xb89878`). Photos showed a typical 2026 JP residential entry: two-tone steel slab with a vertical glass slit, chrome grip pull, brushed kickplate, and mail slot (source: `ozu-test/master-plan.md`, "Phase 7.9" section).

The rebuild has seven elements: lower brown panel, upper charcoal panel, vertical glass slit (transmission glass), chrome grip pull, brushed kickplate, mail slot, transom, and casing. Geometry matches the existing 0.90 m by 2.00 m opening with no other wall or doorway data touched. Architrave matches the trim style used by every other door.

## 15. Where the build sits today

What is live and working:

- Two-layer outer walls with brown wood panel ground-floor inset, cream upper section, all front-facade windows (source: `ozu-test/master-plan.md`, "Exterior" section).
- LDK fully populated: sofa, dining table, coffee table, TV console, kitchen counter, antique clock, pendant lights.
- All four 2F bedrooms populated: iron-frame beds, cabinets, coat racks, AC units, sliding windows with curtains.
- All three wet rooms populated: bathroom (bathtub, tap, shower bar, shower head, towel rail), laundry (washing machine, vanity, basin, faucet, sconce), 1F toilet (bowl, tank, hand-wash basin, paper holder).
- Phases 1 through 7.9 of the master plan all marked done.

What is still open or deferred:

- Brown panel exact top edge plus right edge: needs re-measuring from the front-facade photo.
- Brick texture on brick accent walls: deferred (high risk of looking worse than the flat colour we have now).
- LDK trim and corridor trim: deferred (irregular shapes need a polygon-based perimeter helper).
- Kitchen detail pass (sink, faucet, cooktop, range hood, fridge, upper cabinets, subway tile): complex.
- Phase 8 small clean-ups (`corridor-2` empty photo folder decision, photo-folder rename script, `package.json` Mac-only script tidy).
- Optional: put the project online (Vercel / Netlify / GitHub Pages).

Source: `ozu-test/master-plan.md`, "Exterior" + "Phase 7.6 Deferred" + "Phase 7.7 Deferred" + "Phase 8" + "Optional" sections.

## How to repeat this on the next property

If you are starting a new property, the same flow applies. **Before you start:** copy `ozu-test.html` to a new file (e.g. `<property-name>.html`), rename `ozu-test/` to `<property-name>/`, and gut the contents of every `registerScene(...)` block. Keep the helper functions (`addRoomTrim`, `addRoomPaint2F`, `wallX`, `wallZ`, `addDoor`, `buildRoom1EnvMap` etc) and the F1_WIN / F2_WIN array shapes. That gives you a working empty shell to fill with the new property's data. Walk mode does not need to be added back; it was cut.

Then:

1. Get the blueprint PDF, the per-room corner panoramas, and the front-facade exterior photos onto disk under `<property-name>/blueprints/`, `<property-name>/interior-images/<room>/corner-<id>/`, and `<property-name>/exterior-images/`.
2. Write the global coordinates file from the blueprint at `<property-name>/blueprints/global-coords.md`.
3. Write the room-identity reference at `<property-name>/blueprints/room-identity.md`.
4. Write the per-room map files at `<property-name>/interior-images/<room>/room-map.md` and `room-map-photos.md`. Plain-language wall names matching photo-folder names exactly.
5. Write the master plan at `<property-name>/master-plan.md` covering the whole property in phases. The Ozu-1 master plan at `ozu-test/master-plan.md` is your template.
6. Inline three.js r184 plus HDRLoader from `vendor/` (the `vendor/` folder is shared, no per-property change needed unless a new version drops).
7. Build the foundation: cross-check the blueprint against the photos for any discrepancies. Skip the collision-box audit if not building walk mode (Ozu-1 cut walk mode).
8. Unify exterior and interior wall geometry into one builder. Make the F1_WIN and F2_WIN arrays the single source of truth.
9. Build the two-layer outer walls and front-facade panel inset (if the property has a panel inset; otherwise just one cladding layer).
10. Build interior rooms one at a time. Each room: bounds, walls cut around windows, doors, floor, ceiling, trim, furniture. Hard-reload after each room. See `flow-ozu-1-layout.md` for the full per-room layout recipe.
11. Run the phase sweeps in order: ceilings, doorways, genkan (if JP), 2F toilet (if applicable), stairs, exterior polish.
12. Run a multi-agent presentation-fidelity audit. Ask Claude to fan out parallel audit agents covering: lighting fidelity, material accuracy vs photos, fixture details, perimeter completeness (parapets, baseboards), photo-evidence checks. Apply the wins one at a time.
13. Run a photo-fidelity colour pass. Walk every wall, floor, fixture, fitting against the panoramas. Change colours and materials to match the photo. Use any image viewer's eyedropper to sample colours, or just guess and tune.
14. Add the trim layer (door casings, baseboards, crown moulding) using one shared `trimMat` and the `addRoomTrim` helper. Skip irregular rooms (LDK, corridors) until a polygon-based helper is written.
15. Paint per-room wall colours where the global `wallMat` doesn't match. Use `addRoomPaint2F` (or write `addRoomPaint1F` if a 1F room needs it; doesn't exist yet).
16. Rebuild the front door if the placeholder is too generic.
17. Final clean-ups and optional publish.

Steps that are JP-residential-specific (skip or adapt for non-JP properties): step 11's genkan, the smoke detectors, the taupe-grey bedroom wall paint.

## How this flow relates to the room-1 standalone flow

The Ozu-1 property build and the room-1 standalone sandbox share the same input phase (blueprint, photos, room maps, global coords, room identity) and the same HTML file (`ozu-test.html`). After that they diverge.

- Ozu-1 builds inside the `exterior` and `interior` registerScene blocks. Multi-room. Phases 1 to 7.9 of `master-plan.md`.
- Room-1 builds inside the `registerScene('room-1', ...)` block, separately. Single-room. Phases A to G of `room-1-ONLY-rendering-plan.md`.

A locked rule from user memory: never touch the `registerScene('room-1', ...)` block during property work, even on a sweep. It only unlocks when the user literally types "room-1" (source: memory file `project_room1_is_separate_project.md`).

## Gaps i could not source

- The exact dates of when each room (room-2, room-3, room-4) got built individually are not broken out in commit messages. Commit 4e735e7 mentions "room-4 build" and commit 4a540b1 mentions "build room-2 with corner viewpoints", but room-3 is not isolated to a commit. The handoffs from late April 2026 would fill this in.
- The Phase D numbering (D-1, D-3, D-4, D-5, D-6) skips D-2. The reason for the gap is not in commit 6cbf3de's body or the master plan.
- The exact ordering of furniture placement within each room is not recoverable from git alone. The handoffs at `.handoffs/handoff-2026-04-27-*.md` through `.handoffs/handoff-2026-04-30-*.md` would have the per-piece sequence.
- The "audit fixes" referenced in commit 4756f6e's title are not enumerated in the commit body. They are described at a high level in the master plan but not pinned to specific lines.
- The collision-box audit from commit 4caf784 is not in the source files I read. It may live in one of the early handoffs.
- Phase 7.7 trim deferral for LDK and corridors lists "irregular L-shape" as the blocker, but the proposed polygon-based perimeter helper is not specified anywhere I read.
- (The naming gap between `addBedroomWallPaint` in the master plan and `addRoomPaint2F` in the actual code is documented in `flow-ozu-1-rendering.md`.)
