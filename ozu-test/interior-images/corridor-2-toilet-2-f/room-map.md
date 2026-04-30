# corridor-2-toilet-2-f map (2F 廊下 + 2F トイレ)

## overview

`corridor-2-toilet-2-f` is the 2F transit + WC space — bundles two functional zones in one folder:

- **zone A: 2F 廊下 (corridor)** — central transit space connecting all four 2F rooms (room-1 / room-2 / room-3 / room-4), plus the 2F toilet entry, plus the stair shaft top. Listed as 3.04 ㎡ on the blueprint. Cross-shaped (non-rectangular).
- **zone B: 2F トイレ (toilet)** — small WC at the top-middle of 2F, between room-1 and room-2. Listed as 1.22 ㎡ on the blueprint. Rectangular.

⚠ note: this folder name uses `corridor-2-toilet-2-f` for the **2F** corridor + 2F toilet. The 1F duplicate folder `corridor-2/` is permanently excluded from scenes per memory rule `project_ozu_1f_corridor_rules.md` and is unrelated to this 2F space.

approximate dimensions from blueprint (page-coords, before X-mirror to 3D code):
- corridor envelope: bounded roughly by 2F panel width 6,300 × the vertical strip running between the rooms; total floor area 3.04 ㎡
- toilet: ~900 mm wide (E-W) × ~1,350 mm deep (N-S), footprint 1.22 ㎡

assumed (to confirm in phase D):
- shared ceiling across both zones: **whitewashed wood-plank** finish (matches the 2F rooms — visible in `a/10`, `b/10`, `c/07`, `toilet-2-f/06`)
- shared floor across the corridor: **light maple plank** (continues from rooms — visible in `a/01`, `b/01`, `c/01`)
- toilet floor: probably the same light maple plank (to confirm via mid-sweep frames)
- walls: **warm taupe-grey paint** throughout both zones
- doorframes + door panels: **white painted wood** (visible in every sampled frame)
- toilet has a small dark picture frame on a side wall (visible in `toilet-2-f/01`, `toilet-2-f/06`) — decorative, position TBD east vs west

---

## zone A — corridor (廊下, 3.04 ㎡)

### walls (bounding-box approximation)

the corridor is cross-shaped: a north-south central strip with arms that reach east and west to the room doors. the 4 bounding-box walls below describe the envelope, not the literal corridor surfaces.

#### north-wall
- **interior partition** at the north end of the corridor strip
- contains: door to the **2F toilet** (single hinged 開き — verify in phase E from blueprint arc)
- adjacent to: stair shaft (with step-13 top exit opening east into the corridor — verify door/no-door in phase E)
- opposite: south-wall

#### south-wall
- **interior partition** at the south end of the corridor strip
- short stub between room-3 (SE room) and room-4 (SW room) — 天井点検口 (ceiling inspection hatch) is marked here on the blueprint
- opposite: north-wall

#### east-wall
- **interior partition** running along the east side of the corridor
- contains: door to **room-2** (NE room, 洋室3) at the north end; door to **room-3** (SE room, no number) at the south end; closet (クローゼット) door(s) somewhere in between
- opposite: west-wall

#### west-wall
- **interior partition** running along the west side of the corridor
- contains: door to **room-1** (NW room, 洋室2) at the north end; door to **room-4** (SW room, 洋室1) at the south end; storage (物入) door near the stair shaft; stair-shaft east face (with step-13 top exit) at the very north
- opposite: east-wall

### adjacencies

- north-wall meets east-wall (NE — toilet east side + stair north end)
- north-wall meets west-wall (NW — stair shaft area)
- south-wall meets east-wall (SE — room-3 north door area)
- south-wall meets west-wall (SW — room-4 north door area)
- east-wall meets north-wall and south-wall
- west-wall meets north-wall and south-wall

### corners (template names; not photo capture positions)

| corner id | walls meeting | location | notes |
|---|---|---|---|
| corner-east-north | east-wall × north-wall | NE | between room-2 door and toilet door area |
| corner-east-south | east-wall × south-wall | SE | between room-3 door and ceiling hatch |
| corner-north-west | north-wall × west-wall | NW | stair shaft / step-13 top exit area |
| corner-west-south | west-wall × south-wall | SW | between room-4 door and ceiling hatch |

corner ids list walls in alphabetical order. these are conceptual — the corridor's cross shape means the corners are bounding-box approximations.

### corridor layout (top-down)

```
                north-wall (toilet door + stair shaft area)
       ┌────────────┬────────────────┬────────────┐
       │ stair      │ [toilet door]  │ [room-2    │
       │  shaft     │                │  door]     │
       │  step 13   │                │            │
       │  exit      │                │            │
   west│            │   廊下         │            │east
   wall│            │  (3.04㎡)      │            │wall
       │ [room-1    │                │ [closet    │
       │  door]     │                │  door]     │
       │            │                │            │
       │            │                │            │
       │ [storage   │                │ [room-3    │
       │  door]     │                │  door]     │
       │ [room-4    │                │            │
       │  door]     │                │            │
       └────────────┴────────────────┴────────────┘
                    south-wall (短) — 天井点検口 hatch area
```

