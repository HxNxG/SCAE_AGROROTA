import { recommend, submitObservation } from '../services/aiApi.js';

const zones = ['Babahoyo Centro', 'Pimocha (Bajial)', 'Caracol', 'Febres Cordero', 'La Unión', 'Baba', 'Montalvo (Alto)', 'Vinces (Sur)'];
const fields = [
  ['zona', 'Sector', zones.map(zone => [zone, zone])],
  ['manejo_actual', '¿Cómo trabajas tu parcela arrocera hoy?', [
    ['arroz_barbecho', 'Siembro solo en invierno y en verano la tierra se queda vacía.'],
    ['arroz_doble', 'Siembro arroz dos veces al año sin parar.'],
    ['arroz_rotacion', 'Siembro arroz en invierno y después siembro soya o fréjol.'],
  ]],
  ['mes_inicio', '¿Cuándo empieza tu próximo ciclo?', [
    [5, 'Mayo–junio', 'El cálculo empieza en mayo.'],
    [8, 'Agosto–septiembre', 'El cálculo empieza en agosto.'],
    [1, 'Enero–febrero', 'El cálculo empieza en enero.'],
  ]],
  ['agua_verano', '¿Con qué agua cuentas entre julio y noviembre?', [
    ['solo_lluvia', 'Solo dependo de la lluvia; en verano la tierra se seca.'],
    ['bomba_pozo', 'Tengo bomba para sacar agua de un estero, río o pozo.'],
    ['canal_riego', 'Tengo agua de canal de riego todo el año.'],
  ]],
  ['tipo_terreno', '¿Cómo se comporta tu terreno cuando llueve fuerte?', [
    ['bajial_inundable', 'La tierra se inunda en invierno y se forman pozas.'],
    ['banco_alto', 'La tierra es alta y tiene buen drenaje.'],
    ['tierra_barrial', 'La tierra es barrial y se vuelve lodosa con la lluvia.'],
  ]],
  ['meta', '¿Qué necesitas lograr principalmente este año?', [
    ['ahorrar_abono', 'Ahorrar en abono y recuperar el suelo.'],
    ['resistir_sequia', 'Reducir el riesgo para mi inversión si escasea la lluvia.'],
    ['cosecha_rapida', 'Cosechar rápido para obtener ingresos a corto plazo.'],
  ]],
  ['escenario_clima', 'Escenario climático', [['normal', 'Normal'], ['sequia', 'Sequía'], ['elnino', 'El Niño']]],
];
const displayNumber = new Intl.NumberFormat('es-EC', { maximumFractionDigits: 3 });
const number = (value, unit = '') => Number.isFinite(value) ? displayNumber.format(value) + unit : 'Sin dato';
const items = value => Array.isArray(value) ? value : [];
const emoji = /\p{RGI_Emoji}|\p{Emoji_Presentation}/gv;

function plainText(value) {
  return value.replace(emoji, '').replace(/[ \t]{2,}/g, ' ').trim();
}

function element(tag, ...children) {
  const node = document.createElement(tag);
  node.append(...children.filter(child => child != null).map(child =>
    typeof child === 'string' ? plainText(child) : typeof child === 'number' ? String(child) : child));
  return node;
}

function selectField(name, label, options) {
  const select = element('select');
  select.name = name;
  for (const [value, text] of options) select.add(new Option(text, value));
  const field = element('label', label, select);
  field.className = 'field';
  return field;
}

function questionField(name, question, options) {
  const group = element('fieldset', element('legend', question));
  group.className = 'ai-question';
  for (const [value, label, hint] of options) {
    const input = element('input');
    input.type = 'radio';
    input.name = name;
    input.value = value;
    input.required = true;
    const option = element('label', input, element('span', label, hint ? element('small', hint) : null));
    option.className = 'ai-option';
    group.append(option);
  }
  return group;
}

function facts(entries) {
  const list = element('dl');
  for (const [label, value] of entries) {
    list.append(element('dt', label), element('dd', value ?? 'Sin dato'));
  }
  return list;
}

function details(title, ...content) {
  return element('details', element('summary', title), ...content);
}

