# Flow: Ozu-1 property layout, decoupled

> Just the placement and geometry story for the Ozu-1 property: where rooms sit, how outer walls and inner walls and openings are built, where every room's furniture got placed, where stairs and circulation go. No materials, no lights, no post-processing. For look-and-feel see `flow-ozu-1-rendering.md`. For end-to-end see `flow-ozu-1-full.md`. The standalone room-1 sandbox layout flow lives at `../flow-room-1/flow-room-1-layout.md`.

> See `glossary.md` in this folder for definitions of `F1_WIN`/`F2_WIN`, `wallX`/`wallZ`, `F1H`/`F2H`, `W`/`D`, bi-fold, and the JP residential door types used in this doc.

## 1. We started by reading the blueprint and the panoramas

The blueprint at `ozu-test/blueprints/ozu-1-blueprint.pdf` gave dimensions in metres. The interior panoramas at `ozu-test/interior-images/<room>/corner-<id>/` showed where furniture and fixtures actually sat. The front-facade photos at `ozu-test/exterior-images/` showed the outside (source: directory listings of those folders, plus CLAUDE.md off-limits-paths list).

Anywhere blueprint and photos disagreed, the blueprint at 400 dpi won (source: CLAUDE.md source-of-truth-hierarchy rule). Never eyeball.

## 2. We translated the blueprint into global coordinates

Coordinates were written at `ozu-test/blueprints/global-coords.md` (source: CLAUDE.md folder map). The convention: `x` runs east-west, `y` runs vertical (up), `z` runs north-south. The south-west corner of the property sits at the origin.

A note in user memory: the blueprint X-mirror is a real thing and not to assume sides match without checking (source: memory file `project_blueprint_x_mirror.md`, referenced from CLAUDE.md "Where additional context lives" section).

## 3. We listed every room with its bounds and floor

Each room got registered in the `rooms` array of the interior registerScene block with bounds in metres. Find this array by searching `ozu-test.html` for the literal string `name: 'room-1'` (the room-1 entry sits in the array). The room-1 entry reads `{ name: 'room-1', x1: 3.60, z1: 4.50, x2: 6.30, z2: 7.20, y1: 2.5, y2: 5.0 }`.

For each room a corresponding floor entry went into the floors array, e.g. `{ mat: FLOORS.room, x0: 3.60, z0: 4.50, x1: W, z1: D }` for room-1. Find the floors block by searching for `FLOORS.room` near the inline comment `// room-1`.

## 4. We built the outer walls as one unified geometry

In commit 0046b8b ("unify exterior + interior wall geometry, add cladding split") the exterior and interior wall builders were merged into one geometry source feeding both scenes (source: git short-sha 0046b8b). This is what makes the F1_WIN and F2_WIN arrays a true single source of truth for both scenes.

In commit 4e735e7 ("2-layer outer walls, brown panel inset, LDK polish, room-4 build") the outer wall got split into two layers: outer cladding plus inner finish, with a thin gap between them so window holes and panel insets could be cut at different depths (source: git short-sha 4e735e7).

The cream upper section, the brown wood panel ground-floor inset, and all front-facade window holes are part of the outer-wall geometry (source: `ozu-test/master-plan.md`, "Exterior" section).

## 5. We defined every window as one entry in F1_WIN or F2_WIN

Each window in the property is one entry in either `F1_WIN_FRONT`, `F1_WIN_RIGHT`, `F2_WIN_FRONT`, or `F2_WIN_RIGHT` (plus the `_LEFT` and `_BACK` variants where applicable). Find these arrays by searching `ozu-test.html` for `F1_WIN_FRONT`, `F2_WIN_FRONT`, etc. The window code from the blueprint goes in the inline comment so the array stays readable.

Examples for the 2F (room-1 again as a worked example):

