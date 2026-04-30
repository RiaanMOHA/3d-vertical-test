# room-3 map (= SE 2F room, 洋室1)

## overview

room-3 is the **SE 2F room**, 6 帖, 2.7 × 3.6 m per blueprint (footprint 9.72 ㎡). The Japanese label on the blueprint is **洋室1** (yōshitsu 1). Per the annotated blueprint, this folder is marked with pink **Room3** label.

⚠ different from room-1 + room-2: this room has a **3-camera sweep** (sub-folders `a/`, `b/`, `c/` — only 3 corners), not 4. The 4th corner (most likely the bed-head corner where the bed blocks tripod placement) is skipped per the panorama capture.

approximate dimensions:
- width: 2.7 m (E-W per blueprint)
- depth: 3.6 m (N-S per blueprint)
- footprint: 9.72 ㎡ (6 帖) per blueprint
- ceiling: whitewashed wood-plank (matches the 2F room + corridor convention)
- floor: light maple plank (matches the 2F convention)
- walls: warm taupe-grey paint

## walls

### window-wall (south exterior — SE room's south wall)
- **exterior wall**, ~2.7 m long
- contains: **large sliding window** (引違 15009 — the LARGER window size used for 6帖 rooms, vs 引違 11909 for 4.5帖 rooms; with cream curtains and tieback) — main daylight source
- contains: **wall-mounted Toshiba AC unit** mounted high on this wall, near one corner
- (this is different from room-1/room-2 where AC and large window are on separate walls — in room-3, the AC and the sliding window share the same wall)
- opposite: entrance-wall

### frosted-wall (east exterior — SE room's east wall)
- **exterior wall**, ~3.6 m long
- contains: **narrow vertical frosted privacy window** (縦すべり 02609, FL+2000) high on the wall
- otherwise plain taupe paint
- opposite: closet-wall

### closet-wall (west interior — partition with the closet column / corridor)
- **interior partition**, ~3.6 m long
- partition with the central 900mm closet column between room-3 and room-4 (per blueprint chain 2700+900+2700)
- visible features: dark wood + black metal shelving unit (freestanding), positioned along this wall
- opposite: frosted-wall

### entrance-wall (north interior — partition with the 2F corridor)
- **interior partition**, ~2.7 m long
- contains: **single hinged white door (開き)** from the 2F corridor (verify swing direction in phase E)
- contains: **multi-hook coat rack** mounted on this wall (light wood backing with dark/black metal hooks) — visible in `a/01`, `c/01`
- AC remote panel + light switch likely on this wall (TBD via phase D mid-sweep)
- opposite: window-wall

## adjacencies

- window-wall meets frosted-wall and closet-wall
- entrance-wall meets frosted-wall and closet-wall
- frosted-wall meets window-wall and entrance-wall
- closet-wall meets window-wall and entrance-wall

## corners

| corner id | walls meeting | location | notes |
|---|---|---|---|
| corner-closet-entrance | closet-wall × entrance-wall | NW | dark shelving sits along closet-wall starting near this corner; coat rack on entrance-wall starts near this corner |
| corner-closet-window | closet-wall × window-wall | SW | bed-head area; AC unit mounted high on window-wall near this corner; large sliding window starts near this corner |
| corner-entrance-frosted | entrance-wall × frosted-wall | NE | TBD what's at this corner — possibly a desk/chair if room-1/room-2 pattern holds |
| corner-frosted-window | frosted-wall × window-wall | SE | bed-foot area (if bed runs N-S along east half of room with head at SW); narrow vertical frosted window on frosted-wall starts near this corner |

corner ids list walls in alphabetical order. **only 3 of these have camera sweeps** — the 4th is skipped per the photo capture.

## room layout (top-down, with compass orientation: window-wall=S, frosted-wall=E, closet-wall=W, entrance-wall=N)

✓ compass orientation locked in by Phase C global coords (`blueprints/global-coords.md`). Relative positions are also confirmed by photos.

