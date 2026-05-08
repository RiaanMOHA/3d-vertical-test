# Sub-procedure: how to read a blueprint and extract dimensions

> Used by step 1 of `flow-ozu-1-full.md` and step 1 of `flow-ozu-1-layout.md`. The blueprint is the dimensional source of truth. This procedure says how to translate the PDF into the numbers the build needs.

## What you need to extract

By the end of this procedure you have, for the property:

- **Width (W)** and **depth (D)**: the property's outermost dimensions in metres.
- **Floor heights**: F1H (floor 1 ceiling height), F2H (floor 2 ceiling height). Standard JP residential: F1H = 2.5 m, F2H = 2.5 m.
- **Rooms**: for each room, `{ name, x1, z1, x2, z2, y1 (floor level), y2 (ceiling level) }` in metres.
- **Windows**: for each window, the wall it sits on, its `a` (start along the wall), `b` (end), `y0` (sill height), `y1` (header height), and the blueprint's window code (e.g. `引違 11909`).
- **Doors**: for each interior doorway, the wall axis (X or Z), the wall coordinate (`c`), the open range (`a` to `b`), and the door type (sliding, hinged, bi-fold, archway).
- **Other openings**: archways, corridor entries, structural columns, taupe column boxes if any.

## How to read a JP residential blueprint

1. Open the PDF. Look for the dimension scale or a printed scale bar. JP blueprints typically show dimensions in millimetres (e.g. `4105` means 4.105 metres).
2. Identify the cardinal orientation. JP blueprints usually have north pointing up. Confirm by looking for the front facade label or the entrance position.
3. Locate the dimensional grid. Most JP blueprints use a 910 mm or 1820 mm modular grid (the standard 半間 / 1間 unit). Each grid line is 0.910 m apart.
4. Read the property's outer dimensions. The total width (east-west) becomes `W`, the total depth (north-south) becomes `D`.
5. Confirm by reading two opposite walls and checking they match.

Convert to metres: divide millimetres by 1000. So `4105 mm` becomes `4.105 m`.

## How to extract a room

For each room labelled on the blueprint:

1. Identify the room's four bounding walls. Note which walls are also outer walls of the property (these are already built; you don't add them).
2. Read the room's bounds in metres. The convention for the project is south-west corner of the property at the origin, x runs east-west, z runs north-south.
3. Convert the room's bounds to `{ x1, z1, x2, z2 }`. `x1 < x2`, `z1 < z2`.
4. Read the floor level. Ground floor: `y1 = 0`, `y2 = F1H`. Second floor: `y1 = F1H`, `y2 = F1H + F2H`.
5. Write the entry: `{ name: '<room>', x1: <x1>, z1: <z1>, x2: <x2>, z2: <z2>, y1: <y1>, y2: <y2> }`.

## How to extract a window

For each window on an outer wall:

1. Identify which outer wall it sits on: front (z=D), right (x=W), left (x=0), back (z=0).
2. Identify the window's blueprint code. JP residential codes are typically `引違 NNNNN` (sliding two-panel) or `縦すべり NNNNN` (narrow vertical, often privacy). The 5-digit number encodes the size: first 2 digits are the width in 100s of mm, last 2 digits are the height in 100s of mm. So `11909` is 1190 mm wide and 900 mm tall.
3. Read the window's start position along the wall (`a`) and end position (`b`) in metres.
4. Read the sill height (the bottom of the window opening above the floor), `y0`. Standard JP residential: 1.10 m.
5. Read the header height (the top of the window opening above the floor), `y1`. Standard JP residential: 2.00 m for hikichigai, 1.90 m for narrow vertical.
6. Add the entry to the matching `F1_WIN_*` or `F2_WIN_*` array. Inline-comment with the room name and the blueprint code: `{ a: 4.105, b: 5.795, y0: 1.10, y1: 2.00 },  // room-1 引違 11909`.

