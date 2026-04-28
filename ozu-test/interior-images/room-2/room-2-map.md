# room-2 map

## overview

room-2 is a simple rectangular bedroom with four walls, located at the top-left of the sugimito house 2f plan (洋室2, 7.29 m², 4.5 帖). internal dimensions 2.700 m × 2.700 m (square). ceiling has a whitewashed wood-plank finish at approximately 2.5 m. walls are warm neutral grey. floor is light oak plank. same 帖 class as room-1 (4.5 帖). adjacent storage 物入 (1.42 m²) sits on the other side of the closet-wall and is accessed via sliding doors inside room-2.

## walls

### window-wall
- main sliding window (引違 11909, 1100 × 900 mm, clear glass, sill fl+2000 mm)
- curtains with tiebacks
- faces exterior (townhouse view)
- opposite: closet-wall

### closet-wall
- bi-fold / sliding closet doors opening into 物入 storage behind the wall
- no external window or fixture
- opposite: window-wall

### ac-wall
- wall-mounted toshiba ac unit, high on wall near window-wall corner
- tall narrow frosted privacy window (縦すべり 02609, sill fl+2000 mm)
- faces exterior
- opposite: entrance-wall

### entrance-wall
- single hinged entrance door to 2f 廊下 hallway (swings inward toward ac-wall side)
- wooden plank with black coat hooks mounted on this wall near entrance
- opposite: ac-wall

## adjacencies

- window-wall meets ac-wall and entrance-wall
- closet-wall meets ac-wall and entrance-wall
- ac-wall meets window-wall and closet-wall
- entrance-wall meets window-wall and closet-wall

## corners

| corner id | walls meeting | notes |
|---|---|---|
| corner-ac-window | ac-wall × window-wall | head of bed + ac unit cluster here |
| corner-ac-closet | ac-wall × closet-wall | foot of bed + frosted window side |
| corner-closet-entrance | closet-wall × entrance-wall | closet doors meet hallway door, open floor |
| corner-entrance-window | entrance-wall × window-wall | desk + bookshelf-cabinet + chair sit here |

corner ids always list the two walls in alphabetical order so each corner has exactly one canonical name.

## room layout (top-down)

```
                       window-wall
           ┌──────────────────────────────────┐
           │       [main sliding window]      │
           │                                  │
   ac-wall │ [ac]                   [shelf]   │ entrance-wall
           │ [bed head]              [desk]   │
           │ [bed]                            │ [door]
           │ [bed foot]                       │ [coat hooks]
           │ [frosted window]                 │
           │                                  │
           └──────────────────────────────────┘
                       closet-wall
                 [closet sliding doors → 物入]
```

## furniture anchors

- bed: single white metal-frame bed, long side against ac-wall, head at corner-ac-window (under ac unit), foot at corner-ac-closet
- bookshelf-cabinet: tall gray open-shelf + closed-cabinet piece, against entrance-wall at corner-entrance-window
- desk: small white desk, against entrance-wall next to bookshelf-cabinet at corner-entrance-window
- chair: tan leather swivel chair, between desk and bed
- pendant light: 4-bulb wood-arm fixture with dark shades, centered on ceiling
- ceiling light secondary: small 2-bulb spot near window-wall

## panorama sweep direction

all panoramas are shot from the named corner with the camera sweeping clockwise when viewed from above. sequence number 01 is the start of the sweep, final number is the end. sweep covers the two walls named in the corner id (plus partial views of the opposite walls mid-sweep).

note: existing sequence numbers were preserved from the original a/b/c/d capture. if any folder's native order was ccw, renumbering to cw has not yet been verified per-frame.

## folder structure

```
room-2/
├── room-2-map.md
├── corner-ac-window/
│   ├── room-2-corner-ac-window-01.webp
│   ├── ... (8 images total)
│   └── room-2-corner-ac-window-08.webp
├── corner-entrance-window/
│   ├── room-2-corner-entrance-window-01.webp
│   ├── ... (10 images total)
│   └── room-2-corner-entrance-window-10.webp
├── corner-ac-closet/
│   ├── room-2-corner-ac-closet-01.webp
│   ├── ... (9 images total)
│   └── room-2-corner-ac-closet-09.webp
└── corner-closet-entrance/
    ├── room-2-corner-closet-entrance-01.webp
    ├── ... (8 images total)
    └── room-2-corner-closet-entrance-08.webp
```

## image catalog

| folder | corner id | image count |
|---|---|---|
| corner-ac-window/ | corner-ac-window | 8 |
| corner-entrance-window/ | corner-entrance-window | 10 |
| corner-ac-closet/ | corner-ac-closet | 9 |
| corner-closet-entrance/ | corner-closet-entrance | 8 |

## coordinate system for phase 3 (three.js)

- origin (0, 0, 0) at **corner-ac-window** on the floor
- +x axis runs along **window-wall** away from origin (toward corner-entrance-window)
- +z axis runs along **ac-wall** away from origin (toward corner-ac-closet)
- +y axis is up
- right-handed coordinate system

resulting corner coordinates (w = 2.7 m, d = 2.7 m, h = 2.5 m):

| corner id | (x, z) |
|---|---|
| corner-ac-window | (0, 0) |
| corner-entrance-window | (2.7, 0) |
| corner-ac-closet | (0, 2.7) |
| corner-closet-entrance | (2.7, 2.7) |

## unverified items

- exact ceiling height (2.5 m assumed, not on blueprint)
- exact window sizes beyond blueprint callouts (11909 main window, 02609 frosted narrow)
- exact entrance door hinge side and swing angle (assumed inward toward ac-wall)
- panorama sweep direction of each folder (rename preserved native order; cw not verified frame-by-frame)
- secondary spot light position (visible but placement relative to main pendant not measured)

## usage notes for claude code

- always reference walls by feature name (window-wall, closet-wall, ac-wall, entrance-wall), never by letter or direction
- corners are always alphabetical wall pairs (corner-ac-window, not corner-window-ac)
- the parent folder of each image set IS its corner id
- image paths to use in code:
  - `interior-images/room-2/corner-ac-window/room-2-corner-ac-window-01.webp`
  - `interior-images/room-2/corner-entrance-window/room-2-corner-entrance-window-01.webp`
  - `interior-images/room-2/corner-ac-closet/room-2-corner-ac-closet-01.webp`
  - `interior-images/room-2/corner-closet-entrance/room-2-corner-closet-entrance-01.webp`
