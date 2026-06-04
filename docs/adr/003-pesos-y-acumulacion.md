# ADR 003: Pesos y acumulación de notas

**Fecha**: 2026-06-04
**Estado**: Aceptado

## Contexto
Las notas se acumulan desde criterios hacia competencias específicas y competencias clave. Se necesita un sistema de ponderación editable y un método de acumulación claro.

## Decisión

### Acumulación
- **Criterio**: promedio simple de todas las calificaciones asociadas.
- **CE**: media ponderada de las notas de sus criterios hijos.
- **CC**: media ponderada de las notas de sus CE hijas.

### Pesos
- Cada elemento curricular tiene un campo `peso` (Decimal).
- Peso por defecto: 1.0.
- Los pesos se heredan de la importación LOMLOE pero son **editables por asignatura**.
- La ponderación usa la fórmula: `SUM(nota_hijo × peso_hijo) / SUM(peso_hijo)`.

## Opciones consideradas
- **Suma simple**: no permite diferenciar importancia relativa.
- **Promedio simple**: ignora la ponderación.
- **Media ponderada**: flexible, permite adaptarse a cambios curriculares.

## Consecuencias
- **Positivas**: los pesos reflejan la importancia real de cada elemento, adaptables a nivel de centro.
- **Negativas**: el profesor debe configurar los pesos (aunque vienen con valores por defecto).
