# Room identity — blueprint to photo-folder

source of truth: the blueprint `ozu-1-blueprint.pdf` rendered at 400 dpi.
crops used: `/tmp/1f-real.png`, `/tmp/2f-real.png` (1F left column of page, 2F middle column).

building footprint per blueprint: **6,300 mm wide × 7,200 mm deep**, both floors.
north arrow on page: **page-top = north**. front door / porch is on the north (page-top) side.

axis convention used by existing 3D code (interior scene):
- page-LEFT (small page-x) → code-large-x (X is mirrored)
- page-TOP (small page-y) → code-large-z (front-of-house, z=D)
- so page-bottom = code-z=0 (back of house in code)
- so page-right = code-x=0 (left side in code)

---

## 1F rooms

| page position | japanese label | size from blueprint | photo folder | notes |
|---|---|---|---|---|
| top-left, outside the wall | ポーチ (porch) | — | — | covered entry, exterior |
| top-left, just inside porch | 玄関 (genkan) | 1.62 ㎡ | — | entry, no separate photo folder |
| top-middle small box | トイレ (1F WC) | 1.62 ㎡ | `toilet-1-f` | |
| top-middle large | 浴室 (UB) | ≈ 1,800 × 2,005 | `washroom` | unit-bath; user labels this folder "washroom" (not the powder room) |
| top-right | 洗面所 (powder/laundry room) | 2,700 deep × ~1,800 wide | `laundry` | sink/vanity + washing-machine alcove; user labels this folder "laundry" |
| middle (vertical strip) | 廊下 (corridor) | 2.43 ㎡ | `corridor-1` | `corridor-2` is a duplicate per memory rule, ignore |
| middle small | 物入 (storage) | 0.81 ㎡ | — | no folder |
| middle | クローゼット (closet) | — | — | no folder |
| middle-left | 階段 (stairs, 1F portion) | 1.42 ㎡ | `stairs` | photos may cover both floors of stairwell |
| bottom (large) | L.D.K | 26.13 ㎡ (16.1 帖) | `kitchen` + `living-dining` | LDK split into two photo folders by zone |

kitchen counter on blueprint: **L=2,550 mm**, located on the wall between LDK and the wet rooms (page-z roughly mid-LDK). this is the wall I previously placed it on the wrong side of.

---

## 2F rooms

confirmed by user via the annotated `ozu-1-blueprint-updated.jpeg`. each bedroom has a `Room1`/`Room2`/`Room3`/`Room4` annotation in pink corresponding to the photo folder name, and corner-letter labels (A/B/C/D) marking the four panorama camera positions per room.

| page position | japanese label | size from blueprint | photo folder | notes |
|---|---|---|---|---|
| top-left | 洋室2 | 7.29 ㎡ (4.5 帖) → 2.7 × 2.7 | `room-1` | confirmed |
| top-middle small box | トイレ (2F WC) | (≈ 0.9 × 1.5) | `corridor-2-toilet-2-f` | photo folder combines 2F corridor + 2F toilet; 2F space, unrelated to 1F corridor-2 rule |
| top-right | 洋室3 | 7.29 ㎡ (4.5 帖) → 2.7 × 2.7 | `room-2` | confirmed |
| middle (central) | 廊下 (2F corridor, 3.04 ㎡) | — | `corridor-2-toilet-2-f` | same folder as 2F toilet; 2F space, unrelated to 1F corridor-2 rule |
| various | クローゼット (closets) | — | — | several, no folders |
| bottom-left | 寝室 | 9.72 ㎡ (6 帖) → 2.7 × 3.6 | `room-4` | confirmed |
| bottom-right | 洋室1 | 9.72 ㎡ (6 帖) → 2.7 × 3.6 | `room-3` | confirmed |

