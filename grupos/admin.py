import json
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django import forms
from .models import CursoAcademico, Grupo, Alumno, Asignatura
from curriculo.models import CompetenciaClave, CompetenciaEspecifica, CriterioEvaluacion


class ImportCurriculoForm(forms.Form):
    asignatura = forms.ModelChoiceField(
        queryset=Asignatura.objects.all(), label="Asignatura"
    )
    archivo = forms.FileField(label="Archivo JSON")
    modo = forms.ChoiceField(
        choices=[("actualizar", "Actualizar"), ("sobrescribir", "Sobrescribir")],
        label="Modo",
        initial="actualizar",
    )


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
    actions = ["importar_curriculo"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "importar-curriculo/",
                self.admin_site.admin_view(self.importar_curriculo_view),
                name="grupos_asignatura_importar_curriculo",
            ),
        ]
        return custom_urls + urls

    def importar_curriculo(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Selecciona una sola asignatura.", messages.WARNING)
            return
        asignatura = queryset.first()
        return redirect(
            reverse("admin:grupos_asignatura_importar_curriculo")
            + f"?asignatura={asignatura.id}"
        )
    importar_curriculo.short_description = "Importar currículo LOMLOE"

    def importar_curriculo_view(self, request):
        asignatura_id = request.GET.get("asignatura")
        initial = {}
        if asignatura_id:
            try:
                initial["asignatura"] = Asignatura.objects.get(id=asignatura_id)
            except Asignatura.DoesNotExist:
                pass

        if request.method == "POST":
            form = ImportCurriculoForm(request.POST, request.FILES)
            if form.is_valid():
                asignatura = form.cleaned_data["asignatura"]
                modo = form.cleaned_data["modo"]
                try:
                    data = json.load(request.FILES["archivo"])
                except json.JSONDecodeError:
                    messages.error(request, "El archivo no es un JSON válido.")
                    return render(
                        request, "admin/grupos/importar_curriculo.html", {"form": form}
                    )

                if modo == "sobrescribir":
                    CompetenciaClave.objects.filter(asignatura=asignatura).delete()

                importados = 0
                for cc_data in data:
                    cc, _ = CompetenciaClave.objects.update_or_create(
                        codigo=cc_data["codigo"],
                        asignatura=asignatura,
                        defaults={
                            "descripcion": cc_data["descripcion"],
                            "peso": cc_data.get("peso", 1.0),
                        },
                    )
                    for ce_data in cc_data.get("competencias_especificas", []):
                        ce, _ = CompetenciaEspecifica.objects.update_or_create(
                            codigo=ce_data["codigo"],
                            competencia_clave=cc,
                            defaults={
                                "descripcion": ce_data["descripcion"],
                                "peso": ce_data.get("peso", 1.0),
                            },
                        )
                        for crit_data in ce_data.get("criterios", []):
                            CriterioEvaluacion.objects.update_or_create(
                                codigo=crit_data["codigo"],
                                competencia_especifica=ce,
                                defaults={
                                    "descripcion": crit_data["descripcion"],
                                    "peso": crit_data.get("peso", 1.0),
                                },
                            )
                            importados += 1

                messages.success(
                    request,
                    f"Importados {importados} criterios en '{asignatura}'",
                )
                return redirect(
                    reverse("admin:grupos_asignatura_changelist")
                )
        else:
            form = ImportCurriculoForm(initial=initial)

        return render(
            request, "admin/grupos/importar_curriculo.html", {"form": form}
        )
