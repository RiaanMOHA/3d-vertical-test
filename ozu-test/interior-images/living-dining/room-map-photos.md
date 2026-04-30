# living-dining photo → wall index

companion to `room-map.md`. lists which panorama images from each camera show each of the four LDK walls. use for wall-texture sampling and reference-shot picking.

each camera sweeps clockwise from above; sequence number 01 starts the sweep, highest number ends it. coverage below is derived from sample frames at sweep start, mid, and end across all 6 cameras (18 frames inspected).

## wall visibility

### brick-wall (east — brick cladding, curtained window cut into the brick, toshiba AC mounted high)

| current path | image numbers | notes |
|---|---|---|
| living/a/ | 18, 35 | mid-sweep "opposite-wall" view; full brick + AC visible |
| living/c/ | 1, 10, 20 | full sweep faces brick-wall closely |
| dining/a/ | 1, 18 | brick on left of frame (camera at corner-brick-garden) |
| dining/b/ | 1, 17, 34 | full sweep faces brick-wall (camera at corner-brick-kitchen) |
| dining/c/ | 1, 8 | brick visible as kitchen backsplash in the pass-through |

best brick + AC texture references: `dining/b/` early frames, `living/c/` early frames.

### garden-wall (south — two sliding glass doors with cream curtains and tiebacks)

| current path | image numbers | notes |
|---|---|---|
| living/b/ | (south-facing frames during sweep) | curtain edge mid-sweep |
| living/c/ | 20 | curtain + window visible right side |
| dining/a/ | 18 | full curtain + sliding door panel visible |
| dining/b/ | 1, 17 | curtain edge mid-sweep |
| dining/c/ | 15 | curtain at right side (camera mid-east along garden-wall) |

best sliding-door + curtain texture: `dining/a/` mid-sweep frames.

### kitchen-wall (north — kitchen counter pass-through L=2,550, corridor entry, antique wall clock)

| current path | image numbers | notes |
|---|---|---|
| living/a/ | 1 | kitchen entry + corridor doors in distance |
| living/c/ | 20 | antique clock + chandelier + TV alcove looking N |
| dining/a/ | 1 | clock visible far left, kitchen distant |
| dining/b/ | 1 | kitchen counter visible (camera at NE corner) |
| dining/c/ | 1, 8 | full counter pass-through + refrigerator with brick backsplash behind |

best counter + clock + corridor reference: `dining/c/` early frames.

### stairs-wall (west — exterior wall; stair partition occupies its north end; frosted vertical slit window)

| current path | image numbers | notes |
|---|---|---|
| living/a/ | 35 | curtain + frosted window visible left edge |
| living/b/ | 1, 19, 37 | stair carve-out + frosted slit window visible at b-37 |

note: stairs-wall has the **least photo coverage** — most LDK cameras face away from it. the stair partition is more prominent in photos than the wall surface itself.

## what this confirms

- **brick-wall ↔ stairs-wall** are opposite walls (each visible most often from cameras *on the other side*: brick is heavily covered by `dining/*` cameras at the east; stairs-wall by `living/b/` at the SW).
- **kitchen-wall ↔ garden-wall** are opposite walls (kitchen most visible from `dining/c/` and `dining/b/` near it; garden-wall most visible from `dining/a/` and the mid-wall cameras).
- the adjacency model in `room-map.md` is consistent with the photo evidence.

## ceiling and floor (visible in every photo)

- **ceiling**: whitewashed wood-plank, plank direction parallel to the brick-wall (running east–west). matches room-1 ceiling material.
- **floor**: light oak plank, planks running parallel to the garden-wall (east–west).
- best ceiling sample: `living/c/01` looking up.
- best floor sample: `living/a/01` looking down at the floor.

## file path pattern

each entry corresponds to a file at:

`interior-images/living-dining/<living|dining>/<a|b|c>/living-dining-<living|dining>-<a|b|c>-NN.webp`

example: brick-wall image 18 from `living/a/`:
`interior-images/living-dining/living/a/living-dining-living-a-18.webp`

after the proposed rename in `room-map.md`, paths simplify to:
`interior-images/living-dining/<camera-folder>/living-dining-<camera-folder>-NN.webp`
