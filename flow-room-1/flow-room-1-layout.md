# Flow: room-1 layout, decoupled

> Just the placement and geometry story for room-1: where things sit in 3D space, how the walls and windows and openings were defined, how furniture was positioned. No materials, no lights, no post-processing here. For the look-and-feel see `flow-room-1-rendering.md`. For the end-to-end picture see `flow-room-1-full.md`.

## 1. We started by reading the blueprint and the panoramas

Layout starts from two pieces of evidence: the blueprint and the photos. The blueprint at `ozu-test/blueprints/ozu-1-blueprint.pdf` gave the dimensions in metres. The four corner panoramas at `ozu-test/interior-images/room-1/corner-ac-entrance/`, `corner-ac-window/`, `corner-cabinet-entrance/`, and `corner-cabinet-window/` showed where furniture and fixtures actually sat (source: directory listing).

Anywhere the blueprint and the photos disagreed, the blueprint at 400 dpi won (source: CLAUDE.md source-of-truth-hierarchy rule).

## 2. We wrote down the global coordinates

A coordinate file was written at `ozu-test/blueprints/global-coords.md` (source: CLAUDE.md folder map). This translated blueprint metres into the 3D world's `x` (east-west), `y` (vertical), `z` (north-south) axes, with the south-west corner of the property at the origin.

A note in user memory says the blueprint X-mirror is a real thing and not to assume sides match without checking (source: CLAUDE.md memory pointer).

## 3. We placed room-1 inside the property bounds

Room-1 sits on floor 2, in the 2F bounds described as `x1: 3.60, z1: 4.50, x2: 6.30, z2: 7.20, y1: 2.5, y2: 5.0` (source: ozu-test.html line 889). The same bounds also appear at line 1662 where the wall-cutting logic uses them: "room-1: x=[3.60, W], z=[4.50, D]. Outer walls at z=D (front window) + x=W (right window)" (source: ozu-test.html line 1662).

`W` and `D` are the property width and depth constants, so room-1's east wall and north wall are also outer walls of the property.

## 4. We built the outer wall geometry first

Outer wall geometry was unified in commit 0046b8b ("unify exterior + interior wall geometry, add cladding split") and then split into two layers with the brown panel inset in commit 4e735e7 ("2-layer outer walls, brown panel inset, LDK polish, room-4 build") (source: git short-shas 0046b8b, 4e735e7).

Two-layer outer walls means an outer cladding face plus an inner finish face, with a thin gap between them, so window holes and panel insets can be cut at different depths.

## 5. We defined the window openings as numbered ranges

Each window in the property was registered as one entry in the F1_WIN or F2_WIN arrays. Editing the array updates both the exterior facade scene and the interior scene, because the array is the single source of truth (source: CLAUDE.md window-arrays-as-single-source-of-truth rule).

For room-1 specifically, two windows:

- The front sliding window (引違 11909) on the north wall: `a=4.105, b=5.795, y0=1.10, y1=2.00` (source: ozu-test.html line 1359, comment "room-1 引違 11909").
- The side narrow privacy window (縦すべり 02609) on the east wall: `a=5.720, b=5.980, y0=1.10, y1=2.00` (source: ozu-test.html line 1371, comment "room-1 縦すべり 02609 (NW bedroom)").

The corresponding sill and header bands appear at lines 625-626 (front, 引違 11909) and 668-669 (right, 縦すべり 02609) where the wall is split into the strip below the sill, the strip above the header, and the open hole between (source: ozu-test.html).

## 6. We cut the walls into segments around each window hole

The wall was cut into 4 segments around each window hole so the glass actually shows what's beyond instead of the wall behind it (source: `room-1-ONLY-rendering-plan.md` glass-and-windows section).

The four segments are: below the sill across the full window width, above the header across the full window width, and the two narrow strips on either side. The hole in the middle is where the glass pane sits.

## 7. We placed the doors and openings

Two openings on room-1's inner walls.

The bi-fold closet door is on the west wall (`x=3.60`) at `z=4.65 to 5.25`, opening between room-1 and the closet (source: ozu-test.html line 1502, "room-1 ↔ closet").

The hinged entrance door is on the south wall (`z=4.50`) at `x=3.80 to 4.40`, opening between the corridor and room-1 (source: ozu-test.html line 1507, "room-1 entrance").

