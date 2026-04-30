# toilet-1-f map (1F WC / トイレ)

## overview

`toilet-1-f` is the 1F water closet — the small toilet room (トイレ) in the upper-middle area of 1F, between the genkan / corridor and the UB / laundry. Listed as 1.62 ㎡ on the blueprint.

approximate dimensions from blueprint:
- ~900 mm wide (E-W) × ~1,800 mm deep (N-S)
- footprint: 1.62 ㎡ (per the blueprint label "1.62㎡")

assumed (to confirm in phase D):
- ceiling: flat painted finish (warm off-white, matches the laundry ceiling)
- floor: light oak plank (continues from corridor)
- one accent wall (brick-pattern wallpaper) + three plain taupe-painted walls

## walls

### toilet-wall (north)
- short wall (~900 mm long)
- toilet bowl + tank back against this wall
- hand-wash basin (手洗器) integrated on top of the tank, with a small faucet
- horizontal sliding privacy window high on this wall (横すべり窓 03603, FL+1800)
- opposite: door-wall

### door-wall (south)
- short wall (~900 mm long)
- door from corridor — single hinged door 開き (visible in `b/01` as a white panel with chrome hinges, and in `b/05` + `b/13` swung open to corridor); door type to be re-confirmed in phase E from blueprint arc
- opposite: toilet-wall

### brick-wall (east)
- long wall (~1,800 mm long)
- brick-pattern accent wallpaper (matches the laundry/LDK brick aesthetic)
- opposite: side-wall

### side-wall (west)
- long wall (~1,800 mm long)
- plain taupe paint
- opposite: brick-wall

## adjacencies

- toilet-wall meets brick-wall and side-wall
- door-wall meets brick-wall and side-wall
- brick-wall meets toilet-wall and door-wall
- side-wall meets toilet-wall and door-wall

## corners

| corner id | walls meeting | notes |
|---|---|---|
| corner-brick-door | brick-wall × door-wall | SE; door hinge area + brick accent meet |
| corner-brick-toilet | brick-wall × toilet-wall | NE; behind/beside the toilet tank |
| corner-door-side | door-wall × side-wall | SW; door hinge or jamb at the entry |
| corner-side-toilet | side-wall × toilet-wall | NW; basin spout side, toilet front-left |

corner ids list walls in alphabetical order.

## room layout (top-down)

```
                       toilet-wall (window above)
            ┌────────────────────────────┐
            │ [hand-wash       [toilet   │
            │  basin]           bowl]    │
   side     │                            │  brick
   wall     │                            │   wall
            │                            │ (accent)
            │                            │
            │      [folding door]        │
            └────────────────────────────┘
                       door-wall
```

(toilet placement — bowl + tank centred on toilet-wall, hand-wash basin integrated atop tank facing north — needs phase D verification)

## camera-position mapping

⚠ this room effectively has only ONE inside-toilet camera position. one blue letter "B" is annotated on the blueprint inside the toilet (south-mid area, near the door). there is no second annotated letter inside the toilet box.

| current path | blueprint mark | location | photo count |
|---|---|---|---|
| `toilet-1-f/a/` | (no letter — outside toilet) | corridor-approach views — NOT inside the toilet | 21 |
| `toilet-1-f/b/` | blue B | south-mid inside-toilet sweep | 13 |

verified 2026-04-29 by photo content review:
- `a/01` and `a/10` show corridor content — dark grey-brick wallpaper, 4-panel flat closet doors with chrome handles, taupe wall column/jamb, downlight ceiling. wall-to-wall distance is much larger than a 0.9 m toilet would allow. these are corridor-1 views, not toilet interior.
- `b/05` and `b/13` show inside-toilet content — interior brick wall (with white towel ring + small toilet-paper holder), toilet bowl + lid in foreground, white doorframe with corridor brick visible through the open door.

implication: the only true inside-toilet camera is `b/`. the `a/` folder appears to be misplaced corridor-approach photos. do not source toilet-interior materials from `a/`; treat its content as corridor-1 reference instead.

needs user decision in phase B housekeeping: leave `a/` in place as documented corridor content, or move it under `corridor-1/` as an additional viewpoint.

## panorama sweep direction

clockwise from above (per room-1 convention). sequence 01 starts the sweep, highest number ends it.

## fixture / appliance anchors

- **toilet bowl + tank**: on toilet-wall (north), centred or slightly offset
- **hand-wash basin (手洗器)**: integrated atop the tank on toilet-wall
- **toilet-paper holder**: TBD — likely on brick-wall (east) within easy reach when seated
- **horizontal sliding window**: on toilet-wall, high (FL+1800 sill)
- **folding door**: on door-wall, opens into corridor
- **brick accent wallpaper**: full brick-wall (east), floor to ceiling

## folder structure (current — letter-coded)

```
toilet-1-f/
├── room-map.md          (this file)
├── room-map-photos.md   (photo→wall index)
├── a/   (21 images — corridor-approach views, NOT inside toilet)
└── b/   (13 images — south-mid inside-toilet sweep, the only true toilet-interior camera)
```

## proposed rename

deferred until camera positions are user-confirmed. once confirmed, naming would follow `corner-X-Y` if both cameras are at named corners, or `<wall>-mid` if mid-wall.

## unverified items

- exact toilet footprint dimensions (read from blueprint at 400 dpi, ~900 × 1,800)
- ceiling height (assumed 2.4 m to match the rest of 1F)
- door type — currently described as hinged 開き based on `b/` photo evidence; re-confirm via blueprint arc in phase E
- exact placement of toilet (centred vs offset; tank against north wall confirmed)
- whether the brick accent is on the east wall or west wall — placeholder is east; `b/05` and `b/13` confirm brick is on a long side wall, but orientation analysis is inconclusive without a full sweep review
- presence and position of additional fittings (towel ring confirmed in `b/13`; toilet-paper holder confirmed in `b/13`; robe hook TBD)
- final disposition of the `a/` folder — keep as documented corridor content under `toilet-1-f/`, or move under `corridor-1/` (user decision pending)

## usage notes

- always reference walls by feature name (toilet-wall, door-wall, brick-wall, side-wall)
- corners are alphabetical wall pairs
- this room is the **smallest mapped room** so far — the 4-corner template applies in name only; only `b/` is a true inside-toilet sweep, `a/` is corridor-approach content
- material sampling from photos:
  - toilet's brick wall (interior side wall): `toilet-1-f/b/05`, `b/13`
  - taupe paint (toilet side-wall, opposite the brick): `toilet-1-f/b/01`
  - toilet bowl + lid: `toilet-1-f/b/13` (foreground)
  - towel ring + toilet-paper holder: `toilet-1-f/b/13`
  - toilet door (white hinged panel): `toilet-1-f/b/01` (closed, chrome hinges visible); `b/05` and `b/13` (open)
  - hardwood floor (toilet interior): `toilet-1-f/b/13`
  - corridor-1 reference inside `a/` (NOT toilet content): corridor brick + closet panels in `a/01`; closet panels + taupe column/jamb in `a/10`
- image paths:
  `interior-images/toilet-1-f/<a|b>/toilet-1-f-<a|b>-NN.webp`
