# Guía de trabajo de AgroRota Ecuador

## Alcance y fuentes

El piloto evalúa qué sembrar después del arroz en Babahoyo. La comparación incluye continuidad con arroz, rotación con soya y rotación con maíz amarillo duro. Para cada opción muestra aptitud, ventana de siembra respaldada, ventajas potenciales, riesgos, restricciones y brechas. Conserva la referencia aunque resulte limitada para la parcela. El agricultor elige qué opción explorar.

El [Canva del proyecto](https://www.canva.com/design/DAHa51QXsVY/RPZNwjJNXHc83bJxfmYVSw/edit) describe la comparación visual, las preguntas, el simulador y la comunidad. El documento de alcance aportado por el equipo delimita el piloto y prioriza soya y maíz. Las otras especies y secuencias propuestas en Canva requieren evidencia y una ampliación del alcance. Verifica coordenadas, delimitaciones, umbrales y fichas varietales con las fuentes correspondientes antes de codificarlos.

## Flujo de la interfaz

1. **Seleccionar parcela.** Mostrar el mapa a la izquierda y el formulario a la derecha en pantallas anchas. En móvil mantener el orden mapa, formulario y resultados. Aceptar un punto o una delimitación según lo implementado, indicar cuál se usó y validar que pertenezca al área piloto.
2. **Describir el ciclo.** Preguntar por cultivo o manejo actual y mes previsto de siembra, agua de verano y tipo de riego, comportamiento del terreno ante lluvias y prioridad. Ofrecer respuestas desconocidas cuando corresponda. Si una opción muestra un rango de meses, registrar el mes elegido o evaluar el rango explícitamente.
3. **Mostrar diagnóstico y alternativas.** Presentar las condiciones actuales, luego tres tarjetas comparables lado a lado cuando el ancho lo permita. Permitir abrir el detalle y consultar evidencia en el mapa, requisitos y una guía de siembra por cultivo respaldada por INIAP u otra fuente agronómica documentada.
4. **Explorar escenarios.** El Canva propone un simulador de 18 meses. Empezar por la comparación de un ciclo. Al incorporar el simulador, mostrar el calendario, los supuestos y los cambios respecto al escenario base. Etiquetar una reducción hipotética de lluvia del 25 % como escenario y documentar cualquier clasificación de El Niño. Añadir predicciones o alertas cuando se cuente con fuentes, horizonte y validación apropiados.
5. **Recoger observaciones.** Al final permitir registrar lluvia, inundación, estado de cultivo y resultados posteriores. Guardar el contexto, la fecha, la ubicación necesaria y el estado pendiente de revisión. Restringir el acceso a datos identificables.

## Datos y motor de evaluación

| Insumo | Uso en el piloto |
| --- | --- |
| NASA POWER y GPM IMERG | Temperatura, precipitación, radiación y contexto histórico. Registrar período, resolución y latencia. |
| SMAP | Apoyo regional para humedad superficial o radicular según el producto. El riego y el drenaje declarados conservan su procedencia. |
| ISRIC SoilGrids, análisis de suelo y agricultor | Textura, drenaje y pH cuando se dispone de medición. Identificar estimaciones y documentar incertidumbre. |
| Landsat/HLS y SRTM | Índices de vigor y contexto topográfico. Aplicar controles de calidad y conservar la escala efectiva. |
| INIAP y fuentes oficiales ecuatorianas | Fichas varietales, requerimientos, ciclos y ventanas de siembra. Fechar precios y costos cuando estén disponibles. |

- El contrato de datos debe incluir variable, valor, unidad, fuente y versión, período, resolución cuando aplique, calidad y motivo de ausencia. Usar un CRS explícito y documentar el orden longitud, latitud de las geometrías GeoJSON.
- Evaluar compatibilidad climática, hídrica, edáfica y del ciclo con criterios versionados. Las prioridades del agricultor ordenan opciones compatibles. Si falta un dato crítico, devolver una evaluación preliminar o insuficiente y explicar qué observación resolvería la brecha.
- Mostrar costos y precios con su fecha, unidad y supuestos. Una comparación sin costos suficientes debe indicar que la rentabilidad está sin estimar. Etiquetar los beneficios para suelo, fertilidad y plagas como potenciales hasta contar con mediciones de campo.
- Propuesta inicial de implementación: motor de reglas trazables como referencia. Para incorporar una red neuronal, definir objetivo medible, etiquetas, cobertura y métricas. Comparar contra el motor de referencia con validación espacial y temporal y revisar fuga de información. La estacionalidad cíclica y la lluvia antecedente del Canva son variables candidatas. Calcularlas solo con información disponible al inicio de cada simulación.

## Arquitectura y secuencia de entrega

1. **Contratos y datos.** Definir esquemas en `backend/app/schemas/`. Documentar un ejemplo anonimizado con cobertura parcial. Fijar unidades, tipos, estados y fuentes antes de cablear la interfaz.
2. **Corte vertical.** Conectar el mapa y el formulario al diagnóstico. Implementar rutas en `backend/app/api/v1/endpoints/`, configuración en `core/`, persistencia en `models/` y lógica de datos, GIS y evaluación en `services/`. Mantener artefactos pesados fuera de Git con referencia a su versión y forma de recuperación.
3. **Resultados y retroalimentación.** Usar los componentes de `frontend/src/components/` para presentar diagnóstico, tarjetas y detalle. Centralizar la comunicación HTTP en `frontend/src/services/`. Incorporar el registro de observaciones y su revisión.
4. **Simulación y modelos.** Añadir escenarios reproducibles, validar resultados con casos locales y medir el desempeño antes de habilitar predicciones al usuario.

## Verificación antes de publicar

- Probar desde mapa y formulario hasta las tres tarjetas con un caso de Babahoyo. Cubrir ubicación fuera del piloto, riego desconocido, encharcamiento, datos satelitales ausentes y caída de una fuente.
- Comprobar unidades, coordenadas, fechas y motivos de las recomendaciones. En simulaciones verificar reproducibilidad y que el escenario alternativo conserve intacto el escenario base.
- Revisar el formulario y la comparación en escritorio y móvil. Confirmar que las observaciones quedan pendientes y que el historial de Git contiene únicamente los archivos previstos.
- En la entrega, indicar comandos ejecutados, resultados, fuentes o reglas modificadas y brechas pendientes.
