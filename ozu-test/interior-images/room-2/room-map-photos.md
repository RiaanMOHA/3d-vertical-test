# room-2 photo → wall index

companion to `room-map.md`. lists which photos from each corner sub-folder show each wall and feature of room-2 (= 洋室3, NE 2F room, 4.5 帖, 2.7 × 2.7).

⚠ 4 frames sampled so far (one per corner, frame 01 of each sweep). per-frame position assignment for the remaining 31 frames deferred to phase D.

## wall visibility (from sampled corner-01 frames)

### window-wall (exterior, large sliding window with curtains)

| current path | image numbers | notes |
|---|---|---|
| corner-ac-closet/ | 01 | curtained large window visible on the camera's left when sweep points at ac-wall |
| corner-entrance-window/ | 01 | window-wall is one of the two adjacent walls at this corner; large window not directly seen in 01 (frame points at corridor through entrance door) |

best window-wall reference: `corner-ac-closet/01` (curtain + tieback clearly visible on left side of frame). diagonally-opposite corner, so the window is at distance and on the side.

### ac-wall (exterior, Toshiba AC + narrow vertical frosted window 縦すべり 02609)

| current path | image numbers | notes |
|---|---|---|
| corner-ac-closet/ | 01 | AC unit clearly visible on the wall ahead (Toshiba branding visible); ac-wall is the start-of-sweep wall at this corner |
| corner-ac-window/ | 01 | small narrow window on the right side of frame is the 縦すべり 02609 frosted window on ac-wall |

best AC-unit reference: `corner-ac-closet/01` (clear Toshiba unit, ceiling cornice line visible). best narrow-window reference: `corner-ac-window/01` (curtained smaller window on right side of frame).

### closet-wall (interior, white bi-fold closet doors)

| current path | image numbers | notes |
|---|---|---|
| corner-closet-entrance/ | 01 | closet bi-fold doors visible directly on the far wall (4-panel white doors with chrome handles); bed head visible in foreground |
| corner-ac-closet/ | 01 | closet-wall is the other adjacent wall at this corner; not directly visible in the frame-01 sweep start (which points at ac-wall) |

best closet-wall reference: `corner-closet-entrance/01` (clean bi-fold doors with handles).

### entrance-wall (interior, single hinged door from corridor + coat rack)

| current path | image numbers | notes |
|---|---|---|
| corner-entrance-window/ | 01 | open white door + view through corridor into another room (likely room-1 or room-3); coat rack on near wall (entrance-wall side) |
| corner-closet-entrance/ | 01 | entrance-wall is one of the two adjacent walls at this corner; door not directly visible in 01 (frame likely points at closet-wall) |

best entrance-door reference: `corner-entrance-window/01` (door open, hinge visible, view to corridor + neighboring room).

## furniture / fixtures (per sampled frames)

### single iron-frame bed (head against closet-wall, foot toward ac-wall side)

| frame | content | notes |
|---|---|---|
| corner-ac-closet/01 | bed foot visible bottom-right with pink pillow | foot end of the bed |
| corner-closet-entrance/01 | bed head + headboard against the closet bi-fold doors | head end of the bed |

bed orientation: head against closet-wall, foot toward ac-wall. iron-frame bed with carved/decorative posts at the foot. white headboard. cream / blush bedding.

### desk + chair (against window-wall or near corner-entrance-window)

| frame | content | notes |
|---|---|---|
| corner-ac-window/01 | white desk top + foot of orange leather-seat chair | desk near corner-ac-window |
| corner-entrance-window/01 | white desk + orange leather chair on the right side of frame | confirms desk-and-chair are near the entrance-window corner |

best desk-chair reference: `corner-entrance-window/01` (full chair visible, desk top visible with edge profile).

### tall freestanding cabinet / wardrobe (near corner-ac-window)

| frame | content | notes |
|---|---|---|
| corner-ac-window/01 | tall taupe-painted vertical freestanding piece on left side of frame; could be a tall narrow wardrobe or shelving column | not yet identified — phase D to confirm material/function |

### coat rack (on entrance-wall, near the door)

| frame | content | notes |
|---|---|---|
| corner-entrance-window/01 | wall-mounted dark hook strip with multiple hooks visible on the left wall (entrance-wall side) | matches the iron coat-rack seen from the corridor side in `corridor-2-toilet-2-f/b/01` |

cross-reference: this is the same coat rack visible from outside the room in `corridor-2-toilet-2-f/b/01` (from the corridor camera looking through room-2's open door).

### AC remote control panel + light switch panel (on entrance-wall, near door)

| frame | content | notes |
|---|---|---|
| corner-entrance-window/01 | white wall-mounted control panel + small switch beside it on the right of frame near the door | AC remote holder + room light switch |

## ceiling and floor

| frame | content | notes |
|---|---|---|
| every frame | whitewashed wood-plank ceiling clearly visible at top — distressed/aged look | matches the rest of 2F (corridor + other rooms) |
| every frame | light maple plank floor visible at bottom | matches the rest of 2F |

## what this confirms

- room-2 is a 4-corner rectangular room (4.5 帖, ~2.7 × 2.7 m) with the room-1 wall-naming template (ac / window / closet / entrance) — confirmed by the 4 sub-folder corner names matching the room-1 convention.
- the closet on closet-wall is a built-in white bi-fold doors closet (4-panel white doors with chrome handles).
- the bed runs along the ac-wall direction with head against closet-wall and foot at ac-wall side — same as room-1's bed orientation pattern.
- the desk + chair are near the corner-entrance-window (corner formed by entrance-wall meeting window-wall).
- the coat rack on entrance-wall matches the one visible from the corridor side in the `corridor-2-toilet-2-f/b/01` photo (cross-folder feature confirmation).
- the AC unit is wall-mounted high on ac-wall, near the corner with closet-wall (since corner-ac-closet/01 frame-01 shows the AC ahead).

## what's still TENTATIVE / TBD

- compass orientation (which named wall corresponds to N/S/E/W). most likely (mirror of room-1):
  - window-wall = N (exterior, large sliding window — matches blueprint 引違 11909 placement)
  - ac-wall = E (exterior, AC + narrow vertical frosted window — matches blueprint 縦すべり 02609 placement on east side)
  - entrance-wall = S (interior, corridor side; most likely matches the 2F corridor's east arm / north arm geometry)
  - closet-wall = W (interior partition with the 2F toilet + stair shaft area)
  - phase C will lock this in once the global coords are reconciled
- the tall vertical taupe-painted piece in `corner-ac-window/01` (left of frame) — wardrobe? shelving? wall column? phase D to confirm
- exact furniture coords (the 4 frame-01 photos give corner positions; the remaining 31 frames will give precise furniture orientation)
- door type for the entrance door — appears hinged 開き from `corner-entrance-window/01`; re-confirm via blueprint arc in phase E
- existence of any wall-mounted decor (artwork, mirrors, etc.) — sampled frames don't show any prominent decor; phase D to confirm

## file path pattern

each entry corresponds to a file at:

`interior-images/room-2/<corner-folder>/room-2-<corner-folder>-NN.webp`

example: AC unit reference, frame 01 of corner-ac-closet:
`interior-images/room-2/corner-ac-closet/room-2-corner-ac-closet-01.webp`
