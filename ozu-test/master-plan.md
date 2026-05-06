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

**Status:** not started.

### Phase 2 — Fix the doorways

All 14 doorways currently look the same generic flat panel. Each
needs the right type per the blueprint:

- 🔲 Sliding (Japanese-style) where the blueprint says
- 🔲 Hinged where the blueprint says
- 🔲 Bi-fold (folding) closet doors
- 🔲 Open archways

**Status:** not started.

### Phase 3 — Detail the genkan (entry area)

- 🔲 Doormat
- 🔲 Shoe storage cabinet (玄関収納)
- 🔲 Any other entry detail per the photos

**Status:** not started.

### Phase 4 — Detail the second-floor toilet

- 🔲 Hand-wash basin
- 🔲 Paper holder
- 🔲 Frosted privacy window detail
- 🔲 Picture frame on the long wall (decide which side)

**Status:** not started.

### Phase 5 — Real stairs (both staircases)

- 🔲 Replace each step's box with a real sloped-wedge step
- 🔲 Add handrails
- 🔲 Add wooden side brackets / carriage

Applies to both ground-floor and second-floor staircases.

**Status:** not started.

### Phase 6 — Finish exterior polish

- 🔲 Re-measure brown panel's exact edges from the front-facade photo
- 🔲 Settle the back-of-house door-or-window question
- 🔲 Add the frosted privacy window on room-4's outside wall

**Status:** not started.

### Phase 7 — Walk-through-the-house mode

- 🔲 Currently half-broken (camera passes through walls + furniture).
  Either fix it (add furniture to the wall-collision list, fix
  through-wall) or remove the mode.

**Status:** not started.

### Phase 8 — Small clean-ups

- 🔲 Decide what to do with the empty `corridor-2` photo folder
  (keep or delete)
- 🔲 Decide whether to run the photo-folder rename script (some
  folders are still named `a/b/c/d` instead of by which corner they
  show)
- 🔲 `package.json` — currently flagged "leave it"; the `npm run dev`
  script also fails on Linux because it uses a Mac-only command.
  Could be tidied while we're here.

**Status:** open.

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
