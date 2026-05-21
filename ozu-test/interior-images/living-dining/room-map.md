# living-dining map (LDK)

## overview

the LDK is the main open ground-floor space — 26.13 ㎡ (16.1 帖) per the blueprint. it has four walls but no internal walls separating living, dining, and kitchen zones; only a half-height kitchen counter (L=2,550 mm) divides the kitchen zone visually.

photo organisation splits the LDK into two folders: `living-dining/` (this document — covers the open living-dining area, 6 panorama positions) and `kitchen/` (separate, has its own map). this document covers `living-dining/` only.

assumed dimensions from blueprint (page-coords, before X-mirror to 3D code coords):
- footprint: 6,300 mm × 4,500 mm
- NW corner has a stair carve-out (≈ 900 × 1,600 mm, partitioned with walls — counts as part of the LDK shape but not as room area)
- ceiling: whitewashed wood-plank finish (same as room-1)
- floor: light oak plank
- walls: warm neutral grey, with a brick-clad accent on the east wall

## walls

### kitchen-wall (north)
- interior wall separating the LDK from the kitchen and the corridor
- kitchen counter pass-through (L=2,550 mm) at half-height — opens into the kitchen zone behind
- corridor entry near the west end (alongside the stair carve-out)
- the stair partition starts at the west end of this wall
- opposite: garden-wall

### garden-wall (south)
- exterior wall, full 6,300 mm long
- two large sliding glass doors (引違) with cream curtains and tiebacks
- main daylight source
- opposite: kitchen-wall

### brick-wall (east)
- exterior wall
- brick accent cladding across the full wall
- one curtained window cut into the brick
- toshiba-style AC unit mounted high near the ceiling
- opposite: stairs-wall

### stairs-wall (west)
- exterior wall
- stair shaft + partition occupies the upper (north) portion of this wall
- exterior windows TBD (none confirmed in first-photo samples)
- opposite: brick-wall

## adjacencies

- kitchen-wall meets brick-wall and stairs-wall
- garden-wall meets brick-wall and stairs-wall
- brick-wall meets kitchen-wall and garden-wall
- stairs-wall meets kitchen-wall and garden-wall

## corners

| corner id | walls meeting | notes |
|---|---|---|
| corner-brick-garden | brick-wall × garden-wall | SE corner |
| corner-brick-kitchen | brick-wall × kitchen-wall | NE corner; next to kitchen counter end |
| corner-garden-stairs | garden-wall × stairs-wall | SW corner |
| corner-kitchen-stairs | kitchen-wall × stairs-wall | NW corner; just below the stair carve-out |

corner ids always list walls in alphabetical order.

## room layout (top-down)

```
                          kitchen-wall
       ┌─────────────────────────────────────────────┐
       │  [stair      [counter pass-through]         │
       │   shaft]  [corridor entry]                  │
       │   ─────                                     │
 stairs│                                             │ brick
  wall │              [LDK open floor]               │ wall
       │  [sofa]                       [dining]      │ [AC]
       │                                             │
       │     [<──── sliding glass doors ────>]       │
       └─────────────────────────────────────────────┘
                          garden-wall
```

## camera-position mapping

confirmed: red letters = `living/` sub-folder, blue letters = `dining/` sub-folder. blueprint positions:

| current path | blueprint mark | location in LDK | corner / mid-wall |
|---|---|---|---|
| `living/a/` | red A | NW area, just under the stair carve-out | corner-kitchen-stairs |
| `living/b/` | red B | SW corner | corner-garden-stairs |
| `living/c/` | red C | along the south (garden-wall), mid-left | garden-wall mid-west |
| `dining/a/` | blue A | SE corner | corner-brick-garden |
| `dining/b/` | blue B | NE corner, next to kitchen counter end | corner-brick-kitchen |
| `dining/c/` | blue C | along the south (garden-wall), mid-right | garden-wall mid-east |

four cameras sit at the four LDK corners; two (`living/c` and `dining/c`) sit mid-way along the garden-wall (closer-up sweeps of the south sliding-door area).

## panorama sweep direction

per the room-1 convention: each panorama is shot from the camera position with the camera sweeping clockwise viewed from above. sequence 01 starts the sweep; the highest number ends it. each corner sweep covers two adjacent walls + glimpses of the opposite walls.

