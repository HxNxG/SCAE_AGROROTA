# MapBiomas Ecuador · superficie provincial 2015–2025

Descarga del 14 de noviembre de 2026. [Colección 4, cobertura y uso del suelo](https://ecuador.mapbiomas.org/iniciativas-y-productos/cobertura-y-uso-del-suelo/cobertura-30m/), estadísticas versión 1-0, licencia CC BY 4.0. Se descargó la [tabla oficial provincial](https://ecuador.stg.mapbiomas.org/wp-content/uploads/sites/8/2026/09/mapbiomas-ecuador-collection-4-coverage-provincia_conali_2024_e47848f9-1-0.xlsx) (224094 bytes, SHA-256 0e3d6162d068766b4491e1e9b84e86760da465845dae11ac41663e41bf6dec40).

El [CSV](superficie_provincial_2015_2025.csv) contiene 1232 filas de superficies estimadas en hectáreas por clase y año. Se extrajo la hoja pivot_ha, se filtraron siete códigos provinciales y las columnas y2015 a y2025, y se normalizaron los nombres provinciales por código. Se conservaron las clases y los valores originales. Se verificaron 77 pares provincia-año, claves únicas y valores no negativos. SHA-256 del CSV: 21f93188b2de48463fe164931dd378edc0d95707dcb17ae9f3939dff014b2b36.

El recorte de la tabla corresponde a CONALI 2024 (PROVINCIA_CONALI_2024_E47848F9). Es una agregación provincial de mapas anuales Landsat de 30 m. Queda pendiente una validación local de las clases. El año 2025 es el último de la colección. Los GeoTIFF se obtuvieron por las exportaciones provinciales de la plataforma oficial.

Para reproducir la extracción, guardar la tabla oficial y asignar su ruta a MB_TEMP. Asignar a MB_OUT la carpeta de salida y ejecutar uv run --python 3.13 --with openpyxl python extraer_superficie.py.

## Cobertura 2010–2025

El [resumen cantonal](superficie_canton_CONALI2024_2010_2025.csv) contiene 14.832 filas para 86 cantones y 16 años. Suma las superficies de las parroquias publicadas por los cuatro primeros dígitos del código DPA, año y clase. Se comprobó que los 86 códigos tienen una correspondencia única con el nombre cantonal de la fuente y que los totales por año y clase coinciden con la tabla parroquial. `parroquias_con_fila` cuenta registros de origen por clase. SHA-256: `9e8c26f6e1694604eef9a875e72b01471ec27ae0fa10de6b38c5870f57ae156c`.

Se incorporaron [1.792 filas provinciales](superficie_provincia_CONALI2024_2010_2025.csv) y [44.720 filas de 313 parroquias](superficie_parroquia_CONALI2024_2010_2025.csv). La tabla parroquial incluye el cantón declarado por la fuente. Las dos extracciones usan la hoja `pivot_ha`, las columnas `y2010` a `y2025` y los códigos provinciales 07, 08, 09, 12, 13, 23 y 24. Ambas conservan clases y superficies de CONALI 2024. Para unirlas con capas DPA 2019, comprobar cambios de límites.

La [tabla oficial parroquial](https://ecuador.stg.mapbiomas.org/wp-content/uploads/sites/8/2026/09/mapbiomas-ecuador-collection-4-coverage-parroquia_conali_2024_16528a13-1-0.xlsx) ocupa 4.801.993 bytes y tiene SHA-256 `2f0c75d22045b773e3d16e80a97f1de61d92ae3d6faf1d243422a90919e596b0`. SHA-256 de las salidas provincial y parroquial, respectivamente, `0c4de47a5330389cff07a87d76151b7cdf3fc1cdb3648cab6ffd919d60a540ac` y `efff9bd1998733bc7e371fcf00d2bb55d39e43c9cf41433cb479f296a78270d6`.

## GeoTIFF anuales de la Costa

Once archivos costa_conali2024_col4_AAAA.tif, desde 2015 hasta 2025. Se unieron 77 exportaciones de cobertura de MapBiomas Ecuador, una por provincia y año, usando su categoría provincial CONALI 2024. Los mosaicos conservan la cuadrícula EPSG:4326 de origen (0,000269494585° por píxel, aproximadamente 30 m en el ecuador), las clases originales y el valor 0 como NoData. Se guardaron como GeoTIFF de una banda, UInt8, con compresión LZW.

Se verificó la alineación de las siete fuentes, se comprobó un píxel válido por provincia y año contra su exportación de origen, y se verificaron las sumas SHA-256 de los 11 mosaicos. El [manifiesto](manifiesto_geotiff.json) contiene las URLs de exportación, conteos por clase, cobertura y sumas de comprobación. Consultar la [leyenda oficial](https://ecuador.mapbiomas.org/descargas/informacion-de-la-leyenda/).

Para reproducir la descarga y el mosaico desde la raíz: uv run --no-project --python 3.13 --with rasterio python 04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/descargar_geotiffs.py