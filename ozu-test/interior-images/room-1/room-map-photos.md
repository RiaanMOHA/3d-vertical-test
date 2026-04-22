# room-1 photo → wall index

companion to `room-map.md`. lists which panorama images show each of the four walls. use this for wall texture mapping or for picking reference shots.

## wall visibility

### entrance-wall
| corner folder | image numbers |
|---|---|
| corner-cabinet-window | 02, 03, 04, 05 |
| corner-ac-window | 06, 07, 08, 09 |

### cabinet-wall
| corner folder | image numbers |
|---|---|
| corner-ac-entrance | 04, 05, 06, 07 |
| corner-cabinet-window | 04, 05, 06, 07, 08 |

### window-wall
| corner folder | image numbers |
|---|---|
| corner-cabinet-entrance | 06, 07, 08, 09 |
| corner-ac-window | 02, 03, 04 |

### ac-wall
| corner folder | image numbers |
|---|---|
| corner-cabinet-entrance | 01, 02, 03, 04, 05, 06 |
| corner-ac-entrance | 02, 03, 04 |

## what this confirms

- cabinet-wall and ac-wall are opposite walls (each one is visible from the two corners that sit on the *other* one)
- entrance-wall and window-wall are opposite walls (same pattern)
- the adjacency model in `room-map.md` is consistent with the photo evidence

## file path pattern

each entry above corresponds to a file at:

`interior-images/room-1/<corner-folder>/room-1-<corner-folder>-NN.webp`

example: cabinet-wall image 04 from corner-ac-entrance =
`interior-images/room-1/corner-ac-entrance/room-1-corner-ac-entrance-04.webp`
