# room-2 map (= 洋室3, NE 2F room)

## overview

room-2 is the **NE 2F room (洋室3)**, 4.5 帖, 2.7 × 2.7 m per blueprint. Simple rectangular room following the room-1 wall-naming template (ac / window / closet / entrance), with `closet` replacing `cabinet` to reflect a built-in bi-fold closet rather than a freestanding cabinet.

approximate dimensions:
- width: 2.7 m
- depth: 2.7 m
- footprint: 7.29 ㎡ (4.5 帖) per blueprint
- ceiling: whitewashed wood-plank (matches the 2F room + corridor convention)
- floor: light maple plank (matches the 2F room + corridor convention)
- walls: warm taupe-grey paint

## walls

### window-wall
- **exterior wall**, facing the back/side of the house
- large sliding window (引違 / hikichigai) with cream-coloured curtains and tieback
- main daylight source for the room
- opposite: closet-wall

### ac-wall
- **exterior wall**, facing a different exterior side (corner of the room with window-wall)
- wall-mounted Toshiba AC unit, high on wall (visible in `corner-ac-closet/01`)
- narrow vertical frosted privacy window (縦すべり / tatesuberi, type 02609 per blueprint, FL+2000)
- opposite: entrance-wall

### closet-wall
- **interior partition**, opposite the window-wall
- 4-panel white bi-fold closet doors with chrome handles (visible in `corner-closet-entrance/01`)
- closet built-in, full-height
- bed head rests against this wall (under the closet doors)
- opposite: window-wall

### entrance-wall
- **interior partition**, opposite the ac-wall, faces interior corridor
- single hinged white door (開き) opens inward from the 2F corridor (verify swing direction in phase E from blueprint arc)
- multi-hook coat rack on the interior face of the entrance-wall (visible in `corner-entrance-window/01` — cross-confirmed via `corridor-2-toilet-2-f/b/01`)
- AC remote control panel + light switch panel mounted on entrance-wall near the door
- opposite: ac-wall

## adjacencies

- window-wall meets ac-wall and entrance-wall
- closet-wall meets ac-wall and entrance-wall
- ac-wall meets window-wall and closet-wall
- entrance-wall meets window-wall and closet-wall

## corners

| corner id | walls meeting | notes |
|---|---|---|
| corner-ac-closet | ac-wall × closet-wall | foot of bed against ac-wall + closet bi-fold corner; AC unit mounted on ac-wall near this corner |
| corner-ac-window | ac-wall × window-wall | exterior corner of the room (both walls are exterior); narrow vertical frosted window is on ac-wall just past this corner; tall vertical freestanding piece (TBD — wardrobe / shelving) sits at this corner |
| corner-closet-entrance | closet-wall × entrance-wall | head of bed at this corner; closet bi-folds run along closet-wall from this corner toward corner-ac-closet |
| corner-entrance-window | entrance-wall × window-wall | desk + chair sit at this corner; door opens into the room from this corner area; coat rack on entrance-wall just past this corner |

corner ids list walls in alphabetical order (room-1 convention).

## room layout (top-down, with compass orientation: window-wall=N, ac-wall=E, closet-wall=W, entrance-wall=S)

⚠ **KNOWN INCONSISTENCY — flagged 2026-05-11** ⚠

This compass mapping (window=N, ac=E, closet=W, entrance=S, taken from `blueprints/global-coords.md`) **disagrees with the existing folder/corner naming on disk and with the room-2 runtime build in `ozu-test.html`**:

- `global-coords.md` says: window↔entrance are opposite walls (N↔S, z axis), ac↔closet are opposite walls (E↔W, x axis). The 4 corners should then alphabetically be: corner-ac-entrance, corner-ac-window, corner-closet-entrance, corner-closet-window.
- **The actual folders on disk are:** corner-ac-closet, corner-ac-window, corner-closet-entrance, corner-entrance-window. Two of these (`corner-ac-closet`, `corner-entrance-window`) cannot exist as corners under the compass above — they pair walls that are supposed to be opposite.
- The room-2 runtime build (`ozu-test.html` `registerScene('room-2')`) is consistent with the folder names: closet at x=0 / window at x=RW (opposite), entrance at z=0 / ac at z=RD (opposite). I.e. window↔closet pair and ac↔entrance pair.
- The handoff `handoff-2026-05-11-130507.md` flagged this as "room-map compass diagram is internally inconsistent — corner list + photos are correct" and built room-2 against the folder names / runtime convention.

**Resolution required from user:** either the global-coords.md wall assignments for room-2 are wrong (two walls mis-identified), or the on-disk folder names mis-pair walls that are actually opposite. Until resolved, runtime code follows the folder-name convention (window↔closet opp, ac↔entrance opp) because that's what the photo evidence supports. Trust the corner list + folder names + photos over the compass diagram below.

```
                       window-wall  (large sliding window + curtains)
       ┌─────────────────────────────────────────┐
       │ [tall freestanding piece]    [desk      │
       │ [vertical column]             + chair]  │
       │                                         │
   ac  │                                         │  closet
   wall│           room-2                        │   wall
  [AC ]│       (4.5 帖, 2.7 × 2.7)               │ [bi-fold
  [vrt│                                          │  closet
   win │                                         │  doors]
   ow] │      [bed (head→closet, foot→ac)]       │
       │                                         │
       │ [coat rack]                  [AC remote │
       │ [hinged door from corridor]   + switch] │
       └─────────────────────────────────────────┘
                       entrance-wall  (corridor side)
```

(in the layout above, the bed is shown horizontally for clarity — actual bed orientation may be slightly different. phase D will lock in furniture coords.)

## camera-position mapping

confirmed by folder names (room-2 has already been renamed to the corner-X-Y convention). photo evidence verifies content per corner:

