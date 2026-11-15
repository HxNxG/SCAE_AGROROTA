# Revisión del archivo NASA POWER recibido

Fecha de revisión: 14 de noviembre de 2026.

## Archivo y alcance observado

- Archivo: `POWER_Point_Daily_20200131_20251231_002d19S_079d90W_LST.csv`.
- Tamaño: 106.770 bytes.
- Ubicación del encabezado: latitud -2,19; longitud -79,90. Es una consulta puntual, no un inventario espacial de toda la Costa.
- Período observado: 2020-01-31 a 2025-12-31, frecuencia diaria, estándar temporal LST (tiempo solar local).
- El encabezado atribuye meteorología a MERRA-2 y radiación a CERES SYN1deg. Informa una región de 0,5 × 0,625 grados para la elevación MERRA-2; esta información no debe aplicarse automáticamente como resolución de todas las variables.
- Versión del producto, fecha de descarga, licencia y consulta original: no documentadas en el archivo recibido; pendientes de completar.

## Controles realizados sobre el CSV

| Control | Resultado |
| --- | --- |
| Registros diarios | 2.162 |
| Fechas duplicadas | 0 |
| Días ausentes dentro del intervalo observado | 0 |
| Valores con marcador de ausencia `-999` en las siete variables | 0 |
| Casos que incumplen temperatura mínima ≤ media ≤ máxima | 0 |
| Registros por año | 2020: 336; 2021: 365; 2022: 365; 2023: 365; 2024: 366; 2025: 365 |

El año 2020 no está completo: faltan los días 1–30 de enero respecto de un año calendario, aunque no hay huecos dentro del intervalo solicitado. Estos controles comprueban consistencia básica, no exactitud frente a estaciones meteorológicas ni validación agronómica.

| Variable | Unidad según encabezado | Mínimo observado | Máximo observado | Utilidad prevista |
| --- | --- | --- | --- | --- |
| T2M | °C | 24,17 | 30,55 | Estacionalidad térmica y comparación con requerimientos de cultivos |
| T2M_MAX | °C | 26,57 | 41,01 | Exploración de episodios de calor |
| T2M_MIN | °C | 18,71 | 25,50 | Condiciones térmicas mínimas |
| PRECTOTCORR | mm/día | 0 | 66,97 | Acumulados mensuales y exploración de períodos secos |
| ALLSKY_SFC_SW_DWN | MJ/m²/día | 5,84 | 22,56 | Disponibilidad de radiación y entrada para modelos agroclimáticos |
| WS2M | m/s | 0,72 | 4,31 | Contexto de viento y entrada para modelos que requieran esta variable |
| RH2M | % | 50,41 | 92,92 | Contexto de humedad atmosférica |

## Dictamen de utilidad

Útil como muestra provisional para probar lectura, agregaciones mensuales, gráficos y estructura de integración de la web. Permite explorar la variación estacional en el punto consultado y comparar los años completos 2021–2025.

Su utilidad para aptitud climática y calendarios de siembra es preliminar: requiere requisitos por cultivo, información de suelo y agua, y contraste local. El CSV no aporta humedad del suelo ni identifica por sí mismo rotaciones o asociaciones adecuadas.

No representa todas las provincias ni las diferencias agroclimáticas de la Costa. Tampoco debe usarse como medición exacta por parcela, pronóstico futuro o base histórica definitiva para tendencias de cambio climático y anomalías de largo plazo. Los cinco años completos disponibles no sustituyen una referencia climática de largo plazo.

La [documentación oficial de la API diaria de NASA POWER](https://power.larc.nasa.gov/docs/services/api/temporal/daily/) indica que las variables se entregan en la resolución espacial de su fuente y permite especificar LST o UTC. Al integrar otras bases se debe comprobar esa compatibilidad temporal y espacial, sin interpretar LST automáticamente como hora civil de Ecuador.

## Nueva descarga pendiente

El histórico común para los datos de fuentes globales aún no está definido. Este intervalo se conserva como muestra, sin adoptarlo como estándar del repositorio.

Cuando el equipo acuerde fecha inicial y final, el asistente deberá volver a descargar NASA POWER para ese período y la cobertura de la Costa que se defina, respetando disponibilidad por variable y almacenamiento limitado. Registrar parámetros, fechas, coordenadas o área, estándar temporal, versión disponible, fecha de extracción y controles; comparar el nuevo resultado antes de reemplazar el CSV actual. No se realizó una nueva descarga en esta revisión.
