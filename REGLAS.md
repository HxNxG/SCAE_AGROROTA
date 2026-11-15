# Reglas del repositorio de datos agrícolas

## Finalidad

Este repositorio se crea para analizar bases de datos de la región Costa del Ecuador y alimentar una herramienta de apoyo a decisiones agrícolas que combine datos satelitales de NASA, información agropecuaria ecuatoriana y experiencias reales de agricultores.

La herramienta debe traducir la evidencia en recomendaciones sobre qué cultivar, cuándo cultivar, cómo rotar los cultivos y qué asociaciones pueden mejorar la resiliencia del suelo frente al cambio climático. Mostrar mapas de temperatura, humedad o vegetación es un insumo, no el resultado final.

## Alcance geográfico

- Priorizar Esmeraldas, Manabí, Santo Domingo de los Tsáchilas, Los Ríos, Guayas, Santa Elena y El Oro como alcance administrativo inicial de la Costa.
- Registrar siempre provincia, cantón y, cuando sea posible, parroquia, coordenadas y delimitación del área analizada.
- La delimitación administrativa no sustituye la clasificación agroecológica: identificar zonas de transición y condiciones locales antes de generalizar resultados.
- Toda extracción debe indicar el polígono o los límites utilizados, su fuente, versión y sistema de coordenadas.
- La información de Sierra, Amazonía y región Insular se documentará mediante instrucciones de acceso. Solo se almacenará si resulta necesaria para un análisis autorizado y acotado.

## Organización

Cada tema contiene una carpeta por fuente o plataforma y un `README.md` con su enlace oficial, propósito documental e instrucciones de acceso. Las plataformas de exploración se distinguen de las bases o productos que permiten consultar.

- `01_suelos_y_salud_del_suelo/`: SMAP e ISRIC.
- `02_clima_temperatura_y_meteorologia/`: NASA POWER y GPM.
- `03_agua_y_recursos_hidricos/`: ECOSTRESS y GRACE/GRACE-FO.
- `04_vegetacion_cultivos_y_monitoreo/`: Landsat, MODIS y NASA Harvest.
- `05_topografia_y_modelado_del_terreno/`: SRTM.
- `06_visualizacion_exploracion_y_gis/`: Worldview, Giovanni, AppEEARS y VEDA.
- `07_informacion_agropecuaria_ecuatoriana/`: inventario pendiente de fuentes oficiales nacionales.
- `08_experiencias_de_agricultores/`: documentación de experiencias y consentimiento.
- `09_cobertura_y_brechas/`: estado de disponibilidad por región.
- `10_instructivos/`: acceso a otras regiones.

## Uso limitado de almacenamiento

### Período histórico definido: 2010–actualidad

El 14 de noviembre de 2026 el equipo definió el intervalo solicitado como 2010–actualidad. Para consultas reproducibles se interpreta el inicio como 2010-01-01 y se registra un corte explícito por ejecución; en esta fase, 2026-11-14. El extremo efectivo será la última fecha disponible por producto, no una fecha futura ni un dato inventado.

Cada fuente debe documentar su cobertura efectiva y los años sin información. SMAP L4 v8 comienza el 2015-03-31: el tramo 2010-01-01 a 2015-03-30 queda como ausencia temporal de esta fuente y no se rellenará con ceros ni con otra misión bajo el nombre SMAP.

Se autoriza recopilar y preparar SMAP para ese intervalo, acotado a las siete provincias de la Costa e incluyendo Los Ríos. La cobertura global de la fuente no autoriza almacenar todo el planeta. NASA POWER y las demás muestras deberán adecuarse al intervalo acordado en su respectiva tarea; no modificar entregables de otras personas sin coordinación. Conservar archivos provisionales hasta validar sus reemplazos.

### Criterios de almacenamiento

