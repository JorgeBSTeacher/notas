# Plan de Implementación

## Milestones

### M1: Modelo de datos + Admin básico
**Objetivo**: Tener la base de datos funcional con admin para gestionar datos manualmente.

Tareas:
- [ ] Inicializar proyecto Django (`django-admin startproject`)
- [ ] Crear apps: `grupos`, `curriculo`, `evaluacion`
- [ ] Definir modelos: CursoAcademico, Grupo, Alumno, Asignatura, Trimestre
- [ ] Definir modelos: CompetenciaClave, CompetenciaEspecifica, CriterioEvaluacion
- [ ] Definir modelos: ActividadEvaluable, Pregunta, Calificacion
- [ ] Configurar admin para todos los modelos
- [ ] Instalar y configurar django-admin-interface
- [ ] Migraciones y migrar
- [ ] Verificar administración manual

### M2: Elementos curriculares LOMLOE
**Objetivo**: Poder importar y gestionar el currículo LOMLOE.

Tareas:
- [ ] Crear comando de gestión para importar currículo desde JSON/CSV
- [ ] Crear vista en admin para subir archivo de importación
- [ ] Incluir archivo JSON con currículo por defecto (materias comunes)
- [ ] CRUD completo de elementos curriculares con edición de pesos
- [ ] Validaciones de códigos duplicados y consistencia jerárquica

### M3: Actividades y calificaciones
**Objetivo**: Poder crear actividades y registrar calificaciones.

Tareas:
- [ ] CRUD de actividades evaluables (modo global y por pregunta)
- [ ] CRUD de preguntas (modo por pregunta)
- [ ] Registro de calificaciones numéricas (0-10)
- [ ] Registro de calificaciones con rúbrica (4-5 niveles)
- [ ] Conversión automática rúbrica ↔ numérica
- [ ] Validaciones: nota no nula cuando hay actividad, rango 0-10

### M4: Vistas de evaluación por trimestre y global
**Objetivo**: Visualizar notas acumuladas con cálculos automáticos.

Tareas:
- [ ] Implementar cálculo de nota acumulada por criterio (promedio simple)
- [ ] Implementar cálculo de nota de CE (media ponderada)
- [ ] Implementar cálculo de nota de CC (media ponderada)
- [ ] Vista de tabla Alumnos × Criterios por trimestre
- [ ] Vista global (acumula los tres trimestres)
- [ ] Selector de trimestre funcional
- [ ] Vistas personalizadas en admin para la tabla de notas

### M5: Autenticación multi-profesor
**Objetivo**: Soporte para múltiples profesores con aislamiento de datos.

Tareas:
- [ ] Activar y configurar autenticación Django
- [ ] Login/logout y protección de vistas
- [ ] Asociar grupos, asignaturas y datos al profesor
- [ ] Aislamiento: cada profesor solo ve sus datos
- [ ] Landing page con selector de curso académico y lista de grupos
- [ ] Pruebas de aislamiento entre cuentas

## Priorización

```
M1 ████████████████░░░░  (semana 1)
M2 ██████████░░░░░░░░░░  (semana 2)
M3 ██████████████████░░  (semanas 2-3)
M4 ██████████████░░░░░░  (semanas 3-4)
M5 ████████░░░░░░░░░░░░  (semana 4+)
```
