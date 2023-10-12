from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_proyecto, name="listar_proyectos"),
    path('proyectos/<int:pk>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/editar/<int:pk>/', views.editar_proyecto, name='editar_proyecto'),
    path('proyectos/eliminar/<int:pk>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('mis_solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
    path('gestionar_solicitudes/', views.gestionar_solicitudes, name='gestionar_solicitudes'),
    path('inscribir/<int:proyecto_id>/', views.inscribir_proyecto, name='inscribir_proyecto'),
]