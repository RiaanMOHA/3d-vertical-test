import * as THREE from 'three';
import {
  ROOM, COLOR,
  SLIDING_WINDOW, DOOR, CLOSET, HOOK_BAR, AC_UNIT, FROSTED_WINDOW,
} from './constants.js';

const WT      = 0.05;   // visual wall thickness
const FEAT    = 0.02;   // flat-feature thickness
const BIAS    = 0.003;  // z-fighting bias
const FRAME_T = 0.04;   // window frame bar thickness

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

// Place a flat feature on a wall. Accepts a color OR a Material instance.
function wallFeature(group, wallAxis, wallInnerCoord, inward, dims, matOrColor) {
  const alen = dims.a2 - dims.a1;
  const blen = dims.b2 - dims.b1;
  const aCen = (dims.a1 + dims.a2) / 2;
  const bCen = (dims.b1 + dims.b2) / 2;
  const coord = wallInnerCoord + inward * BIAS;
  const mat = (matOrColor instanceof THREE.Material)
    ? matOrColor
    : new THREE.MeshStandardMaterial({ color: matOrColor, roughness: 0.9 });
  let geom, mesh;
  if (wallAxis === 'x') {
    geom = new THREE.BoxGeometry(FEAT, blen, alen);
    mesh = new THREE.Mesh(geom, mat);
    mesh.position.set(coord, bCen, aCen);
  } else {
    geom = new THREE.BoxGeometry(alen, blen, FEAT);
    mesh = new THREE.Mesh(geom, mat);
    mesh.position.set(aCen, bCen, coord);
  }
  group.add(mesh);
  return mesh;
}

// 4 thin white frame bars around a window opening (a along wall, b vertical)
function windowFrame(group, wallAxis, wallInnerCoord, inward, a1, a2, b1, b2, mat) {
  const t = FRAME_T;
  wallFeature(group, wallAxis, wallInnerCoord, inward,
    { a1: a1 - t, a2: a2 + t, b1: b2,     b2: b2 + t }, mat); // top
  wallFeature(group, wallAxis, wallInnerCoord, inward,
    { a1: a1 - t, a2: a2 + t, b1: b1 - t, b2: b1     }, mat); // bottom
  wallFeature(group, wallAxis, wallInnerCoord, inward,
    { a1: a1 - t, a2: a1,     b1: b1,     b2: b2     }, mat); // left
  wallFeature(group, wallAxis, wallInnerCoord, inward,
    { a1: a2,     a2: a2 + t, b1: b1,     b2: b2     }, mat); // right
}

