# AgroRota Ecuador

Sistema web de apoyo a la rotación agrícola en Babahoyo, Los Ríos. Combina datos ambientales, referencias agronómicas ecuatorianas y observaciones del agricultor para comparar arroz, soya y maíz amarillo duro después de un ciclo de arroz.

- [Instrucciones para agentes](AGENTS.md)
- [Guía de trabajo y alcance](docs/GUIA_AGENTES.md)
- [Reglas de los datos del repositorio](../REGLAS.md)

Las carpetas de backend y frontend contienen la estructura inicial. Los comandos de ejecución se documentarán al implementar la aplicación.

## Estructura de la aplicación

| Ruta | Responsabilidad |
| --- | --- |
| [backend/app](backend/app/) | API, contratos de datos, configuración, persistencia y evaluación agronómica. |
| [backend/models_ml](backend/models_ml/) | Referencias a modelos. Los pesos voluminosos se gestionan fuera de Git. |
| [frontend/src](frontend/src/) | Mapa, cuestionario, diagnóstico, comparación y retroalimentación. |
| [docs](docs/) | Guía de implementación y verificación del piloto. |
| [docker-compose.yml](docker-compose.yml) | Plantilla para la futura ejecución conjunta. |

El inventario y los insumos se consultan desde el [índice del repositorio](../README.md#datos-y-evidencia).
