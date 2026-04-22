import {
  TextureLoader, RepeatWrapping, SRGBColorSpace, MeshStandardMaterial
} from 'three';

const loader = new TextureLoader();
const cache = new Map();

function loadSet(slug) {
  if (cache.has(slug)) return cache.get(slug);
  const base = `/textures/${slug}/${slug}`;
  const map = loader.load(`${base}_diff.jpg`);
  map.colorSpace = SRGBColorSpace;
  const normalMap = loader.load(`${base}_nor_gl.jpg`);
  const roughnessMap = loader.load(`${base}_rough.jpg`);
  [map, normalMap, roughnessMap].forEach(t => {
    t.wrapS = RepeatWrapping;
    t.wrapT = RepeatWrapping;
  });
  cache.set(slug, { map, normalMap, roughnessMap });
  return cache.get(slug);
}

export function pbrMaterial(slug, repeatU = 1, repeatV = 1, extras = {}) {
  const set = loadSet(slug);
  // clone textures so each material can have its own repeat
  const map = set.map.clone();
  const normalMap = set.normalMap.clone();
  const roughnessMap = set.roughnessMap.clone();
  [map, normalMap, roughnessMap].forEach(t => {
    t.wrapS = RepeatWrapping;
    t.wrapT = RepeatWrapping;
    t.repeat.set(repeatU, repeatV);
    t.needsUpdate = true;
  });
  map.colorSpace = SRGBColorSpace;
  return new MeshStandardMaterial({ map, normalMap, roughnessMap, ...extras });
}
