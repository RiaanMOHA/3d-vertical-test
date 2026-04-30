# laundry map (洗面所 / powder + washing-machine room)

## overview

`laundry` is the user's label for the **洗面所** — the powder room with a vanity sink and a washing-machine alcove, on 1F east of the UB. The bath unit itself is the `washroom` folder, not this one.

approximate dimensions from blueprint:
- 1,800 mm wide (E-W) × 2,700 mm deep (N-S)
- footprint: ~4.86 ㎡

assumed (to confirm in phase D):
- ceiling: flat painted finish, taupe-tinged off-white
- floor: light oak plank (continues from corridor)
- main accent: brick-pattern wallpaper on the vanity-wall (east); other walls in warm taupe-grey paint

## walls

### bath-wall (west)
- interior wall, partition with the UB
- single hinged door (開き) into the UB at the south end of this wall, based on the swing-arc shown on the blueprint inside the UB box (door type to be re-confirmed in phase E)
- two flush white access panels mounted high (likely attic access hatch + plumbing/electrical access)
- opposite: vanity-wall

### door-wall (south)
- interior wall, partition toward the corridor / LDK
- door from the corridor (interior swing door) — main entry to the laundry
- opposite: window-wall

### vanity-wall (east)
- exterior wall
- **brick-pattern wallpaper** across full wall (the room's only accent wall)
- north portion: washing-machine alcove (washer sits against this wall in the north half)
- south portion: vanity sink with circular basin + faucet + sconce light above
- opposite: bath-wall

### window-wall (north)
- exterior wall
- horizontal sliding window high on the wall (横すべり窓 06003, FL+1800)
- a small built-in PS (pipe shaft) recess in the NW corner area — interior bulkhead for plumbing/HVAC risers; takes a small chunk out of the laundry's NW footprint
- clothes-drying rails (chrome) mounted on this wall (TBD — may be on bath-wall instead, full-sweep verification needed)
- opposite: door-wall

## adjacencies

- bath-wall meets door-wall and window-wall
- vanity-wall meets door-wall and window-wall
- door-wall meets bath-wall and vanity-wall
- window-wall meets bath-wall and vanity-wall

## corners

| corner id | walls meeting | notes |
|---|---|---|
| corner-bath-door | bath-wall × door-wall | SW; UB folding door immediately north of this corner |
| corner-bath-window | bath-wall × window-wall | NW; access panels above + drying rails to the right |
| corner-door-vanity | door-wall × vanity-wall | SE; basin + faucet immediately north of this corner |
| corner-vanity-window | vanity-wall × window-wall | NE; washing-machine alcove sits against this corner |

corner ids list walls in alphabetical order.

## room layout (top-down)

```
                       window-wall (exterior, sliding window high)
        ┌─────────────────────────────────────────┐
        │ [drying rails]   [washing machine alcove]
        │                                         │
        │                                         │
   bath │  [access                  [vanity       │ vanity
   wall │   panels]                  sink         │  wall
        │                            + sconce]    │ (brick
        │                                         │  accent)
        │ [UB folding door]                       │
        │                                         │
        └─────────────────────────────────────────┘
                       door-wall (corridor entry)
```

## camera-position mapping

confirmed by the green letters on the annotated blueprint `ozu-1-blueprint-updated.jpeg`:

| current path | blueprint mark | corner |
|---|---|---|
| `laundry/a/` | green A | corner-bath-door (SW) |
| `laundry/b/` | green B | corner-door-vanity (SE) |
| `laundry/c/` | green C | corner-vanity-window (NE) |
| `laundry/d/` | green D | corner-bath-window (NW) |

## panorama sweep direction

clockwise from above (per room-1 convention). sequence 01 starts the sweep, highest number ends it.

## fixture / appliance anchors

- **washing machine**: in alcove against vanity-wall, north portion (anchored to corner-vanity-window)
- **vanity sink (circular basin)**: against vanity-wall, south portion (anchored toward corner-door-vanity)
- **vanity faucet**: above the basin, mounted on vanity-wall
- **sconce wall light**: above the vanity, on vanity-wall (small white globe)
- **brick accent wallpaper**: full vanity-wall (east), floor to ceiling
- **horizontal sliding window**: window-wall (north), high (FL+1800 sill)
- **clothes-drying rails (chrome bars)**: TBD — likely window-wall (north) or bath-wall (west)
- **access hatch panels**: bath-wall (west), high — attic hatch and plumbing/electrical access
- **UB folding door**: bath-wall (west), south end

## folder structure (current — letter-coded)

```
laundry/
├── room-map.md          (this file)
├── room-map-photos.md   (photo→wall index)
├── a/   (22 images — corner-bath-door sweep)
├── b/   (25 images — corner-door-vanity sweep)
├── c/   (24 images — corner-vanity-window sweep)
└── d/   (24 images — corner-bath-window sweep)
```

## proposed rename

```bash
cd /Users/riaan/3d-vertical-test/ozu-test/interior-images/laundry
mv a corner-bath-door
mv b corner-door-vanity
mv c corner-vanity-window
mv d corner-bath-window

for d in corner-bath-door corner-door-vanity corner-vanity-window corner-bath-window; do
  cd "$d"
  i=1
  for f in $(ls *.webp 2>/dev/null | sort -V); do
    padded=$(printf "%02d" $i)
    mv "$f" "laundry-$d-$padded.webp"
    i=$((i+1))
  done
  cd ..
done
```

(don't run until confirmed.)

## unverified items

- exact laundry footprint (read from blueprint at 400 dpi, ~1,800 × 2,700)
- ceiling height (assumed 2.4 m to match the rest of 1F)
- precise position of clothes-drying rails (window-wall vs bath-wall)
- exact 横すべり窓 06003 sliding-window dimensions and centring along window-wall
- door type for corridor entry door on door-wall (hinged interior door — confirmed in a-1 — but swing direction TBD)
- whether the washing machine is wall-mounted (top-loader on legs) or pedestal-mounted (front-loader on plinth) — appears to be a top-loading machine in c-1
- the access panels on bath-wall: how many, what they cover (attic vs plumbing)
- whether the vanity has a mirror cabinet above the basin

## usage notes

- always reference walls by feature name (bath-wall, door-wall, vanity-wall, window-wall), never by direction or coord
- corners are alphabetical wall pairs (corner-bath-door, not corner-door-bath)
- the vanity-wall is the room's accent — brick-pattern wallpaper running floor to ceiling
- the bath-wall and vanity-wall are the OPPOSITE long walls (they share the partition story between UB and the powder room — bath-wall is the laundry-side face of the partition that is also the UB's entry-wall)
- material sampling from photos:
  - brick accent: `laundry/b/` and `laundry/c/` (close-ups of brick around the washer)
  - taupe paint finish: `laundry/a/` (south-facing view shows clean taupe wall)
  - hardwood floor: `laundry/a/01` (floor visible toward the corridor)
  - access panels: `laundry/a/01` upper-left + `laundry/b/` (access panels on bath-wall side)
  - sconce light: `laundry/c/01` (top-left of frame near the basin)
  - drying rails: `laundry/d/01` (chrome bars on left)
- image paths after rename:
  `interior-images/laundry/<corner-folder>/laundry-<corner-folder>-NN.webp`
