# Susceptibilidad a inundaciones en Babahoyo

El visor local muestra el recorte cartográfico del CONAGE 2024 publicado por la Secretaría Nacional de Gestión de Riesgos. La paleta corresponde a las clases oficiales baja, media y alta. Los espacios transparentes quedan sin clasificación visible. Los límites del cantón o de la parroquia seleccionada recortan la visualización.

- [Capa fuente y leyenda](https://sgrportal.gestionderiesgos.gob.ec/server/rest/services/Susceptibilidad_de_Inundaciones/MapServer/0)
- [Consulta de exportación](<https://sgrportal.gestionderiesgos.gob.ec/server/rest/services/Susceptibilidad_de_Inundaciones/MapServer/export?bbox=-8873276.61,-248305.16,-8819843.26,-178134.34&bboxSR=3857&imageSR=3857&size=1024,1344&format=png32&transparent=true&layers=show:0&f=json&dpi=24>), consultada el 15 de noviembre de 2026. PNG32, 1024 × 1344 píxeles, EPSG:3857. La extensión que devuelve el servicio se conserva en el componente de la capa.
- [Catálogo nacional de referencia del MAG](https://www.datosabiertos.gob.ec/dataset/mapa-susceptibilidad-a-inundaciones-escala-1-25-000), edición 2024, escala 1:25.000. La capa del visor representa susceptibilidad física, sin fecha de evento, profundidad ni probabilidad.

Para una capa independiente de eventos observados, [AutoFloods](https://github.com/PratyushTripathy/AutoFloods) ofrece un flujo reproducible con Sentinel-1. Un piloto en Babahoyo puede seleccionar una escena de un evento documentado, compararla con una referencia seca, separar agua permanente y arrozales irrigados, y contrastar la máscara resultante con observaciones locales antes de mostrarla por fecha. Ese procesamiento y su validación quedan pendientes.