function strategyCard(strategy, index) {
  const summary = strategy.resumen_5_logros ?? {};
  const technical = strategy.tecnico_nasa ?? {};
  const confidence = technical.confianza_ia;
  const hasConfidence = Number.isFinite(confidence) && confidence >= 0 && confidence <= 100;
  const confidenceMeter = hasConfidence ? element('meter') : null;
  if (confidenceMeter) {
    confidenceMeter.max = 100;
    confidenceMeter.value = confidence;
    confidenceMeter.setAttribute('aria-label', 'Confianza estimada por el modelo');
  }
  const indicators = facts([
    ['Confiabilidad de los datos', element('div',
      element('strong', hasConfidence ? number(confidence, ' %') : 'Sin dato'),
      confidenceMeter,
      element('small', 'Humedad de verano'))],
    ['Adaptación al clima', element('div',
      element('small', summary.clima_plagas ?? 'Sin evaluación del escenario.'))],
  ]);
  indicators.className = 'ai-card-indicators';
  const steps = items(strategy.pasos).map(step => element('li',
    element('strong', [step.orden, step.planta, step.duracion].filter(Boolean).join(' · ')),
    element('p', step.detalle)));
  const guides = items(strategy.guias).filter(Boolean).map(guide => element('div',
    element('h4', guide.planta), facts([
      ['Papel en la rotación', guide.rol_arroz], ['Preparación', guide.preparacion],
      ['Siembra', guide.siembra], ['Cuidados', guide.cuidados], ['Cosecha', guide.cosecha],
    ])));
  const timeline = items(strategy.timeline);
  const calendarSummary = element('ol');
  calendarSummary.className = 'ai-month-strip';
  calendarSummary.setAttribute('aria-label', 'Secuencia de cultivos por mes');
  const monthDetail = element('div');
  monthDetail.className = 'ai-month-detail';
  monthDetail.id = `strategy-month-${index}`;
  let activeMonth;
  for (const month of timeline) {
    const tile = element('button', month.mes_nombre);
    tile.type = 'button';
    tile.setAttribute('aria-label', plainText(`Mes ${month.step}: ${month.mes_nombre}`));
    tile.setAttribute('aria-controls', monthDetail.id);
    tile.setAttribute('aria-pressed', 'false');
    if (/^#[0-9a-f]{6}$/i.test(month.color)) tile.style.setProperty('--crop-color', month.color);
    function showMonth() {
      if (activeMonth === tile) return;
      activeMonth?.setAttribute('aria-pressed', 'false');
      activeMonth = tile;
      tile.setAttribute('aria-pressed', 'true');
      monthDetail.replaceChildren(
        element('strong', `Mes ${month.step} · ${month.mes_nombre}`),
        facts([
          ['Cultivo', month.cultivo],
          ['Humedad estimada', number(month.humedad_ia, ' %')],
          ['Fuerza del suelo', number(month.fuerza_suelo)],
          ['Alerta', month.alerta],
        ]));
    }
    tile.addEventListener('pointerenter', event => {
      if (event.pointerType === 'mouse') showMonth();
    });
    tile.addEventListener('focus', showMonth);
    tile.addEventListener('click', showMonth);
    calendarSummary.append(element('li', tile));
    if (!activeMonth) showMonth();
  }
  const category = element('p', index === 0 ? 'Diagnóstico actual' : `Plan recomendado ${index}`);
  category.className = 'ai-card-category';
  const impact = (strategy.impacto_directo ?? '').split('•').map(part => plainText(part)).filter(Boolean);
  const impactList = element('ul', ...impact.map(part => element('li', part)));
  impactList.className = 'ai-impact-list';
  const intro = element('div', category, element('h4', strategy.titulo),
    impact.length ? impactList : null);
  intro.className = 'ai-card-intro';
  const outcomes = facts([
      ['Ventas', summary.ventas], ['Clima y plagas', summary.clima_plagas],
      ['Arroz principal', summary.arroz_principal], ['Fuerza de la tierra', summary.fuerza_tierra],
      ['Casa y ganado', summary.casa_ganado],
    ]);
  outcomes.className = 'ai-card-outcomes';
  const drilldowns = element('div',
    details('Resultados esperados', outcomes),
    details('Pasos de la estrategia', steps.length ? element('ol', ...steps) : element('p', 'Sin pasos disponibles.')),
    details('Evidencia y límites', facts([
      ['Humedad de verano', number(technical.humedad_verano, ' %')],
      ['Margen reportado', number(technical.margen_error, ' puntos porcentuales')],
      ['Historial', technical.historial], ['Limitaciones', technical.honestidad],
    ]), element('ul', ...items(technical.evidencia).map(line => element('li', line)))),
    guides.length ? details('Guías de cultivo', ...guides) : null);
  drilldowns.className = 'ai-card-details';
  const card = element('article', intro, indicators,
    timeline.length ? calendarSummary : null, timeline.length ? monthDetail : null, drilldowns);
  card.className = 'ai-card';
  card.dataset.kind = index === 0 ? 'baseline' : 'plan';
  return card;
}

function renderResults(container, response, scenario) {
  if (!Array.isArray(response?.estrategias) || !response.estrategias.length) {
    throw new Error('La API no devolvió estrategias para mostrar.');
  }
  const metrics = response.metricas_modelo ?? {};
  const comparison = element('div', ...response.estrategias.map(strategyCard));
  comparison.className = 'ai-grid';
  const demo = response.modo === 'demo' || /\bdemostración\s*$/i.test(response.zona ?? '');
  const title = element('h3', demo ? 'Ejemplo de Pimocha' : `${response.zona} · ${scenario}`);
  title.tabIndex = -1;
  const context = element('p', demo
    ? 'Demostración con resultados guardados de Pimocha para un escenario de sequía.'
    : 'Simulación de rotación de cultivos por sector.');
  if (demo) context.className = 'ai-demo-note';
  container.replaceChildren(
    title,
    context,
    details('Métricas del modelo', facts([
      ['R²', number(metrics.r2_score)],
      ['Error absoluto medio de humedad', number(metrics.mae_humedad_pct, ' puntos porcentuales')],
      ['Error absoluto medio del balance hídrico', number(metrics.mae_balance_mm, ' mm')],
    ])),
    comparison);
  return title;
}

function handleSubmit(form, status, action) {
  const button = form.querySelector('button');
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (button.disabled) return;
    const data = Object.fromEntries(new FormData(form));
    button.disabled = true;
    status.textContent = 'Enviando…';
    try {
      await action(data);
    } catch (error) {
      status.textContent = error.message;
    } finally {
      button.disabled = false;
    }
  });
}

