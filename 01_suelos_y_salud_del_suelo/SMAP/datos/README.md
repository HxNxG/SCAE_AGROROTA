# CSV de humedad SMAP para la Costa

Producto: SPL4SMGP v008, [NSIDC / NASA](https://nsidc.org/data/spl4smgp/versions/8), DOI [10.5067/T5RUATAQREF8](https://doi.org/10.5067/T5RUATAQREF8). Al reutilizar, citar el producto conforme a la ficha oficial y describir este subconjunto.

## Archivos y alcance

- `prueba_2025_01_01/`: primer día validado, ocho intervalos y 8.360 observaciones; no es el histórico completo.
- `historico/`: recopilación reanudable desde 2015-03-31 hasta el corte efectivo 2026-11-11 00:00 UTC, último extremo encontrado antes de ejecutar. Consultar `estado.json` para saber qué meses están completos y cuáles siguen pendientes.
- `smap_costa_3horas_YYYY-MM.csv.gz`: CSV UTF-8 comprimido, separado por comas y con punto decimal. Python, pandas, R y herramientas compatibles pueden leerlo directamente; también se puede descomprimir para obtener `.csv`.
- `calidad_YYYY-MM.json`: granules de origen, conteos de registros y ausencias, tamaño y SHA-256.

El período solicitado es 2010–actualidad. SMAP no aporta 2010-01-01 a 2015-03-30. La recopilación efectiva no debe presentarse como actualizada al día de hoy cuando el catálogo termina antes. El estado `completed_catalog_intervals` significa que se procesaron todos los intervalos seleccionados del catálogo; no certifica exactitud agronómica ni calidad satelital perfecta.

## Columnas

| Columna | Significado |
| --- | --- |
| `time_start_utc`, `time_end_utc` | Inicio y final del intervalo de tres horas, en UTC; el final es exclusivo |
| `cell_id` | Celda nativa EASE2_M09; unir con `../geografia/celdas.csv` para coordenadas y con `../geografia/celda_provincia.csv` para provincias y ponderaciones |
| `sm_surface_m3_m3` | Humedad volumétrica media de la capa 0–5 cm |
| `sm_rootzone_m3_m3` | Humedad volumétrica media de la capa 0–100 cm |
| `quality_status` | Control derivado: valores presentes dentro del rango declarado o ausencia; no equivale a una bandera oficial de validación agronómica |
| `source_granule` | Nombre del archivo original, con revisión científica y revisión de archivo |

Los campos vacíos indican ausencia y no se rellenan con cero. `valid` significa únicamente que ambas variables están presentes y dentro de su rango declarado. Los datos de 2026-05-14 a 2026-07-28 incluyen además `geolocation_2026_notice_review_required`: deben revisarse frente al aviso vigente del proveedor antes de usarlos en recomendaciones.

Se almacenan una sola vez las observaciones de celdas que intersectan dos o más provincias. Los resúmenes provinciales deben usar las áreas intersectadas y reportar cobertura válida. La malla tiene 1.045 celdas únicas; 134 intersectan Los Ríos. La cobertura geométrica de las siete provincias y de los 13 cantones de Los Ríos es completa respecto de la referencia DPA 2019 utilizada. Esto no asegura datos válidos en todas las celdas y fechas ni reconoce límites legales actuales.

## Verificación inicial

El día 2025-01-01 tiene ocho intervalos consecutivos, 8.360 claves únicas y 128 valores ausentes por variable en el conjunto de la Costa. En las 134 celdas que intersectan Los Ríos hay 1.072 observaciones, todas con ambas variables presentes. Son controles de ese día, no una conclusión sobre todo el histórico.

La extracción conserva la malla nativa, sin interpolación. Los archivos globales no se descargan a disco: OPeNDAP devuelve solamente las dos variables y coordenadas del rectángulo acotado, y se retienen únicamente las celdas que intersectan las provincias. En la prueba se recibieron 344.580 bytes de subconjuntos y el CSV comprimido ocupó 105.384 bytes. Extrapolar ese día al histórico arroja un orden de 0,45 GB de CSV comprimidos; el tamaño real debe revisarse en los reportes mensuales.

## Reanudar

Para verificar los meses publicados y actualizar la serie provincial, ejecutar desde la raíz:

```powershell
& .\.venv-smap\Scripts\python.exe .\01_suelos_y_salud_del_suelo\SMAP\actualizar_resumen_provincial.py
```

El comando actualiza `historico/meses_verificados.csv` y `historico/humedad_mensual_provincial.csv`. La fracción válida del resumen usa como denominador el área provincial intersectada multiplicada por el número de intervalos publicados para el mes.

Para iniciar o reanudar en segundo plano en Windows, manteniendo el equipo encendido y con Internet:

```powershell
& .\01_suelos_y_salud_del_suelo\SMAP\iniciar_historico.ps1
```

El lanzador comprueba que no haya otro proceso del histórico, ejecuta sin ventana y guarda `historico/recopilacion.log`, `historico/recopilacion.err.log` y `historico/proceso.json`. `estado.json` es una instantánea: comprobar que el proceso siga activo antes de interpretar `running` como una descarga en curso. Cerrar o suspender el equipo puede interrumpir la recopilación; se puede reanudar con el mismo comando.

Para ejecutar en primer plano:

Desde la raíz del repositorio:

```powershell
& .\.venv-smap\Scripts\python.exe -u .\01_suelos_y_salud_del_suelo\SMAP\recopilar_humedad.py --start 2015-03-31 --end 2026-11-11 --name historico --workers 4
```

`--end` es exclusivo. No ejecutar dos procesos sobre la misma carpeta de salida. Se reutilizan fragmentos con SHA-256 correcto y meses completos compatibles con el catálogo guardado. Las fechas y el nombre deben mantenerse para reanudar la misma ejecución; una actualización a otro corte requiere una carpeta distinta y comparar resultados antes de sustituir archivos.

El catálogo se deduplica por inicio UTC, conservando la mayor revisión científica `Vv`, luego revisión de archivo y fecha de actualización. Conservar el catálogo como evidencia: una selección reproducible no implica que los reprocesamientos futuros ya estén incorporados.
