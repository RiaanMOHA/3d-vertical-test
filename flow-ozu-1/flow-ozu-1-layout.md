# Flow: Ozu-1 property layout, decoupled

> Just the placement and geometry story for the Ozu-1 property: where rooms sit, how outer walls and inner walls and openings are built, where every room's furniture got placed, where stairs and circulation go. No materials, no lights, no post-processing. For look-and-feel see `flow-ozu-1-rendering.md`. For end-to-end see `flow-ozu-1-full.md`.

## 1. We started by reading the blueprint and the panoramas

The blueprint at `ozu-test/blueprints/ozu-1-blueprint.pdf` gave dimensions in metres. The interior panoramas at `ozu-test/interior-images/<room>/corner-<id>/` showed where furniture and fixtures actually sat. The front-facade photos at `ozu-test/exterior-images/` showed the outside (source: directory listing, CLAUDE.md off-limits-paths list).

Anywhere blueprint and photos disagreed, the blueprint at 400 dpi won (source: CLAUDE.md source-of-truth-hierarchy rule). Never eyeball.

## 2. We translated the blueprint into global coordinates

Coordinates were written at `ozu-test/blueprints/global-coords.md` (source: CLAUDE.md folder map). The convention: `x` runs east-west, `y` runs vertical (up), `z` runs north-south. The south-west corner of the property sits at the origin.

A note in user memory: the blueprint X-mirror is a real thing and not to assume sides match without checking (source: CLAUDE.md memory pointer).

## 3. We listed every room with its bounds and floor

Each room got registered in the `rooms` array of the interior scene with bounds in metres. Room-1 (zone inside the master interior scene): `{ name: 'room-1', x1: 3.60, z1: 4.50, x2: 6.30, z2: 7.20, y1: 2.5, y2: 5.0 }` (source: ozu-test.html line 889). The other rooms follow the same shape.

For each room a corresponding floor entry went into the floors array, e.g. `{ mat: FLOORS.room, x0: 3.60, z0: 4.50, x1: W, z1: D }` for room-1 (source: ozu-test.html line 1314). `W` and `D` are the property width and depth constants.

## 4. We built the outer walls as one unified geometry

In commit 0046b8b ("unify exterior + interior wall geometry, add cladding split") the exterior and interior wall builders were merged into one geometry source feeding both scenes (source: git short-sha 0046b8b). This is what makes the F1_WIN and F2_WIN arrays a true single source of truth for both scenes.

In commit 4e735e7 ("2-layer outer walls, brown panel inset, LDK polish, room-4 build") the outer wall got split into two layers — outer cladding plus inner finish — with a thin gap between them so window holes and panel insets could be cut at different depths (source: git short-sha 4e735e7).

The cream upper section, the brown wood panel ground-floor inset, and all front-facade window holes are part of the outer-wall geometry (source: `ozu-test/master-plan.md` exterior section).

## 5. We defined every window as one entry in F1_WIN or F2_WIN

Each window in the property is one entry in either `F1_WIN_FRONT`, `F1_WIN_RIGHT`, `F2_WIN_FRONT`, or `F2_WIN_RIGHT` (source: ozu-test.html lines 617-721 and 1359-1389). The window code from the blueprint goes in the inline comment so the array stays readable.

Examples for the 2F (room-1 again as a worked example):

- Front sliding window for room-1 (引違 11909): `a=4.105, b=5.795, y0=1.10, y1=2.00` (source: ozu-test.html line 1359, inline comment).
- Side narrow privacy window for room-1 (縦すべり 02609, NW bedroom): `a=5.720, b=5.980, y0=1.10, y1=2.00` (source: ozu-test.html line 1371).

For each window the corresponding sill-band wall and header-band wall pieces are added at `solidWall(...)` calls referenced by the same window code, e.g. lines 625-626 for the room-1 front window (source: ozu-test.html).

The single-source-of-truth rule: editing one F1_WIN/F2_WIN entry updates both the exterior facade scene and the interior scene because both scenes read from the same array (source: CLAUDE.md window-arrays-as-single-source-of-truth rule).

## 6. We cut the walls into segments around each window hole

For each window, the wall got split into 4 segments: below the sill (full window width), above the header (full window width), and the two narrow strips on either side. The hole between is where the glass pane sits.

This lets the glass actually look through to what's beyond instead of looking at the wall behind it. The full geometry-cutting pattern is documented in the room-1 rendering plan but applies to every window in the property (source: `ozu-test/room-1-ONLY-rendering-plan.md` glass-and-windows section).

