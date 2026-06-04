# Navegación

## Estructura general

```
Home
└── Panel del profesor
    │
    ├── [Selector de curso académico]
    │
    └── Lista de Grupos
        │
        └── Grupo "1º ESO A"
            ├── Info del grupo (nombre, alumnos, asignaturas)
            │
            └── Lista de Asignaturas
                │
                └── Asignatura "Matemáticas"
                    │
                    ├── [Selector de trimestre: 1º | 2º | 3º | Global]
                    │
                    ├── Pestaña "Evaluación" (por defecto)
                    │   └── Tabla: Alumnos × Criterios
                    │       ├── Celdas: nota acumulada del criterio
                    │       ├── Columnas extra: nota CE, nota CC
                    │       └── Filas: alumnos
                    │
                    ├── Pestaña "Actividades"
                    │   └── Lista de actividades evaluables del trimestre
                    │       └── Al hacer clic: detalle de la actividad
                    │           └── Tabla: Alumnos × Criterios/Preguntas
                    │               └── Inputs para introducir notas
                    │
                    └── Pestaña "Currículo"
                        └── Árbol jerárquico: CC → CE → Criterios
                            └── Pesos editables
```

## Mockup textual del Home

```
+----------------------------------------------+
|  📚 Notas  |  Curso 2025-2026  ▼  |  Perfil  |
+----------------------------------------------+
|                                                |
|  Mis Grupos                                    |
|                                                |
|  +------------------------------------------+ |
|  |  1º ESO A                          3 asig | |
|  |  28 alumnos                        →      | |
|  +------------------------------------------+ |
|  +------------------------------------------+ |
|  |  2º ESO B                          3 asig | |
|  |  25 alumnos                        →      | |
|  +------------------------------------------+ |
|  +------------------------------------------+ |
|  |  1º Bach C                         2 asig | |
|  |  20 alumnos                        →      | |
|  +------------------------------------------+ |
|                                                |
|  [+ Nuevo grupo]                               |
+----------------------------------------------+
```

## Mockup textual de la vista de evaluación

```
+----------------------------------------------+
|  1º ESO A > Matemáticas                       |
|  [Trimestre: 1º ▼]  [Evaluación | Actividades | Currículo]
+----------------------------------------------+
|                                                |
| Alumno          | Criterio 1.1 | Criterio 1.2 | CE1 | CC1 |
|                 | peso: 1.0    | peso: 2.0    |     |     |
| ----------------+--------------+--------------+-----+-----|
| García López A. |     7.5      |     6.0      | 6.5 | 6.5 |
| Pérez Ruiz M.   |     8.0      |     5.5      | 6.3 | 6.3 |
| López Soler J.  |     4.0      |     3.0      | 3.3 | 3.3 |
+----------------------------------------------+
```
