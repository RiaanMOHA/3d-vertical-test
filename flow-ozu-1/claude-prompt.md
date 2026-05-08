# Claude prompt: build a new property using the Ozu-1 flow

> Hand this prompt to Claude Code in a new project folder along with the property's blueprint and panoramas. Claude reads this, reads the flow docs in the same folder, and executes the build. The user reviews after each phase.

## What you (Claude) are doing

You are building a 3D web reconstruction of a real residential property using the same flow that produced the Ozu-1 build. The flow is documented in three sibling files in this folder:

- `flow-ozu-1-full.md` — the end-to-end story plus the master recipe
- `flow-ozu-1-layout.md` — placement and geometry recipe
- `flow-ozu-1-rendering.md` — materials and lighting recipe

Plus two sub-procedures in this folder:

- `blueprint-reading.md` — how to extract room bounds, windows, and doors from a blueprint PDF
- `furniture-placement.md` — how to translate panorama observations into 3D positions

Read all five before you start coding. Then execute the master recipe in `flow-ozu-1-full.md`.

## What the user will give you

A folder at the project root containing:

- `<property-name>/blueprints/<property-name>-blueprint.pdf` — the dimensional source of truth
- `<property-name>/interior-images/<room-name>/corner-<corner-id>/*.webp` — corner panoramas, one folder per room corner
- `<property-name>/exterior-images/*.webp` — front-facade photos

If any of these are missing, stop and ask. Do not improvise paths.

## Phase 0: scaffold the file

1. Copy `ozu-test.html` (the Ozu-1 production file) to `<property-name>.html` at the project root.
2. Inside the new file, find every `registerScene(...)` block. Empty out the contents of each `build()` callback, leaving the registration shell.
3. Empty out every per-property data array: `F1_WIN_FRONT`, `F1_WIN_RIGHT`, `F1_WIN_LEFT`, `F1_WIN_BACK`, `F2_WIN_FRONT`, `F2_WIN_RIGHT`, `F2_WIN_LEFT`, `F2_WIN_BACK`, the rooms array, the floors array, `F1_DOORS`, `F2_DOORS`, the chip viewpoints array.
4. Keep all helper functions (`wallX`, `wallZ`, `addDoor`, `addRoomTrim`, `addRoomPaint2F`, `solidWall`, `paneFront`, `paneSide`, `addWinFlex`, `buildRoom1EnvMap`, etc).
5. Keep all material constants (`wallMat`, `trimMat`, `doorMat`, `closetDoorMat`, `matToilet`, `matLower`, `matUpper`, `FLOORS`).
6. Keep the renderer setup, the orbit controls, the chip-navigation tool, the post-processing pipeline switch.
7. Update the property width (`W`) and depth (`D`) constants from the blueprint.
8. Hard reload. The page should load empty (no walls, no rooms, just an empty 3D space). If it crashes, fix the helper imports before continuing.

Stop and check with the user before moving on.

## Phase 1: docs

Follow steps 1 to 5 of the master recipe in `flow-ozu-1-full.md`. Outputs:

- `<property-name>/blueprints/global-coords.md`
- `<property-name>/blueprints/room-identity.md`
- One `<property-name>/interior-images/<room>/room-map.md` per room
- `<property-name>/master-plan.md`

For each room map: walk the corner panoramas, name each visible wall by its dominant feature (window-wall, ac-wall, cabinet-wall, entrance-wall), match the corner folder names exactly.

Stop and check with the user.

## Phase 2: layout

Follow `flow-ozu-1-layout.md` end to end. Use `blueprint-reading.md` to extract dimensions. Use `furniture-placement.md` to position furniture.

Build in this order:

1. Property width and depth. Outer wall geometry (one builder feeding both exterior and interior scenes).
2. Window arrays (`F1_WIN_*`, `F2_WIN_*`). Inline-comment with blueprint codes.
3. Wall cuts around each window hole (4 segments per window).
4. Sill bands and header bands above and below each hole.
5. Rooms array. Floors array.
6. Inner-wall doors. Wall cuts for each door.
7. Ceilings (one sweep across all rooms).
8. Stairs if any. Top-of-stair parapet if any guard gap.
9. Furniture per room, one piece at a time. Hard-reload and visually verify against the panorama after each piece.
10. Trim (`addRoomTrim`) for clean rectangular rooms.
11. Chip viewpoints. One per room. Id, label, parent match folder names exactly.

Stop and check after each room is fully placed.

## Phase 3: rendering

Follow `flow-ozu-1-rendering.md` end to end.

Build in this order:

1. Confirm shared materials (`wallMat`, `trimMat`, `FLOORS.*`) are sensible for this property's photos. Adjust the colour codes if needed.
2. Apply ACES filmic tone mapping globally. Start at exposure 1.0, tune from there. If cream walls blow out white, drop to 0.55.
3. Bake a procedural PMREM env map. Assign as `scene.environment` on every scene.
4. Turn on interior shadows. `DirectionalLight.castShadow = true`. Every solid mesh casts and receives. Add a `HemisphereLight` for sky/floor bounce.
5. Upgrade ceramics (`matToilet`) to `MeshPhysicalMaterial` with `clearcoat: 1.0, clearcoatRoughness: 0.05`.
6. Apply the procedural whitewashed wood-plank ceiling texture if applicable.
7. Place warm-white `PointLight`s at major windows for daylight.
8. Walk every wall, accent surface, and fixture against the panoramas. Make a list of mismatches. Fix one at a time.
9. Trim layer (off-white `trimMat`) on door casings, baseboards, crown moulding.
10. Per-room wall-paint overlays where the global `wallMat` doesn't match.
11. Front-door rebuild if the placeholder is too generic.
12. (JP-residential properties only) smoke detectors on bedroom ceilings and stair tops.

Stop and check after each step. Hard reload between every step. No batching.

## Acceptance criteria per step

For each step in phases 1, 2, and 3, the acceptance test is the same: open the chip viewpoint for the relevant room, screenshot the 3D view, place the corresponding panorama next to it, judge whether the 3D matches the photo within a clear margin. If yes, move on. If no, tune the most recent change until it does.

If you can't decide, screenshot both and show the user.

## Strict rules

- Read all five docs in this folder before writing any code.
- Hard reload after every step. No batching.
- Pause for user review at every phase boundary.
- Plain language status reports — no dev jargon unless the user is technical and asked for it.
- One thing at a time. Never bundle "fixed walls and added trim" into one report; they are two changes.
- Source-of-truth hierarchy: blueprint at high resolution wins over photos. Photos win over room maps. Room maps win over existing 3D code. Memory rules win over default behaviour. Never eyeball.
- If a step in the recipe is JP-residential-specific (smoke detectors, genkan, taupe-grey bedroom paint, sliding 引違 doors), check whether the new property is also JP. If not, skip or adapt.
- If the new property is not JP, the rendering step 13 in `flow-ozu-1-rendering.md` (recolour conventions) needs adapting. Don't blindly apply the cool grey-white brick or warm wood-plank toilet floors; check what the photos actually show.

## Acknowledge before starting

Reply with:
1. The five docs you read.
2. The folder structure you observed (paths and counts).
3. The property width and depth you extracted from the blueprint.
4. The list of rooms you identified.
5. Any clarifications you need before Phase 0.
