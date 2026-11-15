# Piloto de humedad del suelo en Babahoyo

## Fuente y cobertura comprobada

El producto NASA/NSIDC **SMAP L4 SPL4SMGP v008** ofrece estimaciones de humedad volumétrica en intervalos de tres horas. La malla original es EASE-Grid 2.0 Global (EPSG:6933), nominalmente de 9 km. La capa superficial cubre **0–5 cm** y la radicular **0–100 cm**. Ambas se expresan en **m³/m³**. El producto requiere una cuenta Earthdata para descargar datos y la correspondiente cita al reutilizarlos. [Ficha de NSIDC y condiciones de cita](https://nsidc.org/data/spl4smgp/versions/8)

| Evidencia | Alcance verificable |
| --- | --- |
| [Malla y cobertura DPA 2019](../../01_suelos_y_salud_del_suelo/SMAP/geografia/cobertura_malla_los_rios_cantones.csv) | Babahoyo (DPA 1201) intersecta 28 celdas. La cobertura geométrica del cantón es 100 %. |
| [Resumen mensual provincial](../../01_suelos_y_salud_del_suelo/SMAP/datos/historico/humedad_mensual_provincial.csv) y [manifiesto de meses](../../01_suelos_y_salud_del_suelo/SMAP/datos/historico/meses_verificados.csv) | Los Ríos tiene 141 períodos mensuales registrados de marzo de 2015 a noviembre de 2026, dos variables por período. El primer y último mes son parciales. El último intervalo registrado inicia el 10 de noviembre a las 21:00 UTC. |
| [Muestra del 1 de enero de 2025](../../01_suelos_y_salud_del_suelo/SMAP/datos/prueba_2025_01_01/calidad_2025-01.json) | Comprobé el SHA-256 del CSV.GZ local contra el manifiesto y crucé el límite de Babahoyo con la malla nativa. Los ocho intervalos cubren las 28 celdas con 224 claves únicas y valores válidos en ambas profundidades según el control derivado del repositorio. |

El clon versiona malla, metadatos y promedios de Los Ríos. Los CSV.GZ por celda quedan fuera de Git e incluyen la muestra local verificada del 1 de enero de 2025. Los promedios de Los Ríos se pueden mostrar como contexto provincial en una ficha. Para pintar el mapa histórico por celda se necesita preparar y verificar un recorte de las observaciones originales. [Guía de los CSV SMAP](../../01_suelos_y_salud_del_suelo/SMAP/datos/README.md)

## Representación propuesta

- Añadir al selector **Humedad superficial (0–5 cm)** y **Humedad radicular (0–100 cm)**. Mostrar la variable, profundidad, unidad, fecha, escala de 9 km y fuente junto a la leyenda. Usar para ambas una escala secuencial fija de marrón claro a verde azulado. Los intervalos de color son descriptivos.
- Construir las huellas con los centros de `celdas.csv` y los pasos de `malla_resumen.json` (9.008,0557 m en ambos ejes). Seleccionar las celdas con intersección de área positiva en EPSG:6933 para Babahoyo y proyectar los vértices a longitud y latitud WGS 84 para el visor. La ficha de una celda muestra su valor y su cobertura, independientemente de la parcela que contenga.
- El primer piloto puede ofrecer los ocho fotogramas originales del 1 de enero de 2025. Mantener fechas UTC en la API y señalar explícitamente la zona horaria que use el visor. Para un histórico mensual posterior, promediar por celda y variable los intervalos válidos de cada período y publicar los conteos de intervalos disponibles, válidos y esperados. Marcar los meses incompletos como parciales.
- Pintar cobertura faltante con un estilo neutro y mostrar **Sin dato** en la ficha. Conservar los ceros explícitos válidos. Evitar interpolación, extrapolación y relleno con valores de la otra profundidad. Los datos del 14 de mayo al 28 de julio de 2026 requieren revisión de geolocalización antes de agregarlos. [Aviso y versiones del producto](https://nsidc.org/data/spl4smgp/versions/8)

## Contrato propuesto

El piloto utiliza `GET /api/v1/climate/babahoyo/moisture?depth=surface|rootzone`. Devuelve la fuente, unidad, resolución y los ocho fotogramas UTC con las huellas de las celdas y sus valores. Los siguientes endpoints corresponden al diseño para un histórico ampliado.

El recorte versionado corresponde a Babahoyo, el 1 de enero de 2025. Cita del producto: Reichle y colaboradores (2025), NASA NSIDC DAAC, [SMAP L4 SPL4SMGP v008](https://doi.org/10.5067/T5RUATAQREF8). Para regenerarlo desde la raíz, ejecuta `python proyecto-agricultura-ia/scripts/build_babahoyo_smap.py --source <CSV.GZ>` con Shapely 2.1 o posterior y pyproj.

- `GET /api/v1/climate/babahoyo/smap/periods?aggregation=3h` enumera los períodos del recorte efectivamente disponible. Cada entrada contiene `start`, `end` (exclusivo) y `coverage_status`. Ofrecer `aggregation=monthly` cuando se publique un recorte mensual.
- `GET /api/v1/climate/babahoyo/smap/cells?depth=surface&aggregation=3h&start=2025-01-01T00:00:00Z` devuelve `product`, `doi`, `depth` (`surface` o `rootzone`), `depth_cm`, `unit` (`m3/m3`), `native_crs`, `resolution_km`, `start`, `end`, `coverage_status` y `cells`.
- Cada celda contiene `cell_id`, `geometry` GeoJSON Polygon en longitud/latitud WGS 84, `value` numérico o `null`, `quality` (`valid`, `missing`, `partial` o `review_required`) e `intervals_valid` e `intervals_expected`. Devolver celdas con `null` cuando hay un período publicado con cobertura parcial. Para una fecha válida sin recorte disponible, devolver `coverage_status: "unavailable"` y `cells: []`. Un parámetro inválido devuelve HTTP 422.

## Aceptación del piloto

Verificar el recorte contra el manifiesto y conservar el método, SHA-256, geometría de referencia y gránulos. Para la muestra inicial, comprobar ocho intervalos y 28 huellas, comparar valores de ambas profundidades con el CSV y probar ausencia temporal, celdas faltantes y cero válido. Confirmar que el visor actualiza escala, fecha y unidades al alternar capas, y que el zoom conserva la geometría original.
