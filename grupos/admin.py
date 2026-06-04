from django.contrib import admin
from .models import CursoAcademico, Grupo, Alumno, Asignatura


@admin.register(CursoAcademico)
class CursoAcademicoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "curso_academico")
    list_filter = ("curso_academico",)
    search_fields = ("nombre",)


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("apellidos", "nombre", "grupo")
    list_filter = ("grupo__curso_academico", "grupo")
    search_fields = ("nombre", "apellidos")


@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "grupo")
    list_filter = ("grupo__curso_academico", "grupo")
    search_fields = ("nombre",)