export function buildRoom(scene) {
  const g = new THREE.Group();
  g.name = 'room';
  scene.add(g);

  const { W, D, H } = ROOM;

  // ----- materials (v3) -----
  const glassMat = new THREE.MeshStandardMaterial({
    color: 0xb8d4e0, transparent: true, opacity: 0.35, roughness: 0.1,
  });
  const frostedMat = new THREE.MeshStandardMaterial({
    color: 0xe8e8e0, transparent: true, opacity: 0.75, roughness: 0.95,
  });
  const doorMat   = new THREE.MeshStandardMaterial({ color: 0xf2ece4, roughness: 0.6 });
  const closetMat = new THREE.MeshStandardMaterial({ color: 0xf2ece4, roughness: 0.7 });
  const frameMat  = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 });
  const handleMat = new THREE.MeshStandardMaterial({
    color: 0x999999, metalness: 0.7, roughness: 0.3,
  });
  const seamMat   = new THREE.MeshStandardMaterial({ color: 0xbababa });
  const knobMat   = new THREE.MeshStandardMaterial({
    color: 0x222222, metalness: 0.4, roughness: 0.6,
  });

  // ----- floor + ceiling -----
  g.add(boxMesh(W, 0.02, D, W/2, -0.01,    D/2, COLOR.floor,   { roughness: 0.85 }));
  g.add(boxMesh(W, 0.02, D, W/2, H + 0.01, D/2, COLOR.ceiling, { roughness: 0.9  }));

  // ----- walls (4 thin grey boxes, outside the room volume) -----
  g.add(boxMesh(WT, H, D, -WT/2,    H/2, D/2,        COLOR.wall)); // cabinet-wall  x=0
  g.add(boxMesh(WT, H, D, W + WT/2, H/2, D/2,        COLOR.wall)); // window-wall   x=W
  g.add(boxMesh(W, H, WT, W/2,      H/2, -WT/2,      COLOR.wall)); // entrance-wall z=0
  g.add(boxMesh(W, H, WT, W/2,      H/2, D + WT/2,   COLOR.wall)); // ac-wall       z=D

  // ====== wall features (v3 mapping) ======

  // --- window-wall (x=W): sliding window (centered) ---
  {
    const sw = SLIDING_WINDOW;
    const a1 = (D - sw.w) / 2;
    const a2 = a1 + sw.w;
    const b1 = sw.sillY;
    const b2 = sw.sillY + sw.h;
    wallFeature(g, 'x', W, -1, { a1, a2, b1, b2 }, glassMat);
    windowFrame(g, 'x', W, -1, a1, a2, b1, b2, frameMat);
  }

  // --- entrance-wall (z=0): door + silver handle ---
  {
    const d = DOOR;
    wallFeature(g, 'z', 0, +1,
      { a1: d.x1, a2: d.x2, b1: d.y1, b2: d.y1 + d.h }, doorMat);
    // silver horizontal handle near cabinet-side (x=0.1 edge, opposite hinge at x=0.9)
    const hW = 0.10, hH = 0.02, hD = 0.03;
    const handle = new THREE.Mesh(new THREE.BoxGeometry(hW, hH, hD), handleMat);
    handle.position.set(d.x1 + 0.05 + hW / 2, 1.0, BIAS + hD / 2);
    g.add(handle);
  }

  // --- cabinet-wall (x=0): hook bar + closet + frosted window ---
  {
    // hook bar (wood plank protruding into room, square cross-section)
    const hb = HOOK_BAR;
    const barCx = BIAS + hb.d / 2;
    const barCz = (hb.z1 + hb.z2) / 2;
    g.add(boxMesh(hb.d, hb.h, hb.z2 - hb.z1, barCx, hb.y, barCz, COLOR.hookBar));
    // 2 black knobs hanging down at evenly-spaced z positions
    const knobR = 0.01;
    for (let i = 1; i <= 2; i++) {
      const kz = hb.z1 + (hb.z2 - hb.z1) * i / 3;
      const knob = new THREE.Mesh(new THREE.SphereGeometry(knobR, 10, 8), knobMat);
      knob.position.set(barCx, hb.y - hb.h / 2 - knobR - 0.01, kz);
      g.add(knob);
    }

    // closet: offwhite panel + vertical seam + 2 silver handles
    const c = CLOSET;
    wallFeature(g, 'x', 0, +1,
      { a1: c.z1, a2: c.z2, b1: c.y1, b2: c.y1 + c.h }, closetMat);
    const seamZ = (c.z1 + c.z2) / 2;
    wallFeature(g, 'x', 0, +1,
      { a1: seamZ - 0.0025, a2: seamZ + 0.0025, b1: c.y1, b2: c.y1 + c.h }, seamMat);
    // 2 silver handles at y=1.0, one on each side of the seam
    const cHd = 0.025, cHh = 0.10, cHw = 0.04;
    for (const z of [seamZ - 0.06, seamZ + 0.06]) {
      const h = new THREE.Mesh(new THREE.BoxGeometry(cHd, cHh, cHw), handleMat);
      h.position.set(BIAS + cHd / 2, 1.0, z);
      g.add(h);
    }

    // frosted window with frame
    const fw = FROSTED_WINDOW;
    const a1 = fw.z1, a2 = fw.z2;
    const b1 = fw.sillY, b2 = fw.sillY + fw.h;
    wallFeature(g, 'x', 0, +1, { a1, a2, b1, b2 }, frostedMat);
    windowFrame(g, 'x', 0, +1, a1, a2, b1, b2, frameMat);
  }

  // --- ac-wall (z=D): ac unit only (white box protruding into room) ---
  {
    const ac = AC_UNIT;
    g.add(boxMesh(
      ac.x2 - ac.x1, ac.h, ac.d,
      (ac.x1 + ac.x2) / 2, ac.y + ac.h / 2, D - BIAS - ac.d / 2,
      COLOR.white
    ));
  }

  return g;
}
