# Global coordinates — building-wide wall positions (Phase C)

source of truth: `ozu-1-blueprint.pdf` rendered at 400 dpi. each room map's named walls get a real-world (x or z) coordinate in millimetres, inside the building envelope, after X-mirror to code coords.

## building envelope

- footprint: **6,300 mm wide × 7,200 mm deep**, both floors
- north arrow: **page-top = north** (front door / porch on the north side)

## axis convention (carried over from `room-identity.md`)

- page-LEFT (small page-x) → code-large-x (X is mirrored)
- page-TOP (small page-y) → code-large-z (front-of-house, z=D)
- page-bottom = code-z=0 (back of house in code)
- page-right = code-x=0 (left side in code)

so for any wall:
- a wall on the page-LEFT exterior gets **code-x = 6300**
- a wall on the page-RIGHT exterior gets **code-x = 0**
- a wall on the page-TOP exterior gets **code-z = 7200**
- a wall on the page-BOTTOM exterior gets **code-z = 0**

## blueprint chains (verified at 400 dpi)

### 2F width (page-x, left → right)
2,700 + 900 + 2,700 = **6,300 mm**

### 2F depth (page-y, top → bottom)
2,700 + 900 + 3,600 = **7,200 mm**

so 2F page-y bands:
- top row (room-1, room-2): page-y 0..2700
- middle strip (corridor + 2F toilet + closets): page-y 2700..3600
- bottom row (room-3, room-4): page-y 3600..7200

cross-check: middle strip = 0.9 × 6.3 = 5.67 ㎡, minus toilet (1.22) and stair shaft (1.42) = 3.03 ㎡ for the corridor proper — matches blueprint label 3.04 ㎡ ✓

### 1F width (page-x, left → right)
1,800 + 900 + 1,800 + 1,800 = **6,300 mm**

so 1F page-x bands:
- left exterior to first partition: 0..1800 (genkan + stair shaft area)
- 900-wide column: 1800..2700 (toilet width)
- middle section: 2700..4500 (washroom)
- right exterior section: 4500..6300 (laundry / kitchen east)

### 1F depth chains (page-y, top → bottom)

**left edge:** 900 + 900 + 900 + 1,350 + 3,150 = **7,200 mm**
**right edge:** 2,700 + 1,350 + 750 + 2,400 = **7,200 mm**

(the two edges differ because each edge passes through different interior partitions; together they fix the wall positions in each room.)

bands inferred from chain segments + room maps:
- 0..900: porch zone (covered exterior, only on west half of building's north side; laundry's north wall on east half is exterior at y=0)
- 900..1800: genkan + top-row wet rooms (top half)
- 1800..2700: top-row wet rooms (bottom half) + 1F corridor north end
- 2700..4050: stair shaft 1F (1,350 deep — see ⚠ note below) + (continued) corridor + closets
- 2700..4800: kitchen on east side (2,100 deep on east edge: 1,350 + 750)
- 4050 (or 4800)..7200: LDK proper (3,150 deep on west edge, 2,400 deep on east edge — different because of NW stair carve-out and NE kitchen carve-out)

⚠ **1F stair shaft N-S length conflict**: blueprint chain reads **1,350 mm**, but memory rule `project_stair_must_be_l_shape.md` says 1,600 mm. Per "blueprint is authoritative" rule, the chain reading wins — flag for memory rule update + stairs/room-map.md correction.

---

## 2F rooms

### room-1 (= 洋室2, NW 2F, 4.5 帖, 2.7 × 2.7)

page footprint: x=0..2700, y=0..2700 (top-left quadrant of 2F panel)
code footprint: x=3600..6300, z=4500..7200

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| window-wall | exterior | page-top (N) | **z = 7200** | building exterior |
| ac-wall | exterior | page-left (W) | **x = 6300** | building exterior |
| entrance-wall | interior | page-bottom of room (S) | **z = 4500** | west face of the 2F corridor's west arm (room-1 doorway is here) |
| cabinet-wall | interior | page-right of room (E) | **x = 3600** | west face of the central 900-mm column (which runs the full 2,700 mm height of the top row — 2F toilet at its north portion + closet/storage below) |

