# MODIS Terra en la Costa ecuatoriana

Para evaluar cómo han cambiado la vegetación y la temperatura superficial entre temporadas agrícolas, se seleccionaron dos productos mensuales de NASA EOSDIS LP DAAC, colección 6.1, en la misma malla de 0,05° (unos 5,6 km en el ecuador).

| Producto | Variables descargadas | Unidades y codificación |
| --- | --- | --- |
| [MOD13C2.061](https://doi.org/10.5067/MODIS/MOD13C2.061) | NDVI, EVI y VI Quality | Índices adimensionales: dividir el entero por 10.000. Relleno -3000. Calidad en bits, relleno 65535. |
| [MOD11C3.061](https://doi.org/10.5067/MODIS/MOD11C3.061) | Temperatura superficial diurna y nocturna, QC diurno y nocturno | Multiplicar los enteros de temperatura válidos por 0,02 para obtener kelvin, o restar 273,15 al resultado para °C. Relleno de temperatura 0. Interpretar las capas QC en bits junto con la máscara de temperatura, pues QC 0 también puede corresponder a un píxel válido. |

- Consulta y descarga el 2026-11-14, hora de Bogotá. Inicio solicitado 2015-01-01. CMR registra 142 meses por producto, hasta 2026-10 inclusive. Noviembre de 2026 aún estaba en curso al corte.
- Recorte rectangular de Esmeraldas, Manabí, Santo Domingo de los Tsáchilas, Los Ríos, Guayas, Santa Elena y El Oro. Límites de referencia DPA 2019 en WGS84, oeste -81.01135, sur -3.88995, este -78.42639 y norte 1.46958. Centros descargados de -81.025 a -78.425 de longitud y -3.925 a 1.475 de latitud. Se incluyen celdas limítrofes, mar y áreas vecinas. Asignar provincia y cantón por cruce con polígonos antes de calcular estadísticas administrativas. [Límites del repositorio](../../01_suelos_y_salud_del_suelo/SMAP/geografia/limites_por_provincia.csv) · [Servicio cartográfico EEQ](https://geoportal.eeq.com.ec/arcgis/rest/services/WEBGIS/Visor_cartografia/MapServer/31).
- Los NetCDF4 contienen la malla CMG geográfica original, con 109 latitudes × 53 longitudes. El servidor recortó por índices DAP4 de base cero y seleccionó las bandas. Se conservaron los valores enteros sin remuestreo ni filtrado de calidad. Aplicar las máscaras de relleno y revisar los bits de calidad antes de estimar tendencias. La nubosidad puede cambiar el número de observaciones válidas.
- Datos públicos de NASA Earthdata con registro gratuito para acceder a OPeNDAP. Citar los DOI de ambos productos. [Política de datos de NASA Earthdata](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies).

## Reproducir el recorte

1. Consultar CMR con los enlaces de la columna catalogo de [consultas.csv](consultas.csv), que también registra la URL exacta y el archivo de destino de cada mes.
2. Iniciar sesión en Earthdata Login y aplicar la sesión autenticada a las URL OPeNDAP del manifiesto. El servidor devuelve el recorte NetCDF4. [Sintaxis de recorte DAP4](https://forum.earthdata.nasa.gov/viewtopic.php?p=26549).
3. Ejecutar validar.py con Python, NumPy y h5py para revisar cobertura, coordenadas, forma, bandas, rangos y sumas SHA-256. [Estimación previa y espacio libre](preparacion.txt).

Mantener los archivos NetCDF4 fuera del historial Git. Para otras regiones, seguir el [instructivo común](../../10_instructivos/ACCESO_A_OTRAS_REGIONES.md).

## Archivos y validación

- El tramo 2010–2014 añade 120 recortes NetCDF4, 60 por producto. [Consultas](consultas_2010_2014.csv) · [SHA-256](integridad_2010_2014.csv). La [serie agregada 2010–2014](MODIS_mensual_DPA2019_2010-01_2014-12.csv) contiene 22.320 filas para las siete provincias y los 86 cantones. Se usaron los mismos límites, bandas y filtros de calidad del tramo posterior. Para reproducir, ejecutar `descargar_2010_2014.py` y luego `agregar.py --2010-2014`. La cobertura combinada va de enero de 2010 a octubre de 2026.

- [Serie mensual por provincia y cantón](MODIS_mensual_DPA2019_2015-01_2026-10.csv): 52.824 registros, 142 meses, siete provincias y 86 cantones. `agregar.py` pondera por el área geodésica intersectada con los límites DPA 2019. Excluye relleno y conserva píxeles con los dos bits inferiores de calidad iguales a cero. La columna `fraccion_valida` indica qué parte del territorio contribuye a cada media. Si no hay área válida, la media queda vacía. SHA-256: `8a66464a5579ed3487dfc7c22bf0e165d57f4b7c7ad630ef25fc9265ddbcf6d7`.

- [MOD13C2](MOD13C2) y [MOD11C3](MOD11C3) contienen 142 archivos NetCDF4 cada uno, uno por mes. Total de 36.063.285 bytes. [Sumas SHA-256](integridad.csv).
- Se verificaron los 284 archivos, los meses consecutivos, las coordenadas, las dimensiones de cada banda y sus rangos. De 820.334 celdas-mes por banda, se registraron 221.229 valores de relleno tanto en NDVI como en EVI, 254.748 en temperatura diurna y 287.234 en nocturna. Estos conteos incluyen mar y celdas fuera de las provincias.
