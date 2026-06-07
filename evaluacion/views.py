import json
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from grupos.models import CursoAcademico, Grupo, Asignatura, Alumno
from evaluacion.models import (
    Trimestre, ActividadEvaluable, Calificacion, UnidadDidactica, Pregunta
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

    raw_trimestre = request.GET.get("trimestre")
    trimestres = Trimestre.objects.filter(asignatura=asignatura)

    if raw_trimestre == "global":
        trimestre = None
    elif raw_trimestre:
        trimestre = get_object_or_404(trimestres, id=raw_trimestre)
    else:
        trimestre = trimestres.filter(nombre="1").first() or trimestres.first()

    tab = request.GET.get("tab", "panoramica")

    context = {
        "asignatura": asignatura,
        "grupo": grupo,
        "alumnos": alumnos,
        "trimestre": trimestre,
        "trimestres": trimestres,
        "tab": tab,
        "es_global": trimestre is None,
    }

    if tab == "panoramica":
        _panoramica_context(context, asignatura, trimestre, alumnos)
    elif tab == "panel":
        _panel_context(context, asignatura, trimestre, alumnos)
    elif tab == "criterios":
        _criterios_context(context, asignatura, trimestre, alumnos)
    elif tab == "ce":
        _ce_context(context, asignatura, trimestre, alumnos)
    elif tab == "cc":
        _cc_context(context, asignatura, trimestre, alumnos)

    return render(request, "evaluacion/workspace.html", context)


def _panel_context(context, asignatura, trimestre, alumnos):
    if trimestre is not None:
        unidades = UnidadDidactica.objects.filter(trimestre=trimestre).order_by("orden")
        actividades = ActividadEvaluable.objects.filter(trimestre=trimestre).order_by("fecha")
    else:
        unidades = UnidadDidactica.objects.all().order_by("orden")
        actividades = ActividadEvaluable.objects.all().order_by("fecha")

    actividades_por_unidad = []
    for unidad in unidades:
        acts = [a for a in actividades if a.unidad_didactica_id == unidad.id]
        actividades_por_unidad.append((unidad, acts))

    sin_unidad = [a for a in actividades if a.unidad_didactica_id is None]
    if sin_unidad:
        actividades_por_unidad.append((None, sin_unidad))

    notas = _calcular_notas_actividades(alumnos, actividades)

    notas_medias = {}
    for a in actividades:
        avg = Calificacion.objects.filter(actividad=a).aggregate(avg=Avg("nota_final"))["avg"]
        if avg is not None:
            notas_medias[str(a.id)] = round(avg, 2)

    context["actividades_por_unidad"] = actividades_por_unidad
    context["notas"] = notas
    context["notas_medias"] = notas_medias


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

    califs = Calificacion.objects.all()
    if trimestre is not None:
        califs = califs.filter(trimestre=trimestre)
    califs = califs.values("alumno", "criterio").annotate(nota=Avg("nota_final"))

    notas = {}
    for c in califs:
        notas[f"{c['alumno']}_{c['criterio']}"] = c["nota"]

    context["criterios"] = criterios
    context["notas_criterios"] = notas

    medias_alumnos = {}
    for alumno in alumnos:
        pref = f"{alumno.id}_"
        vals = [v for k, v in notas.items() if k.startswith(pref)]
        medias_alumnos[alumno.id] = round(sum(vals) / len(vals), 2) if vals else None
    context["medias_alumnos_criterios"] = medias_alumnos

    medias_criterio = {}
    for criterio in criterios:
        suf = f"_{criterio.id}"
        vals = [v for k, v in notas.items() if k.endswith(suf)]
        medias_criterio[str(criterio.id)] = round(sum(vals) / len(vals), 2) if vals else None
    context["medias_criterio"] = medias_criterio


def _ce_context(context, asignatura, trimestre, alumnos):
    ces = CompetenciaEspecifica.objects.filter(
        competencia_clave__asignatura=asignatura
    ).select_related("competencia_clave").prefetch_related("criterios")

    califs = Calificacion.objects.all()
    if trimestre is not None:
        califs = califs.filter(trimestre=trimestre)
    califs = califs.values("alumno", "criterio").annotate(nota=Avg("nota_final"))

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

    medias_alumnos = {}
    for alumno in alumnos:
        pref = f"{alumno.id}_"
        vals = [v for k, v in notas_ce.items() if k.startswith(pref)]
        medias_alumnos[alumno.id] = round(sum(vals) / len(vals), 2) if vals else None
    context["medias_alumnos_ce"] = medias_alumnos

    medias_ce = {}
    for ce in ces:
        suf = f"_{ce.id}"
        vals = [v for k, v in notas_ce.items() if k.endswith(suf)]
        medias_ce[str(ce.id)] = round(sum(vals) / len(vals), 2) if vals else None
    context["medias_ce"] = medias_ce


def _cc_context(context, asignatura, trimestre, alumnos):
    ccs = CompetenciaClave.objects.filter(
        asignatura=asignatura
    ).prefetch_related("competencias_especificas__criterios")

    califs = Calificacion.objects.all()
    if trimestre is not None:
        califs = califs.filter(trimestre=trimestre)
    califs = califs.values("alumno", "criterio").annotate(nota=Avg("nota_final"))

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

    medias_alumnos = {}
    for alumno in alumnos:
        pref = f"{alumno.id}_"
        vals = [v for k, v in notas_cc.items() if k.startswith(pref)]
        medias_alumnos[alumno.id] = round(sum(vals) / len(vals), 2) if vals else None
    context["medias_alumnos_cc"] = medias_alumnos

    medias_cc = {}
    for cc in ccs:
        suf = f"_{cc.id}"
        vals = [v for k, v in notas_cc.items() if k.endswith(suf)]
        medias_cc[str(cc.id)] = round(sum(vals) / len(vals), 2) if vals else None
    context["medias_cc"] = medias_cc


def _panoramica_context(context, asignatura, trimestre, alumnos):
    if trimestre is not None:
        actividades = ActividadEvaluable.objects.filter(trimestre=trimestre).order_by("fecha")
        unidades = UnidadDidactica.objects.filter(trimestre=trimestre).order_by("orden")
    else:
        actividades = ActividadEvaluable.objects.all().order_by("fecha")
        unidades = UnidadDidactica.objects.all().order_by("orden")

    # Group actividades by UD (unidad_didactica can be None)
    sin_ud = []
    agrupaciones = []
    for u in unidades:
        acts = [a for a in actividades if a.unidad_didactica_id == u.id]
        if acts:
            agrupaciones.append((u, acts))
    sin_ud = [a for a in actividades if a.unidad_didactica_id is None]
    if sin_ud:
        agrupaciones.append((None, sin_ud))

    context["agrupaciones_ud"] = agrupaciones

    # Grades lookup: notas_grid[alumno_id][actividad_id] = nota
    califs = Calificacion.objects.filter(
        actividad__in=actividades
    ).values("alumno", "actividad").annotate(nota=Avg("nota_final"))

    notas_grid = {}
    for alumno in alumnos:
        notas_grid[alumno.id] = {}
    for c in califs:
        alumno_id = c["alumno"]
        actividad_id = str(c["actividad"])
        nota = c["nota"]
        notas_grid[alumno_id][actividad_id] = nota
    context["notas_grid"] = notas_grid

    # Per-UD average per student (string keys for template safety)
    medias_ud = {}
    for alumno in alumnos:
        medias_ud[alumno.id] = {}
        for unidad, acts in agrupaciones:
            ud_key = str(unidad.id) if unidad else "0"
            notas = [notas_grid[alumno.id].get(str(a.id)) for a in acts if notas_grid[alumno.id].get(str(a.id)) is not None]
            if notas:
                medias_ud[alumno.id][ud_key] = round(sum(notas) / len(notas), 2)
    context["medias_ud"] = medias_ud

    # Overall student average
    medias_alumnos = {}
    for alumno in alumnos:
        notas = list(notas_grid.get(alumno.id, {}).values())
        if notas:
            medias_alumnos[alumno.id] = round(sum(notas) / len(notas), 2)
        else:
            medias_alumnos[alumno.id] = None
    context["medias_alumnos"] = medias_alumnos

    # Class average per activity
    medias_actividad = {}
    for a in actividades:
        avg = Calificacion.objects.filter(actividad=a).aggregate(avg=Avg("nota_final"))["avg"]
        medias_actividad[str(a.id)] = round(avg, 2) if avg is not None else None
    context["medias_actividad"] = medias_actividad


@login_required
def notas_actividad(request, actividad_id):
    actividad = get_object_or_404(
        ActividadEvaluable.objects.select_related("trimestre__asignatura__grupo"),
        id=actividad_id,
    )
    asignatura = actividad.trimestre.asignatura
    alumnos = Alumno.objects.filter(grupo=asignatura.grupo).order_by("apellidos", "nombre")
    criterios = actividad.criterios.all()
    preguntas = actividad.preguntas.select_related("criterio").order_by("orden")

    if actividad.modo == "por_pregunta" and not preguntas:
        preguntas = list(Pregunta.objects.none())

    calificaciones = Calificacion.objects.filter(
        actividad=actividad
    ).select_related("criterio")
    califs_dict = {}
    for c in calificaciones:
        key = f"{c.alumno_id}_{c.criterio_id}"
        califs_dict[key] = c

    return render(request, "evaluacion/notas_actividad.html", {
        "actividad": actividad,
        "asignatura": asignatura,
        "grupo": asignatura.grupo,
        "alumnos": alumnos,
        "criterios": criterios,
        "preguntas": preguntas,
        "calificaciones": califs_dict,
    })


@require_POST
@login_required
def guardar_nota(request):
    data = json.loads(request.body)
    alumno_id = data["alumno_id"]
    actividad_id = data["actividad_id"]
    modo = data.get("modo", "global")
    valor = data.get("valor")
    tipo = data.get("tipo", "numerica")

    actividad = get_object_or_404(ActividadEvaluable, id=actividad_id)
    alumno = get_object_or_404(Alumno, id=alumno_id)

    if modo == "global":
        criterios = list(actividad.criterios.all())
        if not criterios:
            return JsonResponse({"saved": False, "error": "no_criterios"}, status=400)
    else:
        criterio_id = data.get("criterio_id")
        if not criterio_id:
            return JsonResponse({"saved": False, "error": "no_criterio"}, status=400)
        criterios = [get_object_or_404(CriterioEvaluacion, id=criterio_id)]

    results = []
    for criterio in criterios:
        if valor is None or valor == "":
            Calificacion.objects.filter(
                alumno=alumno, actividad=actividad, criterio=criterio, trimestre=actividad.trimestre
            ).delete()
            results.append({"criterio": criterio.id, "deleted": True})
            continue

        defaults = {
            "tipo_evaluacion": tipo,
            "nota_final": Decimal("0"),
        }
        if tipo == "numerica":
            defaults["valor_numerico"] = Decimal(str(valor))
        elif tipo == "rubrica":
            defaults["nivel_rubrica"] = int(valor)

        try:
            calif, created = Calificacion.objects.get_or_create(
                alumno=alumno,
                actividad=actividad,
                criterio=criterio,
                trimestre=actividad.trimestre,
                defaults=defaults,
            )
        except ValidationError as e:
            return JsonResponse({"saved": False, "error": str(e)}, status=400)

        if not created:
            if tipo == "numerica":
                calif.tipo_evaluacion = "numerica"
                calif.valor_numerico = Decimal(str(valor))
            elif tipo == "rubrica":
                calif.tipo_evaluacion = "rubrica"
                calif.nivel_rubrica = int(valor)
            try:
                calif.save()
            except ValidationError as e:
                return JsonResponse({"saved": False, "error": str(e)}, status=400)

        results.append({
            "criterio": criterio.id,
            "saved": True,
            "nota_final": str(calif.nota_final),
            "created": created,
        })

    return JsonResponse({"results": results, "saved": True})
