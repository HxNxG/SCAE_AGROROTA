const MAX_LATITUDE = 85.05112878;
const TILE_SIZE = 256;
const SVG = 'http://www.w3.org/2000/svg';
export const SATELLITE_DATE = '2025-09-07';
const GIBS_TILES = 'https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_CorrectedReflectance_TrueColor';

// Both OSM tiles and the interactive layers use this normalized Web Mercator space.
export function toWorld([longitude, latitude]) {
  const radians = Math.max(-MAX_LATITUDE, Math.min(MAX_LATITUDE, latitude)) * Math.PI / 180;
  return [(longitude + 180) / 360, (1 - Math.asinh(Math.tan(radians)) / Math.PI) / 2];
}

export function fromWorld([x, y]) {
  return [x * 360 - 180, Math.atan(Math.sinh(Math.PI * (1 - 2 * y))) * 180 / Math.PI];
}

export function mountBasemap(group, status) {
  const displayed = new Map();

  function updateStatus() {
    status.hidden = !displayed.size || [...displayed.values()].some(tile => !tile.failed);
  }

  return function update(worldBounds, pixelsPerWorld, toView, satellite) {
    const [west, north, east, south] = worldBounds;
    const z = Math.max(0, Math.min(satellite ? 9 : 19, Math.round(Math.log2(pixelsPerWorld / TILE_SIZE))));
    const count = 2 ** z;
    const xStart = Math.max(0, Math.floor(west * count));
    const yStart = Math.max(0, Math.floor(north * count));
    const xEnd = Math.min(count - 1, Math.ceil(east * count) - 1);
    const yEnd = Math.min(count - 1, Math.ceil(south * count) - 1);
    const visible = new Set();

    for (let row = yStart; row <= yEnd; row++) {
      for (let column = xStart; column <= xEnd; column++) {
        const key = satellite
          ? `${GIBS_TILES}/default/${SATELLITE_DATE}/GoogleMapsCompatible_Level9/${z}/${row}/${column}.jpg`
          : `https://tile.openstreetmap.org/${z}/${column}/${row}.png`;
        visible.add(key);
        if (displayed.has(key)) continue;
        const [x, y] = toView([column / count, row / count]);
        const [right, bottom] = toView([(column + 1) / count, (row + 1) / count]);
        const image = document.createElementNS(SVG, 'image');
        image.setAttribute('x', x);
        image.setAttribute('y', y);
        image.setAttribute('width', right - x);
        image.setAttribute('height', bottom - y);
        image.setAttribute('preserveAspectRatio', 'none');
        const tile = { image, failed: false };
        displayed.set(key, tile);
        image.addEventListener('error', () => {
          tile.failed = true;
          image.remove();
          updateStatus();
        }, { once: true });
        image.setAttribute('href', key);
        group.append(image);
      }
    }

    for (const [key, tile] of displayed) {
      if (visible.has(key)) continue;
      tile.image.remove();
      displayed.delete(key);
    }
    updateStatus();
  };
}
