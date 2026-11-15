# Inventario priorizado de fuentes y bases de datos

Fecha de actualización: 14 de noviembre de 2026.

Alcance: Costa del Ecuador, conforme a [REGLAS.md](REGLAS.md). Las prioridades, variables y aplicaciones de esta tabla corresponden a la planificación proporcionada por el equipo; no constituyen una verificación de disponibilidad de los productos.

## Fuentes por prioridad

| Fuente | Datos útiles previstos | Aplicación en la web | Prioridad | Estado de trabajo | Carpeta |
| --- | --- | --- | --- | --- | --- |
| NASA POWER | Temperatura, lluvia, humedad relativa, radiación | Aptitud climática y calendario de siembra | Alta | CSV provisional recibido y revisado; histórico definitivo y nueva descarga pendientes | [NASA_POWER](02_clima_temperatura_y_meteorologia/NASA_POWER/README.md) |
| ISRIC SoilGrids | pH, textura, carbono, nitrógeno | Aptitud y recuperación del suelo | Alta | 144 capas SoilGrids 2.0 de 250 m descargadas y verificadas | [ISRIC](01_suelos_y_salud_del_suelo/ISRIC/README.md) |
| NASA SMAP | Humedad superficial y radicular | Riesgo de déficit hídrico | Alta | Acceso verificado; malla de 1.045 celdas con Los Ríos; CSV de prueba validado e histórico en recopilación | [SMAP](01_suelos_y_salud_del_suelo/SMAP/README.md) |
| NASA GPM IMERG | Precipitación espacial y temporal | Lluvias, sequías y anomalías | Alta | Serie mensual 2010-01 a 2025-09 con agregados para siete provincias y 86 cantones | [GPM](02_clima_temperatura_y_meteorologia/GPM/README.md) |
| Landsat / HLS | Bandas espectrales, índices de vegetación | Estado de la vegetación por parcela, sujeto a resolución y calidad disponibles | Alta | Pendiente de asignación y evaluación; documentar por separado los productos Landsat y HLS elegidos | [LANDSAT](04_vegetacion_cultivos_y_monitoreo/LANDSAT/README.md) |
| SRTM | Elevación y pendiente | Restricciones del terreno | Media | Pendiente de asignación y evaluación | [SRTM](05_topografia_y_modelado_del_terreno/SRTM/README.md) |
| MODIS | NDVI, EVI, temperatura superficial | Tendencias históricas regionales | Media | Serie mensual 2010-01 a 2026-10 con agregados y calidad para siete provincias y 86 cantones | [MODIS](04_vegetacion_cultivos_y_monitoreo/MODIS/README.md) |
| ECOSTRESS | Temperatura superficial, evapotranspiración | Estrés térmico e hídrico | Media | Piloto descargado en siete provincias; dos ventanas con píxeles comunes válidos | [ECOSTRESS](03_agua_y_recursos_hidricos/ECOSTRESS/README.md) |
| GRACE-FO | Cambios regionales en almacenamiento de agua | Contexto de sequía a gran escala | Baja | Pendiente de asignación y evaluación | [GRACE_Y_GRACE_FO](03_agua_y_recursos_hidricos/GRACE_Y_GRACE_FO/README.md) |
| NASA Harvest | Investigación y herramientas agrícolas | Referencia metodológica | Complementaria | Protocolo GEOGLAM adaptado; GLAD como referencia histórica; [serie provincial y GeoTIFF MapBiomas 2015–2025](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/README.md) descargada; validación local pendiente | [NASA_HARVEST](04_vegetacion_cultivos_y_monitoreo/NASA_HARVEST/README.md) |

El orden dentro de cada prioridad sigue la lista del equipo y no establece una dependencia obligatoria entre fuentes.

## Coordinación y orden de atención

1. NASA POWER cuenta con un CSV provisional recibido y una [revisión de utilidad](02_clima_temperatura_y_meteorologia/NASA_POWER/REVISION_UTILIDAD.md). El histórico común se definió como 2010–actualidad; la nueva descarga de POWER sigue pendiente en su propia tarea. Coordinar con la persona responsable y conservar el archivo actual hasta validar su reemplazo.
2. Atender las demás fuentes de prioridad alta: SoilGrids, SMAP, GPM IMERG y Landsat / HLS. Antes de descargar, seleccionar productos y evaluar cobertura, calidad y tamaño para la Costa.
3. Incorporar SRTM, MODIS y ECOSTRESS según las necesidades del análisis, respetando su prioridad media.
4. Evaluar GRACE-FO como contexto regional de prioridad baja y NASA Harvest como apoyo metodológico complementario.

## Pendientes antes de considerar una fuente lista

- Registrar responsable y estado real: pendiente, en trabajo, disponible para revisión o validada.
- Identificar productos y versiones concretos. Los nombres de misión, proveedor o programa no bastan como identificadores de una base.
- Confirmar para cada variable su disponibilidad, origen, unidades, resolución, profundidad cuando corresponda y controles de calidad. No asumir que todas las variables de una fila provienen del mismo producto.
- Documentar cobertura espacial y temporal de la Costa, procedimiento reproducible, licencia y tamaño estimado antes de descargar.
- Registrar diferencias de escala y período antes de combinar lluvia de POWER e IMERG, o variables de vegetación y temperatura de distintas fuentes.
- Actualizar el [estado por región](09_cobertura_y_brechas/ESTADO_POR_REGION.md) con las carencias comprobadas. Un estado de trabajo no confirma que ya existan datos descargados o validados.

## Recursos de acceso y evidencia complementaria

Worldview, Giovanni, AppEEARS y VEDA se mantienen en [visualización, exploración y GIS](06_visualizacion_exploracion_y_gis/) como recursos de consulta o procesamiento, sin prioridad independiente de descarga en esta lista.

La [información agropecuaria ecuatoriana](07_informacion_agropecuaria_ecuatoriana/README.md) y las [experiencias de agricultores](08_experiencias_de_agricultores/README.md) siguen siendo insumos necesarios del proyecto. Su prioridad específica está pendiente de definición; esta tabla no las reemplaza.

Para otras regiones, seguir el [instructivo de acceso](10_instructivos/ACCESO_A_OTRAS_REGIONES.md), conservando enlaces y procedimientos antes de almacenar nuevos datos.

## Histórico común definido: 2010–actualidad

El equipo acordó 2010–actualidad el 14 de noviembre de 2026. Registrar corte explícito, última fecha publicada y cobertura efectiva por producto. SMAP L4 comienza el 2015-03-31: no dispone del tramo anterior solicitado. Se mantiene el recorte a la Costa y la inclusión de Los Ríos. La autenticación Earthdata está verificada; SMAP tiene CSV de prueba validado e histórico en recopilación. Consultar el estado en su carpeta de datos.
