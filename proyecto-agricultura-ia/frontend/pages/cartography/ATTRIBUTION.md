# Fuentes de los límites territoriales

Límites territoriales de la Organización Territorial del Estado interparroquiales, aprobados por el Directorio del CONALI en sesión ordinaria del 24 de marzo de 2022, 17 de enero de 2023 y 13 de marzo de 2026.

- Fuente original: Comité Nacional de Límites Internos (CONALI), Dirección de Límites Territoriales Internos del Ministerio de Gobierno del Ecuador. [Organización Territorial Parroquial, Datos Abiertos Ecuador](https://www.datosabiertos.gob.ec/dataset/organizacion-territorial-parroquial?activity_id=e5e0e58b-2812-4d13-987a-2970fe788ba3).
- Licencia de los datos: Creative Commons Atribución (CC BY), según el catálogo oficial.
- Fuente intermedia: [paquete de datos geoecu v0.3.0](https://github.com/f-slg/geoecu/releases/tag/datos-v0.3.0), derivado de la capa de CONALI del 17 de julio de 2026. [Metodología de geoecu](https://f-slg.github.io/geoecu/articles/datos.html).

BioTinder extrajo los registros con `dpa_canton = '1201'` de las tablas `cantones` y `parroquias` en `geoecu_dpa_baja.gpkg` (MD5 `66e9f34f0f616ff8ee6e194f50072a31`). Los archivos [babahoyo.geojson](babahoyo.geojson) y [parroquias.geojson](parroquias.geojson) conservan la simplificación de 250 m de esa edición y usan longitud y latitud WGS 84 (EPSG:4326), redondeadas a siete decimales. Las cinco unidades incluyen la cabecera cantonal y las cuatro parroquias rurales.
