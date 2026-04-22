// Coord system (v3):
//   origin (0,0,0) at corner-cabinet-entrance, on floor
//   +x along entrance-wall toward corner-entrance-window
//   +z along cabinet-wall  toward corner-ac-cabinet
//
// Walls (opposite pairs): cabinet↔window, entrance↔ac
//   cabinet-wall  : x=0
//   entrance-wall : z=0
//   window-wall   : x=W
//   ac-wall       : z=D

export const ROOM = { W: 2.7, D: 2.7, H: 2.4 };

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

// window-wall (x=W): sliding window, waist-height, centered
export const SLIDING_WINDOW = {
  w: 1.19, h: 0.9, sillY: 0.85,
};

// entrance-wall (z=0): door near corner-cabinet-entrance
export const DOOR = {
  w: 0.8, h: 2.0,
  x1: 0.1, x2: 0.9,
  y1: 0,
};

// cabinet-wall (x=0): hooks near entrance corner, closet in middle,
// frosted window near ac corner
export const HOOK_BAR = {
  w: 0.5, h: 0.04, d: 0.04,
  z1: 0.2, z2: 0.7,
  y: 1.65,
};
export const CLOSET = {
  w: 1.0, h: 2.1,
  z1: 1.0, z2: 2.0,
  y1: 0,
};
export const FROSTED_WINDOW = {
  w: 0.26, h: 1.0,
  z1: 2.25, z2: 2.51,
  sillY: 1.1,
};

// ac-wall (z=D): only the ac unit, near corner-ac-window, high up
export const AC_UNIT = {
  w: 0.8, h: 0.25, d: 0.2,
  x1: 1.7, x2: 2.5,
  y: 2.05,
};

// ----- furniture -----
export const BED = {
  // mattress: 1.0 wide × 2.0 long × 0.4 tall, top at y=0.5
  mattress:  { x1: 0.7,  x2: 2.7,  z1: 1.7, z2: 2.7, y1: 0.1, y2: 0.5 },
  headboard: { x1: 2.65, x2: 2.7,  z1: 1.7, z2: 2.7, y1: 0,   y2: 1.0 },
  footboard: { x1: 0.7,  x2: 0.75, z1: 1.7, z2: 2.7, y1: 0,   y2: 0.7 },
};

export const DESK = {
  // top 1.2 × 0.6 × 0.05, top surface at y=0.75
  footprint: { x1: 2.1, x2: 2.7, z1: 0.4, z2: 1.6 },
  topY: 0.75,
  topThick: 0.05,
  legThick: 0.04,
};

export const SHELF = {
  footprint: { x1: 2.3, x2: 2.7, z1: 0, z2: 0.4 },
  h: 1.3,
  postThick: 0.03,
  tierThick: 0.025,
  tierYs: [0.05, 0.47, 0.89, 1.27],
};

export const CHAIR = {
  footprint: { x1: 1.6, x2: 2.1, z1: 0.7, z2: 1.2 },
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
  cx: 1.35, cz: 1.35,
  frameY: 2.4,         // frame pressed against ceiling
  frameBarL: 0.3,
  frameBarThick: 0.03,
  shadeBottomY: 2.0,   // shades hang to y=2.0
  shadeDia: 0.15,
  shadeH: 0.3,
  shadeOffset: 0.1,    // shades spaced ±0.1 from center
};

export const CAMERA = {
  orbitTarget:  [1.35, 1.0, 1.35],
  orbitInitial: [4.5,  3.5, 4.5 ],
  walkEyeY:     1.6,
  walkStart:    [0.5,  1.6, 0.5],     // just inside corner-cabinet-entrance
  walkLookAt:   [2.5,  1.1, 2.5],     // aim diagonally toward corner-ac-window
};
