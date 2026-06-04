# ADR 002: Modelo de evaluación

**Fecha**: 2026-06-04
**Estado**: Aceptado

## Contexto
Las calificaciones deben soportar dos tipos de evaluación (numérica y rúbrica) y estar siempre ligadas a un criterio de evaluación. Cada actividad evaluable puede tener modo global (criterios a nivel actividad) o por pregunta (cada pregunta con su criterio).

## Decisión

### Modelo de calificación
Una sola entidad `Calificacion` con campos:
- `tipo_evaluacion`: "numerica" | "rubrica"
- `valor_numerico`: Decimal (0-10), usado si tipo = numérica
- `nivel_rubrica`: Integer (1-N), usado si tipo = rúbrica
- `nota_final`: Decimal (0-10), siempre contiene el valor numérico definitivo

### Modos de actividad
Un campo `modo` en `ActividadEvaluable`:
- `global`: relación M2M con CriterioEvaluacion
- `por_pregunta`: entidad `Pregunta` con FK a CriterioEvaluacion

## Opciones consideradas
- **Entidades separadas** (`CalificacionNumerica`, `CalificacionRubrica`): más puras pero complejidad innecesaria.
- **Una sola entidad con tipo**: más simple, suficiente para el alcance actual.

## Consecuencias
- **Positivas**: modelo simple, cálculos directos, validaciones claras.
- **Negativas**: campos nulos según el tipo (manejado con validación en el modelo).
