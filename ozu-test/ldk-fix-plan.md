# LDK fix plan

Plan to fix the audit findings on `ozu-test.html` LDK + front-facade work. Three phases, pause for review between each.

Sources of truth (in priority order):
1. `blueprints/ozu-1-blueprint.pdf` (rendered at 400 dpi when measuring)
2. `exterior-images/ozu-1-test-exterior-primary-{1..4}.webp`
3. `interior-images/living-dining/room-map.md` + `interior-images/kitchen/room-map.md`

---

## Phase 1 — LDK layout repositioning

Re-derive all LDK furniture positions from the LDK map's stated layout, fix in one coordinated pass. The current placements are wrong because they were dropped in piecemeal without checking against the map's spatial logic.

### Reasoning anchors (from `living-dining/room-map.md`)

- **Sofa**: south-west half of LDK, facing north toward TV
  → code: large-x (west), small-z (south)
- **Dining table**: north-east half, near kitchen counter end
  → code: small-x (east), large-z (north), near x=2.55 boundary
- **Coffee table**: between sofa and TV
  → in front of sofa, between sofa and TV console
- **TV console**: against kitchen-wall, between corner-kitchen-stairs and the kitchen counter pass-through
  → z=4.10..4.50, x range bounded by counter-end (2.55) and stair-shaft (5.40); should be aligned roughly with sofa for "facing TV" to work
- **Antique clock**: on kitchen-wall near corridor entry (the archway)
  → x=5.40..6.10 archway → clock on the small wall stub immediately east of archway, x=6.10..6.25
- **Pendants**: 1 over dining table, 1 over living area
  → height ~1.55 m above the surface they light, with cord up to ceiling

### Position changes

| Item | Current | Target | Note |
|---|---|---|---|
| Sofa | x=2.50..4.30, z=0.10..0.95 | x=4.00..5.80, z=0.20..1.10 | move west (large x), faces north |
| Coffee table | x=3.20..4.20, z=1.30..2.30 | x=4.30..5.50, z=1.40..2.20 | in front of new sofa position |
| Dining table | x=3.00..4.40, z=1.60..2.40 | x=2.40..3.80, z=2.80..4.10 | NE half near counter |
| TV console | x=3.00..5.40, z=4.10..4.50 | x=3.80..5.40, z=4.10..4.50 | aligned with new sofa centre (~4.90) |
| Clock | x=4.00..4.40, z=4.42..4.48 | x=6.10..6.25, z=4.42..4.48 | east of archway |
| Dining pendant | (3.70, 2.30, 2.00) | (3.10, 1.55, 3.45) | over new dining position |
| Living pendant | (3.40, 2.30, 0.55) | (4.90, 1.80, 1.80) | over new coffee table |

### Files touched

- `ozu-test.html` — furniture lines around 1056-1095 (1F LDK section)

### Acceptance check

- Reload browser → walk into LDK from any angle → spatial layout matches the LDK map's top-down diagram
- No furniture overlaps
- Sofa, coffee table, TV console roughly in line on x-axis (so sofa "faces" TV)
- Pendants visibly hang lower than ceiling

**STOP. Pause for user review before Phase 2.**

---

## Phase 2 — Calibrate depths + proportions

Items needing blueprint re-read, photo measurement, or a known standard. Bundle into one verify-then-edit pass.

### Items

| # | Question | Source | Action |
|---|---|---|---|
| 2A | Kitchen counter depth | Standard (real counter ~0.60 m); current is 0.20 m | Change z=2.30..2.50 → z=2.30..2.90 (counter overhang into LDK) |
| 2B | Brown panel y top edge | `exterior-images/ozu-1-test-exterior-primary-1.webp` pixel measurement | Update `BROWN_Y1` constant in both interior + exterior scenes |
| 2C | Brown panel x right edge | Same photo, compare to blueprint x=4.50 | Reconcile per source-of-truth rule (blueprint usually wins; flag if photo strongly disagrees) |
| 2D | LDK back garden-wall: secondary 引違 16009 — door or window? | `blueprints/ozu-1-blueprint.pdf`, 400 dpi south wall of LDK | If full-height door, change `F1_WIN_BACK[1]` y0 to 0.0 |

### Process

1. Render blueprint pages at 400 dpi (reuse `/tmp/ozu-1f-panel.png` if already cached, otherwise re-render with `magick -density 400 ... +repage`)
2. Open primary-1 exterior photo, eyeball measure brown panel proportions (height / width relative to whole front facade)
3. Update constants in `ozu-test.html`:
   - `BROWN_X1` (currently 4.50) at lines ~318 and ~833
   - `BROWN_Y1` (currently 2.10) at lines ~318 and ~833
   - `F1_WIN_BACK[1]` y-range at line ~815 if it should be a door

### Files touched

- `ozu-test.html` — constants in exterior scene (~313-336) + interior scene (~830-836)

### Acceptance check

- Reload browser → front facade brown panel proportions look like primary-1 photo
- Back of building (LDK garden side) shows two full-height sliding doors if blueprint confirms

**STOP. Pause for user review before Phase 3.**

---

## Phase 3 — Geometric polish

Status: 4 of 5 done. Brick texture deferred indefinitely (UV pipeline complexity).

| Item | Status |
|---|---|
| TV console with directional screen face on south side | ✓ done |
| Kitchen counter pass-through built as 2-piece (cabinet + overhang counter-top) | ✓ done |
| AC unit shape detail (body + recessed grille + bottom vent slit) | ✓ done |
| Window curtains as fabric-folds geometry (4 alternating strips) | ✓ done |
| Procedural brick texture instead of flat colour for `matBrick` | ⏸ deferred — needs per-mesh UV scale to look right; high risk of worse-than-flat result |

---

## Out of scope for this plan

The audit also surfaced a non-LDK issue:
- 1F storage closet (物入, x=3.60..4.50, z=3.60..4.50) has no south wall and no door — open to LDK. Probably intentional for Phase E (door type pass), so leaving alone.