| folder | corner | sweep start (frame 01 wall) | photo evidence summary |
|---|---|---|---|
| corner-ac-closet/ | ac-wall × closet-wall | ac-wall (AC unit visible ahead) | 9 images. `01` shows AC + curtained window on left + bed foot in foreground |
| corner-ac-window/ | ac-wall × window-wall | ac-wall (or window-wall) | 8 images. `01` shows freestanding tall vertical piece on left + small narrow window on right + desk + chair foreground |
| corner-closet-entrance/ | closet-wall × entrance-wall | closet-wall (bi-folds visible ahead) | 8 images. `01` shows bi-fold closet doors on far wall + bed head + small high vertical white window on far-left |
| corner-entrance-window/ | entrance-wall × window-wall | entrance-wall (door visible ahead) | 10 images. `01` shows open door + corridor + view into another room + desk + chair on right + coat rack on left |

⚠ camera positions are LOCKED by folder names — these match the room-1 4-corner template. phase D photo-by-photo verification will confirm sweep directions and assign each frame's exact orientation.

## panorama sweep direction

clockwise from above (per room-1 convention). sequence 01 starts the sweep, highest number ends it.

## furniture anchors

- **single bed (iron frame)**: long axis runs from ac-wall to closet-wall; head against closet-wall (under bi-fold doors), foot toward ac-wall. iron frame with carved/decorative posts at the foot, white painted. cream / blush bedding with pink pillow at the foot end.
- **desk + chair**: at corner-entrance-window. white desk top, light wood / metal frame. orange/tan leather-seat office chair with rolling base.
- **tall freestanding vertical piece**: at corner-ac-window. taupe-painted, narrow tall column shape. wardrobe / shelving / cabinet — function TBD (phase D)
- **coat rack**: on entrance-wall, mounted high on the wall near the door. dark/black multi-hook strip mounted on a wood backing
- **AC remote panel + light switch**: on entrance-wall near the door (right side as you enter)
- **wall-mounted AC unit (Toshiba)**: high on ac-wall, near corner-ac-closet
- **ceiling light**: assumed centred ceiling pendant or downlight (not directly sampled in `01` frames — phase D)

## folder structure (current — already renamed to corner convention)

```
room-2/
├── room-map.md                  (this file)
├── room-map-photos.md           (photo→wall index)
├── room-2-map.md                (existing legacy file — DO NOT READ per memory rule `feedback_only_named_reference.md`)
├── corner-ac-closet/             (9 images — start frame at ac-wall pointing toward AC unit)
├── corner-ac-window/             (8 images — exterior corner, both walls exterior)
├── corner-closet-entrance/       (8 images — start frame at closet-wall pointing at bi-folds)
└── corner-entrance-window/       (10 images — start frame at entrance-wall pointing at door)
```

## proposed rename

**not needed** — folder names already follow the corner-X-Y convention. files are named `room-2-corner-X-Y-NN.webp` format.

## unverified items

- exact compass orientation locked in: window-wall=N, ac-wall=E, closet-wall=W, entrance-wall=S (per `blueprints/global-coords.md`)
- exact dimensions (2.7 × 2.7 read from blueprint at 400 dpi; not site-measured)
- ceiling height (assumed 2.4 m to match other 2F rooms)
- the tall freestanding vertical piece at corner-ac-window — wardrobe? shelving? bulkhead? phase D to identify from mid-sweep frames
- door type — currently described as "hinged 開き" based on `corner-entrance-window/01`; re-confirm via blueprint arc in phase E
- exact swing direction of the entrance door (into closet-wall side vs into ac-wall side) — phase E
- exact placement of the closet bi-fold doors along closet-wall (full-wall bi-folds vs partial)
- exact placement of the AC unit and the narrow vertical frosted window along ac-wall
- whether there are wall-mounted decor items (artwork, mirrors, etc.) — none visible in frame-01 of any corner; phase D to confirm
- ceiling light type (pendant vs downlight vs flush) — not visible in sampled frames

## usage notes

- always reference walls by feature name (window-wall, ac-wall, closet-wall, entrance-wall), never by direction or coord
- corners are alphabetical wall pairs (corner-ac-closet, not corner-closet-ac)
- the parent folder of each image set IS its corner id (already renamed); the containing folder path tells you which corner the camera is in
- when placing a camera in the 3D scene, use the corner id to position it and the sweep direction (clockwise from above) to orient it
- for wall texture mapping, each panorama sweep covers exactly two adjacent walls (the two walls named in its corner id), with the remaining two walls visible in the middle of the sweep
- material sampling from photos:
  - whitewashed wood-plank ceiling: every corner frame-01
  - light maple plank floor: every corner frame-01
  - taupe-grey wall paint: every frame
  - large curtained sliding window: `corner-ac-closet/01` (left side)
  - narrow vertical frosted window (small): `corner-ac-window/01` (right side), `corner-closet-entrance/01` (far-left)
  - white bi-fold closet doors: `corner-closet-entrance/01`
  - Toshiba AC unit: `corner-ac-closet/01`
  - iron-frame bed: `corner-ac-closet/01` (foot), `corner-closet-entrance/01` (head)
  - desk + orange chair: `corner-entrance-window/01`, `corner-ac-window/01`
  - coat rack on entrance-wall: `corner-entrance-window/01` (interior side); also visible from corridor in `corridor-2-toilet-2-f/b/01`
- image paths:
  `interior-images/room-2/<corner-folder>/room-2-<corner-folder>-NN.webp`
- this room is structurally analogous to room-1 (room-1 is the NW mirror at 洋室2). the cabinet/closet naming difference reflects room-2's built-in bi-fold doors vs room-1's freestanding cabinet — phase D will use the room-1 inline 3D code as a structural starting point, with the mirror flip applied
