export const options = [
  { name: 'Arroz', sequence: 'Arroz → arroz', label: 'Referencia', description: 'Continuidad del cultivo para comparar con las alternativas de rotación.' },
  { name: 'Soya', sequence: 'Arroz → soya', label: 'Rotación prioritaria', description: 'Una alternativa de rotación para explorar después del arroz.' },
  { name: 'Maíz amarillo duro', sequence: 'Arroz → maíz', label: 'Segunda alternativa', description: 'Otra alternativa de rotación para explorar después del arroz.' },
];
export function field(label, name, choices, hint = '') {
  return `<label class="field"><span>${label}</span>${hint ? `<small>${hint}</small>` : ''}<select name="${name}" required><option value="">Selecciona una opción</option>${choices.map(([value, text]) => `<option value="${value}">${text}</option>`).join('')}</select></label>`;
}
export function card(item, index) {
  return `<article class="card"><div class="card-top"><span class="tag">${item.label}</span><span class="card-number">0${index + 1}</span></div><p class="sequence">${item.sequence}</p><h3>${item.name}</h3><p>${item.description}</p><div class="status"><span aria-hidden="true">◌</span><div><strong>Aptitud pendiente</strong><small>Requiere evaluación y datos de la parcela.</small></div></div><dl><div><dt>Ventana de siembra</dt><dd>Sin evaluar</dd></div><div><dt>Rentabilidad</dt><dd>Sin estimar</dd></div></dl><details><summary>Ver qué falta para evaluar</summary><p>La evaluación requiere condiciones de la parcela y criterios agronómicos documentados. Las ventajas, riesgos y restricciones se mostrarán cuando estén disponibles.</p></details></article>`;
}
