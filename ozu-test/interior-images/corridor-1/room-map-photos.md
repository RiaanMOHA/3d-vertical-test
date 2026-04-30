# corridor-1 photo → wall index

companion to `room-map.md`. lists which panorama images from each sub-folder show each wall of the combined transit space.

each camera sweeps clockwise from above; sequence 01 starts the sweep, highest number ends it. coverage notes derived from first-frame samples (full sweep verification pending in phase D).

## wall visibility

### entry-wall (north — front door + 3-hook coat rack + single coat hook)

| current path | image numbers | notes |
|---|---|---|
| corridor-1/b/ | 1 | front door directly visible (camera SW looking N through the entire transit space) |
| corridor-1/a/ | 1 | 3-hook coat rack on entry-wall taupe section (camera NW close-up of the genkan area) |
| corridor-1/d/ | mid-late sweep | entry-wall behind the camera at NE; visible at sweep end if camera rotates 180° |

best front-door reference: `corridor-1/b/01`.
best coat-rack reference: `corridor-1/a/01`.

### bath-wall (east — brick-pattern accent, corridor section only; doors to laundry; single coat hook in the genkan section)

| current path | image numbers | notes |
|---|---|---|
| corridor-1/c/ | 1, early sweep | brick on right close-up (camera SE adjacent to bath-wall) |
| corridor-1/d/ | 1 | brick on left close-up (camera NE adjacent to bath-wall) |
| corridor-1/b/ | 1 (right edge) | single coat hook on taupe section visible far right |
| corridor-1/a/ | mid-sweep | bath-wall across the room from genkan NW |

best brick reference: `corridor-1/c/01` (right) and `corridor-1/d/01` (left) — both close-up.
best laundry-door reference: needs `corridor-1/d/` mid-sweep frames to capture the laundry door head-on (the door is on bath-wall, mid-corridor north end).

### ldk-wall (south — LDK archway, plus closet/storage partitions)

| current path | image numbers | notes |
|---|---|---|
| corridor-1/c/ | mid-late sweep | ldk-wall behind camera at SE; visible at sweep mid-rotation |
| corridor-1/d/ | mid-sweep | ldk-wall across the room (camera NE looking S, opening visible far) |
| corridor-1/b/ | mid-late sweep | ldk-wall close behind/adjacent (camera SW looking back at the LDK opening) |

note: ldk-wall has the **least photo coverage** in the first-frame samples — most cameras are oriented along the corridor axis (N-S), so the south LDK opening tends to be at sweep-edge or sweep-end frames.

best LDK-archway reference: `corridor-1/d/` mid-sweep frames (looking S along the corridor with LDK ahead).

### stairs-wall (west — toilet door, closets, stair shaft, genkan storage)

| current path | image numbers | notes |
|---|---|---|
| corridor-1/a/ | 1 | doorframe edge on the right (likely genkan-storage door) — close-up of stairs-wall north section |
| corridor-1/d/ | 1 | folding closet doors on the right (camera NE looking S, closets close-up on the west wall) |
| corridor-1/c/ | 1 (left edge) | folding doors visible on the left (closets across the corridor) |
| corridor-1/b/ | mid-sweep | stairs-wall on the left (camera SW close-up of west wall) |

best toilet-door reference: needs `corridor-1/a/` or `corridor-1/d/` mid-sweep frames to capture the toilet door head-on.
best closet-doors reference: `corridor-1/d/01` (right side).
best stair-shaft entry: needs `corridor-1/b/` early sweep (camera SW is adjacent to the stair entry).

## what this confirms

- **bath-wall ↔ stairs-wall** are opposite walls (the two long sides of the corridor): bath-wall most visible from `c` and `d` (close-up brick); stairs-wall most visible from `a` and `b` (close-up closets / toilet door).
- **entry-wall ↔ ldk-wall** are opposite walls (the two short ends): entry-wall most visible from `a` and `b` (the genkan / front-door zone); ldk-wall most visible from `c` and `d` (the corridor's south end + LDK opening).
- the adjacency model in `room-map.md` is consistent with the photo evidence — but several items (exact coat-rack position, exact brick start point, door types) need full-sweep verification.

## ceiling and floor

- **ceiling**: flat warm off-white painted finish (visible top of every photo)
- **floor**: light oak plank (visible bottom of every photo); the planks appear to run continuously from the genkan into the corridor and onward into adjacent rooms (LDK, laundry)
- **possible 土間 (step-down) at the genkan**: Japanese homes often step down ~150 mm at the genkan; needs phase D verification from a side-view sweep frame

## file path pattern

each entry corresponds to a file at:

`interior-images/corridor-1/<a|b|c|d>/corridor-1-<a|b|c|d>-NN.webp`

example: brick + folding-doors reference, corridor-1/c photo 1:
`interior-images/corridor-1/c/corridor-1-c-1.webp`

future-state note: when didi's `pano-a` + `pano-a2` re-shoots land, paths will collapse to:
`interior-images/corridor-1/<pano-a|pano-a2>/corridor-1-<pano-a|pano-a2>-NN.webp`
and this file will be rewritten accordingly.
