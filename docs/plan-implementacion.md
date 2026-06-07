# Plan de Implementación

## Milestones

### M1: Modelo de datos + Admin básico ✅
**Objetivo**: Tener la base de datos funcional con admin para gestionar datos manualmente.

Tareas:
- [x] Inicializar proyecto Django (`django-admin startproject`)
- [x] Crear apps: `grupos`, `curriculo`, `evaluacion`
- [x] Definir modelos: CursoAcademico, Grupo, Alumno, Asignatura, Trimestre
- [x] Definir modelos: CompetenciaClave, CompetenciaEspecifica, CriterioEvaluacion
- [x] Definir modelos: ActividadEvaluable, Pregunta, Calificacion
- [x] Configurar admin para todos los modelos
- [x] Instalar y configurar django-admin-interface
- [x] Migraciones y migrar
- [x] Verificar administración manual

### M2: Elementos curriculares LOMLOE ✅
**Objetivo**: Poder importar y gestionar el currículo LOMLOE.

Tareas:
- [x] Crear comando de gestión para importar currículo desde JSON/CSV
- [x] Crear vista en admin para subir archivo de importación
- [x] Incluir archivo JSON con currículo por defecto (materias comunes)
- [x] CRUD completo de elementos curriculares con edición de pesos
- [x] Validaciones de códigos duplicados y consistencia jerárquica

### M3: Actividades y calificaciones ✅
**Objetivo**: Poder crear actividades y registrar calificaciones.

Tareas:
- [x] CRUD de actividades evaluables (modo global y por pregunta)
- [x] CRUD de preguntas (modo por pregunta)
- [x] Registro de calificaciones numéricas (0-10 con 2 decimales)
- [x] Registro de calificaciones con rúbrica (4-5 niveles)
- [x] Conversión automática rúbrica ↔ numérica (regla de tres o personalizada)
- [x] Validaciones: nota no nula cuando hay actividad, rango 0-10
- [x] Modelo RubricaConfig + RubricaNivel para niveles personalizados
- [x] Vista de entrada masiva de notas (tabla Alumnos × Criterios)

### M4: Workspace con vistas de evaluación ✅
**Objetivo**: Panel de trabajo con tabla Alumnos × Actividades y vistas por criterios/CE/CC.

Tareas:
- [x] Modelo UnidadDidactica para agrupar actividades por tema/SA
- [x] FK de ActividadEvaluable → UnidadDidactica
- [x] Página principal (Home) con lista de grupos y asignaturas
- [x] Workspace con selector de trimestre y pestañas
- [x] Pestaña Panel: tabla Alumnos × Actividades agrupadas por unidad
- [x] Pestaña Criterios: tabla Alumnos × Criterios (promedio) + columna Media + fila Media clase
- [x] Pestaña CE: tabla Alumnos × Competencias Específicas (media ponderada) + Media + Media clase
- [x] Pestaña CC: tabla Alumnos × Competencias Clave (media ponderada) + Media + Media clase
- [x] Cálculo de nota global de unidad (promedio simple de actividades)
- [x] Pestaña Panorámica: tabla Alumnos × Actividades agrupadas por UD con celdas coloreadas
- [x] Columna de media por UD en Panorámica (promedio del alumno en cada unidad)
- [x] Selector de trimestre con opción "🌍 Global" (acumula todos los trimestres)
- [x] Página de entrada rápida de notas con auto‑save (AJAX + debounce + indicador de estado)
- [x] Botón ✕ para eliminar nota de un alumno (con confirmación)
- [x] Parseo locale‑seguro de números con coma decimal (valueAsNumber)

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
