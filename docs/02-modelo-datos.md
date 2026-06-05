# Modelo de Datos

## Entidades y Relaciones

```
CursoAcademico
├── nombre: str (ej: "2025-2026")
│
└── Grupo (Clase)
    ├── nombre: str (ej: "1º ESO A")
    ├── curso_academico: FK → CursoAcademico
    │
    ├── Alumno
    │   ├── nombre: str
    │   ├── apellidos: str
    │   └── grupo: FK → Grupo
    │
    └── Asignatura
        ├── nombre: str (ej: "Matemáticas")
        ├── grupo: FK → Grupo
        │
        ├── CompetenciaClave
        │   ├── codigo: str (ej: "CC1")
        │   ├── descripcion: str
        │   ├── peso: Decimal (editable por asignatura)
        │   └── asignatura: FK → Asignatura
        │   │
        │   └── CompetenciaEspecifica
        │       ├── codigo: str (ej: "CE1.1")
        │       ├── descripcion: str
        │       ├── peso: Decimal (editable por asignatura)
        │       └── competencia_clave: FK → CompetenciaClave
        │       │
        │       └── CriterioEvaluacion
        │           ├── codigo: str (ej: "CRIT1.1.1")
        │           ├── descripcion: str
        │           ├── peso: Decimal (editable por asignatura)
        │           └── competencia_especifica: FK → CompetenciaEspecifica
        │
        └── Trimestre (1º, 2º, 3º, Global)
            ├── nombre: str (1º, 2º, 3º, Global)
            ├── asignatura: FK → Asignatura
            │
            ├── UnidadDidactica (Tema / Situación de Aprendizaje)
            │   ├── nombre: str (ej: "UD1: Números naturales")
            │   ├── trimestre: FK → Trimestre
            │   └── orden: int
            │
            └── ActividadEvaluable (opcionalmente agrupada en UnidadDidactica)
                ├── nombre: str (ej: "Examen Tema 3")
                ├── tipo: str (examen, libreta, exposicion, tarea, otro)
                ├── modo: enum (global, por_pregunta)
                ├── fecha: date
                ├── trimestre: FK → Trimestre
                ├── unidad_didactica: FK → UnidadDidactica (nullable)
                │
                ├── [Modo global] CriteriosAsignados (M2M con CriterioEvaluacion)
                └── [Modo por pregunta] Pregunta
                    ├── enunciado: str
                    ├── orden: int
                    ├── criterio: FK → CriterioEvaluacion
                    └── puntuacion_maxima: Decimal
                    │
                    └── Calificacion
                        ├── alumno: FK → Alumno
                        ├── actividad: FK → ActividadEvaluable
                        ├── criterio: FK → CriterioEvaluacion
                        ├── trimestre: FK → Trimestre
                        ├── tipo_evaluacion: enum (numerica, rubrica)
                        ├── valor_numerico: Decimal (0-10) | null
                        ├── nivel_rubrica: int (1-5) | null
                        └── nota_final: Decimal (0-10) [calculado]
```

## Diagrama de relaciones (textual)

```
CursoAcademico 1──n Grupo
Grupo 1──n Alumno
Grupo 1──n Asignatura
Asignatura 1──n CompetenciaClave
CompetenciaClave 1──n CompetenciaEspecifica
CompetenciaEspecifica 1──n CriterioEvaluacion
Asignatura 1──n Trimestre
Trimestre 1──n UnidadDidactica
Trimestre 1──n ActividadEvaluable
UnidadDidactica 1──n ActividadEvaluable (nullable)
ActividadEvaluable n──m CriterioEvaluacion (modo global)
ActividadEvaluable 1──n Pregunta
Pregunta n──1 CriterioEvaluacion
ActividadEvaluable 1──n Calificacion
Pregunta 1──n Calificacion
Alumno 1──n Calificacion
CriterioEvaluacion 1──n Calificacion
Trimestre 1──n Calificacion
```

## Notas

- Los pesos de CC, CE y Criterio son editables por asignatura para adaptarse a cambios a nivel de centro.
- `valor_numerico` y `nivel_rubrica` se excluyen mutuamente según `tipo_evaluacion`.
- `nota_final` es el valor numérico final (directo si es numérica, convertido si es rúbrica).
- En modo global, la relación es M2M entre ActividadEvaluable y CriterioEvaluacion.
- En modo por pregunta, cada pregunta tiene un solo criterio.
