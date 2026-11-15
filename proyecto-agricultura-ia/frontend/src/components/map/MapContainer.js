import { fromWorld, mountBasemap, SATELLITE_DATE, toWorld } from './Basemap.js';
import { isPublicMap, loadPublicBoundary } from '../../services/pagesGeography.js';

const WIDTH = 640;
const HEIGHT = 440;
const PAD = 24;
const MAX_ZOOM = 8;
const ZOOM_STEP = 1.5;
// WGS 84 locality references: https://ec.micodigopostal.info/distrito/los-rios-babahoyo
const pointsOfInterest = [
  ['Pimocha', '120154', [-79.600000, -1.833333]],
  ['Caracol', '120152', [-79.463188, -1.670986]],
  ['La Unión', '120155', [-79.466667, -1.783333]],
  ['Febres Cordero', '120153', [-79.307800, -1.965183]],
];

export async function mountMap(container, controls, onPointChange) {
  const [boundary, parishResponse] = await Promise.all([
    isPublicMap ? loadPublicBoundary() : fetch(new URL('./babahoyo-display.json', import.meta.url))
      .then(response => {
        if (!response.ok) throw new Error('Límite de referencia no disponible');
        return response.json();
      }),
    fetch(new URL(isPublicMap ? '../../../cartography/parroquias.geojson' : './babahoyo-parroquias-2023.json',
      import.meta.url)).catch(() => null),
  ]);
  const parishes = parishResponse?.ok ? (await parishResponse.json()).features : [];
  const rings = boundary.geometry.type === 'MultiPolygon'
    ? boundary.geometry.coordinates.flat() : boundary.geometry.coordinates;
  const worldPositions = rings.flat().map(toWorld);
  const xValues = worldPositions.map(([x]) => x);
  const yValues = worldPositions.map(([, y]) => y);
  const west = Math.min(...xValues);
  const north = Math.min(...yValues);
  const regionWidth = Math.max(...xValues) - west;
  const regionHeight = Math.max(...yValues) - north;
  const scale = Math.min((WIDTH - 2 * PAD) / regionWidth, (HEIGHT - 2 * PAD) / regionHeight);
  const offsetX = (WIDTH - regionWidth * scale) / 2;
  const offsetY = (HEIGHT - regionHeight * scale) / 2;

  function toView([x, y]) {
    return [offsetX + (x - west) * scale, offsetY + (y - north) * scale];
  }

  function toWorldFromView(x, y) {
    return [west + (x - offsetX) / scale, north + (y - offsetY) / scale];
  }

  function project(coordinates) {
    return toView(toWorld(coordinates));
  }

  function selectAt(x, y) {
    const [longitude, latitude] = fromWorld(toWorldFromView(x, y));
    onPointChange({ longitude: Number(longitude.toFixed(6)), latitude: Number(latitude.toFixed(6)) });
  }

  function pathFor(projectedRings) {
    return projectedRings.map(ring =>
      ring.map((point, index) => `${index ? 'L' : 'M'}${point.map(value => value.toFixed(2)).join(' ')}`).join(' ') + ' Z'
    ).join(' ');
  }
  const outline = pathFor(rings.map(ring => ring.map(project)));
  const parishShapes = new Map(parishes.map(({ properties, geometry }) => {
    const parishRings = geometry.type === 'MultiPolygon' ? geometry.coordinates.flat() : geometry.coordinates;
    const projected = parishRings.map(ring => ring.map(project));
    const vertices = projected.flat();
    const xs = vertices.map(([x]) => x);
    const ys = vertices.map(([, y]) => y);
    return [properties.dpa_parroq, {
      path: pathFor(projected),
      bounds: [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)],
    }];
  }));

  container.innerHTML = `
    <svg role="group" tabindex="0" aria-labelledby="parcel-map-title" aria-describedby="parcel-map-help">
      <title id="parcel-map-title">Mapa de Babahoyo</title>
      <desc id="parcel-map-help">Arrastra para desplazar el mapa. Con el teclado, usa las flechas para desplazar, más y menos para acercar y alejar, e Intro para elegir el punto central.</desc>
      <path class="boundary-fill" fill-rule="evenodd" aria-hidden="true"></path>
      <g class="map-basemap" aria-hidden="true" pointer-events="none"></g>
      <defs>
        <clipPath id="babahoyo-coverage"><path clip-rule="evenodd"></path></clipPath>
      </defs>
      <g clip-path="url(#babahoyo-coverage)">
      <g class="map-layer" aria-hidden="true" pointer-events="none">
        <g id="rain-layer" hidden></g>
        <g id="moisture-layer" hidden></g>
        <g id="temperature-layer" hidden></g>
        <g id="flood-layer" hidden></g>
      </g>
      </g>
      <path class="boundary-outline" fill="none" vector-effect="non-scaling-stroke" aria-hidden="true"></path>
      <g class="parish-outlines" fill="none" pointer-events="none" aria-hidden="true"></g>
      <path class="poi-area" fill="none" vector-effect="non-scaling-stroke" pointer-events="none" hidden></path>
      <g class="map-pois" aria-label="Sectores de referencia"></g>
      <g class="map-marker" hidden aria-hidden="true" pointer-events="none">
        <circle r="8" fill="#fff" stroke="#1e5944" stroke-width="3"></circle>
        <circle r="2.5" fill="#1e5944"></circle>
      </g>
      <g class="map-reticle" aria-hidden="true" pointer-events="none">
        <path d="M-12 0H-4 M4 0H12 M0 -12V-4 M0 4V12" stroke-width="2"></path>
      </g>
    </svg>
    <p class="basemap-status" role="status" hidden>Mapa base no disponible. Se muestran el límite y las capas de BioTinder.</p>`;
  const svg = container.querySelector('svg');
  const updateBasemap = mountBasemap(svg.querySelector('.map-basemap'), container.querySelector('.basemap-status'));
  for (const path of svg.querySelectorAll('.boundary-fill, .boundary-outline')) {
    path.setAttribute('d', outline);
  }
  const layer = svg.querySelector('.map-layer');
  const coverage = svg.querySelector('#babahoyo-coverage path');
  coverage.setAttribute('d', outline);
  const poiLayer = svg.querySelector('.map-pois');
  const selector = controls.parentElement.querySelector('#poi-selector');
  const area = svg.querySelector('.poi-area');
  const svgElement = tag => document.createElementNS('http://www.w3.org/2000/svg', tag);
  const parishOutlines = svg.querySelector('.parish-outlines');
  for (const { path } of parishShapes.values()) {
    const line = svgElement('path');
    line.setAttribute('d', path);
    line.setAttribute('vector-effect', 'non-scaling-stroke');
    parishOutlines.append(line);
  }
  const poiMarkers = pointsOfInterest.filter(([, code]) => parishShapes.has(code)).map(([name, code, coordinates]) => {
    const link = svgElement('a');
    link.setAttribute('href', isPublicMap ? '#visor' : '#recommendations');
    link.dataset.sector = name === 'Pimocha' ? 'Pimocha (Bajial)' : name;
    selector.add(new Option(name, link.dataset.sector));
    link.addEventListener('click', event => {
      if (isPublicMap) event.preventDefault();
      selector.value = link.dataset.sector;
      selector.dispatchEvent(new Event('change', { bubbles: true }));
    });
    link.setAttribute('aria-label', (isPublicMap ? 'Enfocar ' : 'Consultar recomendaciones de ') + name);
    const dot = svgElement('circle');
    dot.setAttribute('r', '7');
    const label = svgElement('text');
    label.setAttribute('x', '11');
    label.setAttribute('y', '4');
    label.textContent = name;
    link.append(dot, label);
    poiLayer.append(link);
    return { link, shape: parishShapes.get(code), position: project(coordinates) };
  });
  const marker = svg.querySelector('.map-marker');
  const reticle = svg.querySelector('.map-reticle');
  const zoomIn = controls.querySelector('[data-map-control="zoom-in"]');
  const zoomOut = controls.querySelector('[data-map-control="zoom-out"]');
  const satelliteButton = document.createElement('button');
  satelliteButton.type = 'button';
  satelliteButton.className = 'map-satellite';
  satelliteButton.textContent = 'Satélite';
  satelliteButton.setAttribute('aria-pressed', 'false');
  controls.append(satelliteButton);

  const satelliteCredit = document.createElement('span');
  satelliteCredit.hidden = true;
  const imagery = document.createElement('a');
  imagery.href = 'https://worldview.earthdata.nasa.gov/?v=-80,-2.25,-79.1,-1.45&l=MODIS_Terra_CorrectedReflectance_TrueColor&t=' + SATELLITE_DATE;
  imagery.target = '_blank';
  imagery.rel = 'noopener';
  imagery.textContent = 'NASA Terra/MODIS · 7 sep 2025';
  satelliteCredit.append(' · ', imagery);
  controls.parentElement.querySelector('.map-attribution').append(satelliteCredit);

  let center = [WIDTH / 2, HEIGHT / 2];
  let zoom = 1;
  let pixelsPerUnit = 1;
  let selectedPoint;
  let pointer;
  let satellite = false;

  function setMarker(point) {
    selectedPoint = point;
    marker.toggleAttribute('hidden', !point);
    if (point) {
      const [x, y] = project(point.coordinates);
      marker.setAttribute('transform', `translate(${x} ${y}) scale(${1 / pixelsPerUnit})`);
    }
  }

  function render() {
    const width = container.clientWidth;
    const height = container.clientHeight;
    if (!width || !height) return;
    const style = getComputedStyle(container);
    const usableWidth = width - parseFloat(style.getPropertyValue('--map-inset-right'));
    const usableHeight = Math.max(height * 0.5, height - parseFloat(style.getPropertyValue('--map-inset-top')));
    const anchorX = usableWidth / 2;
    const anchorY = height - usableHeight / 2;
    pixelsPerUnit = Math.min(usableWidth / WIDTH, usableHeight / HEIGHT) * zoom;
    const x = center[0] - anchorX / pixelsPerUnit;
    const y = center[1] - anchorY / pixelsPerUnit;
    const viewWidth = width / pixelsPerUnit;
    const viewHeight = height / pixelsPerUnit;
    svg.setAttribute('viewBox', `${x} ${y} ${viewWidth} ${viewHeight}`);
    updateBasemap([
      ...toWorldFromView(x, y),
      ...toWorldFromView(x + viewWidth, y + viewHeight),
    ], pixelsPerUnit * scale, toView, satellite);
    reticle.setAttribute('transform', `translate(${center.join(' ')}) scale(${1 / pixelsPerUnit})`);
    setMarker(selectedPoint);
    for (const { link, position } of poiMarkers) {
      link.setAttribute('transform', `translate(${position.join(' ')}) scale(${1 / pixelsPerUnit})`);
    }
    zoomIn.setAttribute('aria-disabled', String(zoom === MAX_ZOOM));
    zoomOut.setAttribute('aria-disabled', String(zoom === 1));
  }

  function eventLocation(event) {
    const matrix = svg.getScreenCTM();
    if (!matrix) return null;
    return new DOMPoint(event.clientX, event.clientY).matrixTransform(matrix.inverse());
  }

  function changeZoom(factor, [x, y] = center) {
    const next = Math.max(1, Math.min(MAX_ZOOM, zoom * factor));
    if (next === zoom) return;
    center = [x + (center[0] - x) * zoom / next, y + (center[1] - y) * zoom / next];
    zoom = next;
    render();
  }

  function pan(dx, dy) {
    center = [center[0] + dx / pixelsPerUnit, center[1] + dy / pixelsPerUnit];
    render();
  }

  function reset() {
    zoom = 1;
    center = [WIDTH / 2, HEIGHT / 2];
    render();
  }

  selector.closest('label').hidden = !poiMarkers.length;
  selector.addEventListener('change', () => {
    const point = poiMarkers.find(({ link }) => link.dataset.sector === selector.value);
    area.toggleAttribute('hidden', !point);
    if (!point) {
      coverage.setAttribute('d', outline);
      reset();
      return;
    }
    const { path, bounds: [left, top, right, bottom] } = point.shape;
    coverage.setAttribute('d', path);
    area.setAttribute('d', path);
    center = [(left + right) / 2, (top + bottom) / 2];
    zoom = Math.min(MAX_ZOOM, Math.max(1, Math.min(
      (WIDTH - 2 * PAD) / (right - left), (HEIGHT - 2 * PAD) / (bottom - top),
    )));
    render();
  });

  zoomIn.addEventListener('click', () => changeZoom(ZOOM_STEP));
  zoomOut.addEventListener('click', () => changeZoom(1 / ZOOM_STEP));
  controls.querySelector('[data-map-control="reset"]').addEventListener('click', reset);
  satelliteButton.addEventListener('click', () => {
    satellite = !satellite;
    satelliteButton.setAttribute('aria-pressed', String(satellite));
    satelliteCredit.hidden = !satellite;
    render();
  });
  controls.hidden = false;

  svg.addEventListener('pointerdown', event => {
    if (!event.isPrimary || event.button !== 0 || event.target.closest('[data-sector]')) return;
    pointer = { id: event.pointerId, x: event.clientX, y: event.clientY, moved: false };
    svg.setPointerCapture(event.pointerId);
  });

  svg.addEventListener('pointermove', event => {
    if (event.pointerId !== pointer?.id) return;
    const dx = event.clientX - pointer.x;
    const dy = event.clientY - pointer.y;
    if (!pointer.moved && Math.hypot(dx, dy) < 6) return;
    pointer = { id: pointer.id, x: event.clientX, y: event.clientY, moved: true };
    svg.classList.add('dragging');
    pan(-dx, -dy);
  });

  function stopPointer(event) {
    if (event.pointerId !== pointer?.id) return;
    pointer = null;
    svg.classList.remove('dragging');
  }

  svg.addEventListener('pointerup', event => {
    if (event.pointerId !== pointer?.id) return;
    const location = pointer.moved ? null : eventLocation(event);
    stopPointer(event);
    if (location) selectAt(location.x, location.y);
  });
  svg.addEventListener('pointercancel', stopPointer);
  svg.addEventListener('lostpointercapture', stopPointer);

  svg.addEventListener('wheel', event => {
    if (event.ctrlKey || !event.deltaY) return;
    const location = eventLocation(event);
    if (!location) return;
    event.preventDefault();
    changeZoom(event.deltaY < 0 ? ZOOM_STEP : 1 / ZOOM_STEP, [location.x, location.y]);
  }, { passive: false });

  const keyActions = new Map([
    ['ArrowLeft', () => pan(-48, 0)],
    ['ArrowRight', () => pan(48, 0)],
    ['ArrowUp', () => pan(0, -48)],
    ['ArrowDown', () => pan(0, 48)],
    ['+', () => changeZoom(ZOOM_STEP)],
    ['=', () => changeZoom(ZOOM_STEP)],
    ['-', () => changeZoom(1 / ZOOM_STEP)],
    ['Home', reset],
    ['Enter', () => selectAt(...center)],
  ]);
  svg.addEventListener('keydown', event => {
    if (event.ctrlKey || event.metaKey || event.altKey || event.target.closest('[data-sector]')) return;
    const action = keyActions.get(event.key);
    if (!action) return;
    event.preventDefault();
    action();
  });

  render();
  new ResizeObserver(render).observe(container);

  // Temporal layers project their longitude/latitude geometry into this shared viewBox.
  return { setMarker, project, layer };
}
