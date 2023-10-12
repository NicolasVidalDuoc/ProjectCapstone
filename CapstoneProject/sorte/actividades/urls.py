from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_actividad, name="listar_actividad"),
    path('actividades/<int:pk>/', views.detalle_actividad, name='detalle_actividad'),
    path('actividades/crear/', views.crear_actividad, name='crear_actividad'),
    path('actividades/editar/<int:pk>/', views.editar_actividad, name='editar_actividad'),
    path('actividades/eliminar/<int:pk>/', views.eliminar_actividad, name='eliminar_actividad'),
    path('mis_solicitudes/', views.mis_solicitudes_miembro, name='mis_solicitudes_miembro'),
    path('gestionar_inscripciones/', views.gestionar_inscripciones, name='gestionar_inscripciones'),
    path('inscribir/<int:actividad_id>/', views.inscribir_actividad, name='inscribir_actividad'),
]