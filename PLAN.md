# PLAN.md · Visor agrícola de Babahoyo

Estado — Rama `agrorota/visor-mapa` desde `agrorota/integracion-mapa` (`237d732`). M1–M4 implementadas. M5 verificada en escritorio para el cambio de mes. Queda pendiente la prueba móvil de la capa integrada. Este plan reemplaza la propuesta de delimitación de parcelas como primer producto.

## Primer producto

Abrir en Babahoyo, explorar el mapa, elegir un mes, ver la precipitación por celda y seleccionar un punto para consultar el historial cantonal. El mapa ocupa la pantalla. En escritorio usa paneles flotantes y en móvil la ficha se abre desde abajo. La leyenda indica mm y la fecha activa. Ver [referencia de interacción](https://www.accuweather.com/es/ec/quito/129846/satellite/129846).

Reutilizar el frontend JavaScript/SVG, el proxy Node, la validación FastAPI y el historial cantonal existente. La primera versión local usa cartografía disponible y una capa de precipitación. La base satelital se incorporará cuando se elija una fuente con atribución y condiciones de uso verificadas. Relieve es la siguiente capa candidata. Dibujar parcelas, calcular áreas, responder el cuestionario y simular rotaciones quedan fuera de esta rama.

## Tareas y aceptación

Rutas de código relativas a `proyecto-agricultura-ia/`.

| ID | Esfuerzo | Tarea y archivos | Aceptación |
| --- | --- | --- | --- |
| M1 | medium | Extraer las celdas IMERG que intersectan Babahoyo, a partir de los dos CSV Costa por celda. Script en `scripts/`, servicio de capa en `backend/app/services/` y API en `backend/app/api/v1/`. | Verificar cobertura enero 2010–septiembre 2025, meses y celdas sin duplicados, mm, fuente y escala. Validar un mes contra el CSV y medir el tamaño del recorte. Representar celdas faltantes sin rellenarlas. |
| M2 | medium | Hacer el mapa la entrada principal en `frontend/src/main.js`, `styles.css` y `components/map/`. Añadir zoom, desplazamiento, restablecer vista y selección puntual. | Escritorio y móvil permiten explorar y seleccionar. Controles accesibles y ficha cerrable. Mantener validación del punto y entrada por coordenadas. |
| M3 | medium | Conectar capa, leyenda, control mensual y ficha en `frontend/src/components/map/` y `frontend/src/services/pilotApi.js`. | Cambiar mes actualiza capa, leyenda y fecha. Usar la geometría de celdas conservando su resolución. La ficha distingue el historial cantonal del valor de una celda. Mes sin datos y API caída tienen estados visibles. |
| M4 | low | Revisar procedencia, permisos y atribución de límite y posible mapa base. Registrar en `docs/MAPA_PARCELAS.md`. | Documentar fuente, fecha, condiciones y decisión de publicación. El límite DPA 2019 sigue siendo provisional hasta verificar la redistribución. |
| M5 | medium | Verificar la demo y actualizar `README.md` y `docs/MAPA_PARCELAS.md` con pruebas y fallos. | Probar zoom, toque, punto interior/exterior, primer y último mes y caída de API. Verificar escritorio y móvil estrecho sin desbordamiento y repetir pruebas geográficas. |

M1, M2 y M4 pueden avanzar por separado. M3 depende de los contratos de M1 y M2. M5 prueba el conjunto. Abrir hilos por tarea con este ID y sus rutas, mantener `AGENTS.md` como guía estable y registrar decisiones en la documentación del visor.

## Riesgos

- El gráfico cantonal y la capa de celdas tienen distinta escala. No interpolar la lluvia a resolución de parcela ni mostrar fechas posteriores al último dato como observadas.
- El prototipo visual ilustra una base satelital y una capa de relieve. La demo local puede funcionar con la geometría actual y lluvia. Confirmar los derechos del límite y de la base antes de publicar.

## Siguiente iteración del visor

| ID | Esfuerzo | Tarea | Aceptación |
| --- | --- | --- | --- |
| M6 | medium | Fondo cartográfico incorporado con atribución, control de visibilidad y opacidad. | Prueba de escritorio aprobada con teselas interceptadas. Se verificaron zoom, reinicio, cambio de mes y capa de lluvia visible al fallar el fondo. |
| M7 | medium | Piloto SMAP del 1 de enero de 2025 con humedad superficial y radicular. | API y visor verificados en escritorio. Cada capa tiene 28 celdas, ocho intervalos UTC y leyenda propia. Consultar la [ficha de humedad](proyecto-agricultura-ia/docs/CAPA_HUMEDAD.md). |
| M8 | medium | Reproducción mensual de lluvia y lectura de la celda seleccionada. | Verificado en escritorio con API real. Reproducir, pausar y recorrer meses. La ficha muestra el valor IMERG del mes activo y permite desplegar el promedio cantonal. |
| M9 | medium | Definir [temperatura superficial](proyecto-agricultura-ia/docs/CAPA_TEMPERATURA.md) y [humedad del suelo](proyecto-agricultura-ia/docs/CAPA_HUMEDAD.md). | Diseño y fuentes documentados. Pendiente preparar los recortes y conectar las capas al visor. |
