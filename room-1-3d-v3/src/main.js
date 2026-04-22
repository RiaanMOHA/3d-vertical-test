import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import { ROOM, CAMERA } from './constants.js';
import { buildRoom } from './room.js';
import { buildFurniture } from './furniture.js';

// ---------- renderer / scene / camera ----------
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1b1f);

const camera = new THREE.PerspectiveCamera(
  60, window.innerWidth / window.innerHeight, 0.02, 100);
camera.position.set(...CAMERA.orbitInitial);

// ---------- lighting (spec: ambient + directional, no point lights) ----------
scene.add(new THREE.AmbientLight(0xffffff, 0.6));
const dir = new THREE.DirectionalLight(0xffffff, 0.4);
dir.position.set(5, 8, 3);
const dirTarget = new THREE.Object3D();
dirTarget.position.set(ROOM.W / 2, 1.0, ROOM.D / 2);
scene.add(dirTarget);
dir.target = dirTarget;
scene.add(dir);

// ---------- scene content ----------
buildRoom(scene);
buildFurniture(scene);

// ---------- orbit controls (available via M toggle) ----------
const orbit = new OrbitControls(camera, renderer.domElement);
orbit.target.set(...CAMERA.orbitTarget);
orbit.enableDamping = true;
orbit.dampingFactor = 0.08;
orbit.minDistance = 0.4;
orbit.maxDistance = 20;
orbit.enabled = false;
orbit.update();

// Mac-trackpad phantom-zoom guard: ignore wheel during drag and 400ms after.
let lastOrbitEnd = 0;
let orbitDragging = false;
orbit.addEventListener('start', () => { orbitDragging = true; });
orbit.addEventListener('end',   () => { orbitDragging = false; lastOrbitEnd = performance.now(); });
renderer.domElement.addEventListener('wheel', (e) => {
  if (orbitDragging || (performance.now() - lastOrbitEnd) < 400) {
    e.stopImmediatePropagation();
    e.preventDefault();
  }
}, { capture: true, passive: false });

// ---------- walk controls (click-drag look, no pointer lock) ----------
// Cursor stays visible so Cmd+Shift+4 works for screenshots.
const modeVal = document.getElementById('mode-val');
let mode = 'walk';
const keys = new Set();
const walkSpeed = 2.2; // m/s
let walkYaw = 0;
let walkPitch = 0;
const PITCH_LIM = Math.PI / 2 - 0.05;
let dragging = false;
let dragLast = { x: 0, y: 0 };

function enterWalk() {
  orbit.enabled = false;
  camera.position.set(...CAMERA.walkStart);
  camera.lookAt(...CAMERA.walkLookAt);
  camera.rotation.reorder('YXZ');
  walkYaw = camera.rotation.y;
  walkPitch = camera.rotation.x;
  mode = 'walk';
  modeVal.textContent = 'walk';
  document.body.classList.add('walk');
}

function enterOrbit() {
  orbit.enabled = true;
  orbit.target.set(...CAMERA.orbitTarget);
  camera.position.set(...CAMERA.orbitInitial);
  orbit.update();
  mode = 'orbit';
  modeVal.textContent = 'orbit';
  document.body.classList.remove('walk');
}

function setMode(next) {
  if (mode === next) return;
  if (next === 'walk') enterWalk(); else enterOrbit();
}

function applyWalkRotation() {
  // yaw around y, then pitch around x. Apply via Euler for intuitive FP look.
  camera.rotation.order = 'YXZ';
  camera.rotation.y = walkYaw;
  camera.rotation.x = walkPitch;
  camera.rotation.z = 0;
}

// Click-drag on canvas to look around in walk mode.
renderer.domElement.addEventListener('mousedown', (e) => {
  if (mode !== 'walk') return;
  dragging = true;
  dragLast.x = e.clientX;
  dragLast.y = e.clientY;
});
window.addEventListener('mousemove', (e) => {
  if (!dragging || mode !== 'walk') return;
  const dx = e.clientX - dragLast.x;
  const dy = e.clientY - dragLast.y;
  dragLast.x = e.clientX;
  dragLast.y = e.clientY;
  walkYaw   -= dx * 0.004;
  walkPitch -= dy * 0.004;
  walkPitch = Math.max(-PITCH_LIM, Math.min(PITCH_LIM, walkPitch));
  applyWalkRotation();
});
window.addEventListener('mouseup', () => { dragging = false; });

window.addEventListener('keydown', (e) => {
  if (e.code === 'KeyM') {
    setMode(mode === 'walk' ? 'orbit' : 'walk');
    return;
  }
  if (e.code === 'Escape' && mode === 'walk') {
    setMode('orbit');
    return;
  }
  if (mode === 'walk') keys.add(e.code);
});
window.addEventListener('keyup', (e) => { keys.delete(e.code); });

// ---------- resize ----------
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// ---------- animation loop ----------
const clock = new THREE.Clock();
function tick() {
  const dt = Math.min(clock.getDelta(), 0.08);

  if (mode === 'walk') {
    const f = new THREE.Vector3();
    camera.getWorldDirection(f);
    f.y = 0;
    f.normalize();
    const r = new THREE.Vector3(f.z, 0, -f.x);
    let dx = 0, dz = 0;
    if (keys.has('KeyW') || keys.has('ArrowUp'))    { dx += f.x; dz += f.z; }
    if (keys.has('KeyS') || keys.has('ArrowDown'))  { dx -= f.x; dz -= f.z; }
    if (keys.has('KeyD') || keys.has('ArrowRight')) { dx += r.x; dz += r.z; }
    if (keys.has('KeyA') || keys.has('ArrowLeft'))  { dx -= r.x; dz -= r.z; }
    const m = Math.hypot(dx, dz);
    if (m > 0) {
      const s = walkSpeed * dt / m;
      camera.position.x += dx * s;
      camera.position.z += dz * s;
    }
    camera.position.y = CAMERA.walkEyeY;
  } else {
    orbit.update();
  }

  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
enterWalk();
tick();