export function mountRecommendations(section, demoResponse) {
  const heading = element('h2', 'Recomendaciones de cultivo');
  heading.id = 'recommendations-title';
  if (demoResponse) {
    const comparison = element('div');
    section.append(heading, comparison);
    renderResults(comparison, demoResponse, 'Sequía');
    return;
  }
  const status = element('p');
  status.setAttribute('role', 'status');
  const results = element('div');
  results.className = 'ai-results';
  const submit = element('button', 'Generar diagnóstico');
  submit.className = 'primary';
  const form = element('form', ...fields.map(args =>
    ['zona', 'escenario_clima'].includes(args[0]) ? selectField(...args) : questionField(...args)),
  element('div', submit));
  form.className = 'ai-form';

  const category = element('input');
  category.name = 'categoria';
  category.required = true;
  const observation = element('textarea');
  observation.name = 'observacion';
  observation.rows = 4;
  observation.required = true;
  const consent = element('input');
  consent.type = 'checkbox';
  consent.required = true;
  const feedbackStatus = element('p');
  feedbackStatus.setAttribute('role', 'status');
  const feedbackButton = element('button', 'Enviar observación');
  feedbackButton.className = 'primary';
  const sector = selectField('sector', 'Sector', fields[0][2]);
  const categoryField = element('label', 'Categoría', category);
  categoryField.className = 'field';
  const observationField = element('label', 'Observación', observation);
  observationField.className = 'field';
  const feedback = element('form', sector, categoryField, observationField,
    element('label', consent, ' Acepto enviar esta observación para revisión técnica.'),
    element('div', feedbackButton), feedbackStatus);
  feedback.className = 'ai-feedback';

  const adaptation = details('Cómo evaluar la adaptación al cambio climático',
    element('p', 'Simula tu rotación de 18 meses en condiciones normales, de sequía o de El Niño. Compara las alertas de humedad y las opciones de cultivo de cada escenario para identificar dónde ajustar el riego o la fecha de siembra.'),
    element('p', 'Los escenarios sirven para explorar riesgos. La API no estima cuánto cambiará el clima ni calcula un porcentaje de mitigación.'));
  section.append(heading, element('p', 'Elige el sector de tu parcela y describe tu ciclo de cultivo.'), adaptation, form,
    status, results, details('Compartir una observación de campo', feedback));

  handleSubmit(form, status, async data => {
    results.replaceChildren();
    const response = await recommend({ ...data, mes_inicio: Number(data.mes_inicio) });
    const scenario = fields.find(([name]) => name === 'escenario_clima')[2]
      .find(([value]) => value === data.escenario_clima)[1];
    const title = renderResults(results, response, scenario);
    status.textContent = `${response.estrategias.length} estrategias disponibles.`;
    title.focus();
  });
  handleSubmit(feedback, feedbackStatus, async data => {
    data.categoria = data.categoria.trim();
    data.observacion = data.observacion.trim();
    if (!data.categoria || !data.observacion) throw new Error('Completa la categoría y la observación.');
    const response = await submitObservation(data);
    const selectedSector = data.sector;
    feedback.reset();
    feedback.elements.sector.value = selectedSector;
    feedbackStatus.textContent = plainText(response.mensaje ?? 'Observación enviada para revisión técnica.');
  });
}