- Front sliding window for room-1 (引違 11909): `a=4.105, b=5.795, y0=1.10, y1=2.00`. Find it by searching for the comment `room-1 引違 11909`.
- Side narrow privacy window for room-1 (縦すべり 02609, NW bedroom): `a=5.720, b=5.980, y0=1.10, y1=2.00`. Find it by searching for `room-1 縦すべり 02609 (NW bedroom)`.

For each window the corresponding sill-band wall and header-band wall pieces are added as `solidWall(...)` calls flagged with the same window code. Find the room-1 ones by searching `ozu-test.html` for `room-1 引違 11909 sill` and `room-1 縦すべり 02609 sill`.

The single-source-of-truth rule: editing one F1_WIN/F2_WIN entry updates both the exterior facade scene and the interior scene because both scenes read from the same array (source: CLAUDE.md window-arrays-as-single-source-of-truth rule).

## 6. We cut the walls into segments around each window hole

For each window, the wall got split into 4 segments: below the sill (full window width), above the header (full window width), and the two narrow strips on either side. The hole between is where the glass pane sits.

This lets the glass actually look through to what's beyond instead of looking at the wall behind it. The full geometry-cutting pattern is documented in the room-1 rendering plan but applies to every window in the property (source: `ozu-test/room-1-ONLY-rendering-plan.md`, "Glass + windows" section).

## 7. We placed the inner-wall doors and openings

Each interior doorway is one entry in a doors array. Three properties decide its shape: the wall axis (`X` or `Z`), the wall coordinate (`c`), and the open range (`a` to `b`). Plus a door type (sliding, hinged, bi-fold, archway).

For room-1 the two openings (find by searching `ozu-test.html` for `room-1 ↔ closet` and `room-1 entrance`):

- `{ axis: 'Z', c: 3.60, a: 4.65, b: 5.25, mat: closetDoorMat, type: 'bi-fold' }`. The closet bi-fold door.
- `{ axis: 'X', c: 4.50, a: 3.80, b: 4.40, mat: doorMat }`. The entrance door (no `type` field means hinged).

Wall cuts are issued by `wallZ` and `wallX` helpers that take the wall coordinates plus an array of opening x-ranges. For room-1's closet opening: `wallZ(3.60, 4.50, D, [[4.65, 5.25]], F2H, F1H)`. For its corridor entrance: `wallX(4.50, 3.60, W, [[4.50, 5.20]], F2H, F1H)`. Find these by searching for `room-1 west wall, closet bi-fold` and `room-1 south wall, corridor entrance`.

In Phase 2 of the master plan the 14 generic flat panel doors were each replaced with the right type per the blueprint: sliding (Japanese-style), hinged, bi-fold, archway (source: `ozu-test/master-plan.md`, "Phase 2" section, status: done).

## 8. We placed every room's furniture by reading its panoramas

Furniture for each room was placed by reading that room's corner panoramas one at a time, anchoring each piece to a wall and to a position seen in the photo, never eyeballed (source: memory file `project_room1_visual_source_of_truth.md`, generalises to all rooms).

The furniture inventory across all rooms (source: `ozu-test/master-plan.md`, "What's actually done" section):

**LDK (Living / Dining / Kitchen):** sofa, dining table, coffee table, TV console with directional screen face, kitchen counter with two-piece pass-through, antique clock, pendant lights over dining and sofa, AC unit body, window curtains as folded fabric strips.

**Room-2:** all-white iron-frame bed, taupe column, desk plus chair, coat rack, AC, sliding window with curtains.

**Room-3:** iron-frame bed with wood headboard, 4-tier open shelving (no drawers), coat rack, AC, sliding window with curtains.

**Room-4:** iron-frame bed, dark-wood plus black-metal cabinet, coat rack, AC, sliding window with curtains.

**Room-1 zone (inside the interior scene, distinct from the standalone sandbox):** iron-frame bed, solid wood desk, L-shaped shelf, coat rack, AC, sliding window with curtains.

**Bathroom (washroom):** bathtub, tub tap, shower bar plus shower head, towel rail.

