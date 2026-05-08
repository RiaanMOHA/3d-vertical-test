# Sub-procedure: how to place furniture from corner panoramas

> Used by step 9 of phase 2 in `claude-prompt.md`, step 8 of `flow-ozu-1-full.md`'s recipe, and step 16 of `flow-ozu-1-layout.md`'s recipe. The corner panoramas are the visual source of truth for furniture; this procedure says how to translate "the bed is in this photo" into "the bed sits at these coordinates with these dimensions".

## What "corner panorama" means

Each room has four corner folders (one per inside corner) at `<property-name>/interior-images/<room>/corner-<corner-id>/`. Each folder contains one or more 360-degree panorama photos taken from that corner. The panoramas are the user's primary reference. Before placing any furniture, look at all four.

## Setup before any placement

1. Read every panorama in every corner folder of the room. Note what is visible, which wall each piece sits against, and any fixture-to-fixture relationships (bed-next-to-desk, lamp-above-bed).
2. Confirm the wall names from the room map (`<property-name>/interior-images/<room>/room-map.md`). The naming should be by feature: window-wall, ac-wall, cabinet-wall, entrance-wall. If the room map disagrees with what you see in the photos, fix the room map first.
3. Confirm the room bounds from `global-coords.md` are in metres and follow the convention x runs east-west, z runs north-south.
4. Decide an order for placement: bed first, then large furniture against walls (desk, closet, shelf), then small fixtures (curtains, hooks, intercom, switches). Lamps last.

## Standard piece dimensions

Use these as defaults unless the photo clearly shows otherwise. Override per piece if measurements look wrong.

| Piece | Width (m) | Depth (m) | Height (m) | Notes |
|---|---|---|---|---|
| Single iron-frame bed | 0.97 | 1.95 | 0.90 (frame top) | Add ball finials on 4 corners. |
| Double iron-frame bed | 1.40 | 1.95 | 0.90 | |
| Solid wood desk | 1.20 | 0.55 | 0.72 | Top surface at 0.72 m. |
| Desk chair | 0.50 | 0.50 | 1.00 | |
| 4-tier open shelf | 0.80 | 0.30 | 1.60 | |
| L-shape shelf with X-brace | 0.80 each leg | 0.30 | 1.60 | |
| White closet (bi-fold) | 1.40 | 0.55 | 2.20 | Bi-fold pin handle, single vertical seam. |
| AC unit (wall-mounted) | 0.85 | 0.20 | 0.30 | High on a wall, leaving ~0.15 m to ceiling. |
| Coat hook rail | 0.80 | 0.05 | 0.15 | At eye level (~1.50 m above floor). |
| Curtain panel | half window width | 0.05 | window height + 0.30 | Hourglass-bunched, tieback ring. |
| Pendant lamp shade | 0.20 (cylinder diameter) | 0.20 | 0.20 (height) | On a wood crossbar above the bed area. |
| Doorknob (round) | 0.06 (sphere diameter) | 0.05 (escutcheon) | 0.06 | Centred at handle height ~1.05 m. |
| Light switch plate | 0.07 | 0.01 | 0.12 | Centred at switch height ~1.20 m, next to door. |
| Intercom panel | 0.10 | 0.01 | 0.15 | Below AC, below eye level. |

## How to place one piece

For each piece:

1. **Identify which wall.** From the panoramas, decide which wall the piece sits against. Match to the room map's wall name.
2. **Identify the orientation.** Bed long-side or short-side against the wall? Desk facing into the room or facing the wall? Closet facing into the room (the doors open into the room).
3. **Identify the position along the wall.** Look at the panorama and judge: is the piece centred on the wall? Tucked into a corner? At one-third along? Use the wall's a-to-b range (the full wall length minus any window/door cutouts) and pick a position within that range.
4. **Compute the 3D coordinates** based on the wall.
   - Wall along the X axis (running east-west), at constant `z = c`, with the room interior on the side of `c + dz` where `dz` is positive toward the room: piece centre at `(x_along, y_floor + h/2, c + d/2)` where `d` is the piece's depth and `h` is its height. The piece's outermost face touches the wall at `z = c + small_gap` (use 0.005 m gap to avoid z-fighting).
   - Wall along the Z axis (running north-south), at constant `x = c`, with room interior on the `c + dx` side: piece centre at `(c + d/2 + small_gap, y_floor + h/2, z_along)`.
