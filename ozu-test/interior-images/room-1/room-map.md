# room-1 map

## overview

room-1 is a simple rectangular bedroom with four walls. this document defines the wall names, adjacencies, furniture anchors, folder structure, and panorama image catalog for 3d reconstruction. the room is one of the 4.5 帖 (tatami) bedrooms on 2f of the sugimito house renovation blueprint, likely 洋室2 or 洋室3 (not yet verified). assumed dimensions: 2.7m × 2.7m. ceiling has a whitewashed wood-plank finish. walls are warm neutral grey. floor is light oak plank.

## walls

### window-wall
- large sliding window (引違 / hikichigai) with curtains and tiebacks
- main daylight source, faces exterior
- opposite: entrance-wall

### entrance-wall
- single hinged entrance door (swings inward toward cabinet-wall)
- coat hooks on the interior face of the door
- faces interior hallway
- opposite: window-wall

### cabinet-wall
- closet with white bi-fold doors
- wall-mounted coat hook bar near the entrance-wall corner
- opposite: ac-wall

### ac-wall
- wall-mounted toshiba ac unit, high on wall
- narrow vertical frosted privacy window (縦すべり / tatesuberi)
- faces exterior
- opposite: cabinet-wall

## adjacencies

- window-wall meets cabinet-wall and ac-wall
- entrance-wall meets cabinet-wall and ac-wall
- cabinet-wall meets window-wall and entrance-wall
- ac-wall meets window-wall and entrance-wall

## corners

| corner id | walls meeting | notes |
|---|---|---|
| corner-cabinet-entrance | cabinet-wall × entrance-wall | entrance door swings into this corner |
| corner-cabinet-window | cabinet-wall × window-wall | desk + shelf unit sits in this corner |
| corner-ac-entrance | ac-wall × entrance-wall | foot of bed points toward this corner |
| corner-ac-window | ac-wall × window-wall | head of bed + ac unit + narrow window cluster here |

corner ids always list the two walls in alphabetical order so each corner has exactly one canonical name.

## room layout (top-down)

```
                       cabinet-wall
           ┌──────────────────────────────────┐
           │ [closet]         [coat hooks]    │
           │                                  │
 entrance  │                                  │  window
   wall    │           room-1                 │   wall
  [door]   │                                  │ [sliding window]
           │                                  │ [desk] [shelf]
           │                                  │
           └──────────────────────────────────┘
                       ac-wall
       [ac unit]                 [narrow frosted window]
```

## furniture anchors

- bed: single metal-frame bed, long side against ac-wall, head at corner-ac-window, foot at corner-ac-entrance
- desk: solid wood desk against window-wall, positioned under the sliding window
- shelf: freestanding metal-and-wood shelving unit against cabinet-wall at corner-cabinet-window, forming an l-shape with the desk
- chair: desk chair between desk and cabinet-wall
- ceiling light: 4-bulb linen-shade pendant, centered

## panorama sweep direction

all panoramas are shot from the named corner with the camera sweeping clockwise when viewed from above. the sweep starts at one adjacent wall and ends at the other. sequence number 01 is the start of the sweep, final number is the end.

## folder structure

images are organised one folder per corner inside `/interior-images/room-1/`.

```
room-1/
├── room-map.md
├── corner-cabinet-entrance/
│   ├── room-1-corner-cabinet-entrance-01.webp
│   ├── room-1-corner-cabinet-entrance-02.webp
│   ├── ... (9 images total)
│   └── room-1-corner-cabinet-entrance-09.webp
├── corner-ac-window/
│   ├── room-1-corner-ac-window-01.webp
│   ├── ... (10 images total)
│   └── room-1-corner-ac-window-10.webp
├── corner-cabinet-window/
│   ├── room-1-corner-cabinet-window-01.webp
│   ├── ... (8 images total)
│   └── room-1-corner-cabinet-window-08.webp
└── corner-ac-entrance/
    ├── room-1-corner-ac-entrance-01.webp
    ├── ... (8 images total)
    └── room-1-corner-ac-entrance-08.webp
```

## image catalog

| folder | corner id | image count |
|---|---|---|
| corner-cabinet-entrance/ | corner-cabinet-entrance | 9 |
| corner-ac-window/ | corner-ac-window | 10 |
| corner-cabinet-window/ | corner-cabinet-window | 8 |
| corner-ac-entrance/ | corner-ac-entrance | 8 |

## rename script

current structure uses letter-coded folders (a, b, c, d) and letter-coded filenames. rename both folders and files to semantic corner names. run once from the parent room folder.

```bash
cd /Users/riaan/3d-vertical-test/ozu-test/interior-images/room-1

# rename folders
mv a corner-cabinet-entrance
mv b corner-ac-window
mv c corner-cabinet-window
mv d corner-ac-entrance

# rename files inside corner-cabinet-entrance (was a, 9 images)
cd corner-cabinet-entrance
for i in 1 2 3 4 5 6 7 8 9; do
  padded=$(printf "%02d" $i)
  mv "room-1-a-$i.webp" "room-1-corner-cabinet-entrance-$padded.webp"
done
cd ..

# rename files inside corner-ac-window (was b, 10 images)
cd corner-ac-window
for i in 1 2 3 4 5 6 7 8 9 10; do
  padded=$(printf "%02d" $i)
  mv "room-1-b-$i.webp" "room-1-corner-ac-window-$padded.webp"
done
cd ..

# rename files inside corner-cabinet-window (was c, 8 images)
cd corner-cabinet-window
for i in 1 2 3 4 5 6 7 8; do
  padded=$(printf "%02d" $i)
  mv "room-1-c-$i.webp" "room-1-corner-cabinet-window-$padded.webp"
done
cd ..

# rename files inside corner-ac-entrance (was d, 8 images)
cd corner-ac-entrance
for i in 1 2 3 4 5 6 7 8; do
  padded=$(printf "%02d" $i)
  mv "room-1-d-$i.webp" "room-1-corner-ac-entrance-$padded.webp"
done
cd ..
```

## unverified items

- exact room identity on blueprint: 洋室2 vs 洋室3 (user to confirm)
- compass orientation of walls (blueprint has true north marker, mapping not yet done)
- exact dimensions: 2.7m × 2.7m assumed from blueprint, not measured on-site

## usage notes for claude code

- always reference walls by feature name (window-wall, entrance-wall, cabinet-wall, ac-wall), never by letter or direction
- corners are always alphabetical wall pairs (corner-cabinet-entrance, not corner-entrance-cabinet)
- the parent folder of each image set IS its corner id, so the containing folder path is enough to know which corner the camera is in
- when placing a camera in the 3d scene, use the corner id to position it and the sweep direction (clockwise from above) to orient it
- for wall texture mapping, each panorama sweep covers exactly two adjacent walls (the two walls named in its corner id), with the remaining two walls visible in the middle of the sweep
- image paths to use in code:
  - `interior-images/room-1/corner-cabinet-entrance/room-1-corner-cabinet-entrance-01.webp`
  - `interior-images/room-1/corner-ac-window/room-1-corner-ac-window-01.webp`
  - `interior-images/room-1/corner-cabinet-window/room-1-corner-cabinet-window-01.webp`
  - `interior-images/room-1/corner-ac-entrance/room-1-corner-ac-entrance-01.webp`
