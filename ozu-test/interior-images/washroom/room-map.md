# washroom map (浴室 / unit-bath)

## overview

`washroom` is the user's label for the **浴室 (UB / unit-bath)** — the small enclosed bath module on 1F. It is NOT the powder room (the powder room with vanity sink + washing machine is the `laundry` folder, mapped separately).

approximate dimensions from blueprint:
- 1,800 mm wide (E-W) × 1,800 mm deep (N-S) — depth confirmed in Phase C against blueprint at 400 dpi (the earlier "2,005" reading was wrong)
- footprint: 3.24 ㎡
- modular fiberglass UB unit (TOTO/LIXIL-style)

assumed (to confirm in phase D):
- ceiling: flat white panel (UB units typically have a flat moulded ceiling with a vent grille and a downlight)
- floor: textured non-slip white/grey panel (UB integrated floor)
- wall finish: 3 walls in white panels + 1 dark wood-pattern accent wall (the "wet wall")

## walls

### bath-wall (north)
- exterior wall (the only one of the 4)
- bathtub long edge runs along this wall (bathtub is in the north half of the room)
- dark wood-pattern accent panel — the room's only dark wall
- shower fixtures mounted on this wall: vertical chrome shower bar + handheld shower head + flexible hose
- chrome body-soap shelf with 3 dispensers (2 black "Classical", 1 white "Bodysoap")
- thermostat mixer valve (KVK) mounted at counter height
- frosted vertical privacy window (縦すべり 02607, FL+1800) high on the wall above the bathtub head
- opposite: side-wall

### entry-wall (east)
- interior wall, separates UB from `laundry` (洗面所)
- single white hinged door (開き), based on the smooth swing-arc shown on the blueprint inside the UB box (door swings into UB)
- door type to be re-confirmed in phase E (could also be a single-fold; folding/folded panel `折戸` is unlikely given the arc shape but possible)
- opposite: end-wall

### side-wall (south)
- interior wall, separates UB from corridor / interior
- plain white panel; this is the "wash zone" back wall (facing the bathtub)
- horizontal towel/clothes rail at chest height
- ventilation grille high near ceiling (likely an exhaust vent)
- opposite: bath-wall

### end-wall (west)
- short wall at the head end of the bathtub
- plain white panel
- bathtub head touches this wall
- bathtub spout/tap fixture (faucet) protrudes from this wall above the tub head
- opposite: entry-wall

## adjacencies

- bath-wall meets end-wall and entry-wall
- side-wall meets end-wall and entry-wall
- end-wall meets bath-wall and side-wall
- entry-wall meets bath-wall and side-wall

## corners

| corner id | walls meeting | notes |
|---|---|---|
| corner-bath-end | bath-wall × end-wall | NW; bathtub head + tap fixture cluster here |
| corner-bath-entry | bath-wall × entry-wall | NE; bathtub foot end; folding door immediately south |
| corner-end-side | end-wall × side-wall | SW; wash-zone corner; opposite the tub head |
| corner-entry-side | entry-wall × side-wall | SE; wash-zone corner; folding door immediately north |

corner ids list walls in alphabetical order.

## room layout (top-down)

```
                          bath-wall  (exterior, dark accent)
        ┌─────────────────────────────────────────┐
        │ [tap]                              [shower head + soap shelf]
        │ [───── bathtub (long axis E-W) ─────]   │  [frosted window above]
        │                                         │
   end  │                                         │ entry
   wall │            (wash zone)                  │  wall
        │                                         │  [folding door]
        │              [towel rail]               │
        │              [ceiling vent]             │
        └─────────────────────────────────────────┘
                          side-wall (interior)
```

## camera-position mapping

confirmed by the orange letters on the annotated blueprint `ozu-1-blueprint-updated.jpeg`:

| current path | blueprint mark | corner |
|---|---|---|
| `washroom/a/` | orange A | corner-entry-side (SE) |
| `washroom/b/` | orange B | corner-end-side (SW) |
| `washroom/c/` | orange C | corner-bath-end (NW) |
| `washroom/d/` | orange D | corner-bath-entry (NE) |

plus a `close-up/` folder with 3 detail shots of the bath-wall (body soap shelf + thermostat valve) — not a corner sweep.

## panorama sweep direction

clockwise from above (per room-1 convention). sequence 01 starts the sweep, highest number ends it.

## fixture / appliance anchors

- **bathtub**: long axis east-west; long edge against bath-wall; head (with tap) at corner-bath-end (NW); foot at corner-bath-entry (NE)
- **shower head + bar**: mounted on bath-wall, mid-east portion, between corner-bath-entry and the centre of the bath-wall
- **body soap shelf**: chrome shelf on bath-wall, just below the shower bar
- **thermostat mixer valve (KVK)**: bath-wall, below the soap shelf
- **frosted window 縦すべり 02607**: bath-wall, high above bathtub head (FL+1800 sill height)
- **folding door**: entry-wall, full height
- **bathtub tap (faucet)**: end-wall, above the bathtub head
- **towel rail**: side-wall, chest height
- **ventilation grille**: side-wall (or ceiling), high
- **ceiling downlight**: centred on ceiling

## folder structure (current — letter-coded)

```
washroom/
├── room-map.md          (this file)
├── room-map-photos.md   (photo→wall index)
├── a/         (23 images — corner-entry-side sweep)
├── b/         (22 images — corner-end-side sweep)
├── c/         (23 images — corner-bath-end sweep)
├── d/         (24 images — corner-bath-entry sweep)
└── close-up/  (3 images — bath-wall detail shots)
```

## proposed rename

```bash
cd /Users/riaan/3d-vertical-test/ozu-test/interior-images/washroom
mv a corner-entry-side
mv b corner-end-side
mv c corner-bath-end
mv d corner-bath-entry

for d in corner-entry-side corner-end-side corner-bath-end corner-bath-entry; do
  cd "$d"
  i=1
  for f in $(ls *.webp 2>/dev/null | sort -V); do
    padded=$(printf "%02d" $i)
    mv "$f" "washroom-$d-$padded.webp"
    i=$((i+1))
  done
  cd ..
done
```

(don't run until confirmed.)

## unverified items

- exact UB footprint dimensions (read from blueprint at 400 dpi, ~1,800 × 2,005)
- ceiling height (UB units typically 2,100 mm)
- whether the ventilation grille is on side-wall or on ceiling (probably ceiling for a UB)
- exact placement of shower bar along bath-wall (east half? mid? need full sweep verification)
- exact tatesuberi window position along bath-wall
- whether the bath-wall accent runs full ceiling-to-floor or only above the tub
- door type and exact swing direction (blueprint arc suggests hinged 開き swinging into UB; phase E to confirm)

## usage notes

- always reference walls by feature name (bath-wall, entry-wall, side-wall, end-wall), never by direction or coord
- corners are alphabetical wall pairs (corner-bath-end, not corner-end-bath)
- the bath-wall is the room's only EXTERIOR wall and the only one with a window
- the bath-wall is the dark accent; the other 3 walls are white moulded panel
- material sampling from photos:
  - dark wood-pattern accent panel: `washroom/a/` early frames + `washroom/close-up/` (all 3)
  - white panel finish: `washroom/d/` (entry-wall folding door + adjacent panels)
  - frosted window: `washroom/c/` early frames (window on left)
  - ceiling vent: visible in `washroom/b/` early frames
- image paths after rename:
  `interior-images/washroom/<corner-folder>/washroom-<corner-folder>-NN.webp`
