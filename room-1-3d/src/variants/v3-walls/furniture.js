import * as THREE from 'three';
import { COLOR, BED, DESK, SHELF, CHAIR, PENDANT } from './constants.js';

function boxMesh(w, h, d, cx, cy, cz, color, extra = {}) {
  const mat = new THREE.MeshStandardMaterial({
    color,
    roughness: extra.roughness ?? 0.8,
    metalness: extra.metalness ?? 0,
    emissive: extra.emissive ?? 0x000000,
    emissiveIntensity: extra.emissiveIntensity ?? 0,
  });
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
  m.position.set(cx, cy, cz);
  return m;
}

function aabb(r, color, extra) {
  return boxMesh(
    r.x2 - r.x1, r.y2 - r.y1, r.z2 - r.z1,
    (r.x1 + r.x2) / 2, (r.y1 + r.y2) / 2, (r.z1 + r.z2) / 2,
    color, extra
  );
}

const IRON      = { roughness: 0.45, metalness: 0.6 };
const BLACK_MET = { roughness: 0.5,  metalness: 0.6 };

// Metal-frame headboard / footboard: top rail + bottom rail + N vertical bars.
function metalFrame(group, panel, topRail, botRail, nBars) {
  const w  = panel.x2 - panel.x1;
  const d  = panel.z2 - panel.z1;
  const cx = (panel.x1 + panel.x2) / 2;
  const cz = (panel.z1 + panel.z2) / 2;
  // top rail
  group.add(boxMesh(w, topRail.y2 - topRail.y1, d, cx,
    (topRail.y1 + topRail.y2) / 2, cz, COLOR.ironDark, IRON));
  // bottom rail
  group.add(boxMesh(w, botRail.y2 - botRail.y1, d, cx,
    (botRail.y1 + botRail.y2) / 2, cz, COLOR.ironDark, IRON));
  // vertical bars between rails
  const barT  = 0.03;
  const barH  = topRail.y1 - botRail.y2;
  const barCy = (topRail.y1 + botRail.y2) / 2;
  for (let i = 0; i < nBars; i++) {
    const t = nBars === 1 ? 0.5 : i / (nBars - 1);
    const z = panel.z1 + (panel.z2 - panel.z1) * t;
    group.add(boxMesh(barT, barH, barT, cx, barCy, z, COLOR.ironDark, IRON));
  }
}

// Thin diagonal rod between two world-space points (for shelf x-bracing).
function diagonalRod(start, end, color) {
  const dir = new THREE.Vector3().subVectors(end, start);
  const len = dir.length();
  const geom = new THREE.CylinderGeometry(0.005, 0.005, len, 8);
  const mat  = new THREE.MeshStandardMaterial({
    color, metalness: 0.6, roughness: 0.5,
  });
  const m = new THREE.Mesh(geom, mat);
  m.position.copy(start).add(dir.clone().multiplyScalar(0.5));
  m.quaternion.setFromUnitVectors(
    new THREE.Vector3(0, 1, 0),
    dir.clone().normalize()
  );
  return m;
}

