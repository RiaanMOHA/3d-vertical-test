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

// Expand {x1,x2,z1,z2,y1,y2} -> box at correct position / size.
function aabb(r, color, extra) {
  return boxMesh(
    r.x2 - r.x1, r.y2 - r.y1, r.z2 - r.z1,
    (r.x1 + r.x2) / 2, (r.y1 + r.y2) / 2, (r.z1 + r.z2) / 2,
    color, extra
  );
}

export function buildFurniture(scene) {
  const g = new THREE.Group();
  g.name = 'furniture';
  scene.add(g);

  // ---- BED: long side against ac-wall, head at corner-ac-window ----
  g.add(aabb(BED.mattress,  COLOR.mattress));
  g.add(aabb(BED.headboard, COLOR.ironDark, { roughness: 0.45, metalness: 0.6 }));
  g.add(aabb(BED.footboard, COLOR.ironDark, { roughness: 0.45, metalness: 0.6 }));

  // ---- DESK: top + 4 legs, under sliding window ----
  {
    const f = DESK.footprint;
    const w = f.x2 - f.x1;
    const d = f.z2 - f.z1;
    const cx = (f.x1 + f.x2) / 2;
    const cz = (f.z1 + f.z2) / 2;
    const topCenterY = DESK.topY - DESK.topThick / 2;
    g.add(boxMesh(w, DESK.topThick, d, cx, topCenterY, cz, COLOR.deskWood));

    // 4 legs (black metal) at the four footprint corners
    const legH = DESK.topY - DESK.topThick;
    for (const lx of [f.x1 + DESK.legThick / 2, f.x2 - DESK.legThick / 2]) {
      for (const lz of [f.z1 + DESK.legThick / 2, f.z2 - DESK.legThick / 2]) {
        g.add(boxMesh(DESK.legThick, legH, DESK.legThick, lx, legH / 2, lz,
          COLOR.blackMet, { metalness: 0.6, roughness: 0.5 }));
      }
    }
  }

  // ---- SHELF: 4 posts + 4 wood tiers in corner-cabinet-window ----
  {
    const f = SHELF.footprint;
    const w = f.x2 - f.x1;
    const d = f.z2 - f.z1;
    const cx = (f.x1 + f.x2) / 2;
    const cz = (f.z1 + f.z2) / 2;
    // 4 black metal posts at corners
    for (const px of [f.x1 + SHELF.postThick / 2, f.x2 - SHELF.postThick / 2]) {
      for (const pz of [f.z1 + SHELF.postThick / 2, f.z2 - SHELF.postThick / 2]) {
        g.add(boxMesh(SHELF.postThick, SHELF.h, SHELF.postThick,
          px, SHELF.h / 2, pz, COLOR.blackMet, { metalness: 0.6, roughness: 0.5 }));
      }
    }
    // 4 reddish-brown wood tiers
    for (const y of SHELF.tierYs) {
      g.add(boxMesh(w, SHELF.tierThick, d, cx, y, cz, COLOR.deskWood));
    }
  }

  // ---- CHAIR: seat + backrest + pedestal + base, facing window-wall (+x) ----
  {
    const f = CHAIR.footprint;
    const w = f.x2 - f.x1;
    const d = f.z2 - f.z1;
    const cx = (f.x1 + f.x2) / 2;
    const cz = (f.z1 + f.z2) / 2;

    // seat top surface at CHAIR.seatY (=0.5)
    const seatCy = CHAIR.seatY - CHAIR.seatThick / 2;
    g.add(boxMesh(w, CHAIR.seatThick, d, cx, seatCy, cz, COLOR.chairSeat));

    // backrest on the -x side (so the chair faces +x toward window-wall)
    const backCx = f.x1 + CHAIR.backThick / 2;
    const backCy = CHAIR.seatY + CHAIR.backH / 2;
    g.add(boxMesh(CHAIR.backThick, CHAIR.backH, d, backCx, backCy, cz, COLOR.chairSeat));

    // pedestal post (black metal) from base up to underside of seat
    const pedH = CHAIR.seatY - CHAIR.seatThick - CHAIR.baseThick;
    g.add(boxMesh(
      CHAIR.pedestalThick, pedH, CHAIR.pedestalThick,
      cx, CHAIR.baseThick + pedH / 2, cz,
      COLOR.blackMet, { metalness: 0.6, roughness: 0.5 }
    ));

    // flat square base (black metal)
    g.add(boxMesh(
      w * 0.9, CHAIR.baseThick, d * 0.9, cx, CHAIR.baseThick / 2, cz,
      COLOR.blackMet, { metalness: 0.6, roughness: 0.5 }
    ));
  }

  // ---- PENDANT: wood cross frame + 4 cylindrical linen shades ----
  {
    const p = PENDANT;
    // wood cross bar (two crossed planks) pressed against ceiling
    const barCenterY = p.frameY - p.frameBarThick / 2;
    g.add(boxMesh(p.frameBarL, p.frameBarThick, p.frameBarThick,
      p.cx, barCenterY, p.cz, COLOR.pendantWood));
    g.add(boxMesh(p.frameBarThick, p.frameBarThick, p.frameBarL,
      p.cx, barCenterY, p.cz, COLOR.pendantWood));

    // 4 shades — emissive linen, NO point light
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