For windows on inner walls (not common, but possible for example a borrowed-light window between rooms): treat the inner wall as the host and use the same shape.

## How to extract a door

For each interior doorway:

1. Identify which wall it sits on. Note the wall axis (X-axis if running east-west, Z-axis if running north-south) and the wall coordinate (`c` is the constant axis: for an X-axis wall, `c` is the z value; for a Z-axis wall, `c` is the x value).
2. Read the door's start (`a`) and end (`b`) along the wall in metres.
3. Identify the door type from the blueprint symbol:
   - Two short parallel lines with a curved arc: hinged (typical interior bedroom door).
   - A long slender rectangle on one or both sides: sliding (Japanese-style 引違).
   - A V or Z shape with two short panels: bi-fold (typical closet door).
   - No symbol, just an open break in the wall: open archway.
4. Add the door entry: `{ axis: 'X' | 'Z', c: <c>, a: <a>, b: <b>, mat: doorMat | closetDoorMat, type?: 'bi-fold' | 'sliding' }`. Hinged is the default; omit `type`. Inline-comment with the rooms it connects: `// room-1 ↔ closet`.
5. Add the matching wall cut: `wallX(c, a_wall_start, b_wall_end, [[door_a, door_b]], height, yBase)` or the `wallZ` equivalent.

## How to extract floor levels for split-level rooms

If the blueprint shows a step-down (e.g. genkan) or a step-up (e.g. raised tatami area):

1. Read the step height from the blueprint section view (a side-view diagram, usually on the second or third sheet).
2. Add the room's bounds with a corrected `y1` (floor level).
3. Build the step geometry as a small box bridging the two floor levels.

## How to handle ambiguity

- If two views of the blueprint disagree (plan view vs section view), the section view wins for vertical dimensions; the plan view wins for horizontal dimensions.
- If a room label is missing, name it by its function (e.g. `corridor-1`, `closet-room-2`) and confirm with the user.
- If the front-facade photo and the blueprint disagree on a window's position, the blueprint at high resolution still wins per the source-of-truth hierarchy. Note the photo discrepancy in the room map for later review.
- The user may confirm the blueprint X-mirror (front-facade is mirrored compared to the floor plan). Check carefully: don't assume the blueprint and photos look at the property from the same side.

## Output format

Write findings to two files:

`<property-name>/blueprints/global-coords.md`:

```markdown
# Global coordinates for <property-name>

## Constants
- W (width, east-west): <value> m
- D (depth, north-south): <value> m
- F1H (floor 1 ceiling height): <value> m
- F2H (floor 2 ceiling height): <value> m

## Room bounds (metres)

| Room | Floor | x1 | z1 | x2 | z2 | y1 | y2 |
|---|---|---|---|---|---|---|---|
| room-1 | 2F | 3.60 | 4.50 | 6.30 | 7.20 | 2.5 | 5.0 |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Outer wall windows (F1)

| Window | Wall | a | b | y0 | y1 | Code |
|---|---|---|---|---|---|---|
| LDK 1 | left | 1.20 | 1.46 | 1.00 | 1.90 | 縦すべり 02609 |
| ... | ... | ... | ... | ... | ... | ... |

## Outer wall windows (F2)

(same shape)

## Inner doorways (F1)

| Door | Axis | c | a | b | Type |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Inner doorways (F2)

(same shape)
```

`<property-name>/blueprints/room-identity.md`:

```markdown
# Room identity for <property-name>

| Room | Folder name | Function | Notable features |
|---|---|---|---|
| room-1 | room-1 | NW bedroom | sliding window front, narrow privacy window right, closet on west |
| ... | ... | ... | ... |
```

## Acceptance criteria

- All rooms in the blueprint appear in the table.
- Every dimension in the table can be cross-checked against the blueprint by visual inspection.
- The window codes match the blueprint labels exactly.
- The total of all room widths along an axis equals the property's W (or D) within ±0.05 m.
