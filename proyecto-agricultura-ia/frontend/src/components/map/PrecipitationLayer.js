import { loadMonthlyClimate, loadPrecipitationCells } from '../../services/pilotApi.js';
import { renderCellLayer, renderCellLegend } from './CellLayer.js';

const classes = [
  { minimum: 0, label: '0–<50', color: '#d9eff6' },
  { minimum: 50, label: '50–<100', color: '#a6d8ec' },
  { minimum: 100, label: '100–<200', color: '#67b8dc' },
  { minimum: 200, label: '200–<300', color: '#308dc1' },
  { minimum: 300, label: '300–<400', color: '#135f9b' },
  { minimum: 400, label: '≥400', color: '#073970' },
];
const monthFormat = new Intl.DateTimeFormat('es-EC', { month: 'long', year: 'numeric', timeZone: 'UTC' });
const FRAME_DELAY = 1000;

export function mountPrecipitation(panel, { project, layer }, onFrameChange) {
  const timeline = panel.querySelector('#rain-month');
  const previous = panel.querySelector('#rain-previous');
  const next = panel.querySelector('#rain-next');
  const playback = panel.querySelector('#rain-playback');
  const monthLabel = panel.querySelector('#rain-month-label');
  const legend = panel.querySelector('#rain-legend');
  const status = panel.querySelector('#rain-status');
  const source = panel.querySelector('#rain-source');
  const retry = panel.querySelector('#rain-retry');
  const visible = panel.querySelector('#rain-visible');
  const opacity = panel.querySelector('#rain-opacity');
  const opacityValue = panel.querySelector('#rain-opacity-value');
  let months = [];
  let pending;
  let timelineRequest;
  let timer;
  let playing = false;
  let active = false;

  renderCellLegend(legend, classes);

  function applyVisibility() {
    layer.toggleAttribute('hidden', !active || !visible.checked);
    opacity.disabled = !visible.checked;
  }

  function applyOpacity() {
    const label = `${opacity.valueAsNumber} %`;
    layer.setAttribute('opacity', opacity.valueAsNumber / 100);
    opacityValue.value = label;
    opacity.setAttribute('aria-valuetext', label);
  }

  function updateTransport() {
    const index = timeline.valueAsNumber;
    previous.disabled = index === 0 || !months.length;
    next.disabled = index >= months.length - 1;
    playback.disabled = months.length < 2;
    playback.textContent = playing ? 'Pausar' : 'Reproducir';
  }

  function pause() {
    clearTimeout(timer);
    playing = false;
    updateTransport();
  }

  function setMonth(index) {
    timeline.valueAsNumber = index;
    return showMonth();
  }

  function scheduleFrame() {
    if (!playing || pending) return;
    const index = timeline.valueAsNumber;
    if (index >= months.length - 1) {
      pause();
      return;
    }
    clearTimeout(timer);
    timer = setTimeout(() => setMonth(index + 1), FRAME_DELAY);
  }

  async function showMonth() {
    if (!active) return;
    pending?.abort();
    const controller = new AbortController();
    pending = controller;
    const month = months[timeline.valueAsNumber];
    const label = monthFormat.format(new Date(`${month}-01T00:00:00Z`));
    monthLabel.value = label;
    timeline.setAttribute('aria-valuetext', label);
    updateTransport();
    layer.replaceChildren();
    onFrameChange({ label, state: 'loading' });
    retry.hidden = true;
    status.textContent = 'Cargando precipitación…';
    try {
      const data = await loadPrecipitationCells(month, controller.signal);
      if (controller.signal.aborted) return;
      if (data.month !== month || data.unit !== 'mm' || !Array.isArray(data.cells)) {
        throw new Error('Respuesta de precipitación inválida');
      }
      const measured = renderCellLayer({ layer, project }, data.cells, classes, cell => cell.precipitation_mm);
      source.textContent = data.source || '';
      status.textContent = measured ? `${measured} de ${data.cells.length} celdas con dato` : 'Sin datos para este mes.';
      onFrameChange({ label, state: 'ready', cells: data.cells });
    } catch {
      if (controller.signal.aborted) return;
      status.textContent = 'No se pudo cargar la precipitación de este mes.';
      retry.hidden = false;
      onFrameChange({ label, state: 'error' });
      pause();
    } finally {
      if (pending === controller) {
        pending = undefined;
        scheduleFrame();
      }
    }
  }

  async function loadTimeline() {
    timelineRequest?.abort();
    const controller = new AbortController();
    timelineRequest = controller;
    retry.hidden = true;
    status.textContent = 'Cargando meses disponibles…';
    try {
      const data = await loadMonthlyClimate(controller.signal);
      if (controller.signal.aborted) return;
      months = data.months.map(entry => entry.month);
      if (!months.length) {
        status.textContent = 'No hay meses disponibles.';
        return;
      }
      timeline.max = months.length - 1;
      timeline.value = timeline.max;
      timeline.disabled = false;
      await showMonth();
    } catch {
      if (controller.signal.aborted) return;
      status.textContent = 'No se pudieron cargar los meses disponibles.';
      retry.hidden = false;
    }
  }

  timeline.addEventListener('input', () => {
    pause();
    showMonth();
  });
  previous.addEventListener('click', () => {
    pause();
    setMonth(timeline.valueAsNumber - 1);
  });
  next.addEventListener('click', () => {
    pause();
    setMonth(timeline.valueAsNumber + 1);
  });
  playback.addEventListener('click', () => {
    if (playing) {
      pause();
      return;
    }
    playing = true;
    updateTransport();
    if (timeline.valueAsNumber === months.length - 1) setMonth(0);
    else scheduleFrame();
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) pause();
  });
  visible.addEventListener('change', applyVisibility);
  opacity.addEventListener('input', applyOpacity);
  retry.addEventListener('click', () => months.length ? showMonth() : loadTimeline());
  applyOpacity();

  return function setActive(nextActive) {
    if (active === nextActive) return;
    active = nextActive;
    panel.hidden = !active;
    applyVisibility();
    if (active) return months.length ? showMonth() : loadTimeline();

    pause();
    timelineRequest?.abort();
    pending?.abort();
    layer.replaceChildren();
  };
}