- Seguir el [inventario priorizado](INVENTARIO_PRIORIZADO.md) para organizar el trabajo: prioridad alta, media, baja y complementaria. Registrar responsables y avances; NASA POWER ya está en trabajo por otra persona y requiere coordinación antes de duplicar extracciones o modificar sus entregables.

- Antes de descargar, inventariar productos y definir la pregunta agrícola concreta. La recopilación SMAP ya fue solicitada por el equipo; debe respetar el período acordado, la delimitación y los controles de almacenamiento.
- Consultar remotamente y recortar a la Costa o al área de estudio antes de almacenar; limitar variables, fechas y resolución a lo necesario.
- Antes de cada descarga, registrar tamaño estimado, tamaño libre disponible y justificación. Si no cabe, reducir el alcance o conservar únicamente el enlace y el procedimiento reproducible.
- Evitar escenas globales, archivos duplicados y copias por provincia cuando un único recorte permita atender el análisis.
- Preferir tablas resumidas y formatos comprimidos adecuados; conservar la resolución y unidades originales en los metadatos aunque se generen agregados.
- No incorporar archivos voluminosos al historial Git. Si se necesita almacenamiento externo, documentar ubicación, permisos y recuperación sin publicar credenciales.
- No eliminar originales únicos ni datos aportados por agricultores sin autorización. Los temporales regenerables deben identificarse como tales.
- No se establece una cuota numérica porque aún no se ha definido la capacidad disponible.

## Metadatos mínimos por conjunto de datos

Registrar: institución, URL oficial, identificador de producto, versión, licencia o condiciones de uso, fecha de consulta y descarga, cobertura geográfica y temporal, variables y unidades, resolución espacial y temporal, sistema de coordenadas, indicadores de calidad, valores faltantes, tamaño y transformaciones aplicadas.

Conservar la consulta, parámetros, filtros y procedimiento de extracción. Registrar sumas de comprobación cuando se descarguen archivos. Una fuente enlazada no equivale a un conjunto descargado o validado.

## Calidad y recomendaciones agrícolas

- Verificar cobertura real, fechas, nubes u otros controles de calidad según el producto antes de utilizarlo.
- No tratar una celda satelital como una medición exacta de una parcela ni aumentar artificialmente la precisión mediante remuestreo.
- Integrar clima, suelo, agua, historial de cultivos, manejo e información local antes de recomendar especies, calendarios, rotaciones o asociaciones.
- Distinguir observaciones, estimaciones, testimonios e inferencias. Explicar incertidumbres, limitaciones y condiciones de aplicación.
- Contrastar recomendaciones con evidencia agronómica y validación local; si faltan datos críticos, registrar la brecha y presentar el resultado como preliminar.
- No inventar mediciones, rendimientos, calendarios ni beneficios de asociaciones de cultivos.

## Brechas y otras regiones

Mantener `09_cobertura_y_brechas/ESTADO_POR_REGION.md`. Por cada región o subdivisión estudiada indicar qué falta, por qué importa, fuente potencial, acción de obtención y estado. Distinguir `pendiente de verificar`, `no descargado`, `cobertura parcial` y `ausencia confirmada`; no confundir falta de evaluación con inexistencia de datos.

Para extender el alcance, seguir `10_instructivos/ACCESO_A_OTRAS_REGIONES.md` y las indicaciones de cada fuente, conservando el mismo estándar de metadatos y calidad.

## Experiencias de agricultores

Recopilar únicamente información con consentimiento y finalidad explícita. Anonimizar testimonios y ubicaciones sensibles; no publicar nombres, contactos o coordenadas de predios sin autorización. Registrar contexto, fecha, cultivo y manejo para evitar generalizar experiencias individuales.

## Estado inicial

La estructura y los enlaces fueron proporcionados para organizar el trabajo. No se han consultado catálogos, comprobado disponibilidad, descargado datos ni validado productos. Las instrucciones de acceso son una guía general y deben ajustarse a la documentación oficial vigente al iniciar una extracción.
