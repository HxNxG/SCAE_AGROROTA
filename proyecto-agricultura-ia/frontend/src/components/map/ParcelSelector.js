import { mountMap } from './MapContainer.js';
import { loadMonthlyClimate, validatePoint } from '../../services/pilotApi.js';

const precipitation = new Intl.NumberFormat('es-EC', { maximumFractionDigits: 2 });
const forecastMonth = new Intl.DateTimeFormat('es-EC', {
  month: 'short', year: 'numeric', timeZone: 'UTC',
});

function renderRainOutlook(container, months) {
  const today = new Date();
  const heading = document.createElement('h4');
  heading.textContent = 'Proyección de lluvia · próximos 3 meses';
  const method = document.createElement('p');
  method.textContent = 'Promedio histórico del mismo mes. El rango muestra los extremos observados. Esta referencia no incorpora pronósticos ni tendencias futuras.';
  const list = document.createElement('dl');
  for (let offset = 1; offset <= 3; offset++) {
    const future = new Date(Date.UTC(today.getFullYear(), today.getMonth() + offset, 1));
    const monthNumber = String(future.getUTCMonth() + 1).padStart(2, '0');
    const values = months.filter(entry => /^\d{4}-(0[1-9]|1[0-2])$/.test(entry?.month) &&
      entry.month.endsWith(`-${monthNumber}`) && entry.month < future.toISOString().slice(0, 7))
      .map(entry => entry.precipitation_mm).filter(value => Number.isFinite(value) && value >= 0);
    const label = document.createElement('dt');
    const estimate = document.createElement('dd');
    label.textContent = forecastMonth.format(future);
    if (values.length < 3) {
      estimate.textContent = 'Historial insuficiente';
    } else {
      const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
      estimate.textContent = `${precipitation.format(mean)} mm · rango ${precipitation.format(Math.min(...values))}–${precipitation.format(Math.max(...values))} mm · ${values.length} años`;
    }
    list.append(label, estimate);
  }
  container.replaceChildren(heading, method, list);
  container.hidden = false;
}

function renderHistoryChart(figure, months) {
  const values = new Map();
  for (const entry of months) {
    if (!/^\d{4}-(0[1-9]|1[0-2])$/.test(entry?.month)) continue;
    const [year, month] = entry.month.split('-').map(Number);
    values.set(year * 12 + month - 1, entry.precipitation_mm);
  }
  const measured = value => Number.isFinite(value) && value >= 0;
  const valid = [...values.values()].filter(measured);
  if (!valid.length) return;

  const first = Math.min(...values.keys());
  const last = Math.max(...values.keys());
  const max = Math.max(100, Math.ceil(Math.max(...valid) / 100) * 100);
  const svgNode = (name, attributes, label) => {
    const node = document.createElementNS('http://www.w3.org/2000/svg', name);
    for (const [key, value] of Object.entries(attributes)) node.setAttribute(key, value);
    if (label != null) node.textContent = label;
    return node;
  };
  const svg = svgNode('svg', { viewBox: '0 0 300 114', 'aria-hidden': 'true' });
  for (const tick of [0, max / 2, max]) {
    const y = 92 - 78 * tick / max;
    svg.append(svgNode('path', { d: `M34 ${y}H291`, class: 'history-gridline' }),
      svgNode('text', { x: 30, y: y + 3, 'text-anchor': 'end' }, precipitation.format(tick)));
  }
  const xFor = month => first === last ? 162.5 : 34 + 257 * (month - first) / (last - first);
  let path = '';
  let previous;
  for (const [month, value] of [...values.entries()].sort(([a], [b]) => a - b)) {
    if (!measured(value)) continue;
    const x = xFor(month);
    const y = 92 - 78 * value / max;
    path += `${previous === month - 1 ? 'L' : 'M'}${x} ${y}`;
    if (!measured(values.get(month - 1)) && !measured(values.get(month + 1))) {
      svg.append(svgNode('circle', { cx: x, cy: y, r: 2, class: 'history-point' }));
    }
    previous = month;
  }
  svg.append(svgNode('path', { d: path, class: 'history-line' }));
  for (const month of new Set([first, last])) {
    const label = `${Math.floor(month / 12)}-${String(month % 12 + 1).padStart(2, '0')}`;
    svg.append(svgNode('text', {
      x: xFor(month), y: 108, 'text-anchor': first === last ? 'middle' : month === first ? 'start' : 'end',
    }, label));
  }
  const caption = document.createElement('figcaption');
  caption.textContent = 'Precipitación mensual promedio (mm)';
  figure.append(caption, svg);
  figure.hidden = false;
}

function isPoint(point) {
  return point?.type === 'Point' &&
    Array.isArray(point.coordinates) &&
    point.coordinates.length === 2 &&
    point.coordinates.every(Number.isFinite);
}

