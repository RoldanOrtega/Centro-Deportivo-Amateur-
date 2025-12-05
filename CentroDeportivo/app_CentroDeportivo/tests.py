from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio
    path('', views.inicio_CentroDeportivo, name='inicio'),
    
    # Rutas para Deportista
    path('deportista/agregar/', views.agregar_Deportista, name='agregar_Deportista'),
    path('deportista/ver/', views.ver_Deportista, name='ver_Deportista'),
    path('deportista/actualizar/<int:id>/', views.actualizar_Deportista, name='actualizar_Deportista'),
    path('deportista/realizar-actualizacion/<int:id>/', views.realizar_actualizacion_Deportista, name='realizar_actualizacion_Deportista'),
    path('deportista/borrar/<int:id>/', views.borrar_Deportista, name='borrar_Deportista'),
]