# Glossary: terms used across the Ozu-1 flow docs

> One line per term, plain language. Referenced from every narrative doc in this folder.

## Three.js terms

- **registerScene block:** a chunk of code inside `ozu-test.html` (or your new property's HTML file) that defines one 3D scene. The Ozu-1 file has three: `exterior`, `interior`, and `room-1`. They share the file but are independent.
- **MeshStandardMaterial:** the everyday three.js material. Three knobs that matter most: colour, roughness (0 = mirror, 1 = chalk), metalness (0 = plastic / wood, 1 = polished metal).
- **MeshPhysicalMaterial:** an upgrade with extra knobs for transmission (light passes through), clearcoat (a glossy top layer), sheen.
- **clearcoat:** a thin glossy layer on top of the base material. Used for ceramic toilets and basins to make them read as glazed.
- **transmission:** light passes through the material. Glass has high transmission. Frosted glass also has high transmission but high roughness.
- **emissive:** the object glows on its own (a lit pendant shade, a phone screen). Doesn't actually light other surfaces unless paired with a real light source.
- **anisotropy / anisotropic filtering:** a setting that keeps textures sharp at glancing camera angles. Without it, distant floor planks blur to mush.
- **PBR (physically based rendering):** materials that respond to light realistically. A PBR set has three image files: a colour image (diff), a roughness image, and a surface-bumpiness image (normal).
- **env map (environment map):** a 360-degree image used as the source of indirect light and reflections. Without one, metals look flat and dead.
- **PMREM:** the recipe three.js uses to convert any image (real photo or procedural) into an env map.
- **EffectComposer:** the post-processing pipeline manager. Holds a list of passes. Each pass takes the previous pass's image and adds an effect on top.
- **RenderPass, UnrealBloomPass, SMAAPass, TAA:** kinds of passes. RenderPass draws the 3D. UnrealBloomPass adds glow around bright areas. SMAAPass smooths jagged edges. TAA is a smarter edge-smoother that averages multiple slightly-shifted snapshots.
- **post-processing pipeline:** effects layered on top of the rendered image after the 3D is drawn (the glow around a bright lamp, edge-smoothing, etc).

## Light types

- **DirectionalLight:** light from one direction, like the sun. Casts shadows.
- **PointLight:** a single bright dot, like a bare bulb.
- **RectAreaLight:** a rectangle that emits light, like a window pane. Soft, accurate shape on the floor.
- **HemisphereLight:** a sky colour at the top and a ground colour at the bottom, for general bounce-fill.

## Project-specific terms

- **F1_WIN / F2_WIN arrays:** the lists of windows for floor 1 and floor 2. Suffix says which outer wall: `_FRONT` (z=D, front facade), `_RIGHT` (x=W, right side), `_LEFT` (x=0, left side), `_BACK` (z=0, back). Each entry has `a` (start along wall in metres), `b` (end), `y0` (sill height), `y1` (header height).
- **wallX, wallZ:** helper functions that build a wall along the X axis or the Z axis with a list of openings to leave as holes. Argument order: `wallX(z, a, b, gaps, height, yBase, mat, outerSign)` and `wallZ(x, a, b, gaps, height, yBase, mat, outerSign)`.
- **F1H, F2H:** floor 1 ceiling height and floor 2 ceiling height (numbers in metres).
- **W, D:** the property's full width (east-west) and depth (north-south) (numbers in metres).
- **bi-fold door:** a folding closet door with two hinged panels.
- **Japanese door types:** sliding (Japanese-style 引違), hinged, bi-fold (folding closet), open archway.
- **hex colour `0xRRGGBB`:** colour as a 6-digit hex code. Examples: `0xeeeae3` is the cream walls, `0xfafaf6` is the off-white trim, `0x8e857a` is the taupe-grey bedroom paint, `0x9a9a96` is the cool grey-white brick.

## Web platform terms

- **`<script type="module">`:** a script tag with the `module` attribute. Lets the browser load other JS files via `import`.
- **ESM (ES Modules):** the modern browser-native way to share code between JS files.
- **inline (as a verb):** put the actual JS / shader file on disk under `vendor/` and import it directly, instead of fetching from a CDN.
- **bundler:** a tool that combines many JS files into one. Ozu-1 has none.
- **transpiler:** a tool that translates new JS into older JS for older browsers. Ozu-1 has none.

## JP residential terms (with kanji)

- **引違 (hikichigai):** sliding two-panel window or door.
- **縦すべり (tatesuberi):** narrow vertical privacy window.
- **玄関収納:** shoe storage cabinet near the entrance.
- **土間 (doma):** the lower step-down floor area at the entrance, typically 150 mm below the rest of the house.
- **上がり框 (agarikamachi):** the wood lip step that separates 土間 from the rest of the house.
- **飾り枠:** the trim around a door frame (architrave).
- **巾木 (habaki):** baseboard, the strip along the floor.
- **回り縁 (mawaribuchi):** crown moulding, the strip at the ceiling line.
- **住宅用火災警報器:** residential fire alarm (smoke detector). Mandatory per 消防法.
- **消防法:** Japanese fire-safety law.
