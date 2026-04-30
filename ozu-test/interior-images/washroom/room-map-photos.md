# washroom photo → wall index

companion to `room-map.md`. lists which panorama images from each corner show each of the four walls of the UB.

each camera sweeps clockwise from above; sequence 01 starts the sweep, highest number ends it. coverage notes below are derived from sample first-frames + close-up shots (full sweep verification pending in phase D).

## wall visibility

### bath-wall (north — bathtub long edge + shower head + soap shelf + thermostat valve + tatesuberi window above; dark wood-pattern accent)

| current path | image numbers | notes |
|---|---|---|
| washroom/a/ | 1, mid-sweep | shower fixtures + bathtub edge visible (camera SE looking NW across tub) |
| washroom/b/ | mid-sweep | shower fixtures across the room (camera SW looking N) |
| washroom/d/ | mid-late sweep | bathtub long edge close-up + shower bar (camera NE adjacent to tub foot) |
| washroom/close-up/ | 1, 2, 3 | tight shots of body soap shelf + thermostat valve mounted on dark accent |

best dark-accent + shower fixtures reference: `washroom/a/01` and `washroom/close-up/`.

### entry-wall (east — folding door to laundry; white panels)

| current path | image numbers | notes |
|---|---|---|
| washroom/d/ | 1 | folding door visible on left (camera NE looking S, door close on the east side) |
| washroom/a/ | late sweep | folding door from across (camera SE adjacent to door) |

best folding door reference: `washroom/d/01`.

### side-wall (south — plain white panel + towel/clothes rail + ventilation grille)

| current path | image numbers | notes |
|---|---|---|
| washroom/c/ | 1 | side-wall on right (camera NW looking E, side-wall ahead-right) |
| washroom/b/ | early sweep | side-wall close-up (camera SW adjacent to side-wall) |
| washroom/a/ | early sweep | side-wall close-up (camera SE adjacent to side-wall) |

best ceiling-vent / rail reference: `washroom/c/01` (vent + rail visible on right wall).

### end-wall (west — plain white panel + bathtub tap fixture above tub head)

| current path | image numbers | notes |
|---|---|---|
| washroom/b/ | 1 | end-wall close-up (camera SW adjacent to end-wall) |
| washroom/c/ | mid-sweep | end-wall close-up (camera NW adjacent to end-wall) |

note: end-wall is the **least photo-covered** wall in the first-frame samples; tap fixture position needs full sweep verification in phase D.

## what this confirms

- **bath-wall ↔ side-wall** are opposite walls (the two long walls): bath-wall most visible from south-corner cameras (`a`, `b`), side-wall most visible from north-corner cameras (`c`, `d`) when sweeping inward.
- **end-wall ↔ entry-wall** are opposite walls (the two short walls): end-wall most visible from `b` and `c` (west-side corners), entry-wall most visible from `a` and `d` (east-side corners).
- the adjacency model in `room-map.md` is consistent with the photo evidence and with the orange-letter annotations on the blueprint.

## ceiling and floor

- **ceiling**: flat white moulded panel with a downlight near centre and a ventilation grille (visible in `washroom/b/01`)
- **floor**: textured non-slip panel (UB integrated floor) — visible at the bottom of any wide-frame shot (sample TBD)

## file path pattern

each entry corresponds to a file at:

`interior-images/washroom/<a|b|c|d|close-up>/washroom-<a|b|c|d|close-up>-NN.webp`

example: bath-wall close-up, washroom/a photo 1:
`interior-images/washroom/a/washroom-a-1.webp`

after the proposed rename in `room-map.md`, paths simplify to:
`interior-images/washroom/<corner-folder>/washroom-<corner-folder>-NN.webp`
(close-up folder retained as-is — not a corner sweep)
