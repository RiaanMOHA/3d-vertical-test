import * as THREE from 'three';
import {
  ROOM, COLOR,
  SLIDING_WINDOW, DOOR, DOOR_OPEN, CLOSET, HOOK_BAR, AC_UNIT, FROSTED_WINDOW,
} from './constants.js';

const WT = 0.05;  // visual wall thickness (walls are thin boxes)
const FEAT = 0.02; // feature rectangle thickness (flat on wall surface)
const BIAS = 0.003; // z-fighting bias — push features slightly off wall

function boxMesh(w, h, d, cx, cy, cz, color, extra = {}) {
  const mat = new THREE.MeshStandardMaterial({
    color,
    roughness: extra.roughness ?? 0.9,
    metalness: extra.metalness ?? 0,
  });
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
  m.position.set(cx, cy, cz);
  return m;
}

// Add a flat rectangle feature onto a wall, offset by BIAS so it sits just
// in front of the wall surface (no real cutout — per v1 spec).
function wallFeature(group, wallAxis, wallInnerCoord, inward, dims, colour) {
  // dims = { a1, a2, b1, b2 } where a is along the wall (x for z-walls, z for
  // x-walls) and b is along y (vertical).
  const alen = dims.a2 - dims.a1;
  const blen = dims.b2 - dims.b1;
  const aCen = (dims.a1 + dims.a2) / 2;
  const bCen = (dims.b1 + dims.b2) / 2;
  const coord = wallInnerCoord + inward * BIAS;
  let mesh;
  if (wallAxis === 'x') {
    // wall's plane is perpendicular to x — feature extends in y and z
    mesh = boxMesh(FEAT, blen, alen, coord, bCen, aCen, colour);
  } else {
    // wall's plane is perpendicular to z — feature extends in x and y
    mesh = boxMesh(alen, blen, FEAT, aCen, bCen, coord, colour);
  }
  group.add(mesh);
  return mesh;
}

export function buildRoom(scene) {
  const g = new THREE.Group();
  g.name = 'room';
  scene.add(g);

  const { W, D, H } = ROOM;

  // ----- floor (flat tan box, thin) -----
  g.add(boxMesh(W, 0.02, D, W/2, -0.01, D/2, COLOR.floor, { roughness: 0.85 }));

  // ----- ceiling (single flat plane, no slant, no panels) -----
  g.add(boxMesh(W, 0.02, D, W/2, H + 0.01, D/2, COLOR.ceiling, { roughness: 0.9 }));

  // ----- walls (flat grey, thin boxes on the outside of the room volume) -----
  // entrance-wall (x=0, wall sits at x = -WT/2 .. 0)
  g.add(boxMesh(WT, H, D, -WT/2, H/2, D/2, COLOR.wall));
  // window-wall (x=W, wall sits at x = W .. W+WT)
  g.add(boxMesh(WT, H, D,  W + WT/2, H/2, D/2, COLOR.wall));
  // cabinet-wall (z=0, wall sits at z = -WT/2 .. 0)
  g.add(boxMesh(W, H, WT, W/2, H/2, -WT/2, COLOR.wall));
  // ac-wall (z=D, wall sits at z = D .. D+WT)
  g.add(boxMesh(W, H, WT, W/2, H/2,  D + WT/2, COLOR.wall));

  // ====== wall features (flat rectangles on wall surface) ======

  // --- window-wall (x=W): sliding window (white frame) ---
  {
    const sw = SLIDING_WINDOW;
    const z1 = (D - sw.w) / 2;
    const z2 = z1 + sw.w;
    wallFeature(g, 'x', W, -1,
      { a1: z1, a2: z2, b1: sw.sillY, b2: sw.sillY + sw.h },
      COLOR.white);
  }

  // --- entrance-wall (x=0): door rendered OPEN ---
  {
    // doorway opening (dark rectangle suggesting hallway beyond)
    wallFeature(g, 'x', 0, +1,
      { a1: DOOR.z1, a2: DOOR.z2, b1: DOOR.y1, b2: DOOR.y1 + DOOR.h },
      COLOR.doorway);

    // door panel swung 90° into room, lying near cabinet-wall
    const dop = DOOR_OPEN;
    g.add(boxMesh(
      dop.x2 - dop.x1, dop.y2 - dop.y1, dop.z2 - dop.z1,
      (dop.x1 + dop.x2) / 2, (dop.y1 + dop.y2) / 2, (dop.z1 + dop.z2) / 2,
      COLOR.white
    ));
  }

  // --- cabinet-wall (z=0): closet bi-fold doors + coat-hook bar ---
  {
    wallFeature(g, 'z', 0, +1,
      { a1: CLOSET.x1, a2: CLOSET.x2, b1: CLOSET.y1, b2: CLOSET.y1 + CLOSET.h },
      COLOR.white);

    // coat hook bar: small wood plank, standing off the wall by its own depth
    const hb = HOOK_BAR;
    g.add(boxMesh(
      hb.x2 - hb.x1, hb.h, hb.d,
      (hb.x1 + hb.x2) / 2, hb.y, hb.d / 2 + BIAS,
      COLOR.hookBar
    ));
  }

  // --- ac-wall (z=D): ac unit (box, protrudes into room) + narrow frosted window ---
  {
    const ac = AC_UNIT;
    g.add(boxMesh(
      ac.x2 - ac.x1, ac.h, ac.d,
      (ac.x1 + ac.x2) / 2, ac.y + ac.h / 2, D - ac.d / 2 - BIAS,
      COLOR.white
    ));

    const fw = FROSTED_WINDOW;
    wallFeature(g, 'z', D, -1,
      { a1: fw.x1, a2: fw.x2, b1: fw.sillY, b2: fw.sillY + fw.h },
      COLOR.white);
  }

  return g;
}