## 7. We placed the inner-wall doors and openings

Each interior doorway is one entry in a doors array. Three properties decide its shape: the wall axis (`X` or `Z`), the wall coordinate (`c`), and the open range (`a` to `b`). Plus a door type (sliding, hinged, bi-fold, archway).

For room-1 the two openings:

- `{ axis: 'Z', c: 3.60, a: 4.65, b: 5.25, mat: closetDoorMat, type: 'bi-fold' }` — the closet bi-fold door (source: ozu-test.html line 1502, "room-1 ↔ closet").
- `{ axis: 'X', c: 4.50, a: 3.80, b: 4.40, mat: doorMat }` — the entrance door (source: ozu-test.html line 1507, "room-1 entrance").

Wall cuts are issued by `wallZ` and `wallX` helpers that take the wall coordinates plus an array of opening x-ranges, e.g. `wallZ(3.60, 4.50, D, [[4.65, 5.25]], F2H, F1H)` cuts a Z-axis wall with one opening between `4.65` and `5.25` (source: ozu-test.html lines 1389 and 1395).

In Phase 2 of the master plan the 14 generic flat panel doors were each replaced with the right type per the blueprint: sliding (Japanese-style), hinged, bi-fold, archway (source: `ozu-test/master-plan.md` phase-2 section, status: done).

## 8. We placed every room's furniture by reading its panoramas

Furniture for each room was placed by reading that room's corner panoramas one at a time, anchoring each piece to a wall and to a position seen in the photo, never eyeballed (source: memory file `project_room1_visual_source_of_truth.md`, generalises to all rooms).