export function buildFurniture(scene) {
  const g = new THREE.Group();
  g.name = 'furniture';
  scene.add(g);

  // ---- BED: mattress + metal-frame headboard + metal-frame footboard ----
  g.add(aabb(BED.mattress, COLOR.mattress));
  metalFrame(g, BED.headboard,
    { y1: 0.98, y2: 1.00 }, { y1: 0.53, y2: 0.55 }, 5);
  metalFrame(g, BED.footboard,
    { y1: 0.68, y2: 0.70 }, { y1: 0.53, y2: 0.55 }, 3);

  // ---- DESK ----
  {
    const f = DESK.footprint;
    const w = f.x2 - f.x1;
    const d = f.z2 - f.z1;
    const cx = (f.x1 + f.x2) / 2;
    const cz = (f.z1 + f.z2) / 2;
    const topCenterY = DESK.topY - DESK.topThick / 2;
    g.add(boxMesh(w, DESK.topThick, d, cx, topCenterY, cz, COLOR.deskWood));
    const legH = DESK.topY - DESK.topThick;
    for (const lx of [f.x1 + DESK.legThick / 2, f.x2 - DESK.legThick / 2]) {
      for (const lz of [f.z1 + DESK.legThick / 2, f.z2 - DESK.legThick / 2]) {
        g.add(boxMesh(DESK.legThick, legH, DESK.legThick, lx, legH / 2, lz,
          COLOR.blackMet, BLACK_MET));
      }
    }
  }

  // ---- SHELF: 4 posts + 4 tiers + x-bracing on each side face ----
  {
    const f = SHELF.footprint;
    const w = f.x2 - f.x1;
    const d = f.z2 - f.z1;
    const cx = (f.x1 + f.x2) / 2;
    const cz = (f.z1 + f.z2) / 2;
    for (const px of [f.x1 + SHELF.postThick / 2, f.x2 - SHELF.postThick / 2]) {
      for (const pz of [f.z1 + SHELF.postThick / 2, f.z2 - SHELF.postThick / 2]) {
        g.add(boxMesh(SHELF.postThick, SHELF.h, SHELF.postThick,
          px, SHELF.h / 2, pz, COLOR.blackMet, BLACK_MET));
      }
    }
    for (const y of SHELF.tierYs) {
      g.add(boxMesh(w, SHELF.tierThick, d, cx, y, cz, COLOR.deskWood));
    }
    // X-bracing on the two side faces (z=f.z1 and z=f.z2)
    const yLo = SHELF.tierYs[0];
    const yHi = SHELF.tierYs[3];
    const xLo = f.x1 + SHELF.postThick / 2;
    const xHi = f.x2 - SHELF.postThick / 2;
    for (const faceZ of [f.z1, f.z2]) {
      g.add(diagonalRod(
        new THREE.Vector3(xLo, yLo, faceZ),
        new THREE.Vector3(xHi, yHi, faceZ),
        COLOR.blackMet
      ));
      g.add(diagonalRod(
        new THREE.Vector3(xLo, yHi, faceZ),
        new THREE.Vector3(xHi, yLo, faceZ),
        COLOR.blackMet
      ));
    }
  }

  // ---- CHAIR ----
  {
    const f = CHAIR.footprint;
    const w = f.x2 - f.x1;
    const d = f.z2 - f.z1;
    const cx = (f.x1 + f.x2) / 2;
    const cz = (f.z1 + f.z2) / 2;
    const seatCy = CHAIR.seatY - CHAIR.seatThick / 2;
    g.add(boxMesh(w, CHAIR.seatThick, d, cx, seatCy, cz, COLOR.chairSeat));
    const backCx = f.x1 + CHAIR.backThick / 2;
    const backCy = CHAIR.seatY + CHAIR.backH / 2;
    g.add(boxMesh(CHAIR.backThick, CHAIR.backH, d, backCx, backCy, cz, COLOR.chairSeat));
    const pedH = CHAIR.seatY - CHAIR.seatThick - CHAIR.baseThick;
    g.add(boxMesh(
      CHAIR.pedestalThick, pedH, CHAIR.pedestalThick,
      cx, CHAIR.baseThick + pedH / 2, cz,
      COLOR.blackMet, BLACK_MET
    ));
    g.add(boxMesh(
      w * 0.9, CHAIR.baseThick, d * 0.9, cx, CHAIR.baseThick / 2, cz,
      COLOR.blackMet, BLACK_MET
    ));
  }

  // ---- PENDANT ----
  {
    const p = PENDANT;
    const barCenterY = p.frameY - p.frameBarThick / 2;
    g.add(boxMesh(p.frameBarL, p.frameBarThick, p.frameBarThick,
      p.cx, barCenterY, p.cz, COLOR.pendantWood));
    g.add(boxMesh(p.frameBarThick, p.frameBarThick, p.frameBarL,
      p.cx, barCenterY, p.cz, COLOR.pendantWood));
    const shadeMat = new THREE.MeshStandardMaterial({
      color: COLOR.pendantShade,
      emissive: COLOR.pendantShade,
      emissiveIntensity: 0.7,
      roughness: 0.7,
    });
    const shadeGeom = new THREE.CylinderGeometry(
      p.shadeDia / 2, p.shadeDia / 2, p.shadeH, 20);
    const shadeCenterY = p.shadeBottomY + p.shadeH / 2;
    for (const dx of [-p.shadeOffset, p.shadeOffset]) {
      for (const dz of [-p.shadeOffset, p.shadeOffset]) {
        const shade = new THREE.Mesh(shadeGeom, shadeMat);
        shade.position.set(p.cx + dx, shadeCenterY, p.cz + dz);
        g.add(shade);
      }
    }
  }

  return g;
}