shared-wall checks:
- entrance-wall z=4500 ↔ corridor's 2F-north arm should also have a wall at z=4500 on its room-1 side
- cabinet-wall x=3600 ↔ the central column's west face should also be at x=3600

---

### room-2 (= 洋室3, NE 2F, 4.5 帖, 2.7 × 2.7)

page footprint: x=3600..6300, y=0..2700 (top-right quadrant of 2F panel)
code footprint: x=0..2700, z=4500..7200

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| window-wall | exterior | page-top (N) | **z = 7200** | building exterior |
| ac-wall | exterior | page-right (E) | **x = 0** | building exterior |
| entrance-wall | interior | page-bottom of room (S) | **z = 4500** | east face of the 2F corridor's east arm (room-2 doorway is here) |
| closet-wall | interior | page-left of room (W) | **x = 2700** | east face of the central 900-mm column (toilet at its north portion + closet/storage below) |

shared-wall checks:
- entrance-wall z=4500 ↔ corridor's 2F-north arm (east end)
- closet-wall x=2700 ↔ central column's east face (paired with room-1's cabinet-wall on the column's west face at x=3600; column thickness = 3600−2700 = 900 ✓)

---

### room-3 (= 洋室1, SE 2F, 6 帖, 2.7 × 3.6)

page footprint: x=3600..6300, y=3600..7200 (bottom-right of 2F panel)
code footprint: x=0..2700, z=0..3600

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| window-wall | exterior | page-bottom (S) | **z = 0** | building exterior |
| frosted-wall | exterior | page-right (E) | **x = 0** | building exterior |
| closet-wall | interior | page-left of room (W) | **x = 2700** | east face of the central 900-mm column (closets between room-3 and room-4) |
| entrance-wall | interior | page-top of room (N) | **z = 3600** | south face of the 2F corridor's south arm (room-3 doorway is here) |

shared-wall checks:
- entrance-wall z=3600 ↔ corridor south wall east end
- closet-wall x=2700 ↔ central column's east face (paired with room-4's closet-wall on the column's west face at x=3600; column thickness 900 ✓)

---

### room-4 (= 寝室, SW 2F, 6 帖, 2.7 × 3.6)

page footprint: x=0..2700, y=3600..7200 (bottom-left of 2F panel)
code footprint: x=3600..6300, z=0..3600

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| window-wall | exterior | page-bottom (S) | **z = 0** | building exterior |
| frosted-wall | exterior | page-left (W) | **x = 6300** | building exterior |
| closet-wall | interior | page-right of room (E) | **x = 3600** | west face of the central 900-mm column (closets between room-3 and room-4) |
| entrance-wall | interior | page-top of room (N) | **z = 3600** | south face of the 2F corridor's south arm (room-4 doorway is here) |

shared-wall checks:
- entrance-wall z=3600 ↔ corridor south wall west end
- closet-wall x=3600 ↔ central column's west face (paired with room-3's closet-wall on the column's east face at x=2700)
- frosted-wall x=6300 = room-1's ac-wall x=6300 ✓ (both on the building's west exterior, but room-1 is at z=4500..7200 and room-4 is at z=0..3600 — non-overlapping)

---

### corridor-2-toilet-2-f, zone A — corridor (3.04 ㎡, cross-shape envelope)

page footprint (bounding box): x=0..6300, y=2700..3600 (full middle strip of 2F)
code footprint: x=0..6300, z=3600..4500

⚠ bounding-box approximation. the corridor's actual occupied area is 3.04 ㎡; the rest of the strip is taken by the 2F stair shaft (NW), closets, and the toilet (which sticks up into the top row).

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| north-wall | interior | page-top of strip (N) | **z = 4500** | room-1 entrance (NW), 2F toilet south wall (mid), room-2 entrance (NE) — at the same z |
| south-wall | interior | page-bottom of strip (S) | **z = 3600** | room-4 entrance (SW), central closet column south face (mid), room-3 entrance (SE) — at the same z |
| east-wall | interior | page-right (E) | **x = 0** | building exterior on east side of corridor's east arm — but the corridor doesn't actually reach the building wall here; this is bounding-box only |
| west-wall | interior | page-left (W) | **x = 6300** | building exterior on west side of corridor's west arm — bounding-box only; the actual corridor's west reach is bounded by the 2F stair shaft |

