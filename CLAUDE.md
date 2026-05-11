# 3d-vertical-test

## What this is

A multi-project hub for interactive 3D web prototypes. Each project is a single self-contained HTML file with three.js inlined, served from a static dev server on port 8080. The current main project (`ozu-test.html`) is a 3D reconstruction of a real Japanese house, built from a blueprint PDF and ~950 on-site interior panorama photos.

## Stack

- Vanilla HTML, CSS custom properties, vanilla JavaScript
- **three.js r184 (May 2026)** loaded as ESM from `vendor/three/build/three.module.min.js` (~365 KB minified)
- **HDRLoader** from `vendor/three/examples/jsm/loaders/HDRLoader.js` — loads Poly Haven HDRI for real sky-based IBL
- HDRI asset: `ozu-test/hdri/kloppenheim_06_puresky_2k.hdr` (~4.4 MB, CC0, suburban afternoon sky)
- Project script uses `<script type="module">` — natively ESM, no bundler
- Custom inline `OrbitControls` class kept (with a Mac-trackpad phantom-zoom guard) — distinct from official r184 `OrbitControls`, which is also vendored
- Python `http.server` as the dev server, wrapped with `concurrently` (only npm dependency)
- Package manager: npm
- No bundler, no transpiler, no framework, no build step
- Works offline once `vendor/` + `ozu-test/hdri/` are populated (initial download requires network)

## Folder map

```
index.html                          project hub — lists each project as a card
ozu-test.html                       main project: 3D house reconstruction (~2,200 lines of app code + inlined three.js)
test.html                           playground / prototype sandbox — DO NOT delete or modify
ozu-test/                           source assets + ACTIVE plans for ozu-test.html
  blueprints/                       blueprint PDF + reference data (global-coords.md, room-identity.md)
  exterior-images/                  front-facade photos for the exterior build
  interior-images/                  per-room photo folders + room-map.md per room
  master-plan.md                       ACTIVE — Ozu-1 property master plan (whole house, exterior + interior)
  room-1-ONLY-rendering-plan.md        ACTIVE — room-1 standalone sandbox rendering plan (broad roadmap, Phases A–G)
  room-1-ONLY-cutting-edge-plan.md     ACTIVE — focused quality pass for room-1 sandbox (sub-plan of rendering plan)
  archived/                            SUPERSEDED plans, kept for history (do not follow)
room-1-ONLY-v5-feasibility/         ROOM-1 ONLY — v5 feasibility audit (not the master plan, not the rendering plan)
test/                               playground / prototype assets — DO NOT delete or modify
.handoffs/                          per-session handoff journals — managed by /handoff and /pickup skills
_backups/                           timestamped pre-cleanup backups (safe to delete after verification)
showcase/                           gitignored portfolio documentation (9 files)
```

### Plans hierarchy

- **Ozu-1 master plan** (`ozu-test/master-plan.md`) — the whole property. Phases 1–8.
- **Room-1 standalone rendering plan** (`ozu-test/room-1-ONLY-rendering-plan.md`) — only the standalone `registerScene('room-1', ...)` sandbox. Phases A–G. Distinct scope from the master plan's "room-1 zone" inside the interior scene.
- **Room-1 cutting-edge focused plan** (`ozu-test/room-1-ONLY-cutting-edge-plan.md`) — sub-plan of the rendering plan. Focused quality pass on three specific issues: pixelation, lighting, real-world textures.
- **Room-1 v5 feasibility audit** (`room-1-ONLY-v5-feasibility/`) — read-only research about rebuilding room-1 with 2026 tools (gaussian splats, WebGPU, AR). Not a build plan.
- **Archived plans** (`ozu-test/archived/`) — `phase-d-plan.md` and `ldk-fix-plan.md`. Both superseded by the master plan; kept for history only.

## Conventions

### Architecture

- **One HTML file per project.** Project source code stays in a single `<script type="module">` block. Three.js + HDRLoader + HDRI are vendored into `vendor/` and `ozu-test/hdri/` respectively; the HTML file imports them as ESM modules.
- **Three-layer hierarchy:** platform (`index.html`) → project (`ozu-test.html`) → in-page interior transitions. Never spawn a separate URL or port for an interior view.
- **Window arrays as single source of truth:** in `ozu-test.html`, the `F1_WIN_*` and `F2_WIN_*` arrays drive both the exterior and interior scenes. Edit the array, both scenes update.
- **Source-of-truth hierarchy (when sources conflict):** blueprint at 400 dpi > photos > room maps > HTML code comments > existing 3D code > memory rules > never eyeball.

