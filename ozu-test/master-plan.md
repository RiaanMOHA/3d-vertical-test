# ozu-1 MASTER PLAN — the Japanese house (whole property)

> **SCOPE: OZU-1 PROPERTY MASTER PLAN.** This is the master plan for the **whole Japanese house** — exterior + all interior rooms + circulation + stairs + ceilings. It is **NOT** the room-1 standalone sandbox plan (that's `room-1-ONLY-rendering-plan.md` next to this file). It is **NOT** the room-1 v5 feasibility audit (that lives at `../room-1-ONLY-v5-feasibility/`). This is the daily working document for the whole house.

> **Last audit:** 2026-05-04. The earlier draft of this file claimed
> bedrooms 1/2/3 and all three wet rooms were placeholders. **That was
> wrong.** They were already built. Corrected below.

## Scope (read first)

This is the plan for the **ozu-1 property**: the 3D reconstruction of
the real Japanese house. Two parts:

1. **Exterior** — the outside of the house (front facade, windows,
   brown wood panel, etc.).
2. **Interior** — the inside (all rooms, halls, bathrooms, stairs).

The third thing inside `ozu-test.html` — the **room-1 standalone
sandbox** — is a separate sub-project and is **not** covered by this
plan. It has its own plan at
[room-1-ONLY-rendering-plan.md](room-1-ONLY-rendering-plan.md) and only ever
unlocks for edits when the user literally types "room-1" in a
request.

---

## What's actually done (verified against the code, 2026-05-04)

### Exterior — mostly done
- ✅ Two-layer outer walls, brown wood panel ground-floor inset, cream
  upper section, all front-facade windows in place
- ⏳ Brown panel exact top edge + right edge — still needs re-measuring
  from the front-facade photo
- ⏳ Back-of-house garden side — is the secondary opening a sliding
  door or a window? Still open until the blueprint gets re-read at
  high resolution.
- ⏳ Frosted privacy window on **room-4's outside wall** — currently
  missing (the window is modelled inside the room but the exterior
  wall isn't pierced)

### Interior — Living / Dining / Kitchen — done
- ✅ Sofa, dining table, coffee table, TV console, kitchen counter,
  antique clock, pendant lights — all positioned per the room map
- ✅ AC unit body, kitchen counter pass-through (two-piece), TV
  console with directional screen face, window curtains as folded
  fabric strips
- ⏸ Brick texture on brick accent walls — **deferred** (high risk of
  looking worse than the flat colour we have now)

### Interior — bedrooms — all four done
- ✅ **Room-4** — iron-frame bed, dark-wood + black-metal cabinet,
  coat rack, AC, sliding window with curtains
- ✅ **Room-3** — iron-frame bed with wood headboard, 4-tier open
  shelving (no drawers), coat rack, AC, sliding window with curtains
- ✅ **Room-2** — all-white iron-frame bed, taupe column, desk +
  chair, coat rack, AC, sliding window with curtains
- ✅ **Room-1 zone** (the area inside the main interior scene — not
  the standalone sandbox) — iron-frame bed, solid wood desk, L-shaped
  shelf, coat rack, AC, sliding window with curtains

### Interior — wet rooms — all three done
- ✅ **Bathroom (washroom)** — bathtub, dark wood-pattern accent
  strip, tub tap, shower bar, shower head, towel rail
- ✅ **Laundry** — brick accent on the vanity wall, washing machine
  with chrome top panel, vanity cabinet + countertop + round basin,
  faucet, sconce light
- ✅ **Ground-floor toilet** — brick accent wall, bowl, tank,
  hand-wash basin atop tank, toilet-paper holder

### Interior — circulation
- ⚠ **Genkan (front entry)** — front door is in place but no
  doormat / shoe storage cabinet yet
- ⚠ **Ground-floor staircase** — built but each step is a stacked
  box. No proper sloped underside, no handrail, no side brackets.
- ⚠ **Second-floor staircase** — same as ground-floor: stacked boxes,
  no handrail, no brackets
- ⚠ **Second-floor toilet** — only **2 boxes** (bowl + tank). Missing
  basin, paper holder, frosted window detail.

### Interior — ceilings
- 🔲 Most rooms have **no ceiling**. Looking up shows sky.

### Doorways
- ⚠ **14 doorways** in total are present but all rendered as the same
  generic flat panel. Each one needs the right type per the
  blueprint: sliding (Japanese-style), hinged, bi-fold, archway.

### Tooling
- ✅ **QA navigation tool** — chips at the top let you jump straight
  into any room or viewpoint

### First-person walk mode
- ⚠ Built but reportedly half-broken (camera passes through walls
  and furniture). Furniture isn't in the wall-collision list.

---

## What's actually left — in phases

Each phase ends with **stop, hard-reload, judge before moving on**.

### Phase 1 — Add ceilings everywhere

Most rooms have no ceiling. Looking up shows sky. Add a ceiling to
each room, the corridor, and the entry. Quick once you do them all in
one sweep.

**Status:** done.

### Phase 2 — Fix the doorways

All 14 doorways currently look the same generic flat panel. Each
needs the right type per the blueprint:

- 🔲 Sliding (Japanese-style) where the blueprint says
- 🔲 Hinged where the blueprint says
- 🔲 Bi-fold (folding) closet doors
- 🔲 Open archways

**Status:** done.

### Phase 3 — Detail the genkan (entry area)

- 🔲 Doormat
- 🔲 Shoe storage cabinet (玄関収納)
- 🔲 Any other entry detail per the photos

**Status:** done.

### Phase 4 — Detail the second-floor toilet

- 🔲 Hand-wash basin
- 🔲 Paper holder
- 🔲 Frosted privacy window detail
- 🔲 Picture frame on the long wall (decide which side)

**Status:** done.

### Phase 5 — Real stairs (both staircases)

- 🔲 Replace each step's box with a real sloped-wedge step
- 🔲 Add handrails
- 🔲 Add wooden side brackets / carriage

Applies to both ground-floor and second-floor staircases.

**Status:** done.

### Phase 6 — Finish exterior polish

- 🔲 Re-measure brown panel's exact edges from the front-facade photo
- 🔲 Settle the back-of-house door-or-window question
- 🔲 Add the frosted privacy window on room-4's outside wall

**Status:** done.

### Phase 7 — Walk-through-the-house mode

- ✅ Removed entirely. The walk button + WASD/pointer-lock movement
  + per-scene start positions + the wall-collision list have all
  been deleted. Orbit is now the only camera mode.

**Status:** done (2026-05-06, removed).

### Phase 7.5 — Presentation-fidelity quick wins

Applied 2026-05-06 after a deep multi-agent audit. Each item is a
small, focused edit that closed a specific gap between the current
build and 2026 architectural-visualization standards.

- ✅ Ceramics upgraded to MeshPhysicalMaterial with clearcoat
  (matToilet at line 3363) — toilets / basins now render as glazed
  porcelain instead of matte plaster
- ✅ ACES filmic tone mapping applied globally (was room-1 only) —
  highlights no longer clip on cream walls in exterior + interior
- ✅ Procedural PMREM environment map applied globally — metals now
  reflect indirect light in every scene, not just room-1
- ✅ Interior shadows enabled — DirectionalLight now casts, every
  solid mesh casts + receives. Plus an indoor HemisphereLight for
  sky/floor bounce
- ✅ 2F top-of-stair parapet added — closes the 1.10 m guard gap at
  the south edge of the stair shaft (documented but missing before)
- ✅ Genkan 土間 step-down (150 mm) + 上がり框 wood lip step added
  — proper Japanese front-entry geometry
- ✅ Whitewashed wood-plank ceiling texture applied (was flat
  plaster) — matches the photos' dominant ceiling material
- ✅ Two warm-white PointLights at the LDK back-wall windows
  approximate daylight streaming in (placeholder for proper
  RectAreaLights, which need an extra inlined uniforms library)
- ✅ Smoke detectors (住宅用火災警報器) added on every 2F bedroom
  ceiling + at the top of the stair — mandatory per 消防法
- ✅ 2F toilet picture frame moved from west wall to east wall per
  photo evidence

**Status:** done (2026-05-06).

### Phase 7.6 — Photo-fidelity colour pass

Closing visible mismatches between the build and the room photos. Each
item is a small material-level change.

- ✅ Brick accent recoloured from warm-brown (`0x5e4a3d`) to cool
  grey-white (`0x9a9a96`) — matches the cool grey-white brick + white
  mortar visible in the LDK and 1F-toilet photos
- ✅ Laundry "brick" feature wall removed entirely — photos show plain
  painted wall, not brick. The vanity wall now reverts to default
  cream paint
- ✅ 1F + 2F toilet floors changed from lavender-purple (`0xd6cbe0`)
  flat colour to warm light wood plank (`0xc4a888`) using the same
  procedural plank texture used in the bedrooms
- ✅ LDK pendant lights (sphere shades over dining + sofa) given
  warm-glow emissive — they now read as lit pendants instead of cold
  dark spheres
- ✅ Bi-fold closet door pulls + hinged door handles upgraded from
  matte grey (`0x9a9a9a`, metalness 0.5) to chrome
  (`0xc8cdd2`, metalness 0.85, roughness 0.18) per photos
- ✅ Bi-fold centre seam darkened from bronze tone (`0x8a7a66`) to a
  recessed shadow (`0x4a4a4a`) — was reading as a fake bronze strip,
  now reads as a real fold line

**Status:** done (2026-05-06).

**Deferred** — needed but not yet done:
- ✅ 2F bedroom walls — DONE (see Phase 7.8 below).
- ✅ Front door upgrade — DONE (see Phase 7.9 below).
- ✅ Kitchen detail pass — DONE 2026-05-11. Rebuilt against the
  4-corner kitchen photos. Fridge-wall: white raised-panel lower
  cabinets with brass swing-bail pulls, dark walnut counter, grey-white
  brick feature wall up to ceiling, fridge tucked into the NE alcove.
  Counter-top split into LDK-side light maple bar + kitchen-interior
  stainless work counter. White キッチンパネル behind the cooktop's
  east half. Pass-through bulkhead (south header) with two recessed
  downlights on the underside. Gas cooktop with cast-iron grates +
  control knobs (replacing the flat IH). Stainless utensil rod with
  hooks above the cooktop. Whitewashed wood-plank ceiling continues
  from the LDK into the kitchen. Smoke detector on the kitchen
  ceiling. Also fixed a missing-kitchen-floor regression from the
  2026-05-08 1F LDK clip refactor (kitchen now has its own light oak
  floor entry).
- ⏳ Kitchen exterior window — `kitchen/room-map.md` describes a
  small frosted window high on the "east window-wall". With the
  blueprint X-mirror, the kitchen's only exterior wall is the
  building's WEST (x=0). The existing `F1_WIN_LEFT[1]` casement at
  z=3.30..3.56 sits inside the kitchen footprint and is the most
  likely match. Needs visual confirmation against `kitchen-b-2` to
  decide whether to re-shape it (smaller / higher / frosted).

### Phase 7.8 — Bedroom wall paint (taupe-grey)

Photo evidence shows all four 2F bedrooms have taupe-grey walls
(~`0x8e857a`), not the global cream `wallMat` (`0xeeeae3`) used
elsewhere. The shared `wallMat` can't be tinted per-room without
refactoring the wall builders, so a thin paint overlay was added on
the interior face of each bedroom's walls.

- ✅ New helper `addBedroomWallPaint(x0, z0, x1, z1, yFloor, ceilH,
  doorList, gapsBySide)` — paints all four interior wall faces with
  door + window x-ranges punched out
- ✅ Paint Y range sits between the existing baseboard and crown
  bands so trim still reads as a separate layer
- ✅ Applied to room-1, room-2, room-3, room-4 with their
  respective door + window cutouts wired up

**Status:** done (2026-05-06).

### Phase 7.7 — Architectural trim sweep

Adds the painted-trim layer that real JP residential interiors all
have. Uses one shared off-white `trimMat` (`0xfafaf6`) for visual
consistency.

- ✅ **Door casings (architrave / 飾り枠)** added to all 14 doors
  automatically — the `addDoor` helper now draws four trim strips per
  door (two vertical jambs, one top header, on each face of the
  wall). 70 mm wide × 12 mm proud.
- ✅ **Baseboards (巾木)** added in all four 2F bedrooms — 70 mm tall
  strip along the floor perimeter, with door openings punched out so
  the baseboard doesn't run through the door panels.
- ✅ **Crown molding (回り縁)** added in the same four bedrooms — 50
  mm strip at the ceiling line, same perimeter logic.
- ✅ Reusable helper `addRoomTrim(x0, z0, x1, z1, yFloor, ceilH, doorList)`
  — call it for any clean rectangular room and it handles both
  baseboard + crown + door cuts.

**Status:** done (2026-05-06).

**Deferred** — trim still missing in:
- LDK (irregular L-shape — would need either explicit per-segment
  calls or a polygon-based perimeter helper)
- 1F + 2F corridors (also irregular)
- Closets (small enough not to matter visually)
- Wet rooms (washroom, bath, toilet, laundry, genkan) — JP wet rooms
  typically don't have wood baseboards, so this is correct as-is

### Phase 7.9 — Front door rebuild

The genkan front door was previously a flat tan box (`doorMat 0xb89878`).
Photos show a typical 2026 JP residential entry: two-tone steel slab
with a vertical glass slit, chrome grip pull, brushed kickplate, and
mail slot.

- ✅ Removed the front door from the standard `addDoor` loop and built
  it custom with seven elements: lower brown panel + upper charcoal
  panel + vertical glass slit (transmission glass) + chrome grip pull
  + brushed kickplate + mail slot + transom + casing
- ✅ Geometry matches the existing 0.90 m × 2.00 m opening; no other
  wall or doorway data touched
- ✅ Architrave matches the trim style used by every other door
  (trimMat off-white, 70 mm wide × 12 mm proud)

**Status:** done (2026-05-06).

### Phase 8 — Small clean-ups

- ✅ `corridor-2` folder — clarified 2026-05-07. The user confirmed
  `corridor-2` photos are **the same physical space as `corridor-1`,
  re-shot with the toilet door closed**. No new viewpoints, no new
  geometry information. **Rule: ignore `corridor-2` entirely** — leave
  it on disk untouched, do not rename, do not chip-link, do not
  migrate. (Stored as memory `project_ozu_1f_corridor_rules.md`.)
- 🔲 Photo-folder rename — partial picture. `room-1` and `room-2`
  already use `corner-*-*` names; the rest still use `a/b/c/d`
  (`corridor-1`, `room-3`, `room-4`, `kitchen`, `laundry`,
  `toilet-1-f`, `washroom`, `corridor-2-toilet-2-f`). There is **no
  rename script on disk** — each rename has to be authored from the
  room's `room-map.md`. Special cases:
  - `corridor-1` target shape is `pano-a` + `pano-a2` (2-viewpoint
    capture), not `corner-*-*`. Per
    `project_ozu_1f_corridor_rules.md`. Until re-shoots arrive, the
    existing `a/b/c/d` photos stay on disk as legacy reference.
  - `corridor-2` is excluded from any rename run (see above).
  - Other a/b/c/d rooms can follow the room-1 pattern (corner names
    derived from each room-map.md's wall list).
- ✅ `package.json` — fixed 2026-05-07. The old `dev` script ran
  `concurrently --kill-others-on-fail` with `xdg-open || open` to
  auto-open a browser. On the headless GPU server `xdg-open` errors
  with no DISPLAY, which (per `--kill-others-on-fail`) tore down the
  http.server every time. Now `npm run dev` is just
  `python3 -m http.server 8080` — server starts, user opens the URL
  themselves via VS Code's port-forward. The `concurrently` dep was
  removed; `dev:no-open` is gone too (redundant with the simplified
  `dev`).

**Status:** mostly done; only the photo-folder rename remains, and
that's a "decide" item — not a free-running cleanup.

### Optional — going public

- 🔲 **Put the project online** so it can be opened from a web link
  (Vercel / Netlify / GitHub Pages). Currently it only runs on the
  user's own computer. Independent task.

---

## Recommended order

1. Phase 1 — Ceilings (quick sweep, biggest single visual gap)
2. Phase 2 — Doorways (one sweep across the whole house)
3. Phase 3 — Genkan
4. Phase 4 — 2F toilet
5. Phase 5 — Stairs upgrade
6. Phase 6 — Exterior polish (short, can slot in any time)
7. Phase 7 — Walk mode
8. Phase 8 — Clean-ups
9. Optional — going public

---

## Strict rules

- Only touch the **exterior** and **interior** parts of
  `ozu-test.html`.
- Never touch the **room-1 standalone sandbox** (the
  `registerScene('room-1', …)` block) during property work, even on a
  sweep. That block only unlocks when the user literally types
  "room-1".
- Pause for review after each phase.
- Plain language in status reports — no dev jargon.
- One thing at a time.
