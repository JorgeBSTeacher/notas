from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from grupos.models import Asignatura, Alumno
from curriculo.models import CriterioEvaluacion


MAX_NIVELES_RUBRICA_POR_DEFECTO = 4


def convertir_rubrica_a_numerico(nivel, max_niveles=None):
    if max_niveles is None:
        max_niveles = MAX_NIVELES_RUBRICA_POR_DEFECTO
    if max_niveles <= 1:
        return Decimal("0")
    return Decimal(nivel - 1) * Decimal("10") / Decimal(max_niveles - 1)


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


class UnidadDidactica(models.Model):
    nombre = models.CharField(max_length=200)
    trimestre = models.ForeignKey(
        Trimestre, on_delete=models.CASCADE, related_name="unidades"
    )
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "unidad didáctica / situación de aprendizaje"
        verbose_name_plural = "unidades didácticas / situaciones de aprendizaje"
        ordering = ["trimestre", "orden"]

    def __str__(self):
        return f"{self.nombre}"


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
    unidad_didactica = models.ForeignKey(
        "UnidadDidactica",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actividades",
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


class RubricaConfig(models.Model):
    criterio = models.OneToOneField(
        CriterioEvaluacion,
        on_delete=models.CASCADE,
        related_name="rubrica_config",
        null=True,
        blank=True,
    )
    max_niveles = models.PositiveSmallIntegerField(default=4)

    class Meta:
        verbose_name = "configuración de rúbrica"
        verbose_name_plural = "configuraciones de rúbrica"

    def __str__(self):
        return f"Rúbrica {self.max_niveles} niveles - {self.criterio or '(regla de tres)'}"


class RubricaNivel(models.Model):
    rubrica_config = models.ForeignKey(
        RubricaConfig, on_delete=models.CASCADE, related_name="niveles"
    )
    nivel = models.PositiveSmallIntegerField()
    valor_numerico = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "nivel de rúbrica"
        verbose_name_plural = "niveles de rúbrica"
        unique_together = ("rubrica_config", "nivel")
        ordering = ["rubrica_config", "nivel"]

    def __str__(self):
        return f"Nivel {self.nivel}: {self.valor_numerico}"


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

    def clean(self):
        if self.tipo_evaluacion == "numerica" and self.valor_numerico is None:
            raise ValidationError("El valor numérico es obligatorio para evaluación numérica.")
        if self.tipo_evaluacion == "rubrica" and self.nivel_rubrica is None:
            raise ValidationError("El nivel de rúbrica es obligatorio para evaluación con rúbrica.")
        if self.valor_numerico is not None and not (0 <= self.valor_numerico <= 10):
            raise ValidationError("El valor numérico debe estar entre 0 y 10.")
        if self.nivel_rubrica is not None and not (1 <= self.nivel_rubrica <= 5):
            raise ValidationError("El nivel de rúbrica debe estar entre 1 y 5.")
        if not (0 <= self.nota_final <= 10):
            raise ValidationError("La nota final debe estar entre 0 y 10.")

    def save(self, *args, **kwargs):
        if self.tipo_evaluacion == "numerica":
            self.nota_final = self.valor_numerico
        elif self.tipo_evaluacion == "rubrica" and self.nivel_rubrica is not None:
            config = RubricaConfig.objects.filter(
                criterio=self.criterio
            ).first()
            if config:
                nivel = config.niveles.filter(nivel=self.nivel_rubrica).first()
                if nivel:
                    self.valor_numerico = nivel.valor_numerico
                    self.nota_final = nivel.valor_numerico
                else:
                    self.nota_final = convertir_rubrica_a_numerico(
                        self.nivel_rubrica, config.max_niveles
                    )
                    self.valor_numerico = self.nota_final
            else:
                self.nota_final = convertir_rubrica_a_numerico(self.nivel_rubrica)
                self.valor_numerico = self.nota_final
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alumno} - {self.criterio}: {self.nota_final}"
