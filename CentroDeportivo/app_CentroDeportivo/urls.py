from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # URLs para Deportistas
    path('deportistas/', views.ver_Deportista, name='ver_deportistas'),
    path('deportistas/agregar/', views.agregar_Deportista, name='agregar_deportista'),
    path('deportistas/actualizar/<int:id>/', views.actualizar_Deportista, name='actualizar_deportista'),
    path('deportistas/borrar/<int:id>/', views.borrar_Deportista, name='borrar_deportista'),

    # URLs para Deportes
    path('deportes/', views.ver_Deporte, name='ver_deportes'),
    path('deportes/agregar/', views.agregar_Deporte, name='agregar_deporte'),
    path('deportes/actualizar/<int:id>/', views.actualizar_Deporte, name='actualizar_deporte'),
    path('deportes/borrar/<int:id>/', views.borrar_Deporte, name='borrar_deporte'),

    # URLs para Equipos
    path('equipos/', views.ver_Equipo, name='ver_equipos'),
    path('equipos/agregar/', views.agregar_Equipo, name='agregar_equipo'),
    path('equipos/actualizar/<int:id>/', views.actualizar_Equipo, name='actualizar_equipo'),
    path('equipos/borrar/<int:id>/', views.borrar_Equipo, name='borrar_equipo'),

    # URLs para Partidos
    path('partidos/', views.ver_Partido, name='ver_partidos'),
    path('partidos/agregar/', views.agregar_Partido, name='agregar_partido'),
    path('partidos/actualizar/<int:id>/', views.actualizar_Partido, name='actualizar_partido'),
    path('partidos/borrar/<int:id>/', views.borrar_Partido, name='borrar_partido'),

    # URLs para Inscripciones de Equipos
    path('inscripciones/', views.ver_Inscripcion_Equipo, name='ver_inscripciones'),
    path('inscripciones/agregar/', views.agregar_Inscripcion_Equipo, name='agregar_inscripcion'),
    path('inscripciones/actualizar/<int:id>/', views.actualizar_Inscripcion_Equipo, name='actualizar_inscripcion'),
    path('inscripciones/borrar/<int:id>/', views.borrar_Inscripcion_Equipo, name='borrar_inscripcion'),

    # URLs para Instalaciones Deportivas
    path('instalaciones/', views.ver_Instalacion_Deportiva, name='ver_instalaciones'),
    path('instalaciones/agregar/', views.agregar_Instalacion_Deportiva, name='agregar_instalacion'),
    path('instalaciones/actualizar/<int:id>/', views.actualizar_Instalacion_Deportiva, name='actualizar_instalacion'),
    path('instalaciones/borrar/<int:id>/', views.borrar_Instalacion_Deportiva, name='borrar_instalacion'),

    # URLs para Reservas de Instalaciones
    path('reservas/', views.ver_Reserva_Instalacion, name='ver_reservas'),
    path('reservas/agregar/', views.agregar_Reserva_Instalacion, name='agregar_reserva'),
    path('reservas/actualizar/<int:id>/', views.actualizar_Reserva_Instalacion, name='actualizar_reserva'),
    path('reservas/borrar/<int:id>/', views.borrar_Reserva_Instalacion, name='borrar_reserva'),
]