The furniture inventory across all rooms (source: `ozu-test/master-plan.md` what's-actually-done section):

**LDK (Living / Dining / Kitchen):**
- Sofa, dining table, coffee table, TV console with directional screen face.
- Kitchen counter with two-piece pass-through.
- Antique clock.
- Pendant lights over dining and sofa.
- AC unit body.
- Window curtains as folded fabric strips.

**Room-2:**
- All-white iron-frame bed.
- Taupe column.
- Desk plus chair.
- Coat rack.
- AC.
- Sliding window with curtains.

**Room-3:**
- Iron-frame bed with wood headboard.
- 4-tier open shelving (no drawers).
- Coat rack.
- AC.
- Sliding window with curtains.

**Room-4:**
- Iron-frame bed.
- Dark-wood plus black-metal cabinet.
- Coat rack.
- AC.
- Sliding window with curtains.

**Room-1 zone (inside the interior scene, distinct from the standalone sandbox):**
- Iron-frame bed.
- Solid wood desk.
- L-shaped shelf.
- Coat rack.
- AC.
- Sliding window with curtains.

**Bathroom (washroom):**
- Bathtub.
- Tub tap.
- Shower bar plus shower head.
- Towel rail.

**Laundry:**
- Washing machine with chrome top panel.
- Vanity cabinet plus countertop plus round basin.
- Faucet.
- Sconce light.

**1F toilet:**
- Bowl.
- Tank.
- Hand-wash basin atop tank.
- Toilet-paper holder.

**2F toilet (after Phase 4):**
- Bowl.
- Tank.
- Hand-wash basin.
- Paper holder.
- Frosted privacy window detail.

**Genkan (front entry, after Phase 3):**
- Doormat.
- Shoe storage cabinet (玄関収納).
- 土間 step-down (150 mm).
- 上がり框 wood lip step.

## 9. We added the ceilings

Phase 1 of the master plan added a ceiling to each room, the corridor, and the entry — one sweep across the whole house (source: `ozu-test/master-plan.md` phase-1 section, status: done). Looking up no longer shows sky.

## 10. We built the staircases

Initially each step was a stacked box with no proper sloped underside, no handrail, no side brackets. Phase 5 of the master plan replaced each step with a real sloped-wedge step, added handrails, and added wooden side brackets / carriage. Applied to both ground-floor and second-floor staircases (source: `ozu-test/master-plan.md` phase-5 section, status: done).

A 2F top-of-stair parapet was added during Phase 7.5 to close the 1.10 m guard gap at the south edge of the stair shaft — documented but missing before (source: `ozu-test/master-plan.md` phase-7.5 section).

## 11. We added smoke detectors and the genkan step geometry

During Phase 7.5: smoke detectors (住宅用火災警報器) were added on every 2F bedroom ceiling and at the top of the stair, mandatory per 消防法. The genkan got the 土間 step-down (150 mm) plus the 上がり框 wood lip step — proper Japanese front-entry geometry (source: `ozu-test/master-plan.md` phase-7.5 section).

## 12. We added the trim perimeter for every clean rectangular room

Phase 7.7 added the trim layer using one shared `trimMat`. A reusable helper `addRoomTrim(x0, z0, x1, z1, yFloor, ceilH, doorList)` handles baseboard plus crown plus door cuts for any clean rectangular room. The `addDoor` helper draws four trim strips per door (two vertical jambs, one top header, on each face of the wall). 70 mm wide × 12 mm proud. Baseboards 70 mm tall along the floor perimeter. Crown moulding 50 mm at the ceiling line (source: `ozu-test/master-plan.md` phase-7.7 section).

Trim landed in all four 2F bedrooms and on all 14 doors. Deferred for the LDK (irregular L-shape needs a polygon-based perimeter helper), the corridors (also irregular), the closets (small enough not to matter visually), and the wet rooms (JP wet rooms typically don't have wood baseboards) (source: same).

## 13. We registered the chip viewpoints

Each room got a chip viewpoint in the navigation array. The id, label, and parent fields match the photo folder names exactly (source: CLAUDE.md naming convention). Example for room-1: `{ id: 'room-1', label: 'room-1', parent: '2f', pos: [5.8, 4.1, 4.7], tgt: [4.0, 3.5, 7.0] }` (source: ozu-test.html line 911).

The QA chip-navigation tool itself landed in commit 6cbf3de (source: git short-sha 6cbf3de).

## How to repeat this layout flow on the next property

The repeatable layout sequence for any whole-property build:

1. Read the blueprint at high resolution. Identify every room's bounds in metres.
2. Read every corner panorama in `ozu-test/interior-images/<room>/corner-<id>/`.
3. Read the front-facade photos at `ozu-test/exterior-images/`.
4. Translate blueprint metres into global coordinates and write to `ozu-test/blueprints/global-coords.md`.
5. Write a per-room map at `ozu-test/interior-images/<room>/room-map.md` for every room.
6. Set up `ozu-test.html` with one `registerScene` block per scene (exterior, interior, plus any standalone sandboxes).
7. Build a unified outer + inner wall geometry (one builder, one F1_WIN / F2_WIN array per floor and per side).
8. Split the outer wall into two layers (outer cladding plus inner finish) so window holes and panel insets can be cut at different depths.
9. Add every window as one entry in the appropriate F1_WIN or F2_WIN array. Inline-comment with the blueprint window code (引違 11909, 縦すべり 02609, etc).
10. Cut every wall into 4 segments around each window hole (sill band, header band, two side strips).
11. Add every interior doorway as one entry in the doors array with axis, coordinate, range, and door type.
12. Issue wall cuts via `wallZ` and `wallX` for each opening.
13. Add every room's floor as one entry in the floors array.
14. Add a ceiling to every room, the corridor, and the entry. One sweep.
15. Place each room's furniture by reading its corner panoramas one at a time. Anchor each piece to a wall and to a position seen in the photo. Never eyeball.
16. Build both staircases as proper sloped-wedge steps with handrails and wooden side brackets / carriage.
17. Add a 2F top-of-stair parapet to close any guard gap.
18. Add the genkan 土間 step-down (150 mm) and 上がり框 wood lip step.
19. Add the trim layer using one shared `trimMat` plus the `addRoomTrim` helper for every clean rectangular room.
20. Register one chip viewpoint per room with id, label, and parent matching the photo folder name exactly.

## Gaps i could not source

- The exact ordering of furniture placement within each room is not recoverable from git alone. The handoffs at `.handoffs/handoff-2026-04-27-*.md` through `.handoffs/handoff-2026-04-30-*.md` would have the per-piece sequence.
- The collision-box audit from commit 4caf784 is not in the source files I read. It may live in one of the early handoffs.
- The exact wall-cutting algorithm (how `wallZ` and `wallX` decide segment boundaries) is described by output behaviour in the rendering plan but the function bodies were not read in detail. Reading the helper functions in `ozu-test.html` would fill this in.
- The polygon-based perimeter helper that would unblock LDK and corridor trim is mentioned in the master plan as the next step but not specified.
- Some photo folders are still named `a/b/c/d` instead of by which corner they show — the rename script proposed in Phase 8 has not run yet, so the photo-folder naming is partly inconsistent across rooms.