shared-wall checks:
- north-wall z=4500 ↔ room-1 entrance-wall (✓, room-1 is at z=4500..7200, sharing south face) and room-2 entrance-wall (✓)
- south-wall z=3600 ↔ room-4 entrance-wall (✓) and room-3 entrance-wall (✓)

---

### corridor-2-toilet-2-f, zone B — toilet (1.22 ㎡)

per blueprint label "≈ 0.9 × 1.5": ~900 mm wide × ~1,350 mm deep. (corridor map says 900 × 1350.)

page footprint: x=2700..3600, y=0..1350 (top-middle of 2F, north wall is building exterior — confirmed against ozu-test.html collision box at z=5.85..7.20)
code footprint: x=2700..3600, z=5850..7200

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| window-wall (north) | exterior | page-top of toilet (N) | **z = 7200** | building exterior |
| door-wall (south) | interior | page-bottom of toilet (S) | **z = 5850** | corridor's north arm (a sub-region extending up from the corridor's main strip to meet the toilet door) |
| toilet-wall / side-wall | interior | page-right or page-left (TBD) | **x = 2700 or 3600** | one is room-1's cabinet-wall (x=3600), one is room-2's closet-wall (x=2700) — partial: only the northernmost 1,350 mm of those walls |

⚠ which long wall has the bowl vs the picture frame is TBD per the toilet map. either way, the two long walls are at x=2700 and x=3600 (paired with room-1's cabinet-wall and room-2's closet-wall respectively).

⚠ the central 900-mm column has multiple sub-zones stacked top-to-bottom:
- page-y=0..1350: 2F toilet (this entry)
- page-y=1350..2700: closet zones for room-1 (west half) and room-2 (east half) accessed via bi-fold doors from inside each bedroom
- page-y=2700..3600: corridor's main strip (zone A)
- page-y=3600..7200: closet zones between room-3 and room-4 (per chain `2700+900+2700` width)

