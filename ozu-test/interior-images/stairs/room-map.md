# stairs map (階段 / L-shape stair shaft, 1F → 2F)

## overview

`stairs` is the internal L-shape stairway connecting 1F and 2F. It runs along the west exterior wall, with a 90° bend at the upper-northwest of the 1F portion via 2 winder treads. Total 13 risers (5 + 2 winders + 6).

⚠ this is **not a 4-corner room** — it's a vertical 3D structure spanning two floors. The 4-walls + 4-corners template applies in name only; physical capture is a single walking sequence (`stairs-1.webp` … `stairs-27.webp`), no a/b/c/d sub-folders.

dimensions per memory rule `project_stair_must_be_l_shape.md`:
- 1F shaft footprint: 0.90 m wide (E-W) × 1.60 m long (N-S) — lower flight runs N-S along the west wall
- 2F shaft footprint: 1.575 m long (W-E) × 0.90 m wide (N-S) — upper flight runs W-E along the north edge of the 2F shaft area
- 1F label: 1.42 ㎡ (per blueprint)
- 2F label: 1.42 ㎡ (per blueprint)

step layout (verified against blueprint at 400 dpi):
- 1F lower flight: 5 risers numbered 1–5 (south end = step 1 at 1F floor; north end = step 5 at top of lower flight)
- L-bend: 2 winder treads numbered 6 and 7 (90° turn from north-bound to east-bound)
- 2F upper flight: 6 risers numbered 8–13 (west end = step 8; east end = step 13 at 2F floor level)
- DN arrow at step 13 (per blueprint) — top exit at 2F is at the east end of the upper flight

geometry / materials (mix of confirmed by sample frames and still-assumed items):

confirmed by photo evidence:
- ceiling above 2F top section: whitewashed wood-plank finish (visible in `stairs-1`, `stairs-10`, `stairs-13`, `stairs-24`)
- treads + risers: light maple / birch wood — exact species TBD (visible in `stairs-10`, `stairs-13`, `stairs-17`, `stairs-21`, `stairs-27`)
- handrail: white / cream-painted wood (uniform paint, no grain) with brushed-chrome wall brackets and a white-painted elbow connector at the L-bend (visible in `stairs-4`, `stairs-7`)
- nosing anti-slip: two parallel dark inlay strips per tread nosing (look like dark walnut inlay or rubberised grooves, NOT chrome — visible in `stairs-10`, `stairs-17`, `stairs-27`)
- walls: warm taupe-grey paint throughout the stair shaft (visible in every frame)
- 2F parapet south edge: white-painted with white wood cap (visible in `stairs-1`, `stairs-21`) — half-height construction still TBD via mid-sweep frames

still assumed (to confirm in phase D):
- ceiling above 1F lower flight section: flat painted (probably the underside of the upper flight + surrounding 2F floor); not directly sampled
- ceiling height (1F floor to 2F floor): ~2.4 m + tread riser stack — assumption from house convention
- exact wood species for treads / handrail base material before paint
- exact RAL/colour of the handrail paint
- exact material of the dark inlay nosing strips (walnut inlay vs rubberised vs other)

## walls (bounding-box approximation)

walls describe the stair envelope as a 3D box; the actual stair occupies an L-shape inside this box.

### west-wall
- **exterior wall**, runs full height of both floors
- the long wall the 1F lower flight runs along (lower flight ascends north along this wall)
- continues up to be the back wall of the 2F upper flight at the west end
- handrail mounted on this wall on both flights (`壁付` per blueprint)
- opposite: east-wall

### east-wall
- **interior partition** on both floors
- 1F level: separates the 1F lower flight from the corridor-1's stairs-wall (closet 物入 + クローゼット alcoves are on the corridor-1 side of this partition)
- 2F level: separates the 2F upper flight from the 2F corridor (`corridor-2-toilet-2-f`)
- step 13 exit (top of stairs) is at the east end of the upper flight — opens north into the 2F corridor (verify door/no-door in phase E)
- opposite: west-wall

### north-wall
- **interior partition** on both floors
- 1F level: short wall at the very north end of the lower flight + winder bend area; on the 1F side this is the partition with the laundry's south side (`laundry/door-wall`) and the storage 物入
- 2F level: separates the 2F upper flight from `room-1` (洋室2)
- opposite: south-wall

