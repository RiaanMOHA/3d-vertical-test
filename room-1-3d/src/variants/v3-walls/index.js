import { ROOM, CAMERA } from './constants.js';
import { buildRoom } from './room.js';
import { buildFurniture } from './furniture.js';

export { ROOM, CAMERA };
export const LABEL = 'v3 walls (remap)';

export function buildScene(parent) {
  buildRoom(parent);
  buildFurniture(parent);
}
