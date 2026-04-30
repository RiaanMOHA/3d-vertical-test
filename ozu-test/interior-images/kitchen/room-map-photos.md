# kitchen photo → wall index

companion to `room-map.md`. lists which panorama images from each corner show each of the four kitchen walls.

each camera sweeps clockwise from above; sequence number 01 starts the sweep, highest number ends it. coverage notes below are derived from sample frames at sweep start (more sweep verification pending in phase D).

## wall visibility

### counter-wall (south — sink + stove + range hood + white tile + brick on LDK side)

| current path | image numbers | notes |
|---|---|---|
| kitchen/c/ | 1, 2–10 | full sink + counter view from inside; LDK visible across the pass-through |
| kitchen/d/ | 1, 2–8 | range hood + stove burners + white tile backsplash close-up |
| kitchen/a/ | mid-sweep frames | counter visible from across (north side) |
| kitchen/b/ | mid-sweep frames | counter east end visible from across |

best stove + range hood reference: `kitchen/d/` early frames.
best sink + pass-through reference: `kitchen/c/` early frames.

### fridge-wall (north — refrigerator + storage cabinets + brick feature + dark wood counter)

| current path | image numbers | notes |
|---|---|---|
| kitchen/a/ | 1 | white cabinets + dark wood counter top + brick above (close-up of NW section) |
| kitchen/b/ | 1 | refrigerator + brick wall + small adjacent window (NE section) |
| kitchen/c/ | mid-sweep frames | fridge-wall visible across the kitchen from SW |
| kitchen/d/ | mid-sweep frames | fridge-wall from across (SE) |

best refrigerator + brick reference: `kitchen/b/` early frames.
best cabinets + dark wood counter reference: `kitchen/a/` early frames.

### window-wall (east — small high frosted/clear window)

| current path | image numbers | notes |
|---|---|---|
| kitchen/b/ | 1 | small window visible right of refrigerator |
| kitchen/d/ | mid-late sweep | east wall + window |

best window reference: `kitchen/b/` early frames.

### entry-wall (west — partition with corridor entry)

| current path | image numbers | notes |
|---|---|---|
| kitchen/a/ | mid-late sweep | entry-wall from across (NW corner sweep) |
| kitchen/c/ | late sweep | entry-wall from SW position |

note: entry-wall has the **least photo coverage** in sample frames seen — most kitchen photos face the working walls (north + south), not the side walls. needs full sweep verification in phase D.

## what this confirms

- **counter-wall ↔ fridge-wall** are opposite (the two long walls of the galley). photos from south corners (`c`, `d`) show fridge-wall; photos from north corners (`a`, `b`) show counter-wall.
- **window-wall ↔ entry-wall** are opposite (the two short side walls). less photo coverage but visible from corner sweeps.
- the adjacency model in `room-map.md` is consistent with the photo evidence.

## ceiling and floor

- **ceiling**: TBD — from `kitchen/c/` looking out, the LDK ceiling (whitewashed wood-plank) is visible; the kitchen-interior ceiling may differ (likely flat white or matching wood-plank — confirm in phase D)
- **floor**: light oak plank (continues from LDK)

## file path pattern

each entry corresponds to a file at:

`interior-images/kitchen/<a|b|c|d>/kitchen-<a|b|c|d>-NN.webp`

example: refrigerator + brick reference, kitchen/b photo 1:
`interior-images/kitchen/b/kitchen-b-1.webp`

after the proposed rename in `room-map.md`, paths simplify to:
`interior-images/kitchen/<corner-folder>/kitchen-<corner-folder>-NN.webp`
