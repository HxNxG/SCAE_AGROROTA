# Instrucciones para agentes de AgroRota Ecuador

Sigue las [reglas de datos](../REGLAS.md) y la [guía de trabajo](docs/GUIA_AGENTES.md).

- El piloto cubre Babahoyo, Los Ríos. Compara arroz → arroz como referencia, arroz → soya como alternativa prioritaria y arroz → maíz amarillo duro como segunda alternativa.
- Mantén la lógica agronómica, las consultas y los cálculos en el backend. El frontend presenta resultados, procedencia, limitaciones y motivos de cada alternativa.
- Representa explícitamente valores faltantes y calidad. Una estimación regional conserva su resolución aunque se muestre sobre una parcela.
- Sustenta restricciones y recomendaciones con referencias versionadas. Separa la aptitud agronómica de la prioridad indicada por el agricultor. Aplica las restricciones antes de ordenar por preferencias.
- Cualquier predicción debe indicar su horizonte, validación y límites. Registra fecha, zona y consentimiento para las observaciones y exige revisión antes de usarlas en recomendaciones o entrenamiento.