```
                       entrance-wall  (N interior, door from corridor)
       ┌─────────────────────────────────────────┐
       │ [coat        [door]                     │
       │  rack]                                  │
       │                                         │
       │ [dark wood                              │ frosted
   closet│  + black                              │  wall
   wall │  metal                                 │ (E ext.)
       │  shelving]            room-3            │
       │                       6 帖              │ [narrow vert.
       │                       2.7 × 3.6         │  frosted window
       │                                         │   high on wall]
       │                                         │
       │ [bed        →→→→→ runs N-S →→→→→        │
       │  head against window-wall;              │
       │  foot toward entrance-wall]             │
       │                                         │
       │ [AC unit high]    [large sliding        │
       │                    window + curtains]   │
       └─────────────────────────────────────────┘
                       window-wall  (S exterior, AC + large sliding window)
```

(bed orientation: based on `b/01` showing the bed head against the AC+window wall. exact placement of furniture along the long axis is TBD via phase D.)

## camera-position mapping

⚠ TENTATIVE — folders are still letter-coded (`a/`, `b/`, `c/`), not yet renamed to corner-X-Y. photo-content reasoning below.

| current path | photo count | tentative position | photo evidence |
|---|---|---|---|
| `a/` | 8 | corner-frosted-window (SE) — looking diagonally NW | `a/01` shows: coat rack on entrance-wall on left side of frame; small high vertical frosted window on far-right (frosted-wall); iron-frame bed visible on right. Camera at SE corner sees both adjacent walls (frosted on right + window on bottom-back) and diagonally-opposite corner area (entrance-wall left, closet-wall left-far). |
| `b/` | 10 | corner-closet-entrance (NW) — looking diagonally SE | `b/01` shows: looking down the long axis of the bed (head far, foot near camera); AC + large sliding window with curtains visible on the far wall (window-wall); narrow vertical frosted window on the side wall (frosted-wall, camera-left). Pendant ceiling light visible top-right. Iron bed running into the frame's foreground. Camera at NW corner sees both adjacent walls (closet on left + entrance on right) and diagonally-opposite corner area. |
| `c/` | 9 | corner-entrance-frosted (NE) — looking diagonally SW | `c/01` shows: dark wood + black metal freestanding shelving on left (against closet-wall); white open door ahead (entrance-wall door); coat rack on right wall (entrance-wall continues to camera-right). Camera at NE corner sees both adjacent walls (entrance on right + frosted on... left?) and looks toward closet-window corner. |

**skipped corner**: corner-closet-window (SW) — likely the bed-head corner where the iron-frame bed against the window-wall blocks tripod placement.

⚠ all 3 mappings are TENTATIVE pending phase D photo-by-photo verification. the photo-content reading is plausible but not blueprint-verified at the corner-letter level (B/A/C visible on annotated jpeg crop but assignment to specific folders not 1:1 confirmed).

## panorama sweep direction

clockwise from above (per room-1 convention). sequence 01 starts the sweep, highest number ends it.

## furniture / fixture anchors

