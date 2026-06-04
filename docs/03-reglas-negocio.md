# Reglas de Negocio

## 1. Acumulación de notas

### Por Criterio de Evaluación
La nota de un criterio es el **promedio simple** de todas las calificaciones asociadas a ese criterio para un mismo alumno y trimestre.

```
nota_criterio = SUM(nota_final de cada calificación del criterio) / COUNT(calificaciones del criterio)
```

### Por Competencia Específica
La nota de una CE es la **media ponderada** de las notas de sus criterios hijos.

```
nota_CE = SUM(nota_criterio × peso_criterio) / SUM(peso_criterio)
```

### Por Competencia Clave
La nota de una CC es la **media ponderada** de las notas de sus CE hijas.

```
nota_CC = SUM(nota_CE × peso_CE) / SUM(peso_CE)
```

## 2. Pesos

- Cada CriterioEvaluacion, CompetenciaEspecifica y CompetenciaClave tiene un campo `peso`.
- Los pesos por defecto vienen de la importación LOMLOE.
- Los pesos son **editables por asignatura** para reflejar cambios a nivel de centro.
- Peso por defecto = 1.0 (todos ponderan igual hasta que se editen).

## 3. Conversión rúbrica ↔ numérica

### Modo automático (regla de tres)
```
valor_numerico = (nivel_rubrica - 1) × (10 / (max_niveles - 1))
```
Ejemplo: rúbrica de 4 niveles → nivel 1 = 0.0, nivel 2 = 3.33, nivel 3 = 6.67, nivel 4 = 10.0

### Modo manual
El profesor puede asignar manualmente el valor numérico a cada nivel de la rúbrica (por criterio o por actividad).

### Almacenamiento
- `tipo_evaluacion`: "numerica" | "rubrica"
- Si es numérica: `valor_numerico` guarda la nota (0-10), `nivel_rubrica` = null
- Si es rúbrica: `nivel_rubrica` guarda el nivel (1-N), `valor_numerico` guarda el equivalente numérico calculado
- `nota_final` siempre contiene el valor numérico definitivo

## 4. Vista Global

- La vista global agrega **todas** las calificaciones de los tres trimestres para cada alumno.
- El cálculo sigue las mismas reglas de acumulación (promedio simple por criterio, media ponderada hacia arriba).

## 5. Restricciones

- Toda calificación debe estar asociada a un CriterioEvaluacion.
- No se puede eliminar un criterio que tenga calificaciones asociadas.
- Al cambiar el modo de una actividad (global ↔ por_pregunta) con calificaciones existentes, se debe advertir al usuario.