**Laundry:** washing machine with chrome top panel, vanity cabinet plus countertop plus round basin, faucet, sconce light.

**1F toilet:** bowl, tank, hand-wash basin atop tank, toilet-paper holder.

**2F toilet (after Phase 4):** bowl, tank, hand-wash basin, paper holder, frosted privacy window detail.

**Genkan (front entry, after Phase 3):** doormat, shoe storage cabinet (玄関収納, shoe storage), 土間 step-down (150 mm, the lower entrance floor), 上がり框 wood lip step (separates 土間 from the rest of the house).

## 9. We added the ceilings

Phase 1 of the master plan added a ceiling to each room, the corridor, and the entry. One sweep across the whole house (source: `ozu-test/master-plan.md`, "Phase 1" section, status: done). Looking up no longer shows sky.

## 10. We built the staircases

Initially each step was a stacked box with no proper sloped underside, no handrail, no side brackets. Phase 5 of the master plan replaced each step with a real sloped-wedge step, added handrails, and added wooden side brackets / carriage. Applied to both ground-floor and second-floor staircases (source: `ozu-test/master-plan.md`, "Phase 5" section, status: done).

A 2F top-of-stair parapet was added during Phase 7.5 to close the 1.10 m guard gap at the south edge of the stair shaft. The gap was documented but missing before (source: `ozu-test/master-plan.md`, "Phase 7.5" section).

## 11. We added smoke detectors and the genkan step geometry

During Phase 7.5: smoke detectors (住宅用火災警報器, residential fire alarm) were added on every 2F bedroom ceiling and at the top of the stair. Mandatory per 消防法 (Japanese fire-safety law). The genkan got the 土間 step-down (150 mm) plus the 上がり框 wood lip step. Proper Japanese front-entry geometry (source: `ozu-test/master-plan.md`, "Phase 7.5" section).

## 12. We added the trim perimeter for every clean rectangular room

Phase 7.7 added the trim layer using one shared `trimMat`. A reusable helper `addRoomTrim(x0, z0, x1, z1, yFloor, ceilH, doorList)` handles baseboard plus crown plus door cuts for any clean rectangular room. The `addDoor` helper draws four trim strips per door (two vertical jambs, one top header, on each face of the wall). 70 mm wide and 12 mm proud (sticking out from the wall surface). Baseboards 70 mm tall along the floor perimeter. Crown moulding 50 mm at the ceiling line (source: `ozu-test/master-plan.md`, "Phase 7.7" section).

