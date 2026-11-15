# Plan de recopilación SMAP en CSV para la Costa

Revisión documental: 14 de noviembre de 2026. Prioridad alta. Actualización: el equipo definió el período solicitado como 2010–actualidad. SMAP L4 comienza el 2015-03-31. Se inició la recopilación de geometrías y metadatos públicos; series de humedad, autenticación y malla siguen pendientes. Consultar el [estado actualizado](ESTADO_RECOPILACION.md); esta nota sustituye las referencias de planificación a fechas no definidas.

## Productos y utilidad

| Producto | Qué aporta | Papel propuesto |
| --- | --- | --- |
| SPL4SMGP, versión 8 consultada | Humedad superficial y radicular; malla EASE-Grid 2.0 de 9 km; frecuencia de tres horas | Fuente principal para ambas profundidades y evolución del déficit hídrico |
| SPL3SMP_E, versión 6 consultada | Recuperación radiométrica de humedad superficial en una malla publicada de 9 km, producto diario | Contraste superficial complementario; no sustituye la humedad radicular de L4 |

Las versiones deben comprobarse de nuevo antes de ejecutar. No mezclar versiones silenciosamente. Fuentes: [ficha L4](https://nsidc.org/data/spl4smgp/versions/8) y [ficha L3 Enhanced](https://nsidc.org/data/spl3smp_e/versions/6).

Según la [guía L4 v8](https://nsidc.org/sites/default/files/documents/user-guide/multi_spl4smau-v008-userguide.pdf), L4 integra observaciones con un modelo terrestre. La humedad superficial representa 0–5 cm y la radicular 0–100 cm; las variables de interés son `sm_surface` y `sm_rootzone`, expresadas como fracción volumétrica (m³/m³). La profundidad radicular es una definición del producto, no la profundidad efectiva de las raíces de cualquier cultivo. El producto se distribuye en HDF5: la salida CSV requiere transformar los datos seleccionados.

Estas series sirven para seguimiento regional y comparación estacional. No bastan para calcular necesidades de riego o fijar umbrales universales: se requieren textura, capacidad de campo, punto de marchitez, cultivo, lluvia y validación local. Una celda de 9 km no representa una medición por parcela. En L3, la separación de la malla tampoco debe confundirse con la resolución efectiva de la observación.

## Verificación geográfica y Los Ríos

El alcance administrativo del repositorio comprende Esmeraldas, Manabí, Santo Domingo de los Tsáchilas, Los Ríos, Guayas, Santa Elena y El Oro. Los Ríos se incluye expresamente como provincia completa, no como una franja próxima al mar. Su [PDOT provincial 2024–2027](https://losrios.gob.ec/folder/1721399024diagn%C3%B3stico_pdyot_los_rios_18-07-2024.pdf) permite contrastar los 13 cantones: Baba, Babahoyo, Buena Fe, Mocache, Montalvo, Palenque, Puebloviejo, Quevedo, Quinsaloma, Urdaneta, Valencia, Ventanas y Vinces.

La coordenada de la muestra POWER (-2,19; -79,90) es un punto, no una delimitación de la Costa. No usarla como único centro para seleccionar SMAP.

Se propone **recorte por polígonos provinciales y selección de celdas nativas**, en lugar de un radio único:

1. Obtener la capa provincial con procedencia y fecha identificables mediante el [banco cartográfico del INEC](https://aplicaciones3.ecuadorencifras.gob.ec/sbi-war/paginas/cartografia_2.xhtml) o la [entrega de límites del Ministerio de Gobierno](https://www.ministeriodegobierno.gob.ec/entrega-del-trazado-de-limites-territoriales-internos-y-organizacion-territorial-del-estado/). Distinguir límites estadísticos de límites legales; registrar escala, vigencia y restricciones.
2. Validar geometrías, seleccionar las siete provincias y conservar Los Ríos como geometría independiente para el control. Disolver una copia para formar el área de estudio.
3. Transformar una copia a WGS84 para la búsqueda remota; respetar el orden longitud, latitud. Calcular la caja envolvente desde los polígonos, sin inventar sus extremos numéricos.
4. Usar la caja solamente para localizar y recortar granules. Para el resultado definitivo, intersectar las huellas de las celdas nativas con los polígonos. Incluir toda celda con intersección de área positiva, aunque su centro esté fuera de la provincia; no seleccionar únicamente centros interiores.
5. Calcular áreas y fracciones de intersección en una proyección equivalente adecuada. Conservar identificadores de fila y columna de la malla y centros en latitud/longitud. No construir una cuadrícula arbitraria más fina ni interpolar para aparentar mayor precisión.
6. Crear una relación celda–provincia con fracción de área. Una celda de frontera puede corresponder a varias provincias, pero su observación se almacena una sola vez.

### Condiciones para afirmar que Los Ríos está incluido

- El polígono provincial está presente y su selección no depende de coincidencias frágiles de tildes o mayúsculas; verificar también identificadores administrativos.
- La unión de las huellas seleccionadas cubre el polígono completo dentro de la tolerancia geométrica documentada. Reportar área no cubierta y número de celdas que lo intersectan.
- Contrastar los 13 cantones con una capa cantonal compatible y reportar intersecciones y huecos por cantón. No exigir que cada cantón tenga un centro de celda propio.
- Separar cobertura geométrica de disponibilidad: una celda puede intersectar Los Ríos y no tener humedad válida. Reportar por fecha celdas válidas, ausentes y área representada.
- No descartar silenciosamente zonas de agua, humedales o celdas mixtas. Registrar máscaras y limitaciones; un dato ausente no equivale a humedad cero.

**Pendiente:** no se han obtenido ni procesado los polígonos. Por tanto, aún no están verificados los extremos geográficos, el número de celdas ni el porcentaje efectivo de cobertura. La lista administrativa está contrastada documentalmente; la validación espacial debe ejecutarse antes de descargar el histórico.

## Ruta reproducible de acceso y conversión

1. Crear o utilizar una cuenta NASA Earthdata Login y buscar `SPL4SMGP` en [Earthdata Search](https://search.earthdata.nasa.gov/). No guardar credenciales en el repositorio.
2. Una vez definido el histórico, seleccionar versión, fechas y área; comprobar la disponibilidad real de granules. No adoptar automáticamente las fechas de POWER.
3. Solicitar únicamente las dos variables, geolocalización y campos auxiliares necesarios para calidad y trazabilidad. NSIDC documenta [subconjuntos y transformaciones mediante Harmony](https://nsidc.org/data/user-resources/help-center/what-data-subsetting-reformatting-and-reprojection-services-are-available-smap-data); revisar qué opciones admite la colección concreta. No asumir que entrega CSV directamente.
4. Priorizar recorte en origen. Si no está habilitado para la operación necesaria, evaluar lectura remota o descarga temporal por lotes pequeños, estimando el espacio antes de ejecutar. Evitar acumular archivos globales.
5. Leer los HDF5 recortados con herramientas compatibles, por ejemplo `h5py`, y convertir solamente las celdas seleccionadas a una tabla. Verificar rutas de grupos, atributos de unidades, tiempo, relleno y escalado en los archivos reales antes de programar la extracción.
6. Mantener inicialmente las horas UTC del producto. Si se genera un resumen diario para compararlo con POWER, acordar explícitamente UTC, hora civil o LST; son convenciones diferentes.
7. Exportar CSV UTF-8 por mes, preferentemente comprimido como `.csv.gz`, y un manifiesto con consulta, versión, granules, fecha de extracción, transformaciones y controles. Eliminar temporales regenerables solo después de validar el resultado.

No se ha probado una petición autenticada ni una conversión real. La ejecución dependerá del acceso Earthdata, las opciones de servicio y las fechas acordadas.

## Tablas propuestas

Separar geometría y observaciones evita repetir metadatos en cada fecha:

- `celdas.csv`: `cell_id,grid_row,grid_col,latitude,longitude,grid_crs`.
- `celda_provincia.csv`: `cell_id,provincia_id,provincia,intersection_area_m2,province_area_fraction,cell_area_fraction`.
- `smap_3horas_YYYY_MM.csv.gz`: `time_utc,cell_id,sm_surface_m3_m3,sm_rootzone_m3_m3,source_granule_id,quality_status`.
- Opcional `smap_diario_YYYY_MM.csv.gz`: `date,day_standard,cell_id,sm_surface_mean_m3_m3,sm_rootzone_mean_m3_m3,n_valid_surface,n_valid_rootzone,n_expected`.

`quality_status` es un campo derivado cuyo criterio debe documentarse; no implica que exista una bandera nativa con ese nombre. Conservar los indicadores originales pertinentes en una tabla auxiliar cuando estén disponibles. Usar campos vacíos para valores ausentes, con su motivo registrado.

Para un día UTC completo se esperan ocho intervalos de tres horas. Registrar conteos por variable y no presentar días incompletos como completos. Los promedios provinciales deben ponderarse por área intersectada válida y reportar su cobertura.

## Controles, tamaño y pendientes

- Clave única: producto, versión, instante y celda. Revisar duplicados, orden, intervalos faltantes, valores de relleno, unidades y rangos definidos por el producto.
- Verificar mapas de cobertura antes y después de aplicar máscaras, especialmente en Los Ríos.
- Estimar filas como `n_celdas × n_días × 8` para L4 de tres horas. Medir bytes por fila en un lote pequeño para estimar tamaño y espacio temporal; todavía no hay una cifra fiable sin construir la selección espacial.
- No calcular anomalías o percentiles hasta definir una referencia histórica comparable; no inventar categorías de déficit.
- Revisar avisos de calidad antes de extraer: la [ficha L4 consultada](https://nsidc.org/data/spl4smgp/versions/8) informa un problema de geolocalización entre el 14 de mayo y el 28 de julio de 2026, con reprocesamiento en curso. Si el histórico incluye ese intervalo, confirmar que los granules descargados sean los corregidos o registrar la limitación.
- Próximos pasos: obtener límites, construir y comprobar la selección espacial, definir fechas, verificar acceso y ejecutar un lote acotado antes del histórico completo.