- **single iron-frame bed** with dark-stained WOOD inset on the headboard + iron rails (different from room-2's all-white iron frame): head against window-wall (under AC + large window), foot toward entrance-wall. cream / off-white bedding with grey/blue accent pillow.
- **dark wood + black metal freestanding shelving**: along closet-wall, near corner-closet-entrance (NW) — has dark wood shelves with iron / black metal frame; appears to be a 3-tier or 4-tier industrial-style shelf
- **multi-hook coat rack**: on entrance-wall (light wood backing with dark/black metal hooks); identical style to room-2's coat rack
- **wall-mounted Toshiba AC unit**: high on window-wall, near corner-closet-window (SW)
- **rattan/woven pendant light**: ceiling, possibly centred — visible in `b/01` (top-right of frame, hanging cord visible)
- **desk + chair**: TBD — `c/01` doesn't clearly show a desk; if present, likely at corner-entrance-frosted (NE) per room-1/room-2 pattern

## folder structure (current — letter-coded, not yet renamed)

```
room-3/
├── room-map.md          (this file — to be created)
├── room-map-photos.md   (photo→wall index — to be created)
├── a/   (8 images — tentative SE corner: corner-frosted-window)
├── b/   (10 images — tentative NW corner: corner-closet-entrance)
└── c/   (9 images — tentative NE corner: corner-entrance-frosted)
```

## proposed rename

deferred until camera positions are confirmed in phase D. once confirmed:

```bash
cd /Users/riaan/3d-vertical-test/ozu-test/interior-images/room-3
mv a corner-frosted-window
mv b corner-closet-entrance
mv c corner-entrance-frosted

for d in corner-frosted-window corner-closet-entrance corner-entrance-frosted; do
  cd "$d"
  i=1
  for f in $(ls *.webp 2>/dev/null | sort -V); do
    padded=$(printf "%02d" $i)
    mv "$f" "room-3-$d-$padded.webp"
    i=$((i+1))
  done
  cd ..
done
```

(don't run until confirmed.)

## unverified items

- exact compass orientation locked in: window-wall=S, frosted-wall=E, closet-wall=W, entrance-wall=N (per `blueprints/global-coords.md`)
- exact dimensions (2.7 × 3.6 read from blueprint at 400 dpi)
- ceiling height (assumed 2.4 m to match other 2F rooms)
- camera-position assignments for `a/`, `b/`, `c/` (photo-content reading is plausible but not corner-letter-confirmed)
- which corner is skipped (assumed corner-closet-window per bed-head-blocking; could also be a different corner — phase D verify)
- whether there's a closet (built-in or freestanding) on closet-wall — `b/01` view doesn't clearly show one; the dark shelving piece could BE the closet, OR there's a built-in elsewhere
- exact position of the freestanding dark-wood-and-black-metal shelving along closet-wall
- AC remote control panel + light switch position on entrance-wall — likely near the door (TBD via phase D)
- desk + chair presence — not clearly visible in sampled `c/01` frame; phase D confirm
- door type (currently inferred hinged 開き; re-confirm via blueprint arc in phase E)
- specific blueprint annotation letters (B/A/C visible on crop) → which folder maps to which letter — TBD via phase D corner-letter verification

## usage notes

- always reference walls by feature name (window-wall, frosted-wall, closet-wall, entrance-wall) — this room differs from room-1/room-2 because the AC and large sliding window share the same wall, so there's no separate "ac-wall" name
- corners are alphabetical wall pairs (corner-closet-entrance, not corner-entrance-closet)
- this is the **first 6帖 room mapped** (room-1, room-2 were 4.5帖). different size + layout than the top-row 4.5帖 rooms
- this is the **first 3-camera room** (room-1, room-2 had 4 corners) — the 4th corner is skipped per the photo capture
- for 3D reconstruction in phase D, build the 4-corner geometry but only place 3 panorama cameras
- material sampling from photos:
  - whitewashed wood-plank ceiling: every frame
  - light maple plank floor: every frame
  - taupe-grey wall paint: every frame
  - large curtained sliding window + AC unit: `b/01` (far wall behind bed)
  - narrow vertical frosted window: `a/01` (far-right), `b/01` (camera-left)
  - dark wood + black metal shelving: `c/01` (foreground left)
  - iron-frame bed (dark wood + iron, different from room-2): `a/01` (right side), `b/01` (foreground)
  - coat rack on entrance-wall: `a/01` (left wall), `c/01` (right wall)
  - rattan pendant light: `b/01` (top-right)
- image paths:
  `interior-images/room-3/<a|b|c>/room-3-<a|b|c>-NN.webp`
- this room follows a different layout from room-1/room-2 (window+AC same wall instead of separate). phase D will use bespoke geometry, not the room-1 inline 3D code template