Trim landed in all four 2F bedrooms and on all 14 doors. Deferred for the LDK (irregular L-shape needs a polygon-based perimeter helper), the corridors (also irregular), the closets (small enough not to matter visually), and the wet rooms (JP wet rooms typically don't have wood baseboards) (source: same).

## 13. We registered the chip viewpoints

Each room got a chip viewpoint in the navigation array. The id, label, and parent fields match the photo folder names exactly (source: CLAUDE.md naming convention). Example for room-1: `{ id: 'room-1', label: 'room-1', parent: '2f', pos: [5.8, 4.1, 4.7], tgt: [4.0, 3.5, 7.0] }`. Find by searching `ozu-test.html` for `id: 'room-1'`.

The QA chip-navigation tool itself landed in commit 6cbf3de (source: git short-sha 6cbf3de).

## How to repeat this layout flow on the next property

The repeatable layout sequence for any whole-property build. **Before you start:** copy `ozu-test.html` to `<property-name>.html` and gut the contents of every `registerScene(...)` block, but keep the helper functions (`wallX`, `wallZ`, `addDoor`, `addRoomTrim`, `addRoomPaint2F`) and the F1_WIN / F2_WIN array shapes. Then run these in order. Hard-reload after each step. Visually verify against the panoramas before moving on.

1. Read the blueprint at high resolution. Identify every room's bounds in metres.
2. Read every corner panorama in `<property-name>/interior-images/<room>/corner-<id>/`.
3. Read the front-facade photos at `<property-name>/exterior-images/`.
4. Translate blueprint metres into global coordinates and write to `<property-name>/blueprints/global-coords.md`.
5. Write a per-room map at `<property-name>/interior-images/<room>/room-map.md` for every room.
6. Add the property width and depth as `W` and `D` constants in the project script.
7. Build the unified outer wall geometry: one builder, one `F1_WIN_*` and `F2_WIN_*` array per floor and per side (FRONT, RIGHT, LEFT, BACK).
8. Split the outer wall into two layers (outer cladding plus inner finish) so window holes and panel insets can be cut at different depths. Skip the panel-inset layer if your property has none.
9. Add every window as one entry in the appropriate F1_WIN or F2_WIN array. Inline-comment with the blueprint window code (引違 11909, 縦すべり 02609, etc, if JP).
10. Cut every wall into 4 segments around each window hole (sill band, header band, two side strips). Reuse the `solidWall(...)` pattern from Ozu-1.
11. Add every room's bounds to the rooms array of the interior registerScene block: `{ name, x1, z1, x2, z2, y1, y2 }`.
12. Add every interior doorway as one entry in the doors array: `{ axis, c, a, b, mat, type? }`. The four door types are sliding, hinged, bi-fold (folding closet), archway. Set type to `'bi-fold'` for closets, omit for hinged, set to `'sliding'` for Japanese-style sliding doors.
13. Issue wall cuts via `wallZ` and `wallX` for each opening: `wallZ(x, z_start, z_end, [[door_a, door_b]], F2H, F1H)` and similar for `wallX`.
14. Add every room's floor as one entry in the floors array: `{ mat: FLOORS.room, x0, z0, x1, z1 }`.
15. Add a ceiling to every room, the corridor, and the entry. One sweep. (Helper does not exist; add a simple plane mesh per room at `y = ceilH`.)
16. Place each room's furniture by reading its corner panoramas one at a time. Anchor each piece to a wall and to a position seen in the photo. Never eyeball. Hard-reload after each piece.
17. Build any staircases as proper sloped-wedge steps with handrails and wooden side brackets / carriage. Skip if no stairs.
18. Add a top-of-stair parapet wherever a guard gap exists. Conditional on stair geometry.
19. (JP-specific, skip for non-JP properties.) Add the genkan 土間 step-down (150 mm) and 上がり框 wood lip step.
20. Add the trim layer using one shared `trimMat` plus the `addRoomTrim(x0, z0, x1, z1, yFloor, ceilH, doorList)` helper for every clean rectangular room. Defer irregular rooms (L-shapes, corridors, wet rooms) until a polygon-based helper is written.
21. Register one chip viewpoint per room with `{ id, label, parent, pos, tgt }`. The id, label, and parent must match the photo folder name exactly. Pick `pos` by standing the camera in one corner of the room and `tgt` at the opposite corner.

Steps marked JP-specific (step 19, plus smoke detectors which are not in this layout flow) only apply to Japanese residential properties.

## Gaps i could not source

- The exact ordering of furniture placement within each room is not recoverable from git alone. The handoffs at `.handoffs/handoff-2026-04-27-*.md` through `.handoffs/handoff-2026-04-30-*.md` would have the per-piece sequence.
- The collision-box audit from commit 4caf784 is not in the source files I read. It may live in one of the early handoffs. Walk mode was later cut entirely so the audit is no longer load-bearing.
- The exact wall-cutting algorithm (how `wallZ` and `wallX` decide segment boundaries) is described by output behaviour in the rendering plan but the function bodies were not read in detail. Read `wallX` and `wallZ` directly in `ozu-test.html` (search for `function wallX` / `function wallZ`) for the algorithm.
- The polygon-based perimeter helper that would unblock LDK and corridor trim is mentioned in the master plan as the next step but not specified.
- Some photo folders are still named `a/b/c/d` instead of by which corner they show. The rename script proposed in Phase 8 has not run yet, so the photo-folder naming is partly inconsistent across rooms.
