# Casos de Uso

## CU01: Crear grupo y asignaturas

**Actor**: Profesor
**Flujo**:
1. El profesor accede a la vista de grupos.
2. Hace clic en "Nuevo grupo".
3. Introduce nombre del grupo (ej: "1º ESO A") y selecciona curso académico.
4. Desde la vista del grupo, añade asignaturas (ej: "Matemáticas", "Lengua").
5. Añade alumnos al grupo (manual o importación).

## CU02: Importar elementos curriculares LOMLOE

**Actor**: Profesor
**Flujo**:
1. Desde la configuración de una asignatura, selecciona "Importar LOMLOE".
2. Sube un archivo (CSV/JSON) con la estructura curricular.
3. El sistema importa y crea la jerarquía Competencias Clave → Específicas → Criterios.
4. El profesor puede revisar y ajustar los pesos importados.

## CU03: Editar pesos curriculares

**Actor**: Profesor
**Flujo**:
1. Desde la asignatura, accede a "Elementos curriculares".
2. Visualiza la jerarquía CC → CE → Criterios con sus pesos.
3. Edita el peso de cualquier elemento.
4. Guarda cambios.

## CU04: Crear actividad evaluable (modo global)

**Actor**: Profesor
**Flujo**:
1. Desde la asignatura y trimestre, selecciona "Nueva actividad".
2. Introduce nombre, tipo (examen, libreta, exposición...) y fecha.
3. Selecciona modo "global".
4. Asigna uno o varios criterios de evaluación a la actividad.
5. Guarda la actividad.

## CU05: Crear actividad evaluable (modo por pregunta)

**Actor**: Profesor
**Flujo**:
1. Desde la asignatura y trimestre, selecciona "Nueva actividad".
2. Introduce nombre, tipo y fecha.
3. Selecciona modo "por pregunta".
4. Añade preguntas: para cada una, introduce enunciado y selecciona un criterio.
5. Guarda la actividad.

## CU06: Poner notas numéricas

**Actor**: Profesor
**Flujo**:
1. Selecciona actividad evaluable.
2. Visualiza tabla: Alumnos × Criterios (o Alumnos × Preguntas).
3. Introduce nota numérica (0-10) en cada celda.
4. Guarda.
5. El sistema recalcula automáticamente las acumulaciones.

## CU07: Poner notas con rúbrica

**Actor**: Profesor
**Flujo**:
1. Selecciona actividad evaluable.
2. Visualiza tabla: Alumnos × Criterios.
3. Para cada celda, selecciona nivel de rúbrica (1-4 o 1-5).
4. El sistema muestra el equivalente numérico (automático o manual).
5. Guarda.

## CU08: Ver notas por trimestre

**Actor**: Profesor
**Flujo**:
1. Navega a Grupo → Asignatura.
2. Selecciona trimestre (1º, 2º, 3º).
3. Visualiza tabla: Alumnos × Criterios con notas acumuladas.
4. Puede expandir para ver desglose por actividad.
5. Ve también las notas calculadas de CE y CC.

## CU09: Ver nota global

**Actor**: Profesor
**Flujo**:
1. Navega a Grupo → Asignatura.
2. Selecciona "Global".
3. Visualiza la misma vista que por trimestre pero con datos acumulados del curso completo.

## CU10: Cambiar entre trimestres

**Actor**: Profesor
**Flujo**:
1. Estando en cualquier vista de asignatura, cambia el selector de trimestre.
2. La vista se actualiza mostrando los datos del trimestre seleccionado.
3. Al cambiar a "Global", se muestran los datos acumulados del curso.
