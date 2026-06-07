# Mejoras pendientes

Anotadas tras la fase de desarrollo M1-M4, pendientes de priorizar tras las pruebas.

---

## Críticas para producción

- [ ] Edición de actividades desde la UI (actualmente solo desde admin)
- [ ] Edición de alumnos del grupo (actualmente solo desde admin)
- [ ] Botón "recalcular todo" para nota_final al cambiar pesos de criterios/CE/CC
- [ ] Mensajes flash de error/éxito en la UI

## Funcionales

- [ ] Exportar notas a PDF/CSV (boletín de notas)
- [ ] Vista resumen por alumno (todas sus notas de todas las asignaturas)
- [ ] Peso configurable por ActividadEvaluable (actualmente la media es simple)
- [ ] Filtro por tipo de actividad en Panorámica/Panel
- [ ] Estadísticas: media, desviación típica, histograma por actividad/criterio

## Rendimiento

- [ ] Optimizar vistas Criterios/CE/CC con `annotate` y `Subquery` (actualmente O(n²) en template)
- [ ] Panorámica: agregar medias de clase en 1 query en vez de 1 por actividad

## UI/UX

- [ ] Modo oscuro
- [ ] Atajos de teclado en entrada de notas (Tab, Enter)
- [ ] Columnas redimensionables / congeladas en Panorámica
- [ ] Vista móvil usable
