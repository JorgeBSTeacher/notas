import json
from decimal import Decimal

from django.test import TestCase, Client
from django.urls import reverse

from grupos.models import CursoAcademico, Grupo, Asignatura, Alumno
from curriculo.models import CompetenciaClave, CompetenciaEspecifica, CriterioEvaluacion
from evaluacion.models import (
    Trimestre, UnidadDidactica, ActividadEvaluable, Calificacion, Pregunta,
)


class TestFlujoSaveNotas(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.curso = CursoAcademico.objects.create(nombre="2025-2026")
        cls.grupo = Grupo.objects.create(
            nombre="1ESO-A",
            curso_academico=cls.curso,
        )
        cls.asignatura = Asignatura.objects.create(
            nombre="Matemáticas",
            grupo=cls.grupo,
        )

        cls.cc = CompetenciaClave.objects.create(
            codigo="CC1",
            descripcion="Competencia en comunicación lingüística",
            asignatura=cls.asignatura,
            peso=Decimal("0.5"),
        )
        cls.ce = CompetenciaEspecifica.objects.create(
            codigo="CE1",
            descripcion="Comprender y producir textos",
            competencia_clave=cls.cc,
            peso=Decimal("0.6"),
        )
        cls.criterio1 = CriterioEvaluacion.objects.create(
            codigo="CR1",
            descripcion="Identificar ideas principales",
            competencia_especifica=cls.ce,
            peso=Decimal("0.4"),
        )
        cls.criterio2 = CriterioEvaluacion.objects.create(
            codigo="CR2",
            descripcion="Analizar estructura de textos",
            competencia_especifica=cls.ce,
            peso=Decimal("0.6"),
        )

        cls.alumno = Alumno.objects.create(
            nombre="Ana",
            apellidos="Martín López",
            grupo=cls.grupo,
        )
        cls.alumno2 = Alumno.objects.create(
            nombre="Luis",
            apellidos="García Pérez",
            grupo=cls.grupo,
        )

        cls.trimestre = Trimestre.objects.create(
            nombre="1",
            asignatura=cls.asignatura,
        )

        cls.unidad = UnidadDidactica.objects.create(
            nombre="UD1: Números",
            trimestre=cls.trimestre,
            orden=1,
        )

        cls.actividad = ActividadEvaluable.objects.create(
            nombre="Examen tema 1",
            tipo="examen",
            modo="global",
            fecha="2026-01-15",
            trimestre=cls.trimestre,
            unidad_didactica=cls.unidad,
        )
        cls.actividad.criterios.add(cls.criterio1, cls.criterio2)

        # Admin user for views
        from django.contrib.auth.models import User
        cls.admin = User.objects.create_superuser(
            username="admin", password="admin", email="admin@test.com"
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="admin")

    # --- API guardar_nota ---

    def test_guardar_nota_global_crea_calificaciones(self):
        """Modo global: al guardar una nota, se crea Calificacion para cada criterio"""
        resp = self.client.post(
            reverse("guardar_nota"),
            data=json.dumps({
                "alumno_id": self.alumno.id,
                "actividad_id": self.actividad.id,
                "valor": 7.5,
                "tipo": "numerica",
                "modo": "global",
            }),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["saved"])
        self.assertEqual(len(data["results"]), 2)  # 2 criterios

        qs = Calificacion.objects.filter(alumno=self.alumno, actividad=self.actividad)
        self.assertEqual(qs.count(), 2)
        for calif in qs:
            self.assertEqual(calif.nota_final, Decimal("7.50"))
            self.assertEqual(calif.trimestre, self.trimestre)

    def test_guardar_nota_global_sin_criterios_da_error(self):
        """Modo global sin criterios en la actividad → 400"""
        act_sin_criterios = ActividadEvaluable.objects.create(
            nombre="Act sin criterios",
            tipo="tarea",
            modo="global",
            fecha="2026-02-01",
            trimestre=self.trimestre,
        )
        resp = self.client.post(
            reverse("guardar_nota"),
            data=json.dumps({
                "alumno_id": self.alumno.id,
                "actividad_id": act_sin_criterios.id,
                "valor": 5,
                "tipo": "numerica",
                "modo": "global",
            }),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_guardar_nota_por_pregunta_crea_calificacion(self):
        """Modo por_pregunta: al guardar, solo se crea para ese criterio"""
        pregunta = Pregunta.objects.create(
            enunciado="Pregunta 1",
            orden=1,
            puntuacion_maxima=Decimal("10"),
            criterio=self.criterio1,
            actividad=self.actividad,
        )
        self.actividad.modo = "por_pregunta"
        self.actividad.save()

        resp = self.client.post(
            reverse("guardar_nota"),
            data=json.dumps({
                "alumno_id": self.alumno.id,
                "actividad_id": self.actividad.id,
                "criterio_id": self.criterio1.id,
                "valor": 8,
                "tipo": "numerica",
                "modo": "por_pregunta",
            }),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["saved"])

        calif = Calificacion.objects.get(
            alumno=self.alumno, actividad=self.actividad, criterio=self.criterio1
        )
        self.assertEqual(calif.nota_final, Decimal("8.00"))

    def test_guardar_nota_actualiza_en_vez_de_duplicar(self):
        """Guardar dos veces la misma nota → actualiza, no duplica"""
        for _ in range(2):
            self.client.post(
                reverse("guardar_nota"),
                data=json.dumps({
                    "alumno_id": self.alumno.id,
                    "actividad_id": self.actividad.id,
                    "valor": 6,
                    "tipo": "numerica",
                    "modo": "global",
                }),
                content_type="application/json",
            )
        qs = Calificacion.objects.filter(alumno=self.alumno, actividad=self.actividad)
        self.assertEqual(qs.count(), 2)  # 1 por criterio, no duplicados
        for calif in qs:
            self.assertEqual(calif.nota_final, Decimal("6.00"))

    def test_guardar_nota_elimina_si_valor_vacio(self):
        """Enviar valor null → elimina la(s) calificación(es)"""
        # Primero guardar
        self.client.post(
            reverse("guardar_nota"),
            data=json.dumps({
                "alumno_id": self.alumno.id,
                "actividad_id": self.actividad.id,
                "valor": 5,
                "tipo": "numerica",
                "modo": "global",
            }),
            content_type="application/json",
        )
        self.assertEqual(
            Calificacion.objects.filter(alumno=self.alumno, actividad=self.actividad).count(),
            2,
        )

        # Luego eliminar
        resp = self.client.post(
            reverse("guardar_nota"),
            data=json.dumps({
                "alumno_id": self.alumno.id,
                "actividad_id": self.actividad.id,
                "valor": None,
                "tipo": "numerica",
                "modo": "global",
            }),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            Calificacion.objects.filter(alumno=self.alumno, actividad=self.actividad).count(),
            0,
        )

    def test_guardar_nota_valor_fuera_rango_da_error(self):
        """Valor > 10 → 400"""
        resp = self.client.post(
            reverse("guardar_nota"),
            data=json.dumps({
                "alumno_id": self.alumno.id,
                "actividad_id": self.actividad.id,
                "valor": 11,
                "tipo": "numerica",
                "modo": "global",
            }),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    # --- Verificación: la nota aparece en las vistas ---

    def _guardar_nota(self, alumno, valor):
        self.client.post(
            reverse("guardar_nota"),
            data=json.dumps({
                "alumno_id": alumno.id,
                "actividad_id": self.actividad.id,
                "valor": valor,
                "tipo": "numerica",
                "modo": "global",
            }),
            content_type="application/json",
        )

    def test_nota_visible_en_panel(self):
        self._guardar_nota(self.alumno, 7.5)
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "panel"},
        )
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()

        key = f"{self.alumno.id}_{self.actividad.id}"
        # Check passing notas dict contains expected average
        notas = resp.context.get("notas", {})
        self.assertIn(key, notas, f"Nota para alumno {self.alumno.id} y actividad {self.actividad.id} debería estar en notas dict")
        self.assertEqual(float(notas[key]), 7.5)

    def test_nota_visible_en_criterios(self):
        self._guardar_nota(self.alumno, 7.5)
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "panel"},
        )
        self.assertEqual(resp.status_code, 200)

    def test_panoramica_muestra_notas_en_grid(self):
        """La vista panorámica muestra notas en la cuadrícula alumnos × actividades"""
        from evaluacion.views import _panoramica_context
        ctx = {}
        _panoramica_context(ctx, self.asignatura, self.trimestre, [self.alumno, self.alumno2])
        self.assertIn("agrupaciones_ud", ctx)
        self.assertIn("notas_grid", ctx)
        self.assertIn("medias_alumnos", ctx)
        self.assertIn("medias_actividad", ctx)
        self.assertIn("medias_ud", ctx)
        # Sin calificaciones, todo vacío, pero grid pre-poblado con alumnos
        self.assertIn(self.alumno.id, ctx["notas_grid"])
        self.assertIn(self.alumno2.id, ctx["notas_grid"])
        self.assertEqual(ctx["notas_grid"][self.alumno.id], {})
        self.assertIsNone(ctx["medias_alumnos"][self.alumno.id])

        # Guardar una nota y verificar que aparece en el grid
        Calificacion.objects.create(
            alumno=self.alumno,
            actividad=self.actividad,
            criterio=self.criterio1,
            trimestre=self.trimestre,
            tipo_evaluacion="numerica",
            valor_numerico=Decimal("7.50"),
            nota_final=Decimal("7.50"),
        )
        ctx2 = {}
        _panoramica_context(ctx2, self.asignatura, self.trimestre, [self.alumno, self.alumno2])
        grid = ctx2["notas_grid"]
        self.assertIn(self.alumno.id, grid)
        self.assertIn(str(self.actividad.id), grid[self.alumno.id])
        self.assertEqual(grid[self.alumno.id][str(self.actividad.id)], Decimal("7.50"))
        # Alumno2 sin notas
        self.assertEqual(grid[self.alumno2.id], {})

    def test_panoramica_es_tab_por_defecto(self):
        """La pestaña panorámica es la que se muestra por defecto"""
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context.get("tab"), "panoramica")
        self.assertIn("agrupaciones_ud", resp.context)

    def test_panoramica_html_se_renderea(self):
        """La plantilla panorámica se renderiza sin errores"""
        # Poner una nota
        Calificacion.objects.create(
            alumno=self.alumno,
            actividad=self.actividad,
            criterio=self.criterio1,
            trimestre=self.trimestre,
            tipo_evaluacion="numerica",
            valor_numerico=Decimal("8.00"),
            nota_final=Decimal("8.00"),
        )
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "panoramica"},
        )
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertIn("Panorámica", html)
        self.assertIn("8,00", html)
        self.assertIn(self.alumno.apellidos, html)
        self.assertIn(self.actividad.nombre, html)

    def test_nota_visible_en_ce(self):
        self._guardar_nota(self.alumno, 7.5)
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "ce"},
        )
        self.assertEqual(resp.status_code, 200)
        notas_ce = resp.context.get("notas_ce", {})

        key = f"{self.alumno.id}_{self.ce.id}"
        self.assertIn(key, notas_ce,
                      f"Nota para CE {self.ce.codigo} debería estar en notas_ce")
        # Ambos criterios tienen 7.5, CR1 (peso 0.4) + CR2 (peso 0.6) = 7.5
        self.assertEqual(float(notas_ce[key]), 7.5)

    def test_nota_visible_en_cc(self):
        self._guardar_nota(self.alumno, 7.5)
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "cc"},
        )
        self.assertEqual(resp.status_code, 200)
        notas_cc = resp.context.get("notas_cc", {})

        key = f"{self.alumno.id}_{self.cc.id}"
        self.assertIn(key, notas_cc,
                      f"Nota para CC {self.cc.codigo} debería estar en notas_cc")
        # CE único con peso 0.6 → se usa como peso_total, nota_ce=7.5
        # CC1: suma(7.5 * 0.6) / 0.6 = 7.5
        self.assertEqual(float(notas_cc[key]), 7.5)

    def test_nota_visible_en_criterios_html(self):
        """Verifica que el valor aparece renderizado en el HTML de criterios"""
        self._guardar_nota(self.alumno, 7.5)
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "criterios"},
        )
        html = resp.content.decode()
        self.assertIn("7,50", html)

    def test_nota_visible_en_ce_html(self):
        self._guardar_nota(self.alumno, 6.0)
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "ce"},
        )
        html = resp.content.decode()
        self.assertIn("6,00", html)

    def test_nota_visible_en_cc_html(self):
        self._guardar_nota(self.alumno, 8.5)
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "cc"},
        )
        html = resp.content.decode()
        self.assertIn("8,50", html)
        """Dos criterios con pesos distintos → nota CE ponderada"""
        self.criterio1.peso = Decimal("0.8")
        self.criterio1.save()
        self.criterio2.peso = Decimal("0.2")
        self.criterio2.save()

        self._guardar_nota(self.alumno, 10.0)
        # Solo CR1 tiene calificación (CR2 no, porque la nota global no se ha guardado aún)
        # Espera, en global se guarda para AMBOS criterios
        # CR1=10.0 (peso 0.8), CR2=10.0 (peso 0.2)
        # CE = (10.0*0.8 + 10.0*0.2) / (0.8+0.2) = 10.0

        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "ce"},
        )
        notas_ce = resp.context.get("notas_ce", {})
        key = f"{self.alumno.id}_{self.ce.id}"
        self.assertEqual(float(notas_ce[key]), 10.0)

    def test_calificacion_de_otro_alumno_no_afecta(self):
        """La nota de un alumno no debe aparecer en el contexto de otro"""
        self._guardar_nota(self.alumno, 5)
        self._guardar_nota(self.alumno2, 8)

        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "criterios"},
        )
        notas = resp.context["notas_criterios"]

        key1 = f"{self.alumno.id}_{self.criterio1.id}"
        key2 = f"{self.alumno2.id}_{self.criterio1.id}"
        self.assertIn(key1, notas)
        self.assertIn(key2, notas)
        self.assertEqual(float(notas[key1]), 5.0)
        self.assertEqual(float(notas[key2]), 8.0)

    def test_sin_notas_no_aparecen_en_vistas(self):
        """Sin calificaciones, los dicts deben estar vacíos"""
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "panel"},
        )
        self.assertEqual(resp.context.get("notas", {}), {})

        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "criterios"},
        )
        self.assertEqual(resp.context.get("notas_criterios", {}), {})

        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "ce"},
        )
        self.assertEqual(resp.context.get("notas_ce", {}), {})

        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "cc"},
        )
        self.assertEqual(resp.context.get("notas_cc", {}), {})

    def test_actividad_sin_criterios_no_rompe_panel(self):
        """Actividad sin criterios no debe causar error 500 en el panel"""
        act_sin_criterios = ActividadEvaluable.objects.create(
            nombre="Tarea extra",
            tipo="tarea",
            modo="global",
            fecha="2026-03-01",
            trimestre=self.trimestre,
            unidad_didactica=self.unidad,
        )
        resp = self.client.get(
            reverse("workspace", args=[self.asignatura.id]),
            {"trimestre": self.trimestre.id, "tab": "panel"},
        )
        self.assertEqual(resp.status_code, 200)
