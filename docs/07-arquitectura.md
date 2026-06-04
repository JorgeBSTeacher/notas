# Arquitectura

## Stack tecnológico

| Componente | Tecnología | Motivo |
|------------|-----------|--------|
| Backend | Django 5.x | ORM potente, admin incluido, autenticación lista |
| Base de datos | SQLite (desarrollo) / PostgreSQL (producción futura) | Cero configuración inicial, migración sencilla |
| Admin UI | django-admin-interface | Theme moderno y limpio sobre el admin de Django |
| Frontend | Django Admin + templates (inicial) / DRF + SPA (futuro) | Mínimo esfuerzo inicial, escalable |

## Por qué Django

1. **ORM maduro**: modela jerarquías complejas (CC → CE → Criterio) con ForeignKey y M2M de forma natural.
2. **Admin automático**: con ~2 líneas por modelo tienes CRUD completo. Ideal para fase personal.
3. **Autenticación integrada**: sistema de usuarios, grupos y permisos listo para M5.
4. **Migraciones**: gestiona cambios en el esquema de BD de forma segura.
5. **Ecosistema**: Django REST Framework si se necesita API en el futuro.
6. **Comunidad y documentación**: amplia, en español.

## Alternativas descartadas

| Opción | Motivo de descarte |
|--------|-------------------|
| FastAPI + React | Más trabajo inicial (frontend desde cero). Mejor cuando se necesite SPA. |
| Next.js | Un solo lenguaje, pero más complejidad en el modelo de datos relacional. |
| Flask | Demasiado minimalista, requeriría añadir muchas extensiones. |

## Estructura del proyecto Django

```
notas/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── config/                    # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── grupos/                # App: Grupos, Alumnos
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── ...
│   ├── curriculo/             # App: CC, CE, Criterios, importación LOMLOE
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── ...
│   ├── evaluacion/            # App: Actividades, Calificaciones
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── ...
│   └── usuarios/              # App: extensión de User (si necesaria)
│       └── ...
├── media/                     # Archivos subidos (importaciones, etc.)
├── static/                    # Archivos estáticos
└── templates/                 # Templates personalizados
    └── admin/
```

## Principios arquitectónicos

- **Lógica de negocio en modelos/services**, no en vistas.
- **Cálculos de acumulación** en métodos del modelo o servicios reutilizables.
- **Admin personalizado** con vistas propias donde la UX lo requiera (tabla de notas).
- **Migraciones** para todos los cambios de esquema.
