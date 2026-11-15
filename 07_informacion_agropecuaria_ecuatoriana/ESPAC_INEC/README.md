# ESPAC 2025 para la Costa

Fuente: Instituto Nacional de Estadística y Censos (INEC), Ecuador. Se usaron los tabulados oficiales de la [ESPAC 2025](https://www.ecuadorencifras.gob.ec/estadisticas-agropecuarias-2/) y del [Módulo de Información Agroambiental y Tecnificación 2025](https://www.ecuadorencifras.gob.ec/informacion-agroambiental/). Fecha de consulta y extracción: 14 de noviembre de 2026.

Cada CSV conserva el código DPA, el nombre provincial, la hoja y la fila de origen. El ámbito es provincial y cubre Esmeraldas, Manabí, Santo Domingo de los Tsáchilas, Los Ríos, Guayas, Santa Elena y El Oro. Son estimaciones de una encuesta para 2025.

| Archivo | Contenido | Fuente |
| --- | --- | --- |
| `costa_cultivos_2025.csv` | 518 filas de 37 productos y dos condiciones de cultivo; superficie, producción y ventas | ESPAC, T12–T48 |
| `costa_uso_suelo_2025.csv` | Superficie en hectáreas por categoría, siete filas | ESPAC, T1 |
| `costa_riego_transitorios_2025.csv` | Superficie regada en hectáreas por método, siete filas | Módulo agroambiental, T14 |
| `costa_labranza_transitorios_2025.csv` | Superficie en hectáreas por tipo de labranza, siete filas | Módulo agroambiental, IND_1 |

Se conservaron las celdas vacías y la precisión numérica publicada. El rendimiento derivado divide toneladas de producción por hectáreas cosechadas cuando ambos valores existen y la superficie es positiva. La condición “Asociado” es la clasificación del tabulado y no identifica las especies acompañantes. Para interpretar estimaciones y comparabilidad, consultar la [metodología ESPAC 2025](https://www.ecuadorencifras.gob.ec/documentos/web-inec/Estadisticas_agropecuarias/espac/2025/Metodologia_ESPAC25.pdf).

Ejecutar `extraer.py` con Python y openpyxl para reproducir la descarga. `origen.json` registra las URL, tamaños y SHA-256 de los libros de origen. Citar al INEC conforme a las indicaciones en los libros. Quedan pendientes los calendarios y los datos a escala cantonal y de parcela.

## Ediciones anteriores incorporadas

`costa_cultivos_ediciones_2018_2024.csv` reúne 3.625 filas de las siete ediciones entre 2018 y 2024. Cada edición incluye las siete provincias y 37 tabulados de cultivos. En 2019, se conservan por separado las dos secciones de banano que distingue el INEC. Las filas ausentes en la fuente quedan sin imputar. Verificar la presentación del producto y la metodología de cada año antes de unir las series.

`costa_cultivos_ediciones_2014_2017.csv` añade 1.918 filas. Cubre las siete provincias en cada edición. Incluye 29 tabulados en 2014, 32 en 2015 y 38 por año en 2016 y 2017. Los puntos que marcan valores ausentes se exportan como campos vacíos.

`costa_cultivos_ediciones_2010_2013.csv` contiene 1.456 filas de 26 tabulados por año para las siete provincias. Los marcadores `.`, `..` y `*` se exportaron como celdas vacías. Conservar el año, la hoja y la fila para recuperar las notas originales de cada tabulado.

Para reproducir, ejecutar `extraer_historico.py` con Python y openpyxl y el argumento `2010_2013`, `2014_2017` o `2018_2024`. Los archivos JSON de origen registran las URL y los SHA-256.
