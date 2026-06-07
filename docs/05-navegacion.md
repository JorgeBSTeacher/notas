# Navegación

## Estructura general

```
Home → Lista de Grupos y Asignaturas
  │
  ├── Admin → django-admin-interface
  │
  └── Asignatura "Matemáticas" (workspace)
       │
       ├── [Selector: 🌍 Global | 1º | 2º | 3º]
       │   [+ Actividad] [+ Unidad]
       │
       ├── Pestaña "📊 Panorámica" (por defecto)
       │   └── Tabla: Alumnos × Actividades agrupadas por UD
       │       ├── Filas: alumnos ordenados por apellido
       │       ├── Columnas: actividades con cabecera de grupo (UD)
       │       ├── Cada celda: nota coloreada (verde ≥7, ámbar ≥4, rojo <4)
       │       ├── Última columna de cada UD: media del alumno en esa UD
       │       ├── Última columna global: media total del alumno
       │       └── Última fila: media de la clase por actividad
       │
       ├── Pestaña "📋 Panel"
       │   └── Lista de actividades agrupadas por UD
       │       ├── Cada actividad: nombre, tipo, fecha, peso, media de clase
       │       └── Botón "Entrar notas" → página de entrada rápida
       │
       ├── Pestaña "📏 Criterios"
       │   └── Tabla: Alumnos × Criterios de Evaluación
       │       ├── Nota acumulada: promedio de todas las calificaciones del criterio
       │       ├── Última columna: media del alumno en todos los criterios
       │       └── Última fila: media de la clase por criterio
       │
       ├── Pestaña "🎯 CE"
       │   └── Tabla: Alumnos × Competencias Específicas
       │       ├── Nota: media ponderada de los criterios hijos (según peso)
       │       ├── Última columna: media del alumno en todas las CE
       │       └── Última fila: media de la clase por CE
       │
       └── Pestaña "🏆 CC"
           └── Tabla: Alumnos × Competencias Clave
               ├── Nota: media ponderada de las CE hijas (según peso)
               ├── Última columna: media del alumno en todas las CC
               └── Última fila: media de la clase por CC
```

## Página de entrada de notas (`/actividad/<id>/notas/`)

```
+----------------------------------------------+
|  ← Volver | Examen T3 (Examen) | Global      |
|  28 alumnos · 3 criterios                    |
+----------------------------------------------+
| Alumno          | Nota (0-10) | Se aplica a: |
|                 |             | CR1, CR2, CR3 |
| ----------------+-------------+--------------|
| García López A. |  [8.00] ●   |    8.00      |
| Pérez Ruiz M.   |  [5.00] ●   |    5.00      |
+----------------------------------------------+
```
- Entrada con auto‑save (AJAX + debounce 400ms)
- Indicador de estado: ● amarillo (guardando), ● verde (guardado), ● rojo (error)
- Modo "por pregunta": tabla Alumnos × Preguntas, cada pregunta vinculada a un criterio

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

## Mockup textual del workspace (Panorámica)

```
+----------------------------------------------+
|  Matemáticas          1º ESO A · 2025-2026   |
+----------------------------------------------+
|  Trimestre: [🌍 Global ▼] [+ Act.] [+ UD]   |
+----------------------------------------------+
|  [📊 Panorámica | 📋 Panel | 📏 Criterios | 🎯 CE | 🏆 CC]
+----------------------------------------------+
|         |  ─── UD1: Números ─── | ─── UD2: Geo. ─── |     |
| Alumno  | Ex.T3 | Libr. | Pres. |MedUD| Ex.T4 | Trab |MedUD|Media|
| --------+-------+-------+-------+-----+-------+------+-----+-----|
| García  |  7.50 |  8.00 |  6.50 |7.33 |  6.00 | 7.50 |6.75 |7.08 |
| Pérez   |  5.00 |  6.00 |  7.00 |6.00 |  4.50 | 5.00 |4.75 |5.50 |
| --------+-------+-------+-------+-----+-------+------+-----+-----|
| Media cl|  6.25 |  7.00 |  6.75 |     |  5.25 | 6.25 |     |     |
+----------------------------------------------+
```
