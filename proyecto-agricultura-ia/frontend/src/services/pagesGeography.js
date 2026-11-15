export const isPublicMap = globalThis.document?.documentElement.dataset.mode === 'pages';

let boundaryRequest;

export function loadPublicBoundary() {
  boundaryRequest ??= fetch(new URL('../../cartography/babahoyo.geojson', import.meta.url))
    .then(response => {
      if (!response.ok) throw new Error('Límite de Babahoyo no disponible');
      return response.json();
    })
    .catch(error => {
      boundaryRequest = undefined;
      throw error;
    });
  return boundaryRequest;
}

function contains(ring, [x, y]) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [ax, ay] = ring[j];
    const [bx, by] = ring[i];
    const cross = (x - ax) * (by - ay) - (y - ay) * (bx - ax);
    if (Math.abs(cross) < 1e-11 && x >= Math.min(ax, bx) && x <= Math.max(ax, bx)
      && y >= Math.min(ay, by) && y <= Math.max(ay, by)) return true;
    if ((ay > y) !== (by > y) && x < (bx - ax) * (y - ay) / (by - ay) + ax) inside = !inside;
  }
  return inside;
}

export async function validatePublicPoint({ longitude, latitude }, signal) {
  if (!Number.isFinite(longitude) || Math.abs(longitude) > 180 ||
      !Number.isFinite(latitude) || Math.abs(latitude) > 90) throw new TypeError('Coordenadas inválidas');
  const { geometry } = await loadPublicBoundary();
  signal?.throwIfAborted();
  const coordinates = [longitude, latitude];
  const polygons = geometry.type === 'MultiPolygon' ? geometry.coordinates : [geometry.coordinates];
  const accepted = polygons.some(([exterior, ...holes]) =>
    contains(exterior, coordinates) && !holes.some(hole => contains(hole, coordinates)));
  return accepted
    ? { accepted, point: { type: 'Point', coordinates }, message: 'Ubicación dentro del límite de referencia de Babahoyo.' }
    : { accepted, message: 'Ubicación fuera del límite de referencia de Babahoyo.' };
}
