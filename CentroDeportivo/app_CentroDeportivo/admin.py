from django.contrib import admin
from .models import Deportista, Deporte, Equipo, Partido, Inscripcion_Equipo, Instalacion_Deportiva, Reserva_Instalacion

# Registrar todos los modelos
admin.site.register(Deportista)
admin.site.register(Deporte)
admin.site.register(Equipo)
admin.site.register(Partido)
admin.site.register(Inscripcion_Equipo)
admin.site.register(Instalacion_Deportiva)
admin.site.register(Reserva_Instalacion)

# Configurar título del admin
admin.site.site_header = "Administración Centro Deportivo"
admin.site.site_title = "Centro Deportivo"
admin.site.index_title = "Panel de Administración"
