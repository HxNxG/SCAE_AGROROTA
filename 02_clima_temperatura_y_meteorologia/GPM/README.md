# NASA GPM IMERG para la Costa ecuatoriana

## Serie mensual descargada

La pregunta agrícola de esta extracción es cómo varían los acumulados mensuales entre temporadas agrícolas y dónde aparecen déficits o excesos frente a la climatología local.

- Institución: NASA GSFC, misión GPM. Producto IMERG Final Run L3 mensual, colección GES DISC GPM_3IMERGM 07, granulos V07B en CMR, DOI 10.5067/GPM/IMERG/3B-MONTH/07. [Catálogo NASA](https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGM_07/summary).
- Distribución: ERDDAP de University of South Florida. El distribuidor publica acumulado mensual y error en mm y enlaza la documentación V07. La cobertura coincide con CMR en el periodo consultado. La equivalencia numérica con los archivos nativos no se verificó. [Metadatos del distribuidor](https://erddap.marine.usf.edu/erddap/griddap/IMERG_monthly_global_precip.das).
- Condiciones: el catálogo de NASA declara acceso público y enlaza las condiciones de las obras del Gobierno de EE. UU. La consulta ERDDAP utilizada es pública. [Licencia en catálogo NASA](https://data.nasa.gov/dataset/gpm-imerg-final-precipitation-l3-1-month-0-1-degree-x-0-1-degree-v07-gpm-3imergm-at-ges-di-75e72).
- Consulta y descarga: 2026-11-14, hora local de Bogotá. Inicio solicitado para esta extracción: 2015-01-01. Corte: 2026-11-14. Disponibilidad efectiva: enero de 2015 a septiembre de 2025, 129 meses continuos. Octubre de 2025 al corte queda pendiente de publicación o incorporación al catálogo consultado.
- Cobertura: un rectángulo alrededor de Esmeraldas, Manabí, Santo Domingo de los Tsáchilas, Los Ríos, Guayas, Santa Elena y El Oro. Límites solicitados oeste -81.02, sur -3.89, este -78.42, norte 1.47, en coordenadas geográficas lon/lat WGS84. Fuente cartográfica [EEQ, DPA 2019](https://geoportal.eeq.com.ec/arcgis/rest/services/WEBGIS/Visor_cartografia/MapServer/31) y [límites provinciales del repositorio](../../01_suelos_y_salud_del_suelo/SMAP/geografia/limites_por_provincia.csv). El rectángulo incluye celdas de mar y de fuera de las provincias. Para calcular estadísticas administrativas, cruzar la malla con los polígonos provinciales o cantonales. El CSV conserva coordenadas por celda y no tiene asignación cantonal o parroquial.
- Resolución: 0.1° × 0.1°, un registro al mes por celda. Centros efectivos: longitudes -81.05 a -78.45 y latitudes -3.85 a 1.45, con pequeñas diferencias de representación de punto flotante. ERDDAP ajusta los extremos a los centros de su malla.
- Variables: precipitación acumulada mensual (mm), índice de calidad de precipitación (adimensional) y error aleatorio acumulado mensual (mm). Fecha UTC al inicio del mes. El CSV conserva la fila de unidades del servidor y no aplica conversiones, interpolación ni filtros de calidad locales. El índice y el error se conservan para la evaluación posterior.
- Validación: 188.082 registros, 1.458 celdas por mes, 129 meses continuos, sin duplicados por mes y coordenada, sin NaN, vacíos o negativos en las tres variables.
- Archivo: [IMERG_Costa_2015-01_2025-09.csv](IMERG_Costa_2015-01_2025-09.csv), 17.060.701 bytes. SHA-256: BE948A5EC7A88F4DAEF624077ED3ADA4C508A6D51F9903E3838E53BE47F41BBA.

## Reproducción

La [ampliación 2010–2014](IMERG_Costa_2010-01_2014-12.csv) añade 60 meses y 87.480 registros en la misma malla. Se generaron [420 registros provinciales](IMERG_provincias_2010-01_2014-12.csv) y [5.160 cantonales](IMERG_cantones_costa_2010-01_2014-12.csv). Para reproducir, añadir `--2010-2014` al comando correspondiente. Consultar el [manifiesto](ampliacion_imerg_2010_2014.json) para la URL y SHA-256. Los dos tramos cubren enero de 2010 a septiembre de 2025, que es el último mes del servidor ERDDAP consultado.

El [CSV de los 86 cantones de la Costa](IMERG_cantones_costa_2015-01_2025-09.csv) contiene 11.094 filas. La cobertura geométrica de la malla es prácticamente total para cada cantón. Ejecutar `agregar_provincias.py --cantones` con el GeoJSON DPA 2019 de EEQ. Las consultas por provincia y la suma del GeoJSON están en [el manifiesto de límites](../../01_suelos_y_salud_del_suelo/SMAP/geografia/costa_cantones_referencia_2019.json). SHA-256 del CSV: `21ba179736bff0ea03537848a4ccbd105082c8ed289e2cf7ef7e98fb317368bb`.

El [CSV cantonal de Los Ríos](IMERG_cantones_los_rios_2015-01_2025-09.csv) contiene 1.677 filas para los 13 cantones durante los 129 meses de la serie. Usa la misma ponderación que el CSV provincial y los límites cantonales DPA 2019. La malla cubre prácticamente toda el área de cada cantón. Ejecutar `agregar_provincias.py --los-rios` para reproducir. SHA-256: `f416f94a3e51a4cea3dd038b2ada4bbf819baf64ce1b762a7829e61102279d9a`.

El [CSV provincial](IMERG_provincias_2015-01_2025-09.csv) contiene 903 filas, una por mes y provincia. `agregar_provincias.py` usa la intersección geodésica de las celdas de 0,1° con los límites DPA 2019 para ponderar precipitación, índice de calidad y error de cada celda. La fracción de área cubierta es aproximadamente 100 % en las siete provincias. El error medio por celda no equivale a la incertidumbre del promedio provincial. No se aplicaron filtros al índice de calidad. SHA-256 del CSV provincial: `f46aca3b4a4108525884dbf92a445346b7f2a7a07326430b0a96b01ca2d70f48`.

1. Consultar [CMR](https://cmr.earthdata.nasa.gov/search/granules.json?concept_id=C2723754851-GES_DISC&temporal=2015-01-01T00:00:00Z,2026-11-14T23:59:59Z&page_size=200) para verificar meses publicados.
2. Usar la URL exacta y el registro de tamaño y espacio libre de [PREPARACION_DESCARGA.txt](PREPARACION_DESCARGA.txt). Descargar con Invoke-WebRequest en PowerShell o abriendo la URL en un navegador. Para una actualización, comprobar primero el último mes publicado también en ERDDAP.
3. Verificar columnas y unidades, continuidad mensual, malla, faltantes y suma de comprobación. Mantener el recorte fuera del historial Git si se incorpora control de versiones.

Para otras regiones, seguir el [instructivo común](../../10_instructivos/ACCESO_A_OTRAS_REGIONES.md).
