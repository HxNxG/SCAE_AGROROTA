import { renderCellLayer, renderCellLegend } from './CellLayer.js';

export function mountTimedCellLayer(panel, view, onFrameChange, settings) {
  const { id, unit, classes, layers, formatTime, timeName, dataName, loadFrames, defaultLatest = false } = settings;
  const heading = panel.querySelector(`#${id}-heading`);
  const time = panel.querySelector(`#${id}-time`);
  const legend = panel.querySelector(`#${id}-legend`);
  const status = panel.querySelector(`#${id}-status`);
  const source = panel.querySelector(`#${id}-source`);
  const retry = panel.querySelector(`#${id}-retry`);
  let mode;
  let activeRequest;
  let frames = [];
  let preferredTime;

  renderCellLegend(legend, classes);
  view.layer.setAttribute('opacity', '0.62');

  function showFrame() {
    const frame = frames[time.selectedIndex];
    const label = formatTime(frame.time);
    const measured = renderCellLayer(view, frame.cells, classes, cell => cell.value);
    preferredTime = frame.time;
    status.textContent = measured
      ? `${measured} de ${frame.cells.length} celdas con dato`
      : `Sin datos válidos en este ${timeName}.`;
    onFrameChange({ label, state: 'ready', cells: frame.cells });
  }

  async function refresh() {
    activeRequest?.abort();
    const controller = new AbortController();
    activeRequest = controller;
    frames = [];
    time.replaceChildren(new Option('Cargando fechas…', ''));
    time.disabled = true;
    view.layer.replaceChildren();
    retry.hidden = true;
    source.textContent = '';
    status.textContent = `Cargando ${dataName}…`;
    onFrameChange({ state: 'loading' });

    try {
      const data = await loadFrames(mode, controller.signal);
      if (controller.signal.aborted) return;
      if (data.unit !== unit || !Array.isArray(data.frames)) {
        throw new Error('Respuesta de capa inválida');
      }

      frames = data.frames;
      source.textContent = data.source || '';
      if (!frames.length) {
        time.replaceChildren(new Option('Sin fechas disponibles', ''));
        status.textContent = `No hay fechas disponibles para ${dataName}.`;
        onFrameChange({ state: 'ready', cells: [] });
        return;
      }

      time.replaceChildren(...frames.map(frame => new Option(formatTime(frame.time), frame.time)));
      time.value = frames.some(frame => frame.time === preferredTime)
        ? preferredTime
        : (defaultLatest ? frames.at(-1) : frames[0]).time;
      time.disabled = false;
      showFrame();
    } catch {
      if (controller.signal.aborted) return;
      time.replaceChildren(new Option('Fechas no disponibles', ''));
      time.disabled = true;
      status.textContent = `No se pudo cargar ${dataName}.`;
      retry.hidden = false;
      onFrameChange({ state: 'error' });
    }
  }

  time.addEventListener('change', showFrame);
  retry.addEventListener('click', refresh);

  return function setMode(nextMode) {
    if (mode === nextMode) return;
    mode = nextMode;
    panel.hidden = !mode;
    view.layer.toggleAttribute('hidden', !mode);
    if (mode) {
      heading.textContent = layers[mode].title;
      return refresh();
    }

    activeRequest?.abort();
    view.layer.replaceChildren();
  };
}
