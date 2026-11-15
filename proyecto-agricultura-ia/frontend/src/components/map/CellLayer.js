const noData = { label: 'Sin dato', color: '#c3cbd0' };

export function renderCellLegend(legend, classes) {
  for (const { label, color } of [...classes, noData]) {
    const item = document.createElement('li');
    const swatch = document.createElement('span');
    swatch.style.backgroundColor = color;
    swatch.setAttribute('aria-hidden', 'true');
    item.append(swatch, label);
    legend.append(item);
  }
}

export function renderCellLayer({ layer, project }, cells, classes, valueOf) {
  const shapes = document.createDocumentFragment();
  let measured = 0;
  for (const cell of cells) {
    const [west, south, east, north] = cell.bounds;
    const [x, y] = project([west, north]);
    const [right, bottom] = project([east, south]);
    const amount = valueOf(cell);
    const color = Number.isFinite(amount) ? classes.findLast(entry => amount >= entry.minimum)?.color : null;
    measured += Number(Boolean(color));
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    for (const [name, attribute] of Object.entries({
      x, y, width: right - x, height: bottom - y, fill: color || noData.color,
    })) {
      rect.setAttribute(name, attribute);
    }
    shapes.append(rect);
  }
  layer.replaceChildren(shapes);
  return measured;
}
