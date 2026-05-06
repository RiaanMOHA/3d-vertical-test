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