Lines 1389 and 1395 show the corresponding wall-cuts: `wallZ(3.60, 4.50, D, [[4.65, 5.25]], F2H, F1H)` for the west wall closet opening, and `wallX(4.50, 3.60, 4.50, [[3.80, 4.40]], F2H, F1H)` for the south wall corridor opening (source: ozu-test.html).

## 8. We placed the floor

The floor was registered at `{ mat: FLOORS.room, x0: 3.60, z0: 4.50, x1: W, z1: D }` for room-1 (source: ozu-test.html line 1314). The floor material is the shared room floor (assigned later in the rendering flow, not here).

## 9. We placed the room trim

Room-1 got crown moulding and door trim added by `addRoomTrim(3.60, 4.50, W, D, F1H, F2H, F2_DOORS)` (source: ozu-test.html line 1569). The trim is part of the layout because it defines where the wall finish meets the ceiling and floor, but the trim's colour and material come later.

## 10. We placed furniture by reading the corner panoramas

Furniture placement was anchored to the four corner panoramas, never eyeballed (source: memory file `project_room1_visual_source_of_truth.md`).

The placement that came out of that, which lives inside the standalone `registerScene('room-1', ...)` block:

- An iron-frame bed with its long side against the ac-wall, ball finials on the four corner posts.
- A solid wood desk against the window-wall.
- An L-shape shelf with X-bracing at corner-cabinet-window.
- A desk chair.
- A white closet against the cabinet-wall (bi-fold pin handle, single vertical seam, not 2 horizontal knobs).
- A coat hook rail with two black peg hooks on the cabinet-wall near the entrance corner.
- A white entrance door panel with a chrome round doorknob (escutcheon, stem, sphere).
- A light switch plate on the entrance-wall next to the door.
- An intercom panel below the AC unit.
- Cream curtains either side of the sliding window, hourglass-bunched with a tieback ring.
- An AC unit on the ac-wall.
- Pendant lamps on a wood crossbar.

Source: `ozu-test/room-1-ONLY-rendering-plan.md` furniture-detail, ac-unit, and pendant-lamps sections.

## 11. We registered the chip viewpoint

A camera viewpoint named `room-1` was registered at position `[5.8, 4.1, 4.7]` looking at target `[4.0, 3.5, 7.0]` (source: ozu-test.html line 911). The viewpoint id matches the chip label and the photo folder name exactly (source: CLAUDE.md naming convention).

## How to repeat this for any other room

The repeatable layout sequence:

1. Read the blueprint, identify the room's bounds in metres.
2. Read every corner panorama for that room.
3. Add the room's bounds to the rooms array in the interior scene's config.
4. If any of the room's walls are also outer walls of the property, make sure the outer-wall geometry is already accounting for that.
5. Add each window in the room as an entry in the corresponding F1_WIN or F2_WIN array. Use the blueprint's window code (引違 11909, 縦すべり 02609, etc) as the inline comment so the array stays readable.
6. Add the wall-cut logic: split walls into segments around each window hole.
7. Add the corresponding sill-band and header-band wall pieces above and below the hole.
8. Place doors and inner-wall openings using `wallZ` and `wallX` cuts.
9. Add the floor as one entry in the floors array.
10. Add the trim with `addRoomTrim`.
11. Place furniture by reading the corner panoramas one at a time, anchoring each piece to a wall and to a position seen in the photo.
12. Register a chip viewpoint with id, label, and parent matching the folder name exactly.

The window arrays are the single source of truth: edit the array, both the exterior facade scene and the interior scene update (source: CLAUDE.md architecture section).

## Gaps i could not source

- The exact order in which furniture was placed during the build is not recoverable from git alone. Each commit groups multiple pieces together. The handoffs at `.handoffs/handoff-2026-04-27-*.md` through `.handoffs/handoff-2026-04-30-*.md` would have the per-piece sequence.
- The "collision-box audit" referenced in commit 4caf784 is not in the source files I read. It may live in one of the early handoffs.
- The exact wall-cutting algorithm (how `wallZ` and `wallX` decide segment boundaries) is described by output behaviour in the rendering plan but the function bodies were not read in detail. Reading the helper functions in `ozu-test.html` would fill this in.
