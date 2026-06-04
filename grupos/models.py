from django.db import models


class CursoAcademico(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = "curso académico"
        verbose_name_plural = "cursos académicos"

    def __str__(self):
        return self.nombre


class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    curso_academico = models.ForeignKey(
        CursoAcademico, on_delete=models.CASCADE, related_name="grupos"
    )

    class Meta:
        verbose_name = "grupo"
        verbose_name_plural = "grupos"
        unique_together = ("nombre", "curso_academico")

    def __str__(self):
        return f"{self.nombre} ({self.curso_academico})"


class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=200)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name="alumnos")

    class Meta:
        verbose_name = "alumno"
        verbose_name_plural = "alumnos"

    def __str__(self):
        return f"{self.apellidos}, {self.nombre}"


class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name="asignaturas")

    class Meta:
        verbose_name = "asignatura"
        verbose_name_plural = "asignaturas"
        unique_together = ("nombre", "grupo")

    def __str__(self):
        return f"{self.nombre} - {self.grupo}"
