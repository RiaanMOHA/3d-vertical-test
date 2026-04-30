# 3d-vertical-test

## What this is

A multi-project hub for interactive 3D web prototypes. Each project is a single self-contained HTML file with three.js inlined, served from a static dev server on port 8080. The current main project (`ozu-test.html`) is a 3D reconstruction of a real Japanese house, built from a blueprint PDF and ~950 on-site interior panorama photos.

## Stack

- Vanilla HTML, CSS custom properties, vanilla JavaScript
- three.js r128 inlined into each project HTML file (no external library load, works offline)
- Custom inline `OrbitControls` class (with a Mac-trackpad phantom-zoom guard)
- Python `http.server` as the dev server, wrapped with `concurrently` (only npm dependency)
- Package manager: npm
- No bundler, no transpiler, no framework, no build step

## Folder map

```
index.html               project hub — lists each project as a card
ozu-test.html            main project: 3D house reconstruction (~2,200 lines of app code + inlined three.js)
test.html                playground / prototype sandbox — DO NOT delete or modify
ozu-test/                source assets for ozu-test.html
  blueprints/            blueprint PDF + derived measurement docs (Phase A/C output)
  exterior-images/       front-facade photos for the exterior build
  interior-images/       per-room photo folders + room-map.md per room
  ldk-fix-plan.md        living-dining-kitchen polish plan
  phase-d-plan.md        per-room rebuild plan
test/                    playground / prototype assets — DO NOT delete or modify
.handoffs/               per-session handoff journals — managed by /handoff and /pickup skills
showcase/                gitignored portfolio documentation (9 files)
```

## Conventions

### Architecture

- **One HTML file per project.** No project may grow into a folder of separate JS files. Three.js stays inlined.
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

User preferences and feedback rules are in the per-project memory at `~/.claude/projects/-Users-riaan-3d-vertical-test/memory/MEMORY.md`. Read that to learn the user's collaboration style, past corrections, and project-specific quirks (e.g. blueprint X-mirror, stair shape, no floating geometry).