shared-wall checks:
- door-wall z=5850 ↔ corridor north arm (sub-region of zone A extending up from z=4500 main strip — corridor zone A's effective shape is more complex than its bounding box)
- toilet's long walls at x=2700 and x=3600 ↔ partition with room-2 closet (north portion only) and room-1 cabinet (north portion only)

---

### stairs (2F portion) — L-shape stair shaft, upper flight

per stairs map: 2F shaft footprint 1.575 m (W-E) × 0.90 m (N-S). located at the west end of the middle strip, north of the parapet, with room-1 partition on the north.

page footprint: x=0..1575, y=2700..3600 (NW of middle strip)
code footprint: x=4050..6300, z=3600..4500

⚠ shaft east edge moved from blueprint x=4725 to x=4050 to fit the 3+4+6 upper flight
(6 × 225 mm = 1350 mm run from L-bend at x=5400 to 2F landing at x=4050). The blueprint
measures the 1F shaft as 900 mm wide, but the 2F upper flight requires a 1350 mm run from
the bend. x=4050 is the accepted code boundary; all 2F floor/ceiling geometry already uses it.

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| west-wall | exterior | page-left (W) | **x = 6300** | building exterior |
| east-wall | interior | page-right (E) | **x = 4050** | corridor's west arm, north end (step 13 top exit opens to corridor). Blueprint reads x=4725; widened to x=4050 for upper flight — see note above. |
| north-wall | interior | page-top (N) | **z = 4500** | room-1 entrance-wall (= room-1's south face at z=4500) |
| south-wall | parapet | page-bottom (S) | **z = 3600** | half-height parapet; void below opens to 1F LDK |

shared-wall checks:
- north-wall z=4500 ↔ room-1 entrance-wall z=4500 ✓ (room-1's south face IS the 2F stair shaft's north face for the western 1.575 m, then continues as the corridor's north wall east of x=4725)
- west-wall x=6300 = room-1 ac-wall x=6300 ✓ (both on building west exterior, non-overlapping in z)

---

## 1F rooms

### living-dining (LDK, 26.13 ㎡, bounding 6,300 × 4,500)

page footprint (bounding box): x=0..6300, y=2700..7200
code footprint: x=0..6300, z=0..4500

⚠ LDK has two carve-outs at its NW and NE corners (stair shaft + kitchen). Bounding-box walls below describe the envelope; carve-outs are listed separately.

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| kitchen-wall | interior | page-top of LDK (N) | **z = 4500** | LDK's north wall — partial (the central section between stair carve-out east edge and kitchen carve-out west edge). Stair shaft and kitchen sit in this same north band but are separate zones. |
| garden-wall | exterior | page-bottom (S) | **z = 0** | building exterior |
| brick-wall | exterior | page-right (E) | **x = 0** | building exterior |
| stairs-wall | exterior | page-left (W) | **x = 6300** | building exterior |

carve-outs (sub-regions inside the bounding box, NOT room area):
- NW stair shaft: page-x=0..900, page-y=2700..4300 → code-x=5400..6300, code-z=2900..4500
- NE kitchen: page-x=3750..6300, page-y=2700..4800 → code-x=0..2550, code-z=2400..4500

shared-wall checks:
- garden-wall z=0 = room-3 window-wall z=0 (both south building exterior) ✓ — but room-3 is on 2F so they don't actually overlap
- LDK's stair-shaft east face at x=900 → code-x=5400 (also = stairs 1F east-wall)

---

### kitchen (~5.4 ㎡, 2,550 × 2,100 per blueprint chain)

⚠ depth 2,100 per blueprint right-edge chain (1,350 + 750), not 1,800 as kitchen map states. Map will need an update.

page footprint: x=3750..6300, y=2700..4800
code footprint: x=0..2550, z=2400..4500

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| counter-wall | interior (half-height) | page-bottom of kitchen (S) | **z = 2400** | LDK pass-through — half-height counter, opens into LDK |
| fridge-wall | interior | page-top of kitchen (N) | **z = 4500** | partition with laundry on east portion (page-x=4500..6300) + corridor or other on west portion (page-x=3750..4500). Kitchen map says "exterior wall" — that's incorrect; flag for kitchen-map fix. |
| window-wall | exterior | page-right (E) | **x = 0** | building exterior (with 縦すべり 02609 windows at FL+1900) |
| entry-wall | interior | page-left of kitchen (W) | **x = 2550** | partition with corridor-1 (kitchen entry from corridor opens through this wall) |

shared-wall checks:
- counter-wall z=2400 ↔ LDK's NE carve-out south edge ✓
- fridge-wall z=4500 ↔ laundry door-wall z=4500 (partial: page-x=4500..6300) and LDK kitchen-wall z=4500 (NW of kitchen carve-out, page-x=0..3750)

---

### washroom (浴室 / UB, ~3.24 ㎡, 1,800 × 1,800)

⚠ depth listed as 1,800 in current map (down from 2,005 per blueprint label). Phase C uses 1,800 (matches "depth re-read at QA" note in map).

page footprint: x=2700..4500, y=0..1800
code footprint: x=1800..3600, z=5400..7200

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| bath-wall | exterior | page-top (N) | **z = 7200** | building exterior (frosted vertical window 縦すべり 02607 + dark accent panel). No porch on this part of the north facade (porch is only at the genkan area to the west). |
| side-wall | interior | page-bottom of washroom (S) | **z = 5400** | partition with corridor-1's east arm (the strip page-y=1800..2700 between wet rooms and LDK) |
| entry-wall | interior | page-right (E) | **x = 1800** | partition with laundry's bath-wall (washroom east wall = laundry west wall) |
| end-wall | interior | page-left (W) | **x = 3600** | partition with toilet-1-f's brick-wall (washroom west wall = toilet east wall, both at page-x=2700) |

shared-wall checks:
- entry-wall x=1800 ↔ laundry bath-wall x=1800 ✓
- bath-wall z=7200 = building's north exterior on this section ✓

---

### laundry (洗面所, ~4.86 ㎡, 1,800 × 2,700)

page footprint: x=4500..6300, y=0..2700
code footprint: x=0..1800, z=4500..7200

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| window-wall | exterior | page-top (N) | **z = 7200** | building exterior (横すべり窓 06003 at FL+1800) |
| door-wall | interior | page-bottom of laundry (S) | **z = 4500** | partition with kitchen fridge-wall (east portion) — laundry's S edge meets kitchen's N edge at page-y=2700 |
| vanity-wall | exterior | page-right (E) | **x = 0** | building exterior (brick accent wallpaper interior face) |
| bath-wall | interior | page-left of laundry (W) | **x = 1800** | partition with washroom entry-wall (washroom's E wall = laundry's W wall) |

shared-wall checks:
- bath-wall x=1800 ↔ washroom entry-wall x=1800 ✓
- door-wall z=4500 ↔ kitchen fridge-wall z=4500 ✓ (page-x range 4500..6300 only; partial overlap)
- window-wall z=7200 = building's north exterior on east half (no porch overhang here)

---

### toilet-1-f (1F WC, トイレ, 1.62 ㎡, 900 × 1,800)

page footprint: x=1800..2700, y=0..1800
code footprint: x=3600..4500, z=5400..7200

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| toilet-wall | exterior | page-top (N) | **z = 7200** | building exterior (横すべり窓 03603 at FL+1800) |
| door-wall | interior | page-bottom of toilet (S) | **z = 5400** | partition with corridor-1's east arm (toilet door from corridor) |
| brick-wall | interior | page-right (E) | **x = 3600** | partition with washroom (washroom's end-wall is at the same x=3600) |
| side-wall | interior | page-left (W) | **x = 4500** | partition with corridor-1 / genkan area on the west |

⚠ "brick-wall" in the toilet map is described as the east accent wall, but its exact placement (east vs west long wall) was flagged TBD in the toilet map. Phase C assumes east per the map's tentative reading.

shared-wall checks:
- door-wall z=5400 = corridor-1 east arm north edge at z=5400 (toilet sits north of the corridor's east arm)
- brick-wall x=3600 = washroom end-wall x=3600 ✓
- toilet-wall z=7200 = washroom bath-wall z=7200 ✓ (contiguous building north exterior, page-x=1800..4500)

---

### corridor-1 (1F 廊下 + 玄関 transit, ~4.05 ㎡ combined)

⚠ irregular L-ish shape combining the genkan (top-left, 1.62 ㎡) and the corridor strip (running south, 2.43 ㎡). The 4 named walls are bounding-box approximations.

page footprint (bounding box): x=0..2700, y=0..2700
code footprint: x=3600..6300, z=4500..7200

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| entry-wall | exterior | page-top (N) | **z = 7200** | building exterior (front door / 玄関ドア at the genkan's north face); porch is north of this wall (off-chain) |
| ldk-wall | interior (open archway) | page-bottom (S) | **z = 4500** | LDK kitchen-wall — open archway, no door panel. partial: only the corridor's south end actually opens to LDK |
| bath-wall | interior | page-right (E) | **x = 3600** | partition with toilet-1-f (mid, brick-wall x=3600 ✓), washroom side-wall (further south at z=4500), laundry door-wall (south end at z=4500). |
| stairs-wall | interior + exterior | page-left (W) | **x = 6300** | building exterior on west boundary (genkan + corridor west wall) + stair shaft east face at south end + 玄関収納 + storage closets along the length |

⚠ corridor-1 is non-rectangular (genkan zone + corridor strip). The bounding-box walls describe the envelope; actual surfaces have multiple sub-segments. Phase D will use bespoke geometry.

shared-wall checks:
- ldk-wall z=4500 ↔ LDK kitchen-wall z=4500 ✓
- bath-wall x=3600 ↔ toilet-1-f brick-wall x=3600 ✓ (partial — only at page-y=900..2700 where toilet sits)

---

### stairs (1F portion) — L-shape stair shaft, lower flight + winders

per blueprint area label "1.42 ㎡" with width 0.90 m, N-S length = **1.58 m** (matches memory rule's 1.60 within rounding).

page footprint: x=0..900, y=2700..4300 (NW corner of LDK, carve-out)
code footprint: x=5400..6300, z=2900..4500

| named wall | exterior/interior | page side | code coord | shares with |
|---|---|---|---|---|
| west-wall | exterior | page-left (W) | **x = 6300** | building exterior |
| east-wall | interior | page-right of shaft (E) | **x = 5400** | partition with corridor-1 stairs-wall (south end) and LDK interior |
| north-wall | interior | page-top (N) | **z = 4500** | partition with corridor-1 / laundry-storage area (1F level) |
| south-wall | open to LDK | page-bottom of shaft (S) | **z = 2900** | open south end (no wall) — stair entry from LDK's NW carve-out |

shared-wall checks:
- north-wall z=4500 = corridor-1 ldk-wall z=4500 (partial, where they meet)
- west-wall x=6300 = LDK stairs-wall x=6300 ✓ (both on building west exterior)
- east-wall x=5400 = LDK stair-carve-out east edge x=5400 ✓
- south-wall z=2900 = LDK stair-carve-out south edge z=2900 ✓

---

## Cross-validation summary

verified shared walls (where two rooms' shared partitions match in code coords):

| pair | wall | code coord | status |
|---|---|---|---|
| room-1 entrance ↔ corridor-2 north | z = 4500 | matches | ✓ |
| room-2 entrance ↔ corridor-2 north | z = 4500 | matches | ✓ |
| room-3 entrance ↔ corridor-2 south | z = 3600 | matches | ✓ |
| room-4 entrance ↔ corridor-2 south | z = 3600 | matches | ✓ |
| room-1 cabinet ↔ central column W face | x = 3600 | matches | ✓ |
| room-2 closet ↔ central column E face | x = 2700 | matches | ✓ |
| room-3 closet ↔ central column E face | x = 2700 | matches | ✓ |
| room-4 closet ↔ central column W face | x = 3600 | matches | ✓ |
| stairs 2F north ↔ room-1 entrance | z = 4500 | matches | ✓ |
| stairs 2F west ↔ building exterior | x = 6300 | matches | ✓ |
| washroom entry ↔ laundry bath | x = 1800 | matches | ✓ |
| washroom end ↔ toilet brick | x = 3600 | matches | ✓ |
| washroom bath ↔ toilet toilet | z = 7200 | matches (contiguous N exterior, page-x=1800..4500) | ✓ |
| washroom side ↔ corridor-1 east arm | z = 5400 | new — corridor east arm south of wet rooms | ✓ |
| toilet door ↔ corridor-1 east arm | z = 5400 | new — same | ✓ |
| laundry door ↔ kitchen fridge | z = 4500 | matches (page-x=4500..6300 portion) | ✓ |
| LDK kitchen-wall ↔ corridor-1 ldk-wall | z = 4500 | matches | ✓ |
| stairs 1F west ↔ LDK stairs-wall | x = 6300 | matches | ✓ |
| stairs 1F east ↔ LDK NW carve-out east | x = 5400 | matches | ✓ |
| stairs 1F south ↔ LDK NW carve-out south | z = 2900 | matches | ✓ |

## Flags for follow-up

1. ~~1F stair shaft N-S length: 1,350 not 1,600~~ **RETRACTED** — blueprint area label is 1.42 ㎡; with width 0.90 m, length = 1.58 m (matches memory rule's 1.60 within rounding). The chain segment "1,350" was a different feature, not the stair length.
2. **Kitchen depth: 2,100 not 1,800** — kitchen map needs correcting per blueprint chain (1,350 + 750 = 2,100 on east edge).
3. **Kitchen fridge-wall labelled "exterior"** in kitchen map — actually interior partition with laundry (east portion) and corridor (west portion). Kitchen map needs correcting.
4. **Washroom depth 1,800** — current map uses 1,800 (down from 2,005 in earlier draft); confirmed.
5. **Toilet "brick-wall" east-vs-west** — flagged TBD in toilet map; Phase C assumes east per current map's tentative reading.
6. **Compass orientation of room-2/3/4 named walls** — global coords above lock these in (window=N for room-1+room-2, window=S for room-3+room-4, etc.). Maps still mark them TENTATIVE; tightening now.


