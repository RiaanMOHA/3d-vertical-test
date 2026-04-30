# Phase D — per-room 3D rebuild plan

Replaces placeholder mattress/toilet boxes in the interior scene's bedroom + wet-room zones with detailed geometry per each room's `room-map.md`.

Sources of truth (in priority order):
1. `interior-images/<room>/room-map.md` (per-room layout + furniture)
2. `blueprints/global-coords.md` (wall positions in code coords)
3. `interior-images/<room>/<corner-folder>/<photo>` (visual confirmation)

Reference quality: the dedicated `room-1` scene at [ozu-test.html:1141+](ozu-test.html#L1141) is the gold standard for furniture detail (iron bed, shelving, chair, AC, pendants, baseboards, real window frames). Apply the same level of detail in each interior-scene zone.

Pause for review after each phase.

---

## Phase D-1 — fix room-1 dedicated scene rotation, port into interior

The dedicated `room-1` scene has a **known 90° rotation bug** per `feedback_check_blueprint_japanese_label.md` and the `room-1/room-map.md` audit — closet/window/door layout doesn't match the blueprint.

Steps:
1. Read `interior-images/room-1/room-map.md` for compass orientation (window-wall, ac-wall, cabinet-wall, entrance-wall)
2. Re-derive correct positions in dedicated scene's local coords (RW=2.70, RD=2.70)
3. Fix the rotation in dedicated scene
4. Port the corrected geometry into the interior scene's room-1 zone (code x=3.60..6.30, z=4.50..7.20, y=F1H..F1H+F2H), replacing the mattress placeholder

**Status: not started.**

---

## Phase D-2 — room-4 fresh build ✓ DONE

Built furniture in interior scene's room-4 zone per `interior-images/room-4/room-map.md`:

| Item | Geometry |
|---|---|
| Iron-frame bed (single, head N foot S) | headboard + footboard + 2 side rails + mattress + accent pillow |
| Dark wood + black metal cabinet | base/drawer block + 2 vertical metal uprights + 3 dark wood shelves (open above) |
| Coat rack on entrance-wall | light-wood backing + 3 dark metal hooks projecting south |
| AC unit on window-wall | body + recessed grille + bottom vent slit (reuses LDK matACUnit/matACGrille/matACVent) |
| Curtains on sliding window | 4 vertical fabric strips with alternating z-offset folds |

**Deferred for D-2**:
- Frosted privacy window 縦すべり 02609 on frosted-wall (x=W=6.30) — needs structural change to add window opening on x=W exterior wall (currently no F2_WIN_RIGHT array, no window symbols on west exterior in code)
- Bi-fold closet doors visual style — currently a plain door panel in F2_DOORS

---

## Phase D-3 — room-3 fresh build

`room-3` (洋室1, SE 2F per real-world; code x=0..2.70, z=0..3.60) is structurally analogous to room-4 (mirror). Same wall-feature names (window-wall, frosted-wall, closet-wall, entrance-wall) with mirrored positions.

Per `interior-images/room-3/room-map.md`:
- Bed (similar to room-4)
- Dark wood + black metal **shelving (no drawers)** — different from room-4 cabinet
- Coat rack on entrance-wall
- AC unit on window-wall
- Sliding window 引違 15009 (already in F2_WIN_BACK)
- Frosted window 縦すべり 02609 (already in F2_WIN_LEFT)
- Note: 3-camera sweep (no D corner) — bed-head corner skipped for tripod

**Status: not started.**

---

## Phase D-4 — room-2 fresh build

`room-2` (洋室3, NE 2F per real-world; code x=0..2.70, z=4.50..7.20) — 4.5 帖 (2.7×2.7), smaller than 6帖 rooms.

Per `interior-images/room-2/room-map.md`:
- Iron-frame bed (different style from room-3/4 — all-white iron frame)
- Window-wall (north) with sliding window 引違 11909
- AC-wall (east, building exterior) with AC unit
- Entrance-wall (south) with door + coat rack
- Closet-wall (west, central column) with bi-fold

**Status: not started.**

---

## Phase D-5 — room-1 (after rotation fix in D-1)

After D-1 fixes the rotation, port the corrected room-1 geometry into the interior scene's room-1 zone.

**Status: blocked on D-1.**

---

## Phase D-6 — wet rooms (washroom, laundry, toilet-1-f)

Detail-level geometry for the 1F wet rooms. Currently each has a single fixture box (bathtub, washbasin, washing machine, toilet seat/tank).

Per kitchen / washroom / laundry / toilet-1-f maps:
- Washroom: bathtub + tile, vanity not in scope
- Laundry: vanity-wall with brick accent, washing machine, sink unit
- Toilet-1-f: bowl, tank, paper holder, brick-wall accent

**Status: not started.**

---

## Phase D-7 — genkan + corridor-1 + 1F stairs

Detail for entry zone:
- Genkan: front door, doormat, shoe storage 玄関収納
- Corridor-1: width per blueprint, no furniture
- 1F stairs: 5+6 step L-shape with proper carriages (per `feedback_no_floating_geometry.md`)

**Status: not started.**

---

## Phase D-8 — 2F toilet + corridor-2

Detail for 2F middle zone:
- 2F toilet: bowl, tank, frosted window, picture frame on long wall (TBD east vs west)
- 2F corridor: closet doors visible (mid-band closets)
- Stair carriage 2F portion

**Status: not started.**

---

## Order of execution (recommended)

1. ✓ D-2 (room-4) — done
2. **D-3 (room-3)** — next, mirrors D-2
3. D-4 (room-2) — different layout, 4.5帖
4. D-1 (room-1 rotation fix) + D-5 (port) — most complex
5. D-6 (wet rooms)
6. D-7 (genkan + corridor + stairs 1F)
7. D-8 (2F toilet + corridor + stairs 2F)

Pause for review after each. Each room is ~50-80 lines of geometry.
