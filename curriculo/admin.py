from django.contrib import admin
from .models import CompetenciaClave, CompetenciaEspecifica, CriterioEvaluacion


class CompetenciaEspecificaInline(admin.TabularInline):
    model = CompetenciaEspecifica
    extra = 1


class CriterioInline(admin.TabularInline):
    model = CriterioEvaluacion
    extra = 1


@admin.register(CompetenciaClave)
class CompetenciaClaveAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descripcion", "peso", "asignatura")
    list_filter = ("asignatura",)
    search_fields = ("codigo", "descripcion")
    inlines = [CompetenciaEspecificaInline]


@admin.register(CompetenciaEspecifica)
class CompetenciaEspecificaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descripcion", "peso", "competencia_clave")
    list_filter = ("competencia_clave__asignatura",)
    search_fields = ("codigo", "descripcion")
    inlines = [CriterioInline]


@admin.register(CriterioEvaluacion)
class CriterioEvaluacionAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descripcion", "peso", "competencia_especifica")
    list_filter = ("competencia_especifica__competencia_clave__asignatura",)
    search_fields = ("codigo", "descripcion")