export function mountParcelSelector(visor, onPointChange) {
  const panel = visor.querySelector('#location-panel');
  const openPanel = visor.querySelector('.panel-toggle');
  const closePanel = panel.querySelector('.panel-close');
  const form = panel.querySelector('#parcel-form');
  const status = panel.querySelector('#parcel-status');
  const climate = panel.querySelector('#climate-card');
  const climateStatus = climate.querySelector('#climate-status');
  const climateSource = climate.querySelector('#climate-source');
  const climateMethod = climate.querySelector('#climate-method');
  const climateScale = climate.querySelector('#climate-scale');
  const history = climate.querySelector('#climate-history-container');
  const chart = climate.querySelector('#climate-history-chart');
  const outlook = climate.querySelector('#climate-rain-outlook');
  const rows = history.querySelector('tbody');
  const { longitude, latitude } = form.elements;
  let activeRequest;
  let acceptedPoint = null;
  let setMarker;

  function showPanel(open) {
    panel.hidden = !open;
    openPanel.hidden = open;
    openPanel.setAttribute('aria-expanded', String(open));
  }

  openPanel.addEventListener('click', () => {
    showPanel(true);
    closePanel.focus();
  });
  function dismissPanel() {
    showPanel(false);
    openPanel.focus();
  }
  closePanel.addEventListener('click', dismissPanel);
  panel.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !event.defaultPrevented) dismissPanel();
  });
  showPanel(!matchMedia('(max-width: 760px)').matches);

  function clearSelection() {
    activeRequest?.abort();
    activeRequest = undefined;
    acceptedPoint = null;
    onPointChange(null);
    setMarker?.(null);
    climate.hidden = true;
    history.hidden = true;
    chart.hidden = true;
    chart.replaceChildren();
    outlook.hidden = true;
    outlook.replaceChildren();
    climateSource.hidden = true;
    climateMethod.hidden = true;
    climateMethod.open = false;
    rows.replaceChildren();
  }

  function showClimate(data) {
    const months = Array.isArray(data?.months) && data.unit === 'mm' ? data.months : [];
    if (typeof data?.source === 'string' && data.source.trim()) {
      climateSource.textContent = `Fuente: ${data.source}`;
      climateSource.hidden = false;
    }
    if (typeof data?.spatial_scale === 'string' && data.spatial_scale.trim()) {
      climateScale.textContent = data.spatial_scale;
      climateMethod.hidden = false;
    }
    if (!months.length) {
      climateStatus.textContent = 'No hay datos mensuales de precipitación disponibles.';
      return;
    }

    let hasMeasurements = false;
    for (const entry of months) {
      const row = document.createElement('tr');
      const month = document.createElement('th');
      const value = document.createElement('td');
      const measured = Number.isFinite(entry?.precipitation_mm) && entry.precipitation_mm >= 0;
      hasMeasurements ||= measured;
      month.scope = 'row';
      month.textContent = typeof entry?.month === 'string' ? entry.month : 'Mes sin fecha';
      value.textContent = measured ? precipitation.format(entry.precipitation_mm) : 'Sin dato';
      row.append(month, value);
      rows.append(row);
    }
    history.hidden = false;
    renderHistoryChart(chart, months);
    renderRainOutlook(outlook, months);
    climateStatus.textContent = hasMeasurements ? '' : 'Los meses del historial figuran sin medición.';
  }

  async function select(point) {
    clearSelection();
    const controller = new AbortController();
    activeRequest = controller;
    const { signal } = controller;
    status.textContent = 'Validando ubicación…';

    try {
      const result = await validatePoint(point, signal);
      if (signal.aborted) return;
      if (result?.accepted === false) {
        status.textContent = result.message || 'El punto está fuera del área piloto de Babahoyo.';
        return;
      }
      if (result?.accepted !== true || !isPoint(result.point)) throw new Error('Respuesta de validación inválida');
      acceptedPoint = result.point;
      onPointChange(acceptedPoint);
      setMarker?.(acceptedPoint);
      status.textContent = result.message || 'Punto validado en el área piloto de Babahoyo.';
    } catch {
      if (!signal.aborted) status.textContent = 'No se pudo validar la ubicación. Vuelve a intentarlo.';
      return;
    }

    climateStatus.textContent = 'Cargando historial de precipitación…';
    climate.hidden = false;
    try {
      const data = await loadMonthlyClimate(signal);
      if (!signal.aborted) showClimate(data);
    } catch {
      if (!signal.aborted) {
        climateStatus.textContent = 'No se pudo cargar el historial. Valida el punto de nuevo para reintentar.';
      }
    }
  }

  form.addEventListener('input', () => {
    clearSelection();
    status.textContent = 'Valida las coordenadas para comprobar la ubicación.';
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    select({ longitude: longitude.valueAsNumber, latitude: latitude.valueAsNumber });
  });

  const map = visor.querySelector('#parcel-map');
  const controls = visor.querySelector('.map-controls');
  return mountMap(map, controls, point => {
    showPanel(true);
    longitude.value = point.longitude;
    latitude.value = point.latitude;
    select(point);
  }).then(view => {
    setMarker = view.setMarker;
    setMarker(acceptedPoint);
    return view;
  }).catch(() => {
    const message = map.querySelector('[role="status"]') ?? document.createElement('p');
    message.setAttribute('role', 'status');
    message.textContent = 'El mapa no está disponible. Puedes validar el punto con sus coordenadas.';
    map.replaceChildren(message);
    controls.hidden = true;
    return null;
  });
}
