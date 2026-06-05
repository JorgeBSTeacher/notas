from django.contrib import admin, messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, reverse
from django import forms
from django.db import transaction
from .models import (
    Trimestre,
    ActividadEvaluable,
    Pregunta,
    Calificacion,
    RubricaConfig,
    RubricaNivel,
)
from grupos.models import Alumno


class RubricaNivelInline(admin.TabularInline):
    model = RubricaNivel
    extra = 0


@admin.register(RubricaConfig)
class RubricaConfigAdmin(admin.ModelAdmin):
    list_display = ("criterio", "max_niveles")
    inlines = [RubricaNivelInline]


class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1


@admin.register(Trimestre)
class TrimestreAdmin(admin.ModelAdmin):
    list_display = ("get_nombre_display", "asignatura")
    list_filter = ("asignatura__grupo__curso_academico",)


class CalificacionForm(forms.Form):
    def __init__(self, *args, alumnos, criterios, tipo_actividad, **kwargs):
        super().__init__(*args, **kwargs)
        for alumno in alumnos:
            for criterio in criterios:
                field_name = f"nota_{alumno.id}_{criterio.id}"
                if tipo_actividad == "rubrica":
                    niveles = [(i, f"Nivel {i}") for i in range(1, 6)]
                    niveles.insert(0, ("", "---"))
                    self.fields[field_name] = forms.ChoiceField(
                        choices=niveles,
                        required=False,
                        label=f"{alumno.apellidos}, {alumno.nombre} - {criterio.codigo}",
                    )
                else:
                    self.fields[field_name] = forms.DecimalField(
                        max_digits=4,
                        decimal_places=2,
                        required=False,
                        min_value=0,
                        max_value=10,
                        label=f"{alumno.apellidos}, {alumno.nombre} - {criterio.codigo}",
                    )


@admin.register(ActividadEvaluable)
class ActividadEvaluableAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "modo", "fecha", "trimestre")
    list_filter = ("tipo", "modo", "trimestre__asignatura__grupo__curso_academico")
    filter_horizontal = ("criterios",)
    inlines = [PreguntaInline]
    actions = ["entrar_notas"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:actividad_id>/entrar-notas/",
                self.admin_site.admin_view(self.entrar_notas_view),
                name="evaluacion_actividadevaluable_entrar_notas",
            ),
        ]
        return custom_urls + urls

    def entrar_notas(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request, "Selecciona una sola actividad.", messages.WARNING
            )
            return
        actividad = queryset.first()
        return redirect(
            reverse(
                "admin:evaluacion_actividadevaluable_entrar_notas",
                args=[actividad.id],
            )
        )
    entrar_notas.short_description = "Entrar notas"

    def entrar_notas_view(self, request, actividad_id):
        actividad = get_object_or_404(ActividadEvaluable, id=actividad_id)
        grupo = actividad.trimestre.asignatura.grupo
        alumnos = Alumno.objects.filter(grupo=grupo).order_by("apellidos", "nombre")

        if actividad.modo == "global":
            criterios = actividad.criterios.all()
        else:
            preguntas = actividad.preguntas.select_related("criterio").order_by("orden")
            criterios = [p.criterio for p in preguntas]

        tipo = "rubrica" if request.GET.get("tipo") == "rubrica" else "numerica"

        if request.method == "POST":
            form = CalificacionForm(
                request.POST,
                alumnos=alumnos,
                criterios=criterios,
                tipo_actividad=tipo,
            )
            if form.is_valid():
                with transaction.atomic():
                    Calificacion.objects.filter(actividad=actividad).delete()
                    creadas = 0
                    for alumno in alumnos:
                        for criterio in criterios:
                            field_name = f"nota_{alumno.id}_{criterio.id}"
                            valor = form.cleaned_data.get(field_name)
                            if valor is not None and valor != "" and valor != "0":
                                if tipo == "rubrica":
                                    nivel = int(valor)
                                    Calificacion.objects.create(
                                        alumno=alumno,
                                        actividad=actividad,
                                        criterio=criterio,
                                        trimestre=actividad.trimestre,
                                        tipo_evaluacion="rubrica",
                                        nivel_rubrica=nivel,
                                    )
                                else:
                                    Calificacion.objects.create(
                                        alumno=alumno,
                                        actividad=actividad,
                                        criterio=criterio,
                                        trimestre=actividad.trimestre,
                                        tipo_evaluacion="numerica",
                                        valor_numerico=valor,
                                    )
                                creadas += 1
                messages.success(
                    request, f"Guardadas {creadas} calificaciones."
                )
                return redirect(
                    reverse("admin:evaluacion_actividadevaluable_changelist")
                )
        else:
            form = CalificacionForm(
                alumnos=alumnos,
                criterios=criterios,
                tipo_actividad=tipo,
            )

        return render(
            request,
            "admin/evaluacion/entrar_notas.html",
            {
                "form": form,
                "actividad": actividad,
                "alumnos": alumnos,
                "criterios": criterios,
                "tipo": tipo,
                "titulo": f"Notas: {actividad.nombre}",
            },
        )


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
