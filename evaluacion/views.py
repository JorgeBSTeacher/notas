from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Avg, Sum
from decimal import Decimal

from grupos.models import CursoAcademico, Grupo, Asignatura, Alumno
from evaluacion.models import (
    Trimestre, ActividadEvaluable, Calificacion, UnidadDidactica
)
from curriculo.models import CompetenciaClave, CompetenciaEspecifica, CriterioEvaluacion


@login_required
def home(request):
    cursos = CursoAcademico.objects.all().order_by("-nombre")
    grupos = Grupo.objects.select_related("curso_academico").prefetch_related("asignaturas").order_by("curso_academico__nombre", "nombre")
    return render(request, "evaluacion/home.html", {
        "cursos": cursos,
        "grupos": grupos,
    })


@login_required
def workspace(request, asignatura_id):
    asignatura = get_object_or_404(Asignatura.objects.select_related("grupo__curso_academico"), id=asignatura_id)
    grupo = asignatura.grupo
    alumnos = Alumno.objects.filter(grupo=grupo).order_by("apellidos", "nombre")

    trimestre_id = request.GET.get("trimestre")
    trimestres = Trimestre.objects.filter(asignatura=asignatura)

    if trimestre_id:
        trimestre = get_object_or_404(trimestres, id=trimestre_id)
    else:
        trimestre = trimestres.filter(nombre="1").first() or trimestres.first()

    tab = request.GET.get("tab", "panel")

    context = {
        "asignatura": asignatura,
        "grupo": grupo,
        "alumnos": alumnos,
        "trimestre": trimestre,
        "trimestres": trimestres,
        "tab": tab,
    }

    if tab == "panel":
        _panel_context(context, asignatura, trimestre, alumnos)
    elif tab == "criterios":
        _criterios_context(context, asignatura, trimestre, alumnos)
    elif tab == "ce":
        _ce_context(context, asignatura, trimestre, alumnos)
    elif tab == "cc":
        _cc_context(context, asignatura, trimestre, alumnos)

    return render(request, "evaluacion/workspace.html", context)


def _panel_context(context, asignatura, trimestre, alumnos):
    unidades = UnidadDidactica.objects.filter(trimestre=trimestre).order_by("orden")
    actividades = ActividadEvaluable.objects.filter(trimestre=trimestre).order_by("fecha")

    actividades_por_unidad = []
    for unidad in unidades:
        acts = [a for a in actividades if a.unidad_didactica_id == unidad.id]
        actividades_por_unidad.append((unidad, acts))

    sin_unidad = [a for a in actividades if a.unidad_didactica_id is None]
    if sin_unidad:
        actividades_por_unidad.append((None, sin_unidad))

    notas = _calcular_notas_actividades(alumnos, actividades)

    context["actividades_por_unidad"] = actividades_por_unidad
    context["notas"] = notas


def _calcular_notas_actividades(alumnos, actividades):
    califs = Calificacion.objects.filter(
        actividad__in=actividades
    ).values("alumno", "actividad").annotate(
        nota=Avg("nota_final")
    )
    notas = {}
    for c in califs:
        notas[f"{c['alumno']}_{c['actividad']}"] = c["nota"]
    return notas


def _criterios_context(context, asignatura, trimestre, alumnos):
    criterios = CriterioEvaluacion.objects.filter(
        competencia_especifica__competencia_clave__asignatura=asignatura
    ).select_related("competencia_especifica__competencia_clave")

    califs = Calificacion.objects.filter(
        trimestre=trimestre
    ).values("alumno", "criterio").annotate(nota=Avg("nota_final"))

    notas = {}
    for c in califs:
        notas[f"{c['alumno']}_{c['criterio']}"] = c["nota"]

    context["criterios"] = criterios
    context["notas_criterios"] = notas


def _ce_context(context, asignatura, trimestre, alumnos):
    ces = CompetenciaEspecifica.objects.filter(
        competencia_clave__asignatura=asignatura
    ).select_related("competencia_clave").prefetch_related("criterios")

    califs = Calificacion.objects.filter(
        trimestre=trimestre
    ).values("alumno", "criterio").annotate(nota=Avg("nota_final"))

    notas_por_criterio = {}
    for c in califs:
        notas_por_criterio[f"{c['alumno']}_{c['criterio']}"] = c["nota"]

    notas_ce = {}
    for alumno in alumnos:
        for ce in ces:
            notas_criterios = []
            peso_total = Decimal("0")
            suma_ponderada = Decimal("0")
            for criterio in ce.criterios.all():
                nota = notas_por_criterio.get(f"{alumno.id}_{criterio.id}")
                if nota is not None:
                    notas_criterios.append(nota)
                    peso = criterio.peso
                    peso_total += peso
                    suma_ponderada += nota * peso
            if peso_total > 0:
                notas_ce[f"{alumno.id}_{ce.id}"] = suma_ponderada / peso_total

    context["competencias_especificas"] = ces
    context["notas_ce"] = notas_ce


def _cc_context(context, asignatura, trimestre, alumnos):
    ccs = CompetenciaClave.objects.filter(
        asignatura=asignatura
    ).prefetch_related("competencias_especificas__criterios")

    califs = Calificacion.objects.filter(
        trimestre=trimestre
    ).values("alumno", "criterio").annotate(nota=Avg("nota_final"))

    notas_por_criterio = {}
    for c in califs:
        notas_por_criterio[f"{c['alumno']}_{c['criterio']}"] = c["nota"]

    notas_cc = {}
    for alumno in alumnos:
        for cc in ccs:
            suma_ce = Decimal("0")
            peso_ce_total = Decimal("0")
            for ce in cc.competencias_especificas.all():
                suma_criterio = Decimal("0")
                peso_total = Decimal("0")
                for criterio in ce.criterios.all():
                    nota = notas_por_criterio.get(f"{alumno.id}_{criterio.id}")
                    if nota is not None:
                        peso = criterio.peso
                        suma_criterio += nota * peso
                        peso_total += peso
                if peso_total > 0:
                    nota_ce = suma_criterio / peso_total
                    suma_ce += nota_ce * ce.peso
                    peso_ce_total += ce.peso
            if peso_ce_total > 0:
                notas_cc[f"{alumno.id}_{cc.id}"] = suma_ce / peso_ce_total

    context["competencias_clave"] = ccs
    context["notas_cc"] = notas_cc
