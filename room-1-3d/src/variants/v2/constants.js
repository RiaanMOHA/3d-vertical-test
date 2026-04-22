// room-1 v3 — photo-driven layout (rectangular room, bed along window-wall).
//
// Coord system (locked per spec):
//   origin (0,0,0) at corner-cabinet-entrance, on the floor
//   +x  along entrance-wall   toward window-wall
//   +z  along cabinet-wall    toward ac-wall
//   +y  up
//
// Corners:
//   corner-cabinet-entrance : (0,   0, 0)
//   corner-cabinet-window   : (W,   0, 0)
//   corner-ac-entrance      : (0,   0, D)
//   corner-ac-window        : (W,   0, D)

export const ROOM = { W: 2.7, D: 3.6, H: 2.4 };

export const COLOR = {
  floor:     0xd4b896,   // light oak, flat tan
  ceiling:   0xf5f0e8,   // off-white, flat
  wall:      0xc8c2b8,   // warm neutral grey
  white:     0xffffff,   // window frames, ac, closet, door
  ironDark:  0x1a1715,   // bed headboard / footboard / metal frames
  mattress:  0xf5eedd,   // white/cream mattress
  deskWood:  0x8b4513,   // reddish-brown desk top & shelf tiers
  chairSeat: 0x3a2513,   // dark brown leather
  blackMet:  0x1a1a1a,   // black metal legs / pedestal / base
  pendantWood: 0x8b6a4a, // wood cross frame
  pendantShade: 0xf0dfb8, // warm beige linen
  hookBar:   0x6a4a30,   // thin wood plank
  doorway:   0x2a2a2a,   // dark, reads as open doorway / hallway beyond
};

// ----- wall features -----
// window-wall (x=W)
export const SLIDING_WINDOW = {
  w: 1.19, h: 0.9,
  sillY: 0.8,
  // centred on wall, so z1 = (D - w)/2
};

// entrance-wall (x=0)
export const DOOR = {
  w: 0.8, h: 2.0,
  z1: 0.1, z2: 0.9,     // near corner-cabinet-entrance
  y1: 0,
};
// Door rendered OPEN: hinged at (x=0, z=0.1), swung 90° into room so the
// panel lies parallel to cabinet-wall, free edge at (x=0.8, z=0.1).
export const DOOR_OPEN = {
  x1: 0, x2: 0.8,
  z1: 0.06, z2: 0.10,
  y1: 0,  y2: 2.0,
};

// cabinet-wall (z=0)
export const CLOSET = {
  w: 1.4, h: 2.2,
  x1: 1.2, x2: 2.6,      // near corner-cabinet-window
  y1: 0,
};
export const HOOK_BAR = {
  w: 0.5, h: 0.05, d: 0.05,
  x1: 0.2, x2: 0.7,      // near corner-cabinet-entrance
  y: 1.7,
};

// ac-wall (z=D)
export const AC_UNIT = {
  w: 0.8, h: 0.25, d: 0.2,
  x1: 1.7, x2: 2.5,      // near corner-ac-window
  y: 2.0,                // bottom of ac unit
};
export const FROSTED_WINDOW = {
  w: 0.26, h: 0.9,
  x1: 1.22, x2: 1.48,    // centred on ac-wall
  sillY: 2.0,
};

// ----- furniture -----
export const BED = {
  // long side along window-wall (x=W). Head at corner-cabinet-window (z=0),
  // foot extending toward corner-ac-window. Mattress 1.0 wide × 1.95 long.
  mattress:  { x1: 1.7, x2: 2.7, z1: 0,   z2: 1.95, y1: 0.1, y2: 0.5 },
  headboard: { x1: 1.7, x2: 2.7, z1: 0,   z2: 0.05, y1: 0,   y2: 1.0 },
  footboard: { x1: 1.7, x2: 2.7, z1: 1.9, z2: 1.95, y1: 0,   y2: 0.7 },
};

export const DESK = {
  // along window-wall, between bed foot and shelf
  footprint: { x1: 2.1, x2: 2.7, z1: 1.95, z2: 3.15 },
  topY: 0.75,
  topThick: 0.05,
  legThick: 0.04,
};

export const SHELF = {
  // at corner-ac-window end of window-wall
  footprint: { x1: 2.3, x2: 2.7, z1: 3.15, z2: 3.55 },
  h: 1.3,
  postThick: 0.03,
  tierThick: 0.025,
  tierYs: [0.05, 0.47, 0.89, 1.27],
};

export const CHAIR = {
  // tucked in front of desk, facing window-wall
  footprint: { x1: 1.6, x2: 2.1, z1: 2.3, z2: 2.8 },
  h: 0.9,
  // breakdown:
  seatY: 0.5,        // top of seat
  seatThick: 0.05,
  backThick: 0.05,
  backH: 0.4,        // 0.5 seat + 0.4 back = 0.9 total
  pedestalThick: 0.08,
  pedestalH: 0.45,
  baseThick: 0.02,
};

export const PENDANT = {
  cx: 1.35, cz: 1.8,
  frameY: 2.4,         // frame pressed against ceiling
  frameBarL: 0.3,
  frameBarThick: 0.03,
  shadeBottomY: 2.0,   // shades hang to y=2.0
  shadeDia: 0.15,
  shadeH: 0.3,
  shadeOffset: 0.1,    // shades spaced ±0.1 from center
};

export const CAMERA = {
  orbitTarget:  [1.35, 1.0, 1.8],
  orbitInitial: [4.5,  3.5, 5.5 ],
  walkEyeY:     1.6,
  walkStart:    [0.5,  1.6, 0.5],     // just inside corner-cabinet-entrance
  walkLookAt:   [2.5,  1.1, 3.4],     // aim diagonally toward corner-ac-window
};
