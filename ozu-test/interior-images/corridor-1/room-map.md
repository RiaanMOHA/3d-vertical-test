# corridor-1 map (1F 廊下 + 玄関 transit space)

## overview

`corridor-1` is the 1F transit space — covers the **玄関 (genkan, 1.62 ㎡)** at the north end (front door + coat hooks) and the **廊下 (corridor, 2.43 ㎡)** strip running south to the LDK opening. The user's photo folder bundles both zones together since the genkan has no separate folder.

⚠ **Capture-rule note (didi's target, not yet on disk):** the eventual plan per memory rule `project_ozu_1f_corridor_rules.md` is to replace the 4-viewpoint a/b/c/d with a leaner 2-viewpoint capture (`pano-a` + `pano-a2`). Until those re-shoots arrive, this map describes the on-disk 4-viewpoint set.

approximate dimensions from blueprint:
- combined transit space: ~4.05 ㎡ (1.62 genkan + 2.43 corridor)
- corridor proper: ~900 mm wide (E-W) × ~2,700 mm long (N-S)
- genkan: ~1,800 × 900 mm (or similar) at the north end, with the front door on the north exterior wall

assumed (to confirm in phase D):
- ceiling: flat warm off-white painted finish (matches laundry / toilet ceiling)
- floor: light oak plank (continues into all adjacent rooms)
- genkan walls: plain taupe-grey paint
- corridor east wall: brick-pattern wallpaper accent (matching laundry's vanity-wall)
- corridor west wall: plain taupe + white folding closet/door panels

## walls

(walls are described for the combined space; the genkan + corridor form an L-ish shape, so the "4 walls" below are the bounding-box approximation, not literal continuous surfaces.)

### entry-wall (north)
- exterior wall at the genkan's north end
- front door (玄関ドア) — full-height steel/wood door with glass slit/panel; opens to the porch (ポーチ)
- 3-hook coat-rack mounted on the genkan's interior face (taupe paint section)
- single coat hook on a side wall near the front door (small accent)
- opposite: ldk-wall

### ldk-wall (south)
- interior boundary at the corridor's south end
- this is more an OPENING into the LDK than a solid wall — the corridor opens directly into the LDK on its south side
- the actual structural wall on this boundary contains the LDK doorway (no door panel — open archway) plus partitions for the closet (クローゼット) and storage (物入)
- opposite: entry-wall

### bath-wall (east)
- east wall of the combined transit space
- corridor section (south of the genkan): **brick-pattern wallpaper** accent, full ceiling-to-floor
- genkan section (north): plain taupe paint
- contains doors on the east side from the corridor into the wet rooms — the laundry door (`laundry`'s bath-wall west face) is on the corridor's east wall at the south end of the wet-room block
- opposite: stairs-wall

### stairs-wall (west)
- west wall of the combined transit space
- corridor section: white folding/sliding closet doors (storage 物入 + クローゼット alcoves) + the toilet door (toilet-1-f's door-wall outside face) + the stair shaft entry
- genkan section: plain taupe; the genkan storage (玄関収納) closet bi-folds open here
- opposite: bath-wall

## adjacencies

- entry-wall meets bath-wall and stairs-wall
- ldk-wall meets bath-wall and stairs-wall
- bath-wall meets entry-wall and ldk-wall
- stairs-wall meets entry-wall and ldk-wall

## corners

| corner id | walls meeting | notes |
|---|---|---|
| corner-bath-entry | bath-wall × entry-wall | NE; genkan east + front-door zone |
| corner-bath-ldk | bath-wall × ldk-wall | SE; corridor south end + brick + laundry south door |
| corner-entry-stairs | entry-wall × stairs-wall | NW; genkan west + genkan storage closet |
| corner-ldk-stairs | ldk-wall × stairs-wall | SW; corridor south end + stair shaft + closet alcove |

corner ids list walls in alphabetical order.

## room layout (top-down)

```
                       entry-wall (front door + 3-hook rack)
       ┌───────────────────────────────────────────────────┐
       │ [front      [3-hook                               │
       │  door]       coat rack]                           │
       │              ───────── (genkan zone) ──────────   │
       │ [genkan                                           │
       │  storage]                            [single hook]│
   stairs                                                   bath
   wall  ──── corridor proper (brick on east) ─────         wall
       │                                                   │ (brick)
       │ [toilet                              [laundry     │
       │  door]                                door]       │
       │                                                   │
       │ [closet       [closet         [LDK opening]       │
       │  doors]        alcove]                            │
       └───────────────────────────────────────────────────┘
                       ldk-wall (LDK archway south)
```

## camera-position mapping

⚠ tentative — full sweep verification pending in phase D. annotated-jpeg letter colors at this resolution are too small to definitively assign each camera; mapping below derived from first-frame photo content.

| current path | likely corner | photo evidence |
|---|---|---|
| `corridor-1/a/` | corner-entry-stairs (NW) | `a-1` shows 3-hook coat rack on a taupe wall + doorframe edge on the right (likely the genkan-storage door visible to camera-right) — consistent with NW genkan corner |
| `corridor-1/b/` | corner-ldk-stairs (SW) | `b-1` shows the front door across a moderate depth (looking N through the entire transit space) + a single coat hook on a taupe wall on the right — consistent with the corridor's south-west corner looking north |
| `corridor-1/c/` | corner-bath-ldk (SE) | `c-1` shows brick on the right + folding doors on the left + view N along the corridor toward the laundry sink (visible at far end) — consistent with SE corner facing N |
| `corridor-1/d/` | corner-bath-entry (NE) | `d-1` shows brick on the left + folding closet doors on the right — consistent with NE corner facing S |

## panorama sweep direction

clockwise from above (per room-1 convention). sequence 01 starts the sweep, highest number ends it.

## fixture / feature anchors

- **front door (玄関ドア)**: on entry-wall, slightly west of centre (best estimate)
- **3-hook coat rack**: in the genkan zone, mounted on a wall — likely entry-wall or stairs-wall (north section); needs full-sweep verification
- **single coat hook**: in the genkan zone, mounted on bath-wall (taupe section, north of where the brick starts)
- **brick accent wallpaper**: full bath-wall (east), corridor section only — does not extend into the genkan; floor to ceiling
- **toilet door**: on stairs-wall (west, corridor section, north end) — opens into toilet-1-f
- **laundry door**: on bath-wall (east, corridor section, north end) — opens into the laundry (the door we noted earlier as the laundry's door-wall outside face)
- **stair shaft entry**: on stairs-wall (west, corridor section, south end)
- **storage closet (物入) door**: on stairs-wall (west, corridor section, mid-south)
- **LDK opening**: ldk-wall (south), open archway

## folder structure (current — letter-coded)

```
corridor-1/
├── room-map.md          (this file)
├── room-map-photos.md   (photo→wall index)
├── a/   (19 images — corner-entry-stairs sweep, tentative)
├── b/   (19 images — corner-ldk-stairs sweep, tentative)
├── c/   (21 images — corner-bath-ldk sweep, tentative)
└── d/   (29 images — corner-bath-entry sweep, tentative)
```

## proposed rename

**deferred** until either (a) didi's `pano-a` + `pano-a2` re-shoots arrive (in which case rename + reshape the folder to that 2-viewpoint structure), or (b) the user confirms the 4-corner mapping above and we rename `a/b/c/d` to `corner-X-Y/`.

## unverified items

- exact transit-space dimensions (read from blueprint at 400 dpi; phase C will measure precisely)
- precise extent of the brick accent (does brick start exactly at the genkan-corridor opening, or further into the corridor?)
- which wall the 3-hook coat rack is mounted on (entry-wall vs stairs-wall north section)
- camera positions for `a` / `b` / `c` / `d` (the photo-content reading above is plausible but not confirmed via annotated letters at this resolution)
- door types for the toilet, laundry, LDK openings (phase E)
- ceiling height (assumed 2.4 m to match the rest of 1F)
- whether the genkan has its own step-down (土間) or is at the same floor level (Japanese houses typically step down ~150 mm at the genkan; phase D photo review)
- **didi's eventual capture-plan target: 2 viewpoints (`pano-a` + `pano-a2`).** the current 4-viewpoint a/b/c/d folders will be replaced when those re-shoots land. until then, build from a/b/c/d.

## usage notes

- always reference walls by feature name (entry-wall, ldk-wall, bath-wall, stairs-wall)
- corners are alphabetical wall pairs (corner-bath-entry, not corner-entry-bath)
- this is the **first non-rectangular room** mapped — the 4-corner template is a bounding-box approximation; the actual transit space is L-shaped (genkan at the north opens off the corridor's main strip)
- material sampling from photos:
  - genkan taupe paint + 3-hook coat rack: `corridor-1/a/01`
  - front door + single coat hook: `corridor-1/b/01`
  - brick accent wallpaper: `corridor-1/c/01` (right side) and `corridor-1/d/01` (left side)
  - white folding closet panels: `corridor-1/d/01` (right side)
  - hardwood floor: every photo
- image paths:
  `interior-images/corridor-1/<a|b|c|d>/corridor-1-<a|b|c|d>-NN.webp`
- when phase D rebuilds this scene, expect didi's pano-a + pano-a2 plan to supersede the 4-viewpoint set; build the geometry once and swap the camera plan separately
