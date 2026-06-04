from django.db import models
from grupos.models import Asignatura


class CompetenciaClave(models.Model):
    codigo = models.CharField(max_length=20)
    descripcion = models.TextField()
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    asignatura = models.ForeignKey(
        Asignatura, on_delete=models.CASCADE, related_name="competencias_clave"
    )

    class Meta:
        verbose_name = "competencia clave"
        verbose_name_plural = "competencias clave"
        unique_together = ("codigo", "asignatura")

    def __str__(self):
        return f"{self.codigo} - {self.asignatura}"


class CompetenciaEspecifica(models.Model):
    codigo = models.CharField(max_length=20)
    descripcion = models.TextField()
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    competencia_clave = models.ForeignKey(
        CompetenciaClave,
        on_delete=models.CASCADE,
        related_name="competencias_especificas",
    )

    class Meta:
        verbose_name = "competencia específica"
        verbose_name_plural = "competencias específicas"
        unique_together = ("codigo", "competencia_clave")

    def __str__(self):
        return f"{self.codigo}"


class CriterioEvaluacion(models.Model):
    codigo = models.CharField(max_length=20)
    descripcion = models.TextField()
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    competencia_especifica = models.ForeignKey(
        CompetenciaEspecifica,
        on_delete=models.CASCADE,
        related_name="criterios",
    )

    class Meta:
        verbose_name = "criterio de evaluación"
        verbose_name_plural = "criterios de evaluación"
        unique_together = ("codigo", "competencia_especifica")

    def __str__(self):
        return f"{self.codigo}"
