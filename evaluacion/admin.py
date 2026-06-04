from django.contrib import admin
from .models import Trimestre, ActividadEvaluable, Pregunta, Calificacion


class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1


@admin.register(Trimestre)
class TrimestreAdmin(admin.ModelAdmin):
    list_display = ("get_nombre_display", "asignatura")
    list_filter = ("asignatura__grupo__curso_academico",)


@admin.register(ActividadEvaluable)
class ActividadEvaluableAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "modo", "fecha", "trimestre")
    list_filter = ("tipo", "modo", "trimestre__asignatura__grupo__curso_academico")
    filter_horizontal = ("criterios",)
    inlines = [PreguntaInline]


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ("enunciado", "orden", "criterio", "actividad")
    list_filter = ("actividad__trimestre__asignatura",)


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = (
        "alumno",
        "actividad",
        "criterio",
        "tipo_evaluacion",
        "nota_final",
        "trimestre",
    )
    list_filter = (
        "trimestre__asignatura",
        "tipo_evaluacion",
        "actividad",
    )
    search_fields = ("alumno__apellidos",)