### south-wall
- 1F level: **open south end** of the lower flight — the stair entry from the LDK (the stair carve-out in the LDK's NW corner). No door; flush opening into the LDK with the half-wall parapet starting above the bottom step
- 2F level: **half-height white-painted parapet** with white wood cap — runs along the south edge of the upper flight, capping off the stair shaft from the void above the 1F LDK below
- opposite: north-wall

## adjacencies

- west-wall meets north-wall and south-wall (corners are at the L-bend NW area on 1F, and at the 2F west end of the upper flight)
- east-wall meets north-wall and south-wall
- north-wall meets west-wall and east-wall (the L-bend area on 1F is at this junction)
- south-wall meets west-wall and east-wall (1F: open to LDK; 2F: parapet)

## corners (template names; not photo capture positions)

| corner id | walls meeting | location | notes |
|---|---|---|---|
| corner-east-north | east-wall × north-wall | NE | upper-east end of 2F upper flight; near the step-13 top exit |
| corner-east-south | east-wall × south-wall | SE | bottom-east of 1F lower flight entry from LDK |
| corner-north-west | north-wall × west-wall | NW | the L-bend itself; winder treads (steps 6–7) |
| corner-west-south | south-wall × west-wall | SW | bottom-west of 1F lower flight; foot of step 1 |

corner ids list walls in alphabetical order. these are conceptual — no panorama camera sits at any of them.

## room layout (top-down, both floors)

```
1F view (looking down on the lower flight + winders):

          north-wall  (interior, partition with laundry / storage)
           ┌───────────────┐
           │ winders 7  6  │   (90° bend at NW area)
           │       ────────│
           │ step 5        │
           │ step 4        │
   west    │ step 3        │   east
   wall    │ step 2        │   wall
   (ext.)  │ step 1        │   (corridor-1
           │ ──── (LDK     │    partition)
           │   carve-out)  │
           └───────────────┘
          south-wall (open to LDK; parapet above starts at 2F level)


2F view (looking down on the upper flight):

          north-wall  (interior, partition with 洋室2 = room-1)
           ┌───────────────────────────┐
           │  step  step  step  step   │
           │   13   12   11   10        ↳ step 13 = 2F top exit
   west    │                            │      (east end → 2F corridor)
   wall    │   step 9   step 8          │   east
   (ext.)  │                            │   wall (2F corridor partition)
           │ ────────half-wall parapet──│
           └───────────────────────────┘
          south-wall  (parapet — half-height white wall + cap;
                      void below opens to 1F LDK)
```

## camera / photo capture (NOT a 4-corner sweep)

photos are a flat list at the room root, no sub-folders. 27 frames (`stairs-1.webp` … `stairs-27.webp`). The capture appears to be a walking sequence covering both flights from multiple positions / angles.

| frame | likely position | content (from sampled frames) |
|---|---|---|
| `stairs-1` | 2F top, looking down at the descent | half-wall parapet in foreground; winder treads + descending lower flight on right; whitewashed wood-plank ceiling above |
| `stairs-4` | handrail straight-section close-up | white / cream-painted handrail with single brushed-chrome wall bracket; taupe wall behind |
| `stairs-7` | mid-bend handrail close-up | white-painted elbow connector on handrail at the bend + brushed-chrome wall bracket below; taupe wall behind |
| `stairs-10` | upper flight, looking up toward step-13 exit | upper-flight ascent view; wood-plank ceiling visible at top; white wall with switch on far face; painted handrail on left |
| `stairs-13` | mid-flight, looking up at upper flight | wood treads ascending on right; painted handrail with painted joint mid-frame; whitewashed wood-plank ceiling visible at the top of the shaft |
| `stairs-17` | top-down at L-bend (winder treads) | clearest top-down geometry of the two winder treads (steps 6–7); dark inlay anti-slip strips visible on each nosing |
| `stairs-21` | 1F bottom area, looking up | lower flight rising on left; LDK visible through the open south end on the right (sofa edge); white parapet cap visible upper-right |
| `stairs-24` | L-bend area looking up at upper section | wood treads ascending on left; taupe-painted bulkhead on right (likely underside of upper flight); wood-plank ceiling at top |
| `stairs-27` | 1F bottom step, looking up the lower flight | full lower flight visible; dark inlay nosings clearest in side-profile; LDK visible through the side opening |

frames not yet sampled: 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 16, 18, 19, 20, 22, 23, 25, 26 — full sweep review deferred to phase D.

## panorama sweep direction

does not apply — this is a sequential walking capture, not a per-corner clockwise sweep.

## fixture / feature anchors

- **light-wood treads + risers**: 13 risers total (5 lower + 2 winders + 6 upper); maple / birch finish
- **dark inlay anti-slip strips**: two parallel dark grooves on each tread nosing (visible in `stairs-10`, `stairs-17`, `stairs-27`); NOT chrome
- **wall-mounted handrail**: white / cream-painted (no wood grain), with brushed-chrome wall brackets + a white-painted elbow connector at the L-bend (visible in `stairs-4`, `stairs-7`); mounted on the west-wall on both flights per `壁付` annotation on the blueprint
- **half-wall parapet (2F)**: south edge of the upper flight, white-painted with white wood cap rail (visible in `stairs-1`, `stairs-21`)
- **whitewashed wood-plank ceiling**: above the 2F top section (visible in `stairs-1`, `stairs-10`, `stairs-13`, `stairs-24`)
- **stair entry from LDK (1F)**: open south end of the lower flight, no door; the stair carve-out in the LDK's NW corner
- **stair exit to 2F corridor (2F)**: east end of the upper flight at step 13; opens into `corridor-2-toilet-2-f` (verify door/no-door in phase E)

## folder structure (current — flat list, no sub-folders)

```
stairs/
├── room-map.md          (this file)
├── room-map-photos.md   (photo→feature index)
├── stairs-1.webp
├── stairs-2.webp
├── …
└── stairs-27.webp
```

## proposed rename

**deferred** — the flat sequential capture format is unique to the stair. Once the photo positions are mapped in phase D (which frames are at 1F bottom vs L-bend vs 2F top), a possible rename would group them into `lower-flight/`, `winder/`, `upper-flight/`, `top-2f/`, `bottom-1f/` — or leave as a flat list. User decision.

## unverified items

- exact stair shaft dimensions (read from blueprint at 400 dpi; phase C will measure precisely). 1F shaft: 0.90 × 1.60 per memory rule. 2F shaft: 1.575 × 0.90 per memory rule.
- exact winder geometry — 2 winder treads at the L-bend per blueprint number sequence (5 → 6, 7 → 8); wedge geometry confirmed top-down via `stairs-17`. Exact tread angles and dimensions still phase D / phase C.
- exact ceiling heights (1F floor to 2F floor; 2F floor to 2F ceiling above the upper flight)
- top-exit (step 13) — is there a door panel between the stair shaft and the 2F corridor, or just an opening? blueprint shows arrow `DN` at step 13 but no door arc visible at this resolution; phase E
- material specifics still TBD (see "confirmed by photo evidence" section above for what IS confirmed):
  - exact tread wood species (maple vs birch vs other light wood)
  - exact dark-inlay nosing material (walnut inlay vs rubberised vs other)
  - exact RAL / colour of the white handrail paint
  - parapet cap construction (half-height wall + cap plank vs single solid element) — confirm in mid-sweep frames
- precise step count at the L-bend — confirmed: 2 winder treads (steps 6 and 7) per blueprint and `stairs-17` top-down view
- stair carve-out shape on 1F LDK side: per the LDK map, the carve-out is ~0.9 × 1.6 = 1.44 ㎡ — matches the 1F shaft footprint (the carve-out IS the stair shaft footprint subtracted from the LDK)
- photo position assignments for frames 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 16, 18, 19, 20, 22, 23, 25, 26 (18 frames remaining; full sweep review deferred to phase D)

## usage notes

- always reference walls by feature name (west-wall, east-wall, north-wall, south-wall) — these are bounding-box names since the stair has no traditional 4-corner room shape
- the stair is structurally an L-shape inside its bounding box; the named walls are the box exterior, not the L-faces
- for 3D reconstruction in phase D, build the stair geometry per memory rule `feedback_no_floating_geometry.md` — boxed carriages under each tread, never thin treads with empty space below; closed forms by default
- material sampling from photos:
  - light-wood treads + risers: `stairs-10`, `stairs-13`, `stairs-17`, `stairs-21`, `stairs-27` (clean step views)
  - dark inlay anti-slip nosing strips: `stairs-10`, `stairs-17` (top-down clearest), `stairs-27` (side profile)
  - handrail + chrome bracket: `stairs-4` (straight-section close-up), `stairs-7` (L-bend with painted elbow connector), `stairs-13` (handrail running up)
  - taupe paint: visible in every frame
  - whitewashed wood-plank ceiling (2F top section): `stairs-1`, `stairs-10`, `stairs-13`, `stairs-24`
  - parapet cap (white wood): `stairs-1`, `stairs-21`
- image paths:
  `interior-images/stairs/stairs-NN.webp` (flat list; no sub-folder prefix)
- in phase G when finalising the stair, replace per-step boxes with one sloped wedge per flight + winders + handrail + stringer per memory rule `project_stair_must_be_l_shape.md`
