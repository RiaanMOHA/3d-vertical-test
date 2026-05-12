# kitchen map

## overview

the kitchen is a small enclosed zone in the upper-right of the 1F. it has 3 fixed walls + a half-height pass-through counter facing the LDK. galley-style with one main working wall (north) and the pass-through counter (south).

the kitchen folder has 4 corner cameras (a, b, c, d) — matches the room-1 4-corner template exactly.

approximate dimensions from blueprint (verified Phase C, 400 dpi chain reading):
- width: 2,550 mm (counter length L=2,550)
- depth: 2,100 mm (east-edge chain reads 1,350 + 750 = 2,100; the prior "1,800" reading was the counter zone only, missing the fridge alcove's extra 300 mm)
- footprint: ~5.4 ㎡

assumed (to confirm):
- ceiling: continues the LDK whitewashed wood-plank, or a flat finish (TBD)
- floor: continues the LDK light oak plank
- ceiling height: 2.4–2.5 m (matching LDK)

## walls

### counter-wall (south)
- half-height pass-through counter, L=2,550 mm
- west portion: stainless steel sink + faucet
- east portion: gas stove with range hood overhead
- kitchen-interior side: white tile backsplash above the counter line, going up to ceiling
- LDK side: dark grey brick backsplash above the counter line, going up to ceiling
- opposite: fridge-wall

### fridge-wall (north)
- **interior partition**, full height (corrected Phase C — kitchen north wall is INTERIOR, not exterior; partitions with laundry on east portion (page-x=4500..6300) and with corridor on west portion (page-x=3750..4500))
- white raised-panel storage cabinets (lower) with brass-style pulls
- dark wood counter top above the lower cabinets
- dark grey brick feature wall above the counter top, continuing to ceiling (matches the LDK brick on the LDK side of the pass-through)
- refrigerator alcove fits between cabinets
- opposite: counter-wall

### window-wall (east)
- exterior wall (the kitchen's only exterior wall — real-world east,
  code x=0 after blueprint X-mirror)
- one small CLEAR (not frosted) narrow vertical window high on the
  wall — confirmed 2026-05-11 from `b/kitchen-b-11.webp` (blue sky
  visible through the pane). 縦すべり 02609 type per blueprint, modelled
  in `ozu-test.html` as `F1_WIN_LEFT[1]` at z=3.30..3.56, y=1.00..1.90.
- opposite: entry-wall

### entry-wall (west)
- interior partition wall separating kitchen from corridor
- entry / opening from corridor on this wall
- opposite: window-wall

## adjacencies

- counter-wall meets entry-wall (SW) and window-wall (SE)
- fridge-wall meets entry-wall (NW) and window-wall (NE)
- entry-wall meets counter-wall and fridge-wall
- window-wall meets counter-wall and fridge-wall

## corners

| corner id | walls meeting | notes |
|---|---|---|
| corner-entry-fridge | fridge-wall × entry-wall | NW; back-left, near corridor entry |
| corner-fridge-window | fridge-wall × window-wall | NE; back-right, refrigerator + small window cluster |
| corner-counter-entry | counter-wall × entry-wall | SW; sink end of pass-through, kitchen entrance from LDK side |
| corner-counter-window | counter-wall × window-wall | SE; stove + range hood end |

corner ids list walls in alphabetical order.

## room layout (top-down)

```
                   fridge-wall
        ┌──────────────────────────────┐
        │ [storage  [refrigerator] [storage]
        │  cabinets]                   │
 entry  │  ────brick feature above──── │  window
  wall  │                              │   wall
        │                              │ [small window]
        │ [sink]              [stove]  │
        │ [counter pass-through ────>] │
        └──────────────────────────────┘
                  counter-wall
              (LDK is south of this)
```

## camera-position mapping

yellow A/B/C/D letters on the annotated blueprint mark the 4 kitchen corners. tentative reading:

| current path | blueprint mark | corner |
|---|---|---|
| `kitchen/a/` | yellow A | corner-entry-fridge (NW) |
| `kitchen/b/` | yellow B | corner-fridge-window (NE) |
| `kitchen/c/` | yellow C | corner-counter-entry (SW) |
| `kitchen/d/` | yellow D | corner-counter-window (SE) |

(this is my reading from sample frames; user to confirm.)

## panorama sweep direction

clockwise from above (per room-1 convention). sequence 01 starts the sweep, highest number ends it.

## fixture / appliance anchors

- **stainless sink + faucet**: on counter-wall, west portion (anchored to corner-counter-entry)
- **gas stove + range hood**: on counter-wall, east portion (anchored to corner-counter-window); range hood mounts overhead from ceiling
- **utensil rod**: on counter-wall above the stove (white tile backsplash)
- **refrigerator**: on fridge-wall, set in an alcove between storage cabinets (anchored ~mid-wall, slightly NE)
- **white storage cabinets**: along fridge-wall, both sides of the refrigerator alcove
- **dark wood working counter**: on top of fridge-wall storage cabinets
- **brick feature wall**: above the dark wood counter on fridge-wall, going up to ceiling

## folder structure (current — letter-coded)

```
kitchen/
├── room-map.md          (this file)
├── room-map-photos.md   (photo→wall index)
├── a/   (23 images — corner-entry-fridge sweep)
├── b/   (29 images — corner-fridge-window sweep)
├── c/   (32 images — corner-counter-entry sweep)
└── d/   (24 images — corner-counter-window sweep)
```

## proposed rename

```bash
cd /Users/riaan/3d-vertical-test/ozu-test/interior-images/kitchen
mv a corner-entry-fridge
mv b corner-fridge-window
mv c corner-counter-entry
mv d corner-counter-window

for d in corner-entry-fridge corner-fridge-window corner-counter-entry corner-counter-window; do
  cd "$d"
  i=1
  for f in $(ls *.webp 2>/dev/null | sort -V); do
    padded=$(printf "%02d" $i)
    mv "$f" "kitchen-$d-$padded.webp"
    i=$((i+1))
  done
  cd ..
done
```

(don't run until confirmed.)

## unverified items

- exact kitchen footprint dimensions (read from blueprint at 400 dpi)
- ceiling height (assumed 2.4–2.5 m)
- ceiling finish (whitewashed wood-plank from LDK, or flat in kitchen — TBD by photos)
- exact small-window dimensions confirmed (縦すべり 02609, ~0.26 wide × 0.90 tall); type confirmed clear (not frosted) — see window-wall entry above
- whether the entry-wall has a hinged door or just an open archway to the corridor
- door type (per phase E)
- exact placement of stove vs sink along the counter-wall (stove appears east, sink west — to confirm)
- whether the utensil rod is a fixed install or removable (probably fixed)

## usage notes

- always reference walls by feature name (counter-wall, fridge-wall, window-wall, entry-wall), never by direction or coord
- corners are alphabetical wall pairs (corner-entry-fridge, not corner-fridge-entry)
- the kitchen brick on fridge-wall is structurally separate from the LDK brick on the south side of the same partition; the partition between kitchen and LDK has brick on BOTH faces (kitchen-interior tile, LDK-interior brick)
- material sampling from photos:
  - white tile backsplash + range hood: `kitchen/d/` early frames
  - brick feature: `kitchen/a/` and `kitchen/b/` early frames
  - LDK pass-through view: `kitchen/c/` early frames
- image paths after rename:
  `interior-images/kitchen/<corner-folder>/kitchen-<corner-folder>-NN.webp`
