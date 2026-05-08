# Claude prompt: build a single-room standalone sandbox using the room-1 flow

> Hand this prompt to Claude Code along with the room's panoramas. Claude reads this, reads the flow docs in the same folder, and executes the build. The user reviews after each phase. Use this when you want a cinematic single-room render isolated from any property file (PBR textures, refractive glass, post-processing pipeline, lamp toggle). For a whole property build, use `../flow-ozu-1/claude-prompt.md`.

## What you (Claude) are doing

You are building a standalone single-room 3D web sandbox using the same flow that produced the room-1 sandbox in Ozu-1. The flow is documented in three sibling files in this folder:

- `flow-room-1-full.md` — the end-to-end story plus the master recipe
- `flow-room-1-layout.md` — placement and geometry recipe
- `flow-room-1-rendering.md` — materials, lighting, glass, post-processing recipe

If the room is part of a property that you are also building separately, the property-level placement goes in the `interior` registerScene block of the property file; the standalone sandbox lives in its own `registerScene('<room-name>', ...)` block in the same file. The two never edit together.

## What the user will give you

A folder at the project root containing:

- `<property-name>/interior-images/<room>/corner-<corner-id>/*.webp` — corner panoramas, one folder per room corner. Typically 4 corners.
- A blueprint of just this room (or the whole property's blueprint).
- Optionally: PBR texture sets at `<property-name>/<room>-textures/<material-name>/` containing `<name>_diff.jpg`, `<name>_rough.jpg`, `<name>_nor_gl.jpg`.
- Optionally: an HDRI file at `<property-name>/hdri/*.hdr` for a real-photo env map.

If any of these are missing, stop and ask. Do not improvise paths.

## Phase 0: scaffold the registerScene block

1. Open the property file (e.g. `<property-name>.html`) or, if there is no property file, copy `ozu-test.html` to a new file at the project root.
2. Add a new `registerScene('<room-name>', ...)` block. The block has a `build()` callback that runs once per scene activation, plus a chip in the dock at the top.
3. Inside `build()`, set the camera position and target so the room is framed cleanly.
4. Hard reload. Click the chip. The page should switch to an empty 3D space with no walls.

Stop and check with the user.

## Phase 1: layout

Follow `flow-room-1-layout.md` end to end. The single-room version is simpler than a whole property because there is only one room.

Build in this order:

1. The four walls. For an isolated sandbox they are not on outer walls of any property, so build them as one box outline using `THREE.BoxGeometry` for each wall, or as four `THREE.PlaneGeometry` faces composed inside a `THREE.Group`. Assign the wall material later.
2. The floor.
3. The ceiling.
4. The window holes. For isolated sandbox use, you can either cut the wall geometry (more work, more realistic) or place the glass plane and the wall in front of each other separately. Cut walls give the right look from outside but the sandbox is meant to be viewed from inside.
5. The door, as either a `THREE.Group` for an openable hinged door or a flat plane for a closed entrance.
6. Each piece of furniture, one at a time, anchored to a specific wall. Use the standard piece dimensions in `../flow-ozu-1/furniture-placement.md`.

Stop and check after each piece.

## Phase 2: rendering

Follow `flow-room-1-rendering.md` end to end. This is where the sandbox earns its keep: the rendering should be more cinematic than the property-level rooms.

Build in this order:

1. ACES filmic tone mapping with exposure 0.55. Gate it so it only applies when the room is the visible scene.
2. Procedural PMREM env map via `buildRoom1EnvMap` (or write `build<RoomName>EnvMap` if the colour palette differs).
3. Anisotropy at the GPU's max on every PBR texture.
4. Window-direction directional sun, intensity 0.85, soft shadows radius 6. Cool-tinted fill, intensity 0.22, no shadows.
5. Walls and ceiling do not cast or receive shadows. Floor receives shadows.
6. The glass: refractive `MeshPhysicalMaterial` with transmission ~1.0, roughness ~0.05 for clear; transmission ~1.0, roughness 0.5 to 0.7 for frosted.
7. Backdrop planes outside each window, painted procedurally to suggest the surroundings.
8. Pendant lamps with linen-weave shades, brass hub, visible bulb spheres. Off by default. Add a Lights button toggle that flips the bulb emissive, the shade emissive, and the bloom enabled state.
9. The post-processing pipeline: `EffectComposer` with `RenderPass` then `UnrealBloomPass` then `SMAAPass`. Bloom enabled only when lamps are on. Inline the SMAA shader source (`SMAAEdgesShader`, `SMAAWeightsShader`, `SMAABlendShader`) or the pass crashes on construction.
10. The fixtures: AC unit, light switch, intercom, doorknob, coat hooks, curtains.
11. Wire any PBR texture sets from `<property-name>/<room>-textures/` via a small `loadPBR(name)` helper.
12. Test PBR on every surface but reject any set that doesn't match the photos.

Stop and check after each step. Hard reload between every step.

## What promotion to the property looks like

If a rendering experiment proves out in the sandbox and the user wants it in the rest of the property:

1. Confirm with the user that promotion is the goal.
2. Identify the smallest set of changes needed to bring the experiment to the `interior` and `exterior` registerScene blocks.
3. Make the changes once, in the property's master flow (`../flow-ozu-1/`), not by mass-editing.

The Ozu-1 ACES tone mapping and PMREM env map both started in the room-1 sandbox and were promoted to global in Phase 7.5 of the master plan.

## Acceptance criteria per step

For each step in phases 1 and 2, the test is: hard reload, click the room's chip, screenshot the 3D view, place the corresponding panorama next to it, judge whether the 3D matches the photo within a clear margin. If yes, move on. If no, tune the most recent change until it does.

For rendering steps where the comparison isn't a single photo (e.g. tone mapping, env map), the test is: visually compare against a reference render the user supplies, or against the existing room-1 sandbox if you're building a sibling.

## Strict rules

- Read all three flow docs in this folder plus the layout sub-procedures in `../flow-ozu-1/blueprint-reading.md` and `../flow-ozu-1/furniture-placement.md` before writing any code.
- Hard reload after every step. No batching.
- Pause for user review at every phase boundary.
- Plain language status reports.
- The sandbox is for cutting-edge / cinematic experiments. If the work is just "make a working 3D room", use the master property flow at `../flow-ozu-1/` instead.
- Memory rule: the standalone `registerScene('room-1', ...)` block in `ozu-test.html` is locked; do not edit it unless the user literally types "room-1". This rule applies to room-1 specifically; other rooms can have their own sandboxes without the lock.

## Acknowledge before starting

Reply with:
1. The five docs you read (three in this folder plus two sub-procedures in `../flow-ozu-1/`).
2. The folder structure you observed (paths and counts).
3. The room dimensions you extracted from the blueprint or panoramas.
4. The list of pieces of furniture you can identify from the panoramas.
5. Any clarifications you need before Phase 0.