5. **Add a small gap from the wall.** Real furniture rarely sits flush against the wall. Use 0.005 m to 0.020 m. This also prevents z-fighting (the rendering bug where two coincident faces flicker).
6. **Add the geometry.** Use a `THREE.BoxGeometry` for blocky pieces (bed frame, desk, closet). Use cylinders for bottles, vases, lamp shades. Use spheres for doorknobs, ball finials, pillows. Compose multiple meshes into one `THREE.Group` if the piece is complex (a bed = mattress box + 4 corner posts + 4 finials + sheet + 2 pillows).
7. **Hard reload.** Open the chip viewpoint for the room. Compare the 3D against the corresponding corner panorama. If the placement is visibly wrong (piece is in the wrong corner, wrong orientation, wrong size), tune. If acceptable, move on.

## Triangulation: how to be more accurate when one panorama is ambiguous

If the piece's exact position along the wall is unclear from one panorama, look at it from a second corner. The piece appears at a different angle in each panorama. Match the piece's position relative to the two corners and the windows visible in each photo.

For example: if the bed appears to be one-third of the way along the ac-wall in the corner-cabinet-window photo and roughly the same fraction in the corner-cabinet-entrance photo, place the bed at one-third along the ac-wall measured from whichever end the photos agree on.

## Anchoring lamps and ceiling-mounted pieces

For pieces that hang from the ceiling:

1. The crossbar carrying pendant lamps usually runs across one direction (parallel to the bed long-side).
2. The crossbar centre sits at `(x_centre, ceilH - 0.10, z_centre)` where `ceilH` is the ceiling height.
3. Each lamp shade hangs below the crossbar, e.g. four lamps spaced 0.40 m apart along the crossbar, each shade centre at `(x_lamp, ceilH - 0.45, z_centre)`.

For wall-mounted pieces above eye level (AC unit, coat hook, intercom): use the same wall-anchoring as the standard procedure but pick a y position in metres directly. AC unit y_centre ~ ceilH - 0.20. Coat hook y_centre ~ 1.50. Intercom y_centre ~ 1.30.

## Common failure modes and fixes

- **Piece passes through wall.** Increase the small_gap from 0.005 to 0.02 m and confirm the piece's depth is correct.
- **Piece is half in the floor.** The y_centre must be `y_floor + h/2`, where `y_floor` is the floor y of that room (often `F1H` for 2F rooms, `0` for 1F rooms).
- **Piece is too big and overlaps a door or window.** Read the wall's a-to-b range and the door/window cutouts; the piece's footprint along the wall must fit between the cutouts.
- **Piece is on the wrong wall.** Re-read the room map. The wall names (window-wall, ac-wall, cabinet-wall, entrance-wall) are stable; if the panorama disagrees with the map, fix the map first.
- **Piece looks too small / too big in the 3D view but the dimensions are correct.** This is a perceptual mismatch. The room may be the wrong scale. Check the room bounds in `global-coords.md` against the blueprint.

## Acceptance criteria for placement

For each piece, the test is: open the chip viewpoint for the room, compare the 3D against the panorama, judge whether the piece is in the right corner, the right orientation, and the right approximate size. Within roughly 0.3 m of position accuracy and within 20% of dimensional accuracy is acceptable for a first pass. Tune later if the user wants more accuracy.

If you're unsure, screenshot both views and ask the user.

## Strict rules

- Never eyeball without consulting the panoramas.
- Place one piece, hard reload, judge, then move on. No batching.
- The visual source of truth is the photos, not your imagination.
- The room map is the wall-naming source of truth. If it's wrong, fix it before placing pieces.
- Memory rule: do not edit the standalone `registerScene('room-1', ...)` block during property work, even if room-1 is one of the rooms you're placing furniture in. The standalone sandbox is a separate sub-project. Property-level room-1 furniture goes in the multi-room `interior` registerScene block.
