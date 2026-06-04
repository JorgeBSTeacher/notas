# ADR 001: Elección del stack Django

**Fecha**: 2026-06-04
**Estado**: Aceptado

## Contexto
Se necesita desarrollar una aplicación web de calificaciones con modelo de datos relacional complejo (jerarquía curricular de 3 niveles), uso personal inicial con posible escalado multi-profesor, y requisito de interfaz limpia e intuitiva.

## Decisión
Usar **Django + SQLite + django-admin-interface**.

## Opciones consideradas
- **Django**: ORM potente, admin incluido, autenticación integrada.
- **FastAPI + React**: más moderno pero requiere frontend desde cero.
- **Next.js**: un solo lenguaje, pero ORM menos maduro para modelos jerárquicos complejos.

## Consecuencias
- **Positivas**: desarrollo rápido, admin funcional sin escribir frontend, escalado sencillo a API con DRF.
- **Negativas**: si se requiere SPA en el futuro, habrá que añadir DRF y construir el frontend.
- **Neutrales**: SQLite es suficiente para uso personal; migrar a PostgreSQL es directo si se necesita.
