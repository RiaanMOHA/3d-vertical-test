// Coord system (v4):
//   origin (0,0,0) at corner-cabinet-entrance, on floor
//   +x along entrance-wall toward corner-entrance-window
//   +z along cabinet-wall  toward corner-ac-cabinet

export const ROOM = { W: 2.7, D: 2.7, H: 2.5 };

export const COLOR = {
  floor:     0xd4b896,
  ceiling:   0xf5f0e8,
  wall:      0xc8c2b8,
  white:     0xffffff,
  ironDark:  0x1a1715,
  mattress:  0xf5eedd,
  deskWood:  0x8b4513,
  chairSeat: 0x3a2513,
  blackMet:  0x1a1a1a,
  pendantWood: 0x8b6a4a,
  pendantShade: 0xf0dfb8,
  doorway:   0x2a2a2a,
};

export const SLIDING_WINDOW = {
  w: 1.19, h: 0.9, sillY: 0.85,
  z1: 0.405, z2: 1.595,
};

export const DOOR = {
  w: 0.8, h: 2.0,
  x1: 0.0, x2: 0.8,
  y1: 0,
};

export const CLOSET = {
  w: 1.2, h: 2.2,
  z1: 0.75, z2: 1.95,
  y1: 0,
};

export const FROSTED_WINDOW = {
  w: 0.26, h: 1.0,
  x1: 0.82, x2: 1.08,
  sillY: 0.9,
};
export const AC_UNIT = {
  w: 0.8, h: 0.25, d: 0.2,
  x1: 1.7, x2: 2.5,
  y: 2.15,
};

export const BED = {
  mattress:  { x1: 0.7,  x2: 2.7,  z1: 1.7, z2: 2.7, y1: 0.1, y2: 0.5 },
  headboard: { x1: 2.65, x2: 2.7,  z1: 1.7, z2: 2.7, y1: 0,   y2: 1.0 },
  footboard: { x1: 0.7,  x2: 0.75, z1: 1.7, z2: 2.7, y1: 0,   y2: 0.7 },
};

export const DESK = {
  footprint: { x1: 2.1, x2: 2.7, z1: 0.4, z2: 1.6 },
  topY: 0.75,
  topThick: 0.05,
  legThick: 0.04,
};

export const SHELF = {
  footprint: { x1: 2.1, x2: 2.7, z1: 0.0, z2: 0.4 },
  h: 1.3,
  postThick: 0.03,
  tierThick: 0.025,
  tierYs: [0.05, 0.47, 0.89, 1.27],
};

export const CHAIR = {
  footprint: { x1: 1.6, x2: 2.1, z1: 1.1, z2: 1.6 },
  h: 0.9,
  seatY: 0.5,
  seatThick: 0.05,
  backThick: 0.05,
  backH: 0.4,
  pedestalThick: 0.08,
  pedestalH: 0.45,
  baseThick: 0.02,
};

export const PENDANT = {
  cx: 1.35, cz: 1.35,
  frameY: 2.5,
  frameBarL: 0.3,
  frameBarThick: 0.03,
  shadeBottomY: 2.1,
  shadeDia: 0.15,
  shadeH: 0.3,
  shadeOffset: 0.1,
};

export const CAMERA = {
  orbitTarget:  [1.35, 1.0, 1.35],
  orbitInitial: [4.5,  3.5, 4.5 ],
  walkEyeY:     1.6,
  walkStart:    [0.5,  1.6, 0.5],
  walkLookAt:   [2.5,  1.1, 2.5],
  walkFov:      70,
};

export const DOOR_OPEN_RAD = Math.PI / 2;
export const BASEBOARD_HEIGHT = 0.05;
export const BASEBOARD_DEPTH = 0.01;
export const CASING_WIDTH = 0.06;
export const CASING_DEPTH = 0.015;
