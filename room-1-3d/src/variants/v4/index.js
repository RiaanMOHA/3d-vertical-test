import { ROOM, CAMERA } from './constants.js';
import { buildRoom } from './room.js';
import { buildFurniture } from './furniture.js';

export { ROOM, CAMERA };
export const LABEL = 'v4 map fix';

export function buildScene(parent) {
  buildRoom(parent);
  buildFurniture(parent);
}