## furniture anchors (from sample photos — to be verified across full sweeps)

- **sofa**: dark leather two-seater, in the living zone (south-west half of LDK), facing north toward the TV
- **coffee table**: low dark wood, between sofa and TV
- **TV + dark wood console with drawers**: against the kitchen-wall, between corner-kitchen-stairs and the kitchen counter pass-through; faces south toward the sofa
- **dining table**: solid wood with metal-framed dining chairs, in the dining zone (north-east half of LDK), near the kitchen counter end
- **antique two-faced wall clock**: mounted on a bracket near the corridor entry on kitchen-wall (visible from both living and dining zones)
- **chandelier-style pendant lights**: one over the dining table, one over the living area

## folder structure (current — pre-rename)

```
living-dining/
├── room-map.md            (this file)
├── room-map-photos.md     (photo→wall index)
├── living/
│   ├── a/    (35 images — corner-kitchen-stairs sweep)
│   ├── b/    (37 images — corner-garden-stairs sweep)
│   └── c/    (20 images — garden-wall mid-west sweep)
└── dining/
    ├── a/    (36 images — corner-brick-garden sweep)
    ├── b/    (34 images — corner-brick-kitchen sweep)
    └── c/    (15 images — garden-wall mid-east sweep)
```

## proposed rename (run after user confirms)

since architecturally the LDK is one open room with 6 camera positions (not two sub-rooms), collapse the `/living/` and `/dining/` shells and rename per camera position:

```bash
cd /Users/riaan/3d-vertical-test/ozu-test/interior-images/living-dining

mv living/a corner-kitchen-stairs
mv living/b corner-garden-stairs
mv living/c garden-wall-mid-west
mv dining/a corner-brick-garden
mv dining/b corner-brick-kitchen
mv dining/c garden-wall-mid-east
rmdir living dining

for d in corner-kitchen-stairs corner-garden-stairs garden-wall-mid-west corner-brick-garden corner-brick-kitchen garden-wall-mid-east; do
  cd "$d"
  # files currently named like  living-dining-{living,dining}-{a,b,c}-N.webp
  # rename to                    living-dining-<d>-NN.webp
  N=$(ls *.webp 2>/dev/null | wc -l | xargs)
  i=1
  for f in $(ls *.webp 2>/dev/null | sort -V); do
    padded=$(printf "%02d" $i)
    mv "$f" "living-dining-$d-$padded.webp"
    i=$((i+1))
  done
  cd ..
done
```

(don't run this until confirmed — folder/file rename is one-shot.)

## unverified items

- exact LDK dimensions (6,300 × 4,500 read from blueprint at 400 dpi; not site-measured)
- exact stair carve-out dimensions (900 × 1,600 read from blueprint)
- ceiling height (assumed 2.4–2.5 m to match room-1 / room-2 conventions)
- exact location of the corridor entry door on kitchen-wall (left of counter vs right of counter)
- existence and position of windows on stairs-wall (west exterior wall) — not visible in first-photo samples
- door types (hinged 開き / sliding 引違 / folding 折戸) for corridor entry — TBD in phase E
- exact furniture coords (will derive from the photo sweeps in phase D)

## usage notes for claude code

- always reference walls by feature name (kitchen-wall, garden-wall, brick-wall, stairs-wall) — never by direction or coord
- corners are alphabetical wall pairs (corner-brick-garden, not corner-garden-brick)
- the parent folder of each image set IS its camera position once renamed: `corner-*` folders sit at corners, `garden-wall-mid-*` folders sit mid-wall
- when placing the LDK in 3D, anchor the 4 corners to phase-C global coords; place the kitchen counter, stair partition, AC unit, and brick cladding relative to wall feature names
- material sampling from photos:
  - brick: `corner-brick-garden/` early sweep frames, `corner-brick-kitchen/` early frames
  - garden-wall sliding doors + curtain: `garden-wall-mid-west/`, `garden-wall-mid-east/`
  - ceiling + floor: visible in every photo
- image paths after rename:
  `interior-images/living-dining/<camera-folder>/living-dining-<camera-folder>-NN.webp`