### Naming

- Chip labels, viewpoint ids, and scene names in `ozu-test.html` exactly match folder names in `ozu-test/interior-images/`. No abbreviation, no friendly relabeling.
- Corner ids list walls in alphabetical order (e.g. `corner-cabinet-window`, never `corner-window-cabinet`).
- Wall names use feature names (`window-wall`, `ac-wall`), never compass directions or coordinates.

### Copy style

- Sentence case everywhere in UI strings. No `text-transform: uppercase`. No all-caps.
- Plain-language labels, no jargon.

### Commit style

- Format: `<scope>: <short description>` followed by a short body.
- Scope is usually `ozu-test` for project work, `cleanup` for housekeeping.
- Examples in the repo log: `ozu-test: 2-layer outer walls, brown panel inset, LDK polish, room-4 build`.

## No constraints — full power, always

You have access to an incredibly powerful GPU. **Never artificially constrain audits, research, parallel agents, search depth, or analysis breadth.** Specifically:

- When the user asks for "cutting edge" / "latest" / "state of the art" research, target THE ABSOLUTE CURRENT MOMENT — not "recent" (months stale), not training-cutoff. Use date-qualified web searches (`"<topic>" "<current month> <current year>"`), pull live release pages (GitHub releases, arXiv recent lists, browser/spec changelogs), cross-check 3+ independent sources before stating a version number. If a finding might be outdated, say so explicitly with the date of the source.
- When auditing, fan out into many parallel agents covering every angle. Don't pre-decide that one phase or one front matters more than another — let the evidence rank itself.
- When researching, never stop at "good enough." If the user reads as wanting the bleeding edge, run multiple search rounds with different query framings (technical / vendor / academic / community).
- Never hedge with vague time language ("recent", "fairly current", "as of training"). Either cite a dated source or flag the gap.
- Token budget, agent count, and search depth are not constraints to manage on the user's behalf. The user will tell you if they want a smaller scope.

If a task could be answered superficially or thoroughly, default to thoroughly.

## Cutting-edge rendering — A6000 bake for every object

For any 3D object pass — adding a new object, improving an existing one, fixing visible mismatch with the photos — runtime-only tweaks are **never** an acceptable end state. The A6000 (24 GB Ada / OptiX) sits idle by default and must be engaged on every render improvement.

The non-negotiable pipeline for every object pass:

1. **Photo-driven PBR.** Pull diffuse / roughness / normal / AO / displacement from the reference photos and from CC0 PBR sources (Poly Haven, ambientCG). Never invent material values; trace them to a source.
2. **Cycles offline bake on the A6000.** Write a Blender Python script under `ozu-test/bake/bake_room1_<object>.py` (matching the existing `bake_room1_ao.py` pattern). Run it with OptiX on the A6000 to bake albedo + normal + roughness + AO (and displacement, if needed) into PNG textures saved under `ozu-test/room-1-textures/<object>/`. Cloth, plush, leather, wrinkled fabric — all require cloth-sim or sculpted source meshes baked to textures.
3. **Cutting-edge runtime stack.** WebGPU renderer + MSAA 8× + `transmissionResolutionScale` + max anisotropy + ACES/AgX tone mapping + HDRI environment + RectAreaLights for soft area illumination + UnrealBloom and SMAA in the composer. The runtime simply samples the baked PBR textures; it doesn't try to compute high-fidelity material response on its own.
4. **Three.js features-first.** Default to the latest material types (`MeshPhysicalMaterial` with `transmission`, `sheen`, `iridescence`, `anisotropy`), the latest geometry helpers (`RoundedBoxGeometry`, custom `ShapeGeometry`, displaced `PlaneGeometry`), and instancing where it pays off. If r184 added it, use it.

A run that improves visual quality but skips the A6000 bake does not meet the rule. If the user explicitly says "no bake this time" the bake is deferred — but the bake script still gets written so it's ready when they greenlight it. Saving the script alone is not enough — it must actually be run on the A6000 before the work counts as done.

## Interior-render daylight rule — Kumamoto, sunny spring, 11:00 AM JST

**This rule applies ONLY to "inside the room" renders — camera placed inside an interior space looking around at walls / floor / ceiling / furniture. It does NOT apply to exterior shots (camera outside the building looking at the facade) — those have their own real-photo references.**

