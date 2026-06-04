from django.db import models
from grupos.models import Asignatura, Alumno
from curriculo.models import CriterioEvaluacion


class Trimestre(models.Model):
    TRIMESTRES = [
        ("1", "1er Trimestre"),
        ("2", "2º Trimestre"),
        ("3", "3er Trimestre"),
        ("G", "Global"),
    ]
    nombre = models.CharField(max_length=1, choices=TRIMESTRES)
    asignatura = models.ForeignKey(
        Asignatura, on_delete=models.CASCADE, related_name="trimestres"
    )

    class Meta:
        verbose_name = "trimestre"
        verbose_name_plural = "trimestres"
        unique_together = ("nombre", "asignatura")

    def __str__(self):
        return f"{self.get_nombre_display()} - {self.asignatura}"


class ActividadEvaluable(models.Model):
    TIPOS = [
        ("examen", "Examen"),
        ("libreta", "Corrección de libreta"),
        ("exposicion", "Exposición"),
        ("tarea", "Tarea"),
        ("otro", "Otro"),
    ]
    MODOS = [
        ("global", "Global"),
        ("por_pregunta", "Por pregunta"),
    ]
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    modo = models.CharField(max_length=15, choices=MODOS)
    fecha = models.DateField()
    trimestre = models.ForeignKey(
        Trimestre, on_delete=models.CASCADE, related_name="actividades"
    )
    criterios = models.ManyToManyField(
        CriterioEvaluacion, blank=True, related_name="actividades_globales"
    )

    class Meta:
        verbose_name = "actividad evaluable"
        verbose_name_plural = "actividades evaluables"

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Pregunta(models.Model):
    enunciado = models.TextField()
    orden = models.PositiveIntegerField()
    puntuacion_maxima = models.DecimalField(max_digits=5, decimal_places=2)
    criterio = models.ForeignKey(
        CriterioEvaluacion, on_delete=models.CASCADE, related_name="preguntas"
    )
    actividad = models.ForeignKey(
        ActividadEvaluable, on_delete=models.CASCADE, related_name="preguntas"
    )

    class Meta:
        verbose_name = "pregunta"
        verbose_name_plural = "preguntas"
        ordering = ["actividad", "orden"]

    def __str__(self):
        return f"P{self.orden}: {self.enunciado[:50]}"


class Calificacion(models.Model):
    TIPOS_EVALUACION = [
        ("numerica", "Numérica"),
        ("rubrica", "Rúbrica"),
    ]
    alumno = models.ForeignKey(
        Alumno, on_delete=models.CASCADE, related_name="calificaciones"
    )
    actividad = models.ForeignKey(
        ActividadEvaluable, on_delete=models.CASCADE, related_name="calificaciones"
    )
    criterio = models.ForeignKey(
        CriterioEvaluacion, on_delete=models.CASCADE, related_name="calificaciones"
    )
    trimestre = models.ForeignKey(
        Trimestre, on_delete=models.CASCADE, related_name="calificaciones"
    )
    tipo_evaluacion = models.CharField(max_length=10, choices=TIPOS_EVALUACION)
    valor_numerico = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    nivel_rubrica = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_final = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "calificación"
        verbose_name_plural = "calificaciones"
        unique_together = ("alumno", "actividad", "criterio", "trimestre")

    def __str__(self):
        return f"{self.alumno} - {self.criterio}: {self.nota_final}"
