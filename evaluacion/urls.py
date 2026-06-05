from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("panel/<int:asignatura_id>/", views.workspace, name="workspace"),
]