each bedroom has 4 corner-letter annotations (A, B, C, D) marked on the blueprint at the corner positions where each panorama was shot. these are the inputs to phase B per-room map authoring (used to derive the corner-name folders following the room-1 template's "corner-WALL-WALL" alphabetical convention).

---

## room-1 audit (against blueprint)

room-1 photo folder is most likely **洋室2** on the 2F blueprint (top-left of page, 4.5 帖, 2.7 × 2.7).

what the existing `room-1/room-map.md` declares:
- window-wall opposite entrance-wall
- cabinet-wall opposite ac-wall
- both external walls (window, ac) face exterior

what the blueprint shows for 洋室2 (top-left of 2F plan, north is page-top):
- north wall (page-top edge) = exterior wall, has window symbols → **this is window-wall**
- west wall (page-left edge) = exterior wall, has the ac unit + frosted-window cluster → **this is ac-wall**
- south wall (page-bottom edge of room) = interior, faces the central 廊下 (corridor)
- east wall (page-right edge of room) = interior, has closet symbols on the corridor side

so per blueprint:
- north wall = window-wall (exterior)
- west wall = ac-wall (exterior)
- → window-wall is **adjacent** to ac-wall, **not opposite**

this contradicts the existing map's "window-wall opposite entrance-wall, cabinet-wall opposite ac-wall." the map's adjacency model is wrong — window-wall and ac-wall both face the exterior corner, they're neighbors.

what the existing room-1 inline 3D code (in `ozu-test.html`) has:
- closet on x=0 (one side), sliding window on x=W (opposite side) → cabinet ↔ window are opposite
- doorway on z=0 (one side), AC on z=D (opposite side) → entrance ↔ ac are opposite

per blueprint, the correct opposite pairs are:
- **window-wall ↔ entrance-wall** (window on north, door on south corridor side)
- **ac-wall ↔ cabinet-wall** (ac on west, closet on east)

so the **map is wrong** about which walls are opposite. the **code is right** about which walls are opposite (cabinet ↔ window in code = ac ↔ cabinet in blueprint terms; entrance ↔ ac in code = entrance ↔ window in blueprint terms — wait, this mapping needs to be properly reconciled).

actually the cleanest way to state it: blueprint says window↔entrance and ac↔cabinet are the two opposite pairs. the existing map.md says window↔entrance and ac↔cabinet too. wait — re-reading:

map.md says:
- "window-wall opposite entrance-wall" ✓ matches blueprint
- "cabinet-wall opposite ac-wall" ✓ matches blueprint

so the map.md adjacency declarations are **correct against the blueprint** after all. my earlier audit was wrong.

let me re-check the code with this corrected understanding:

code has:
- window on x=W, doorway on z=0 (perpendicular, NOT opposite) ✗
- closet on x=0, AC on z=D (perpendicular, NOT opposite) ✗

so the **code is wrong**: the code has window ↔ closet (parallel) and door ↔ ac (parallel), but the blueprint and the map both say window ↔ door and closet ↔ ac should be the parallel pairs.

**conclusion: room-1 inline 3D code needs to be rebuilt to match the blueprint + map.** the map is correct; the code is rotated/swapped.

deferred to phase D when room-1 (the 2F bedroom = 洋室2) gets rebuilt.

---

## items needing user confirmation

all three earlier questions resolved by the annotated `ozu-1-blueprint-updated.jpeg` + verified against the 400 dpi blueprint render on 2026-04-29:

1. ✓ `room-1` = 洋室2 (top-left of 2F plan)
2. ✓ `room-2` = 洋室3 (top-right), `room-3` = 洋室1 (bottom-right), `room-4` = 寝室 (bottom-left)
3. ✓ bottom-left room IS 寝室; bottom-right room IS 洋室1 (an earlier reading of "unnumbered 洋室 / no 寝室 label" was wrong — corrected 2026-04-29 against the 400 dpi blueprint render)

the same updated jpeg also marks corner camera positions A/B/C/D inside every room — these become the per-room corner mapping in phase B.

---

## things measured precisely (for phase C)

- 1F width: 6,300 mm (chain: 1,800 + 900 + 1,800 + 1,800)
- 1F top-left sub-chain: 450 + 1,050 + 300 = 1,800
- 1F depth: 7,200 mm (right-edge chain sums to this)
- 2F width: 6,300 mm (chain: 2,700 + 900 + 2,700)
- 2F depth: 7,200 mm
- kitchen counter: 2,550 mm long
- 2F bedroom sizes: 4.5 帖 = 2.7 × 2.7, 6 帖 = 2.7 × 3.6

precise wall coords for each room → phase C.

---

## things NOT done in phase A (deferred)

- detailed wall-by-wall measurements (phase C)
- photo folder content inspection (phase B per-room)
- door type symbols decoded (phase E)
- material / color sampling from photos (phase D per-room)
