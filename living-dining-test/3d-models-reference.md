# Living-Dining — 3D models reference

All 3D objects in the living-dining scene are built procedurally in three.js inside a single HTML file. There are **no `.glb`/`.gltf`/`.fbx` files** — every object is constructed from boxes, planes, and shape geometry directly in code, then dressed with baked PBR textures and lightmaps.

## Main source file

- **Scene file:** `/Users/riaan/3d-vertical-test/living-dining-test.html`
- **Total lines:** ~3,399
- **Script type:** `<script type="module">` (vanilla three.js r184 ESM, no bundler)

## Asset folders (textures, bakes, references)

- **Baked PBR textures + lightmaps:** `/Users/riaan/3d-vertical-test/living-dining-test/textures/`
  - Lightmaps live at: `/Users/riaan/3d-vertical-test/living-dining-test/textures/lightmap/<slug>.png`
- **Blender bake scripts (run on A6000 GPU):** `/Users/riaan/3d-vertical-test/living-dining-test/bake/`
- **Reference render images:** `/Users/riaan/3d-vertical-test/living-dining-test/new-living-dining-test-renders/`
- **HDRI environment (shared with whole project):** `/Users/riaan/3d-vertical-test/ozu-test/hdri/kloppenheim_06_puresky_2k.hdr`

## Object-by-object location inside `living-dining-test.html`

### Room shell & openings
| Object | Function / section | Line |
|---|---|---|
| LDK enclosing walls (north, south, east, stairwell) | `/* === LDK enclosing walls === */` | 828 |
| Kitchen-wall (north) with two openings | inline | 837 |
| Corridor entry door (white flush panel) | inline | 870 |
| Kitchen counter pass-through (light-wood top) | inline | 952 |
| Stairwell internal partitions | inline | 1171 |
| White trim (cornice + skirting, all faces) | inline | 1281 |
| Stair treads + handrail inside the stair shaft | inline | 1336 |
| Garden-wall sliding glass doors ×2 | `buildSlidingDoor(...)` | 1515 |
| Cream curtains on the sliding doors | `buildCurtain(...)` | 1568 |
| Brick-wall (east) sash window | `buildBrickWindow()` | 1647 |
| Cream curtains on the brick window | `buildBrickCurtain(...)` | 1696 |

### Kitchen-side built-ins visible from LDK
| Object | Function / section | Line |
|---|---|---|
| Tall stainless double-door fridge | inline | 1069 |
| Range hood (black/stainless wall extractor) | inline | 1125 |

### Living-area furniture
| Object | Function / section | Line |
|---|---|---|
| TV console | `buildTVConsole(cx, cz)` | 1996 |
| Sony BRAVIA FW-65BZ30J TV | `buildBravia(cx, cz)` | 2103 |
| Sofa (tufted dark-leather 2-seater, wood arm caps) | `buildSofa(cx, cz)` | 2216 |
| Coffee table | `buildCoffeeTable(cx, cz)` | 2293 |

### Dining-area furniture
| Object | Function / section | Line |
|---|---|---|
| Dining table | inline | 2456 |
| Shell chairs around dining table | `buildShellChair(cx, cz, facing, shellHex)` | 2547 |

### Lighting fixtures
| Object | Function / section | Line |
|---|---|---|
| Two chandelier pendants (wrought-iron + cream tulip shades) | `buildChandelier(cx, cz, dropToY)` | 2674 |
| Recessed ceiling downlights (emissive discs) | inline | 2759 |

### Wall-mounted objects
| Object | Function / section | Line |
|---|---|---|
| AC split-system unit on brick wall | `buildAC(cx, cy, cz)` | 2798 |
| Antique double-faced station clock on wrought-iron bracket | inline | 2848 |
| Intercom panel + light switches (stairwell east partition) | inline | 2997 |
| Floor-level wall outlets | inline | 3223 |

### Decor / dressings
| Object | Function / section | Line |
|---|---|---|
| Lavender stems in glass bottle (on dining table) | inline | 3070 |
| Small pink/white flower jar (on coffee table) | inline | 3139 |

## Lighting rig (for reference — not "objects" but they shape every render)

Inside the same file:
- The sun (DirectionalLight, casts shadows) — line 1760
- Garden-wall RectAreaLight diffuse fill (one per slider) — line 1781
- Brick-wall RectAreaLight at the window aperture — line 1797
- HDR-bright sky proxy planes outside each window — line 1813

Lighting follows the project rule: **Kumamoto, sunny spring day, 11:00 AM JST** — sun azimuth ≈ 160° (SSE), elevation ≈ 60°, color temperature 5500–5800 K.

## How another Claude Code session should use this

1. The source of truth is `living-dining-test.html` — open it and jump to the line numbers above to find / modify any object.
2. Object geometry is built with a `box(w, h, d, cx, cy, cz, color, extra)` helper that creates a brand-new `MeshStandardMaterial` per call. When converting a group of `box(...)` calls to share a single PBR material, add a scoped `<x>Box(...)` helper (see the `hutchBox()` and `woodBox()` pattern documented in the project root `CLAUDE.md`).
3. Any new or improved object must go through the cutting-edge bake pipeline: photo-driven PBR sources → Blender Python script under `living-dining-test/bake/` → Cycles offline bake on the A6000 → PNG textures into `living-dining-test/textures/<object>/` → runtime samples those textures.