(this is a simplified top-down. the actual corridor strip is narrower than the bounding box. door positions per blueprint — phase C will measure precisely.)

### corridor photo capture (a, b, c)

3 camera positions inside the corridor:

| current path | photo count | tentative position | photo evidence (sampled) |
|---|---|---|---|
| `a/` | 20 | north-west, near room-1 doorway | `a/01` shows looking N into room-1: window high on left wall (= room-1's west wall, with the narrow vertical frosted window), bed on left, dark metal-and-wood shelf on right (= room-1's NE shelf-and-desk corner), light maple floor, white doorframe, wood-plank ceiling. `a/10` shows a corridor-ceiling perspective with two openings visible (room + something else) — consistent with mid-corridor near room-1 entry. |
| `b/` | 23 | north-east, near room-2 doorway | `b/01` shows looking N or E into room-2: window high on right wall (= room-2's east exterior wall), single iron-frame bed at far end, 5-hook iron coat-rack on far/left wall, light maple floor, white doorframe + door visible on left. `b/10` shows looking through a doorway with the same coat-rack visible — consistent with room-2 entry. |
| `c/` | 13 | mid-corridor, possibly near toilet entry | `c/01` shows a close wall surface on the left (white panel — could be toilet door or closet door) + an opening on the right going further into corridor. `c/07` shows looking through a doorway INTO a small space with downlight ceiling (possibly the toilet entrance from corridor). |

⚠ all three corridor mappings are **TENTATIVE** — the annotated jpeg's letter colors at this resolution don't form a clean 4-corner annotation, and the corridor's cross shape complicates any "corner-X-Y" naming. phase D photo-by-photo verification will lock in the exact positions.

### corridor sweep direction

clockwise from above (per room-1 convention). sequence 01 starts the sweep, highest number ends it.

### corridor fixture / feature anchors

- **whitewashed wood-plank ceiling** across the entire corridor (visible in `a/10`, `b/10`, `c/07`)
- **light maple plank floor** continuing into all rooms (visible in `a/01`, `b/01`, `c/01`)
- **warm taupe-grey paint** on all walls
- **5-hook iron coat-rack** in room-2 (visible from corridor through room-2 doorway in `b/01`, `b/10`)
- **white painted doorframes + door panels** at every room + toilet doorway
- **closet doors (クローゼット)** on east-wall (TBD position; one or more)
- **storage door (物入)** on west-wall, near stair shaft (床上げ raised-floor annotation — TBD purpose)
- **stair-shaft top exit** at NW corner area, from step 13 of the L-shape stair (per `stairs/room-map.md`)
- **2F toilet door** at north-wall, mid (single hinged 開き — TBD via blueprint arc)

---

## zone B — toilet (トイレ, 1.22 ㎡)

### walls

the toilet is a small enclosed rectangular WC at the top-middle of 2F, sandwiched between room-1 (west), the stair shaft (south-west), the corridor (south), and room-2 (east).

#### window-wall (north)
- **exterior wall**, runs full toilet width (~900 mm)
- contains: vertical frosted privacy window (縦すべり 02609, FL+2000) — visible in `toilet-2-f/01`, `toilet-2-f/06`
- opposite: door-wall

#### door-wall (south)
- **interior partition** at the south end
- contains: single hinged door 開き from the corridor (verify in phase E from blueprint arc — the door-arc visible in the 2f-corr-area crop is consistent with a hinged door)
- opposite: window-wall

#### toilet-wall (TBD — east or west)
- **interior partition** running along one of the long sides
- toilet bowl + tank back against this wall
- per blueprint, the toilet bowl symbol is positioned slightly east of centre — TBD if tank is against east-wall or west-wall
- opposite: side-wall

#### side-wall (the opposite long side)
- **interior partition** running along the other long side
- contains: small dark **picture frame** (decorative, ~30×30 cm) — visible in `toilet-2-f/01`, `toilet-2-f/06` on a side wall opposite the toilet bowl
- TBD which long wall this is

### toilet adjacencies

- window-wall meets toilet-wall and side-wall
- door-wall meets toilet-wall and side-wall
- toilet-wall meets window-wall and door-wall
- side-wall meets window-wall and door-wall

### toilet corners

| corner id | walls meeting | notes |
|---|---|---|
| corner-door-side | door-wall × side-wall | south corner on the side-wall side |
| corner-door-toilet | door-wall × toilet-wall | south corner on the toilet-wall side |
| corner-side-window | side-wall × window-wall | north corner on the side-wall side; window is here |
| corner-toilet-window | toilet-wall × window-wall | north corner on the toilet-wall side; tank is here (or near) |

corner ids list walls in alphabetical order.

### toilet layout (top-down)

```
                     window-wall (frosted vertical window)
            ┌──────────────────────────────┐
            │     [frosted vertical window]
            │                              │
   toilet   │  [tank +    ┊                │  side
   wall     │   bowl]     ┊  [picture      │   wall
   (bowl    │             ┊   frame]       │  (decor)
    side)   │             ┊                │
            │                              │
            │       [hinged door]          │
            └──────────────────────────────┘
                     door-wall
```

(toilet vs side wall orientation is TBD — the bowl is against ONE long wall, the picture frame is on the OTHER. east vs west placement to confirm in phase D.)

### toilet photo capture (toilet-2-f/)

| current path | photo count | position |
|---|---|---|
| `toilet-2-f/` | 12 | inside the toilet — single corner sweep covering all 4 walls + window + bowl + picture frame |

### toilet sweep direction

clockwise from above. sequence 01 starts the sweep.

### toilet fixture / appliance anchors

- **toilet bowl + tank**: against the toilet-wall (east or west — TBD); blueprint shows the bowl symbol slightly east of centre
- **frosted vertical window 縦すべり 02609** at FL+2000: window-wall (north exterior)
- **small dark picture frame** on side-wall (decorative, ~30×30 cm)
- **whitewashed wood-plank ceiling** with single downlight (visible in `toilet-2-f/06`)
- **hinged door from corridor**: door-wall (south)
- **toilet-paper holder + handwash basin (手洗器)**: TBD — not yet visible in sampled frames

---

## folder structure (current — letter-coded for corridor + named for toilet)

```
corridor-2-toilet-2-f/
├── room-map.md          (this file)
├── room-map-photos.md   (photo→feature index)
├── a/            (20 images — corridor sweep, tentative position near room-1)
├── b/            (23 images — corridor sweep, tentative position near room-2)
├── c/            (13 images — corridor sweep, tentative position mid-corridor)
└── toilet-2-f/   (12 images — single inside-toilet sweep)
```

## proposed rename

**deferred** until camera positions are confirmed in phase D. once confirmed:
- corridor `a/`, `b/`, `c/` → `corner-X-Y/` or `<wall>-mid/` per the room-1 convention
- `toilet-2-f/` → `corner-X-Y/` if it's at a clear corner, or `toilet-mid/` if mid-room

(don't run rename until user confirms.)

## unverified items

### corridor (zone A)
- exact corridor dimensions (read from blueprint at 400 dpi; phase C will measure precisely)
- exact position of each room door along east-wall and west-wall
- closet (クローゼット) count and exact position(s) on east-wall
- storage (物入) door position on west-wall (near stair shaft)
- camera position interpretations for `a/`, `b/`, `c/` (photo-content reading is plausible but not blueprint-confirmed)
- door types (hinged 開き / sliding 引違 / folding 折戸) for each room door — phase E
- top-exit at step 13: door panel vs open archway — phase E

### toilet (zone B)
- exact toilet dimensions (~900 × 1,350 read from blueprint, ~1.22 ㎡ — phase C precise)
- which long wall the toilet bowl is against (east vs west)
- which long wall the picture frame is on (opposite the toilet)
- whether there's a hand-wash basin (手洗器) integrated atop the tank — not visible in sampled frames
- whether there's a toilet-paper holder visible on a wall
- door type (currently inferred hinged from blueprint arc and `c/07` photo evidence; re-confirm via blueprint at 400 dpi in phase E)
- ceiling height (assumed 2.4 m to match the rest of 2F)

### shared
- whether any corridor-side walls have additional fittings (thermostat panel, light switches, AC controllers)
- the white panel visible close-up on the left side of `c/01` — toilet door? closet door? thermostat panel? TBD
- ceiling height across both zones (assumed 2.4 m)

## usage notes

- this is a **two-zone room**: zone A (corridor) and zone B (toilet) share the same folder but are functionally distinct rooms; the map describes both
- always reference walls by feature name within each zone (e.g., corridor's north-wall vs toilet's window-wall) — never confuse cross-zone names
- corner ids are alphabetical wall pairs within their zone
- the corridor is **non-rectangular** (cross-shaped) — the 4-corner template is a bounding-box approximation, not literal geometry; phase D rebuild will use bespoke geometry
- material sampling from photos:
  - whitewashed wood-plank ceiling: `a/10`, `b/10`, `c/07`, `toilet-2-f/06`
  - light maple plank floor: `a/01`, `b/01`, `c/01`
  - warm taupe-grey paint: every frame
  - white doorframes: every frame with a doorway visible
  - room views from corridor: `a/01` (room-1), `b/01` (room-2)
  - toilet vertical window + interior: `toilet-2-f/01`, `toilet-2-f/06`
  - 5-hook coat-rack inside room-2: `b/01`, `b/10`
- image paths:
  - corridor: `interior-images/corridor-2-toilet-2-f/<a|b|c>/corridor-2-toilet-2-f-<a|b|c>-NN.webp`
  - toilet: `interior-images/corridor-2-toilet-2-f/toilet-2-f/corridor-2-toilet-2-f-toilet-2-f-NN.webp`
- when phase D rebuilds the 2F, build the corridor envelope first (cross shape with room-door cutouts), then place the toilet as an attached small box at the north-mid wall, then place the rooms around the corridor
- the toilet shares a wall with: the stair shaft (south-west), room-1 (west), room-2 (east), the corridor (south)
- this is the **second non-rectangular zone** in this project (after corridor-1) — pattern: cross-shaped corridor with rooms around it; bounding-box walls cover the envelope
