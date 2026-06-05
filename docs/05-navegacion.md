# Navegación

## Estructura general

```
Home → Lista de Grupos y Asignaturas
  │
  └── Asignatura "Matemáticas" (workspace)
       │
       ├── [Selector de trimestre: 1º | 2º | 3º | Global]
       │   [+ Actividad] [+ Unidad]
       │
       ├── Pestaña "Panel" (por defecto)
       │   └── Tabla: Alumnos × Actividades
       │       ├── Actividades agrupadas por Unidad Didáctica / Tema
       │       ├── Cada celda: nota media de todos los criterios de esa actividad
       │       ├── Botón "notas" → entrada rápida de calificaciones
       │       └── Columnas agrupadas visualmente por unidad
       │
       ├── Pestaña "Criterios"
       │   └── Tabla: Alumnos × Criterios de Evaluación
       │       └── Nota acumulada: promedio de todas las calificaciones del criterio
       │
       ├── Pestaña "CE"
       │   └── Tabla: Alumnos × Competencias Específicas
       │       └── Nota: media ponderada de los criterios hijos
       │
       └── Pestaña "CC"
           └── Tabla: Alumnos × Competencias Clave
               └── Nota: media ponderada de las CE hijas
```

## Mockup textual del Home

```
+----------------------------------------------+
|  📚 Notas                        Inicio Admin |
+----------------------------------------------+
|                                                |
|  Mis Grupos                                    |
|                                                |
|  +------------------------------------------+ |
|  |  1º ESO A · 2025-2026         28 alumnos  | |
|  |  [Matemáticas] [Lengua] [Inglés]          | |
|  +------------------------------------------+ |
|  +------------------------------------------+ |
|  |  2º ESO B · 2025-2026         25 alumnos  | |
|  |  [Matemáticas] [Lengua]                   | |
|  +------------------------------------------+ |
+----------------------------------------------+
```

## Mockup textual del workspace (Panel)

```
+----------------------------------------------+
|  Matemáticas          1º ESO A · 2025-2026   |
+----------------------------------------------+
|  Trimestre: [1º ▼]  [+ Actividad] [+ Unidad] |
+----------------------------------------------+
|  [Panel | Criterios | CE | CC]                |
+----------------------------------------------+
|                                                |
|  ─── UD1: Números naturales ───                |
| Alumno          | Examen T3 | Libreta | Pres. |
| ----------------+-----------+---------+-------|
| García López A. |   7.50    |  8.00   | 6.50  |
| Pérez Ruiz M.   |   5.00    |  6.00   | 7.00  |
|                 |           |         |       |
|  ─── UD2: Geometría ────────                |
| Alumno          | Examen T4 | Trabajo |       |
| ----------------+-----------+---------+-------|
| García López A. |   6.00    |  7.50   |       |
| Pérez Ruiz M.   |   4.50    |  5.00   |       |
+----------------------------------------------+
```

## Mockup textual del workspace (Criterios)

```
+----------------------------------------------+
|  [Panel | Criterios | CE | CC]                |
+----------------------------------------------+
| Alumno          | CRIT1.1.1 | CRIT1.1.2 | CE1 |
| ----------------+-----------+-----------+-----|
| García López A. |   7.50    |   6.00    |6.75 |
| Pérez Ruiz M.   |   5.00    |   6.00    |5.50 |
+----------------------------------------------+
```
