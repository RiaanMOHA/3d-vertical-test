import * as THREE from 'three';
import {
  ROOM, COLOR,
  SLIDING_WINDOW, DOOR, CLOSET, AC_UNIT, FROSTED_WINDOW,
  BASEBOARD_HEIGHT, BASEBOARD_DEPTH, CASING_WIDTH, CASING_DEPTH,
} from './constants.js';
import { pbrMaterial } from './textures.js';

const WT      = 0.02;
const FEAT    = 0.02;
const BIAS    = 0.003;
const FRAME_T = 0.04;

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

function windowFrame(group, wallAxis, wallInnerCoord, inward, a1, a2, b1, b2, mat) {
  const t = FRAME_T;
  wallFeature(group, wallAxis, wallInnerCoord, inward,
    { a1: a1 - t, a2: a2 + t, b1: b2,     b2: b2 + t }, mat);
  wallFeature(group, wallAxis, wallInnerCoord, inward,
    { a1: a1 - t, a2: a2 + t, b1: b1 - t, b2: b1     }, mat);
  wallFeature(group, wallAxis, wallInnerCoord, inward,
    { a1: a1 - t, a2: a1,     b1: b1,     b2: b2     }, mat);
  wallFeature(group, wallAxis, wallInnerCoord, inward,
    { a1: a2,     a2: a2 + t, b1: b1,     b2: b2     }, mat);
}

