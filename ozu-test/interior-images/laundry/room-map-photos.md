# laundry photo → wall index

companion to `room-map.md`. lists which panorama images from each corner show each of the four walls.

each camera sweeps clockwise from above; sequence 01 starts the sweep, highest number ends it. coverage notes below derived from sample first-frames (full sweep verification pending in phase D).

## wall visibility

### vanity-wall (east — brick-pattern wallpaper + washing-machine alcove (north) + vanity sink + faucet + sconce (south))

| current path | image numbers | notes |
|---|---|---|
| laundry/b/ | 1 | brick on right + washer top in foreground (camera SE looking N along vanity-wall) |
| laundry/c/ | 1 | brick on right + washer + plumbing connections + wall sconce on left (camera NE adjacent to vanity-wall) |
| laundry/a/ | 1 (left edge) | brick visible on left of frame, viewed across the room (camera SW facing S) |
| laundry/d/ | mid-late sweep | brick visible across the room (camera NW facing E) |

best brick + washer reference: `laundry/c/01`.
best vanity sink + sconce reference: needs `laundry/b/` mid-sweep (sweep should pass over the basin).

### bath-wall (west — folding door from UB at south end + access panels high)

| current path | image numbers | notes |
|---|---|---|
| laundry/a/ | 1 | bath-wall on right of frame (taupe paint + UB folding door at south end visible behind the corridor door) |
| laundry/d/ | early sweep | access panel high on left edge of frame (camera NW close to bath-wall) |
| laundry/b/ | mid-sweep | bath-wall across the room (camera SE facing W) |

best access panel reference: `laundry/d/` early frames.
best UB folding door reference (interior side): `laundry/a/` early frames.

### door-wall (south — door to corridor, hinged interior door)

| current path | image numbers | notes |
|---|---|---|
| laundry/a/ | 1 | corridor door directly ahead (camera SW facing S, door open showing corridor beyond) |
| laundry/b/ | 1 (corner) | corridor door visible on right (camera SE adjacent to door-wall) |

best corridor-door reference: `laundry/a/01`.

### window-wall (north — horizontal sliding window 横すべり窓 06003 high + drying rails)

| current path | image numbers | notes |
|---|---|---|
| laundry/d/ | 1 | drying rails (chrome bars) on left edge of frame (camera NW close to window-wall) |
| laundry/c/ | mid-sweep | window-wall close-up (camera NE adjacent to window-wall) |

note: the sliding window is high on the wall (FL+1800), so it may be partially out of frame in close-up corner sweeps. drying rails position needs confirmation across full sweeps.

## what this confirms

- **vanity-wall ↔ bath-wall** are opposite walls (the two long walls of the powder room). vanity-wall heavily covered from south-corner cameras (`a` looking across, `b` facing N along it); bath-wall covered from `d` close-up + `a` adjacent.
- **window-wall ↔ door-wall** are opposite walls (the two short walls). window-wall covered from `c` and `d`; door-wall covered from `a` and `b`.
- the adjacency model in `room-map.md` is consistent with the photo evidence and the green-letter annotations on the blueprint.

## ceiling and floor

- **ceiling**: flat painted finish, taupe-tinged off-white (visible top of every photo)
- **floor**: light oak plank, planks running E-W (visible at floor level in `laundry/a/01`)

## file path pattern

each entry corresponds to a file at:

`interior-images/laundry/<a|b|c|d>/laundry-<a|b|c|d>-NN.webp`

example: brick + washer reference, laundry/c photo 1:
`interior-images/laundry/c/laundry-c-1.webp`

after the proposed rename in `room-map.md`, paths simplify to:
`interior-images/laundry/<corner-folder>/laundry-<corner-folder>-NN.webp`
