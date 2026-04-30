# room-4 map (= SW 2F room, 寝室)

## overview

room-4 is the **SW 2F room (寝室)**, 6 帖, 2.7 × 3.6 m per blueprint (footprint 9.72 ㎡). The Japanese label on the blueprint is **寝室** (shinshitsu / sleep room), with a pink **Room4** annotation. Per the annotated blueprint corner-letter scheme, this room has 4 corner camera positions (purple letters: A, B, C, D — matching the 4 sub-folders a/b/c/d).

approximate dimensions:
- width: 2.7 m (E-W per blueprint)
- depth: 3.6 m (N-S per blueprint)
- footprint: 9.72 ㎡ (6 帖) per blueprint
- ceiling: whitewashed wood-plank (matches the 2F room + corridor convention)
- floor: light maple plank (matches the 2F convention)
- walls: warm taupe-grey paint

## walls

### window-wall (south exterior)
- **exterior wall**, ~2.7 m long
- contains: **large sliding window** (引違 15009 — note: this is the LARGER window size used for the 6帖 rooms, vs 引違 11909 used for 4.5帖 rooms like room-1/room-2) with cream curtains and tieback
- contains: **wall-mounted Toshiba AC unit** mounted high on this wall, near one corner
- (similar to room-3, room-4 has the AC and the large sliding window on the SAME wall — different from room-1/room-2 where they're on separate walls)
- opposite: entrance-wall

### frosted-wall (west exterior)
- **exterior wall**, ~3.6 m long
- contains: **narrow vertical frosted privacy window** (縦すべり 02609, FL+2000) high on the wall
- otherwise plain taupe paint
- opposite: closet-wall

### closet-wall (east interior — partition with the central closet column)
- **interior partition**, ~3.6 m long
- partition with the central 0.9 m closet column between room-4 and room-3 (per blueprint chain 2700+900+2700)
- contains: **white painted bi-fold closet doors** (visible in `b/01`)
- visible features: dark wood + black metal freestanding shelving unit positioned along this wall (with drawer compartments at the bottom + open shelves above — visible in `a/01`, `b/01`, `d/01`)
- opposite: frosted-wall

### entrance-wall (north interior — partition with the 2F corridor)
- **interior partition**, ~2.7 m long
- contains: **single hinged white door (開き)** from the 2F corridor (corridor's south arm)
- contains: **multi-hook coat rack** (light wood backing with dark/black metal hooks — visible in `a/01`, `d/01`); identical to room-2 and room-3's coat racks
- AC remote control panel + light switch on this wall near the door (visible in `a/01` thermostat panel, `b/01` AC remote)
- opposite: window-wall

## adjacencies

- window-wall meets frosted-wall and closet-wall
- entrance-wall meets frosted-wall and closet-wall
- frosted-wall meets window-wall and entrance-wall
- closet-wall meets window-wall and entrance-wall

## corners

| corner id | walls meeting | location | notes |
|---|---|---|---|
| corner-closet-entrance | closet-wall × entrance-wall | NE | door from corridor + bi-fold closet doors meet here; dark shelving sits along closet-wall starting near this corner |
| corner-closet-window | closet-wall × window-wall | SE | dark cabinet (with drawers) + window/AC corner; bed-foot likely positioned here |
| corner-frosted-entrance | frosted-wall × entrance-wall | NW | corner-of-room with frosted window above + entrance corner |
| corner-frosted-window | frosted-wall × window-wall | SW | corner with both exterior walls meeting; AC + sliding window adjacent + frosted window adjacent |

corner ids list walls in alphabetical order (room-1 convention).

## room layout (top-down, with compass orientation: window-wall=S, frosted-wall=W, closet-wall=E, entrance-wall=N)

✓ compass orientation locked in by Phase C global coords (`blueprints/global-coords.md`). Relative positions are also confirmed by photos.

```
                       entrance-wall  (N interior, door from corridor)
       ┌─────────────────────────────────────────┐
       │ [coat rack + thermostat panel]   [hinged door]
       │                                         │
       │                                         │
       │                                         │ closet
   frosted│            room-4                    │  wall
   wall │              寝室                      │ (E int.)
       │           6 帖, 2.7 × 3.6              │ [bi-fold
   [narrow│                                       │  closet
   vertical│                                      │  doors]
   frosted │                                      │
   window  │     [bed running N-S along           │ [dark wood +
    high]  │      closet-wall area;               │  black metal
       │      bed foot toward S window-wall]    │  shelving
       │                                         │  with drawers
       │                                         │  at bottom]
       │                                         │
       │ [AC unit high]    [large sliding        │
       │                    window 引違 15009     │
       │                    + curtains]          │
       └─────────────────────────────────────────┘
                       window-wall  (S exterior, AC + large sliding window)
```

(bed orientation: from photos, bed appears to run with foot toward S window-wall and head toward N entrance-wall; exact placement TBD via phase D)

## camera-position mapping

⚠ TENTATIVE — folders are still letter-coded (`a/`, `b/`, `c/`, `d/`), not yet renamed to corner-X-Y. Photo-content reasoning below.

| current path | photo count | tentative position | photo evidence |
|---|---|---|---|
| `a/` | 8 | corner-frosted-entrance (NW) | `a/01` shows: bed visible far-left (in distance), high small white window on left wall (likely the 縦すべり 02609 frosted window on frosted-wall), tall freestanding shelving (open shelves) on right with multi-hook coat rack and thermostat panel on the wall behind (entrance-wall side). Camera at NW sees bed and frosted window across the room (south + west) and shelving + coat rack on near side (east + north). |
| `b/` | 9 | corner-closet-entrance (NE) | `b/01` shows: open white door on the left (entrance-wall door), corridor visible through doorway (with another doorway and bedroom visible far), white bi-fold closet doors on the right (closet-wall), back of dark shelving on left foreground, AC remote panel mounted on metal frame. Camera at NE sees both adjacent walls (entrance + closet). |
| `c/` | 9 | corner-frosted-window (SW) | `c/01` shows: bed in foreground (running into frame), AC unit + large curtained sliding window visible on the left wall (window-wall, on camera-LEFT when sweep starts pointing at frosted-wall). Camera at SW sees both exterior walls. |
| `d/` | 9 | corner-closet-window (SE) | `d/01` shows: bed in foreground (foot end), dark wood + black metal cabinet/shelving with 9 drawer compartments + shelves above ahead (against closet-wall), coat rack on far wall (entrance-wall, north), small high vertical frosted window on far-left wall (frosted-wall, west). Camera at SE sees both adjacent walls (closet + window) and looks NW toward the diagonally-opposite corner. |

⚠ all 4 mappings are TENTATIVE pending phase D photo-by-photo verification. corner-letter assignment from the blueprint annotated jpeg (purple A/B/C/D) → folders (a/b/c/d) needs corner-letter-confirmation in phase D.

## panorama sweep direction

clockwise from above (per room-1 convention). sequence 01 starts the sweep, highest number ends it.

## furniture / fixture anchors

- **single iron-frame bed** with dark iron rails: positioned roughly along the closet-wall side or in the middle of the room; head toward N entrance-wall, foot toward S window-wall (TENTATIVE — phase D to confirm exact placement). Cream / off-white bedding with grey accent pillow (similar to room-3's bedding style).
- **dark wood + black metal freestanding shelving / cabinet (with drawers)**: along closet-wall, near the SE corner area. Has 9 drawer compartments at the bottom (3×3 grid with dark wood drawer fronts and metal pull handles) + open shelves above. Different from room-3's all-shelf unit (room-3 has open shelves with mesh; room-4 has drawers + shelves).
- **multi-hook coat rack**: on entrance-wall (light wood backing with dark/black metal hooks); identical style to room-2 + room-3's coat racks
- **AC remote panel + light switch**: mounted on entrance-wall near the door
- **wall-mounted Toshiba AC unit**: high on window-wall, near corner-frosted-window (SW)
- **bi-fold closet doors**: white painted, 2-panel bi-fold style on closet-wall (not yet measured for exact extent — phase D)
- **ceiling light**: TBD — not clearly visible in sampled `01` frames

## folder structure (current — letter-coded, not yet renamed)

```
room-4/
├── room-map.md          (this file)
├── room-map-photos.md   (photo→wall index)
├── a/   (8 images — tentative NW corner: corner-frosted-entrance)
├── b/   (9 images — tentative NE corner: corner-closet-entrance)
├── c/   (9 images — tentative SW corner: corner-frosted-window)
└── d/   (9 images — tentative SE corner: corner-closet-window)
```

## proposed rename

deferred until camera positions are confirmed in phase D. once confirmed:

```bash
cd /Users/riaan/3d-vertical-test/ozu-test/interior-images/room-4
mv a corner-frosted-entrance
mv b corner-closet-entrance
mv c corner-frosted-window
mv d corner-closet-window

for d in corner-frosted-entrance corner-closet-entrance corner-frosted-window corner-closet-window; do
  cd "$d"
  i=1
  for f in $(ls *.webp 2>/dev/null | sort -V); do
    padded=$(printf "%02d" $i)
    mv "$f" "room-4-$d-$padded.webp"
    i=$((i+1))
  done
  cd ..
done
```

(don't run until confirmed.)

## unverified items

- exact compass orientation locked in: window-wall=S, frosted-wall=W, closet-wall=E, entrance-wall=N (per `blueprints/global-coords.md`)
- exact dimensions (2.7 × 3.6 read from blueprint at 400 dpi)
- ceiling height (assumed 2.4 m to match other 2F rooms)
- camera-position assignments for `a/`, `b/`, `c/`, `d/` (photo-content reading is plausible but not corner-letter-confirmed)
- exact bed orientation and placement (tentative head-N / foot-S along closet-wall area)
- exact bi-fold closet extent on closet-wall (full-wall vs partial — phase D)
- exact placement of dark cabinet/shelving along closet-wall
- door type (currently inferred hinged 開き from `b/01`; re-confirm via blueprint arc in phase E)
- exact swing direction of the entrance door (TBD via phase E)
- specific blueprint corner-letter assignments (purple A/B/C/D visible on annotated jpeg) → which folder maps to which letter — TBD via phase D

## usage notes

- always reference walls by feature name (window-wall, frosted-wall, closet-wall, entrance-wall) — like room-3, this room has the AC and large sliding window on the SAME wall (window-wall), so there's no separate "ac-wall" name
- corners are alphabetical wall pairs (corner-closet-entrance, not corner-entrance-closet)
- room-4 is the **second 6帖 room mapped** (after room-3); structurally a mirror of room-3 (room-3 is SE, room-4 is SW). same window types (引違 15009 + 縦すべり 02609), same wall convention.
- material sampling from photos:
  - whitewashed wood-plank ceiling: every frame
  - light maple plank floor: every frame
  - taupe-grey wall paint: every frame
  - large curtained sliding window 引違 15009 + AC: `c/01` (left wall), partial in `d/01`
  - narrow vertical frosted window 縦すべり 02609: `a/01` (left, near bed), `d/01` (far-left)
  - bi-fold closet doors: `b/01` (right side)
  - dark wood + black metal cabinet with drawers: `a/01`, `b/01` (back), `d/01` (full view)
  - iron-frame bed: `c/01` (foot near camera), `d/01` (foot near camera), `a/01` (mid-distance)
  - coat rack on entrance-wall: `a/01` (background right), `d/01` (mid-distance)
  - AC remote + thermostat panel: `a/01` (right, on entrance-wall), `b/01` (left)
- image paths:
  `interior-images/room-4/<a|b|c|d>/room-4-<a|b|c|d>-NN.webp`
- this room is structurally analogous to room-3 (room-3 is the SE mirror). phase D will use room-3's geometry as a starting point with the mirror flip applied