export function buildRoom(scene) {
  const g = new THREE.Group();
  g.name = 'room';
  scene.add(g);

  const { W, D, H } = ROOM;

  const glassMat = new THREE.MeshStandardMaterial({
    color: 0xb8d4e0, transparent: true, opacity: 0.35, roughness: 0.1,
  });
  const frostedMat = new THREE.MeshStandardMaterial({
    color: 0xe8e8e0, transparent: true, opacity: 0.75, roughness: 0.95,
  });
  const closetMat = new THREE.MeshStandardMaterial({ color: 0xf2ece4, roughness: 0.7 });
  const frameMat  = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 });
  const handleMat = new THREE.MeshStandardMaterial({
    color: 0x999999, metalness: 0.7, roughness: 0.3,
  });
  const seamMat   = new THREE.MeshStandardMaterial({ color: 0xbababa });

  // ----- floor (oak parquet, 1.7m source) -----
  {
    const mat = pbrMaterial('wood_floor', W / 1.7, D / 1.7, { roughness: 0.85 });
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(W, 0.02, D), mat);
    mesh.position.set(W / 2, -0.01, D / 2);
    g.add(mesh);
  }

  // ----- ceiling (plaster) -----
  {
    const mat = pbrMaterial('painted_plaster_wall', W / 2, D / 2, { roughness: 0.9 });
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(W, 0.02, D), mat);
    mesh.position.set(W / 2, H + 0.01, D / 2);
    g.add(mesh);
  }

  // ----- walls (plaster, per-wall tiling) -----
  {
    // cabinet-wall (x=0)
    const m1 = pbrMaterial('painted_plaster_wall', D / 2, H / 2);
    const w1 = new THREE.Mesh(new THREE.BoxGeometry(WT, H, D), m1);
    w1.position.set(-WT / 2, H / 2, D / 2);
    g.add(w1);

    // window-wall (x=W)
    const m2 = pbrMaterial('painted_plaster_wall', D / 2, H / 2);
    const w2 = new THREE.Mesh(new THREE.BoxGeometry(WT, H, D), m2);
    w2.position.set(W + WT / 2, H / 2, D / 2);
    g.add(w2);

    // entrance-wall (z=0)
    const m3 = pbrMaterial('painted_plaster_wall', W / 2, H / 2);
    const w3 = new THREE.Mesh(new THREE.BoxGeometry(W, H, WT), m3);
    w3.position.set(W / 2, H / 2, -WT / 2);
    g.add(w3);

    // ac-wall (z=D)
    const m4 = pbrMaterial('painted_plaster_wall', W / 2, H / 2);
    const w4 = new THREE.Mesh(new THREE.BoxGeometry(W, H, WT), m4);
    w4.position.set(W / 2, H / 2, D + WT / 2);
    g.add(w4);
  }

  // ----- baseboards (4 walls) -----
  {
    const bbH = BASEBOARD_HEIGHT;
    const bbD = BASEBOARD_DEPTH;
    const bbColor = 0xf2f0eb;
    const bbExtra = { roughness: 0.7 };
    // cabinet-wall (x=0): protrudes in +x
    g.add(boxMesh(bbD, bbH, D, bbD / 2, bbH / 2, D / 2, bbColor, bbExtra));
    // window-wall (x=W): protrudes in -x
    g.add(boxMesh(bbD, bbH, D, W - bbD / 2, bbH / 2, D / 2, bbColor, bbExtra));
    // entrance-wall (z=0): protrudes in +z
    g.add(boxMesh(W, bbH, bbD, W / 2, bbH / 2, bbD / 2, bbColor, bbExtra));
    // ac-wall (z=D): protrudes in -z
    g.add(boxMesh(W, bbH, bbD, W / 2, bbH / 2, D - bbD / 2, bbColor, bbExtra));
  }

  // ====== wall features ======

  // --- window-wall (x=W): sliding window (centered on z=1.0, above new desk) ---
  {
    const sw = SLIDING_WINDOW;
    const a1 = sw.z1;
    const a2 = sw.z2;
    const b1 = sw.sillY;
    const b2 = sw.sillY + sw.h;
    wallFeature(g, 'x', W, -1, { a1, a2, b1, b2 }, glassMat);
    windowFrame(g, 'x', W, -1, a1, a2, b1, b2, frameMat);
  }

  // --- entrance-wall (z=0): dark doorway + 3-piece casing (door panel in furniture.js) ---
  {
    const d = DOOR;
    // dark doorway (suggests hallway beyond)
    wallFeature(g, 'z', 0, +1,
      { a1: d.x1, a2: d.x2, b1: d.y1, b2: d.y1 + d.h }, COLOR.doorway);

    // casing: 3 pieces, light white, protrudes CASING_DEPTH from wall
    const cD = CASING_DEPTH;
    const cW = CASING_WIDTH;
    const cZ = cD / 2 + BIAS;
    const casingColor = 0xfafafa;
    const casingExtra = { roughness: 0.6 };
    // top: x=0 to 0.86, y=2.0 to 2.06
    g.add(boxMesh(
      d.x2 + cW, cW, cD,
      (d.x2 + cW) / 2, d.y1 + d.h + cW / 2, cZ,
      casingColor, casingExtra
    ));
    // left (clamped to room side): x=0 to 0.06, y=0 to 2.06
    g.add(boxMesh(
      cW, d.h + cW, cD,
      cW / 2, (d.h + cW) / 2, cZ,
      casingColor, casingExtra
    ));
    // right: x=0.8 to 0.86, y=0 to 2.06
    g.add(boxMesh(
      cW, d.h + cW, cD,
      d.x2 + cW / 2, (d.h + cW) / 2, cZ,
      casingColor, casingExtra
    ));
  }

  // --- cabinet-wall (x=0): closet only ---
  {
    const c = CLOSET;
    wallFeature(g, 'x', 0, +1,
      { a1: c.z1, a2: c.z2, b1: c.y1, b2: c.y1 + c.h }, closetMat);
    const seamZ = (c.z1 + c.z2) / 2;
    wallFeature(g, 'x', 0, +1,
      { a1: seamZ - 0.0025, a2: seamZ + 0.0025, b1: c.y1, b2: c.y1 + c.h }, seamMat);
    const cHd = 0.025, cHh = 0.10, cHw = 0.04;
    for (const z of [seamZ - 0.06, seamZ + 0.06]) {
      const h = new THREE.Mesh(new THREE.BoxGeometry(cHd, cHh, cHw), handleMat);
      h.position.set(BIAS + cHd / 2, 1.0, z);
      g.add(h);
    }
  }

  // --- ac-wall (z=D): ac unit + frosted window ---
  {
    const ac = AC_UNIT;
    g.add(boxMesh(
      ac.x2 - ac.x1, ac.h, ac.d,
      (ac.x1 + ac.x2) / 2, ac.y + ac.h / 2, D - BIAS - ac.d / 2,
      COLOR.white
    ));

    const fw = FROSTED_WINDOW;
    const a1 = fw.x1, a2 = fw.x2;
    const b1 = fw.sillY, b2 = fw.sillY + fw.h;
    wallFeature(g, 'z', D, -1, { a1, a2, b1, b2 }, frostedMat);
    windowFrame(g, 'z', D, -1, a1, a2, b1, b2, frameMat);
  }

  return g;
}