Every interior render must be lit as if it is:

1. **Kumamoto, Japan** (latitude ≈ 32.8°N, longitude ≈ 130.7°E)
2. **A sunny spring day** (clear sky, mid-April baseline)
3. **11:00 AM Japan Standard Time** (≈ 10:43 AM local solar time)

**Resulting sun position** (computed, not eyeballed):
- **Azimuth ≈ 160°** (SSE — south-southeast, ~20° east of due south)
- **Elevation ≈ 60°** above horizon
- **Color temperature ≈ 5500–5800 K** — neutral-cool, very slight warm cast. Never warm-yellow (no sunset/golden-hour tones).

**Consequences for any window-facing-direction:**
- **South-facing window:** direct sun streams in. Bright cast pattern on the floor opposite the window. Warmest direct contribution.
- **East-facing window:** sun is past peak-east; window catches strong direct light at a fairly steep angle.
- **West-facing window:** no direct sun yet (sun comes round in the afternoon). Bright diffuse sky only.
- **North-facing window:** NO direct sun at all — diffuse pale-blue sky only. Light entering reads as cool / overcast-bright even on a clear day. Frosted-glass north windows in particular should NOT use warm sun tones.

**Lighting rig template for runtime + bake:**

Every interior render needs ALL THREE pieces below. Shadows are non-negotiable — without a directional shadow-caster, geometry floats and the room reads as a render preview, not a scene.

1. **Direct sun.** DirectionalLight or SUN lamp at azimuth 160°, elevation 60°, neutral-cool color (`0xf6f5ec` / 5500K daylight). Full intensity for south/east-facing windows (sun streams in); the light's position is *outside* the window, target inside.
2. **Sky bounce.** HemisphereLight (sky `0xc8d6e8` cool pale blue, ground `0xa89878` warm floor bounce) + HDRI environment rotated so its bright sun zone aligns with azimuth 160°. Plus a RectAreaLight at the window plane for the diffuse area-fill from the sky disc.
3. **Window-direction shadow-caster.** A DirectionalLight positioned *outside the window*, pointed into the room, with `castShadow: true`. This is what grounds geometry. Even when no direct sun enters (north/west windows at 11 AM), the bright sky is still a directional source — the room still has soft cast shadows from it.

**Per-window-facing recipe:**
- **South / east window** — pieces 1 + 2 + 3 are the same DirectionalLight (the sun IS the shadow-caster). Warm-neutral color (`0xf6f5ec`), full intensity (~2.5–4), tight shadow disc.
- **North / west window** — pieces 1 and 3 are SEPARATE. Piece 1 (the actual sun) is positioned outside the building but its light doesn't reach the room interior (or contribute baked GI only). Piece 3 is a low-intensity (~0.8–1.2) DirectionalLight in COOL color (`0xe0e8f4` / `0xdde6f0`) at the window plane, wide `shadow.radius` (≥8) so frosted-glass scatter reads softly. RectAreaLight is also cool-tinted.
- **Color temperature consistency:** every light in the scene reads as the same 11 AM clock-time. No warm tungsten interior lights ON during daytime renders unless photo evidence shows them on.

**This rule overrides** any earlier interior-render lighting decisions that picked warmer / lower-angle / golden-hour values.

## Commands

- Start dev server: `npm run dev` (runs `python3 -m http.server 8080` and opens `localhost:8080/index.html`)
- No build, no lint, no typecheck, no test scripts. The runtime is the HTML files.

**Important:** never auto-start the dev server. The user runs `npm run dev` themselves; auto-starting collides with their session.

## Off-limits paths

Do not modify, rename, archive, or delete:

- `test.html` and `test/` — intentional playground / prototype sandbox
- `.handoffs/` — session journals (managed by /handoff and /pickup skills)
- `ozu-test/blueprints/ozu-1-blueprint.pdf` — source blueprint
- `ozu-test/exterior-images/` and `ozu-test/interior-images/` — source photos
- `showcase/` — portfolio docs (gitignored anyway)

## Where additional context lives

User preferences and feedback rules are in the per-project memory at `~/.claude/projects/-home-moha-Project-3d-vertical-test/memory/MEMORY.md`. Read that to learn the user's collaboration style, past corrections, and project-specific quirks (e.g. blueprint X-mirror, stair shape, no floating geometry).
