const colors = [
  ['Baja', '#9fcbe0'], ['Media', '#3183bd'], ['Alta', '#09529c'],
];

// Extent returned by the source's PNG export in EPSG:3857.
const extent = [-8873291.675952379, -248305.16, -8819828.194047617, -178134.34];
const earthRadius = 6378137;

function unproject(x, y) {
  return [x / earthRadius * 180 / Math.PI,
    Math.atan(Math.sinh(y / earthRadius)) * 180 / Math.PI];
}

export function mountFloodSusceptibility(panel, { project, layer }) {
  const legend = panel.querySelector('#flood-legend');
  const status = panel.querySelector('#flood-status');
  for (const [label, color] of colors) {
    const item = document.createElement('li');
    const swatch = document.createElement('span');
    swatch.style.backgroundColor = color;
    item.append(swatch, label);
    legend.append(item);
  }
  const [west, south, east, north] = extent;
  const [x, y] = project(unproject(west, north));
  const [right, bottom] = project(unproject(east, south));
  const image = document.createElementNS('http://www.w3.org/2000/svg', 'image');
  for (const [key, value] of Object.entries({
    x, y, width: right - x, height: bottom - y, opacity: .75, preserveAspectRatio: 'none',
  })) image.setAttribute(key, value);
  image.addEventListener('error', () => { status.textContent = 'No se pudo cargar la capa.'; });
  layer.append(image);
  return visible => {
    panel.hidden = !visible;
    layer.toggleAttribute('hidden', !visible);
    if (visible && !image.hasAttribute('href')) {
      image.setAttribute('href', new URL('./babahoyo-flood-2024.png', import.meta.url).href);
    }
  };
}
