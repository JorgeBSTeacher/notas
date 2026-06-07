from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("panel/<int:asignatura_id>/", views.workspace, name="workspace"),
    path("actividad/<int:actividad_id>/notas/", views.notas_actividad, name="notas_actividad"),
    path("api/guardar-nota/", views.guardar_nota, name="guardar_nota"),
]
