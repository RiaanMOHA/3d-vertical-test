# Glossary: terms used across the room-1 standalone flow docs

> One line per term, plain language. Referenced from every narrative doc in this folder. For the property-level glossary including JP-residential terms see `../flow-ozu-1/glossary.md`.

## Three.js terms

- **registerScene block:** a chunk of code inside `ozu-test.html` (or your property's HTML file) that defines one 3D scene. The Ozu-1 file has three: `exterior`, `interior`, and `room-1`. They share the file but are independent.
- **MeshStandardMaterial:** the everyday three.js material. Responds to light realistically. Three knobs that matter most: colour, roughness (0 = mirror, 1 = chalk), metalness (0 = plastic / wood, 1 = polished metal).
- **MeshPhysicalMaterial:** an upgrade of MeshStandardMaterial with extra knobs for transmission (light passes through), clearcoat (a glossy top layer), sheen.
- **transmission:** light passes through the material. Glass has high transmission. Frosted glass also has high transmission but high roughness.
- **clearcoat:** a thin glossy layer on top of the base material. Used for ceramic toilets and basins.
- **emissive:** the object glows on its own. Doesn't actually light other surfaces unless paired with a real light source.
- **anisotropy / anisotropic filtering:** a setting that keeps textures sharp at glancing camera angles. Without it, distant floor planks blur to mush.
- **PBR (physically based rendering):** materials that respond to light realistically, parameterised by roughness, metalness, and a handful of texture maps (colour, roughness, normal).
- **env map (environment map):** a 360-degree image used as the source of indirect light and reflections. Without one, metals look flat and dead.
- **PMREM:** the recipe three.js uses to convert any image into an env map.
- **EffectComposer:** the post-processing pipeline manager. Holds a list of passes. Each pass takes the previous pass's image and adds an effect on top.
- **RenderPass, UnrealBloomPass, SMAAPass, TAA:** kinds of passes. RenderPass draws the 3D. UnrealBloomPass adds glow around bright areas. SMAAPass smooths jagged edges. TAA is a smarter edge-smoother that averages multiple slightly-shifted snapshots.
- **post-processing pipeline:** effects layered on top of the rendered image after the 3D is drawn.

## Light types

- **DirectionalLight:** light from one direction, like the sun.
- **PointLight:** a single bright dot, like a bare bulb.
- **RectAreaLight:** a rectangle that emits light, like a window pane.
- **HemisphereLight:** a sky colour at the top and a ground colour at the bottom for general bounce-fill.

## Project-specific terms

- **F1_WIN / F2_WIN arrays:** the lists of windows for floor 1 and floor 2. Each entry has `a` (start along the wall in metres), `b` (end), `y0` (sill height in metres above the floor), `y1` (header height).
- **wallX, wallZ:** helper functions that build a wall along the X axis or the Z axis, with a list of openings to leave as holes. Argument order: `wallX(z, a, b, gaps, height, yBase, mat, outerSign)`.
- **F1H, F2H:** floor 1 ceiling height and floor 2 ceiling height (both numbers in metres).
- **W, D:** the property's full width and depth (both numbers in metres).
- **bi-fold door:** a folding closet door with two hinged panels.
- **hex colour `0xRRGGBB`:** colour written as a 6-digit hex code. `0xa9a59f` is the warm neutral grey of room-1's walls.
