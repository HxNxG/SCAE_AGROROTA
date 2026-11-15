const climateAmount = new Intl.NumberFormat('es-EC', { maximumFractionDigits: 2 });
const moisture = new Intl.NumberFormat('es-EC', { maximumFractionDigits: 3 });

function containsPoint({ bounds: [west, south, east, north] }, [longitude, latitude]) {
  return longitude >= west && longitude < east && latitude >= south && latitude < north;
}

export function mountCellReading(panel) {
  const title = panel.querySelector('#climate-title');
  const month = panel.querySelector('#cell-month');
  const value = panel.querySelector('#cell-value');
  const source = panel.querySelector('.cell-source');
  const history = panel.querySelector('#climate-history-details');
  let point;
  let frame;
  let reading;

  function render() {
    month.textContent = frame?.label || '';
    if (reading?.staticMessage) {
      value.textContent = reading.staticMessage;
      return;
    }
    if (!point || !frame) {
      value.textContent = 'Sin fecha disponible';
      return;
    }
    if (frame.state === 'loading') {
      value.textContent = 'Cargando…';
      return;
    }
    if (frame.state === 'error') {
      value.textContent = 'Dato no disponible';
      return;
    }
    const cell = frame.cells.find(candidate => containsPoint(candidate, point.coordinates));
    const amount = cell?.[reading.field];
    const format = reading.unit === 'm³/m³' ? moisture : climateAmount;
    value.textContent = Number.isFinite(amount) && (reading.unit === '°C' || amount >= 0)
      ? `${format.format(amount)} ${reading.unit}`
      : 'Sin dato para esta ubicación';
  }

  return {
    setLayer(next) {
      reading = next;
      frame = null;
      title.textContent = next.title;
      source.textContent = next.source;
      history.hidden = next.unit !== 'mm';
      render();
    },
    setPoint(next) {
      point = next;
      render();
    },
    setFrame(next) {
      frame = next;
      render();
    },
  };
}
