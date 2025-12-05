from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Deportista, Deporte, Equipo, Partido, Inscripcion_Equipo, Instalacion_Deportiva, Reserva_Instalacion
from django.utils import timezone
import json
from django.core.serializers.json import DjangoJSONEncoder

def inicio(request):
    total_deportistas = Deportista.objects.count()
    total_equipos = Equipo.objects.count()
    context = {
        'total_deportistas': total_deportistas,
        'total_equipos': total_equipos,
    }
    return render(request, 'inicio.html', context)

# ---------------------------------------------------------------
# VISTAS PARA DEPORTISTA
# ---------------------------------------------------------------
def agregar_Deportista(request):
    if request.method == 'POST':
        try:
            # Se asegura de obtener el objeto Deporte
            deporte_id = request.POST['deporte_principal']
            deporte = get_object_or_404(Deporte, pk=deporte_id)

            deportista = Deportista(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                fecha_nacimiento=request.POST['fecha_nacimiento'],
                genero=request.POST['genero'],
                email=request.POST['email'],
                telefono=request.POST['telefono'],
                # Se asigna el objeto Deporte, no solo el ID
                deporte_principal=deporte.nombre_deporte,
                nivel_habilidad=request.POST['nivel_habilidad'],
                fecha_registro=timezone.now().date(),
                lesiones_previas=request.POST.get('lesiones_previas', '')
            )
            deportista.save()
            return redirect('ver_deportistas')
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    
    # Se obtienen todos los deportes para el menú desplegable
    deportes = Deporte.objects.all().order_by('nombre_deporte')
    # Se convierten a JSON para usarlos en JavaScript
    deportes_data = list(deportes.values())

    return render(request, 'Deportista/agregar_Deportista.html', {
        'deportes': deportes,
        'deportes_data': json.dumps(deportes_data)
    })

def ver_Deportista(request):
    deportistas = Deportista.objects.all().order_by('-id_deportista')
    return render(request, 'Deportista/ver_Deportista.html', {'deportistas': deportistas})

def actualizar_Deportista(request, id):
    deportista = get_object_or_404(Deportista, id_deportista=id)
    
    if request.method == 'POST':
        try:
            # Se obtiene el objeto Deporte desde el ID
            deporte_id = request.POST['deporte_principal']
            deporte = get_object_or_404(Deporte, pk=deporte_id)

            deportista.nombre = request.POST['nombre']
            deportista.apellido = request.POST['apellido']
            deportista.fecha_nacimiento = request.POST['fecha_nacimiento']
            deportista.genero = request.POST['genero']
            deportista.email = request.POST['email']
            deportista.telefono = request.POST['telefono']
            # Se actualiza con el nombre del deporte
            deportista.deporte_principal = deporte.nombre_deporte
            deportista.nivel_habilidad = request.POST['nivel_habilidad']
            deportista.lesiones_previas = request.POST.get('lesiones_previas', '')
            deportista.save()
            return redirect('ver_deportistas')
        except Exception as e:
            return HttpResponse(f"Error al actualizar: {str(e)}")
            
    # Se obtienen los datos para los desplegables
    deportes = Deporte.objects.all().order_by('nombre_deporte')
    deportes_data = list(deportes.values())

    return render(request, 'Deportista/actualizar_Deportista.html', {
        'deportista': deportista,
        'deportes': deportes,
        'deportes_data': json.dumps(deportes_data)
    })

def borrar_Deportista(request, id):
    deportista = get_object_or_404(Deportista, id_deportista=id)
    if request.method == 'POST':
        try:
            deportista.delete()
            return redirect('ver_deportistas')
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    
    return render(request, 'Deportista/borrar_Deportista.html', {'deportista': deportista})

# ---------------------------------------------------------------
# VISTAS PARA DEPORTE
# ---------------------------------------------------------------
def agregar_Deporte(request):
    if request.method == 'POST':
        try:
            deporte = Deporte(
                nombre_deporte=request.POST['nombre_deporte'],
                descripcion=request.POST.get('descripcion', 'Sin descripción.'),
                num_jugadores_equipo=request.POST.get('num_jugadores_equipo', 1),
                es_individual=request.POST.get('es_individual') == 'on',
                reglas_basicas=request.POST.get('reglas_basicas', 'No especificadas.'),
                tipo_superficie=request.POST.get('tipo_superficie', 'No especificada.')
            )
            deporte.save()
            return redirect('ver_deportes')
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    
    return render(request, 'Deporte/agregar_Deporte.html')

def ver_Deporte(request):
    deportes = Deporte.objects.all().order_by('nombre_deporte')
    return render(request, 'Deporte/ver_Deporte.html', {'deportes': deportes})

def actualizar_Deporte(request, id):
    deporte = get_object_or_404(Deporte, id_deporte=id)
    if request.method == 'POST':
        try:
            deporte.nombre_deporte = request.POST['nombre_deporte']
            deporte.descripcion = request.POST.get('descripcion', deporte.descripcion)
            deporte.num_jugadores_equipo = request.POST.get('num_jugadores_equipo', deporte.num_jugadores_equipo)
            deporte.es_individual = request.POST.get('es_individual') == 'on'
            deporte.reglas_basicas = request.POST.get('reglas_basicas', deporte.reglas_basicas)
            deporte.tipo_superficie = request.POST.get('tipo_superficie', deporte.tipo_superficie)
            deporte.save()
            return redirect('ver_deportes')
        except Exception as e:
            return HttpResponse(f"Error al actualizar: {str(e)}")
            
    return render(request, 'Deporte/actualizar_Deporte.html', {'deporte': deporte})

def borrar_Deporte(request, id):
    deporte = get_object_or_404(Deporte, id_deporte=id)
    if request.method == 'POST':
        try:
            deporte.delete()
            return redirect('ver_deportes')
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
            
    return render(request, 'Deporte/borrar_Deporte.html', {'deporte': deporte})

# ---------------------------------------------------------------
# VISTAS PARA EQUIPO
# ---------------------------------------------------------------
def ver_Equipo(request):
    equipos = Equipo.objects.select_related('deporte').all().order_by('nombre_equipo')
    return render(request, 'Equipo/ver_Equipo.html', {'equipos': equipos})

def agregar_Equipo(request):
    if request.method == 'POST':
        try:
            deporte_id = request.POST.get('deporte')
            deporte = get_object_or_404(Deporte, pk=deporte_id)
            
            equipo = Equipo(
                nombre_equipo=request.POST['nombre_equipo'],
                deporte=deporte,
                fecha_fundacion=request.POST['fecha_fundacion'],
                entrenador=request.POST.get('entrenador', ''),
                capitan=request.POST.get('capitan', ''),
                num_jugadores_actual=request.POST.get('num_jugadores_actual', 0),
                categoria_edad=request.POST.get('categoria_edad', ''),
                colores_equipo=request.POST.get('colores_equipo', '')
            )
            equipo.save()
            return redirect('ver_equipos')
        except Exception as e:
            return HttpResponse(f"Error al agregar el equipo: {str(e)}")
            
    deportes = Deporte.objects.all().order_by('nombre_deporte')
    return render(request, 'Equipo/agregar_Equipo.html', {'deportes': deportes})

def actualizar_Equipo(request, id):
    equipo = get_object_or_404(Equipo, id_equipo=id)
    if request.method == 'POST':
        try:
            deporte_id = request.POST.get('deporte')
            deporte = get_object_or_404(Deporte, pk=deporte_id)

            equipo.nombre_equipo = request.POST['nombre_equipo']
            equipo.deporte = deporte
            equipo.fecha_fundacion = request.POST['fecha_fundacion']
            equipo.entrenador = request.POST.get('entrenador', '')
            equipo.capitan = request.POST.get('capitan', '')
            equipo.num_jugadores_actual = request.POST.get('num_jugadores_actual', 0)
            equipo.categoria_edad = request.POST.get('categoria_edad', '')
            equipo.colores_equipo = request.POST.get('colores_equipo', '')
            
            equipo.save()
            return redirect('ver_equipos')
        except Exception as e:
            return HttpResponse(f"Error al actualizar el equipo: {str(e)}")

    deportes = Deporte.objects.all().order_by('nombre_deporte')
    return render(request, 'Equipo/actualizar_Equipo.html', {
        'equipo': equipo,
        'deportes': deportes
    })

def borrar_Equipo(request, id):
    equipo = get_object_or_404(Equipo, id_equipo=id)
    if request.method == 'POST':
        try:
            equipo.delete()
            return redirect('ver_equipos')
        except Exception as e:
            return HttpResponse(f"Error al eliminar el equipo: {str(e)}")
            
    return render(request, 'Equipo/borrar_Equipo.html', {'equipo': equipo})

# ---------------------------------------------------------------
# VISTAS PARA PARTIDO
# ---------------------------------------------------------------
def ver_Partido(request):
    partidos = Partido.objects.select_related('deporte', 'equipo_local', 'equipo_visitante').all().order_by('-fecha_partido')
    return render(request, 'Partido/ver_Partido.html', {'partidos': partidos})

def agregar_Partido(request):
    if request.method == 'POST':
        try:
            deporte = get_object_or_404(Deporte, pk=request.POST['deporte'])
            equipo_local = get_object_or_404(Equipo, pk=request.POST['equipo_local'])
            equipo_visitante = get_object_or_404(Equipo, pk=request.POST['equipo_visitante'])
            
            partido = Partido(
                deporte=deporte,
                fecha_partido=request.POST['fecha_partido'],
                hora_partido=request.POST['hora_partido'],
                lugar_partido=request.POST['lugar_partido'],
                equipo_local=equipo_local,
                equipo_visitante=equipo_visitante,
                resultado_local=request.POST.get('resultado_local', 0),
                resultado_visitante=request.POST.get('resultado_visitante', 0),
                arbitro=request.POST.get('arbitro', '')
            )
            partido.save()
            return redirect('ver_partidos')
        except Exception as e:
            return HttpResponse(f"Error al agregar el partido: {str(e)}")
    
    deportes = Deporte.objects.all()
    equipos = list(Equipo.objects.values('id_equipo', 'nombre_equipo', 'deporte_id'))

    return render(request, 'Partido/agregar_Partido.html', {
        'deportes': deportes,
        'equipos_json': json.dumps(equipos)
    })

def actualizar_Partido(request, id):
    partido = get_object_or_404(Partido, id_partido=id)
    if request.method == 'POST':
        try:
            partido.deporte = get_object_or_404(Deporte, pk=request.POST['deporte'])
            partido.fecha_partido = request.POST['fecha_partido']
            partido.hora_partido = request.POST['hora_partido']
            partido.lugar_partido = request.POST['lugar_partido']
            partido.equipo_local = get_object_or_404(Equipo, pk=request.POST['equipo_local'])
            partido.equipo_visitante = get_object_or_404(Equipo, pk=request.POST['equipo_visitante'])
            partido.resultado_local = request.POST.get('resultado_local', 0)
            partido.resultado_visitante = request.POST.get('resultado_visitante', 0)
            partido.arbitro = request.POST.get('arbitro', '')
            partido.save()
            return redirect('ver_partidos')
        except Exception as e:
            return HttpResponse(f"Error al actualizar el partido: {str(e)}")
            
    deportes = Deporte.objects.all()
    equipos = list(Equipo.objects.values('id_equipo', 'nombre_equipo', 'deporte_id'))
    
    return render(request, 'Partido/actualizar_Partido.html', {
        'partido': partido,
        'deportes': deportes,
        'equipos_json': json.dumps(equipos)
    })

def borrar_Partido(request, id):
    partido = get_object_or_404(Partido, id_partido=id)
    if request.method == 'POST':
        try:
            partido.delete()
            return redirect('ver_partidos')
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    
    return render(request, 'Partido/borrar_Partido.html', {'partido': partido})


# ---------------------------------------------------------------
# VISTAS PARA INSCRIPCION_EQUIPO
# ---------------------------------------------------------------
def ver_Inscripcion_Equipo(request):
    inscripciones = Inscripcion_Equipo.objects.select_related('deportista', 'equipo').all().order_by('-fecha_inscripcion')
    return render(request, 'Inscripcion_Equipo/ver_Inscripcion_Equipo.html', {'inscripciones': inscripciones})

def agregar_Inscripcion_Equipo(request):
    if request.method == 'POST':
        try:
            deportista = get_object_or_404(Deportista, pk=request.POST['deportista'])
            equipo = get_object_or_404(Equipo, pk=request.POST['equipo'])
            
            inscripcion = Inscripcion_Equipo(
                deportista=deportista,
                equipo=equipo,
                fecha_inscripcion=request.POST['fecha_inscripcion'],
                rol_en_equipo=request.POST.get('rol_en_equipo', ''),
                num_camiseta=request.POST.get('num_camiseta', 0),
                es_titular=request.POST.get('es_titular') == 'on',
                fecha_baja_equipo=request.POST.get('fecha_baja_equipo') or None
            )
            inscripcion.save()
            return redirect('ver_inscripciones')
        except Exception as e:
            return HttpResponse(f"Error al agregar la inscripción: {str(e)}")
    
    deportistas = Deportista.objects.all()
    equipos = Equipo.objects.all()
    deportes = Deporte.objects.all()
    
    deportistas_data = list(deportistas.values())
    equipos_data = list(equipos.values('id_equipo', 'nombre_equipo', 'entrenador', 'capitan', 'deporte_id', 'categoria_edad', 'num_jugadores_actual'))
    deportes_data = list(deportes.values('pk', 'nombre_deporte'))

    return render(request, 'Inscripcion_Equipo/agregar_Inscripcion_Equipo.html', {
        'deportistas': deportistas,
        'equipos': equipos,
        'deportes': deportes,
        'deportistas_data': deportistas_data,
        'equipos_data': equipos_data,
        'deportes_data': deportes_data,
    })

def actualizar_Inscripcion_Equipo(request, id):
    inscripcion = get_object_or_404(Inscripcion_Equipo, id_inscripcion=id)
    if request.method == 'POST':
        try:
            inscripcion.deportista = get_object_or_404(Deportista, pk=request.POST['deportista'])
            inscripcion.equipo = get_object_or_404(Equipo, pk=request.POST['equipo'])
            inscripcion.fecha_inscripcion = request.POST['fecha_inscripcion']
            inscripcion.rol_en_equipo = request.POST.get('rol_en_equipo', '')
            inscripcion.num_camiseta = request.POST.get('num_camiseta', 0)
            inscripcion.es_titular = request.POST.get('es_titular') == 'on'
            fecha_baja = request.POST.get('fecha_baja_equipo')
            inscripcion.fecha_baja_equipo = fecha_baja if fecha_baja else None
            
            inscripcion.save()
            return redirect('ver_inscripciones')
        except Exception as e:
            return HttpResponse(f"Error al actualizar la inscripción: {str(e)}")
            
    deportistas = Deportista.objects.all()
    equipos = Equipo.objects.all()
    deportes = Deporte.objects.all()
    
    deportistas_data = list(deportistas.values())
    equipos_data = list(equipos.values('id_equipo', 'nombre_equipo', 'entrenador', 'capitan', 'deporte_id', 'categoria_edad', 'num_jugadores_actual'))
    deportes_data = list(deportes.values('pk', 'nombre_deporte'))

    return render(request, 'Inscripcion_Equipo/actualizar_Inscripcion_Equipo.html', {
        'inscripcion': inscripcion,
        'deportistas': deportistas,
        'equipos': equipos,
        'deportes': deportes,
        'deportistas_data': deportistas_data,
        'equipos_data': equipos_data,
        'deportes_data': deportes_data,
    })

def borrar_Inscripcion_Equipo(request, id):
    inscripcion = get_object_or_404(Inscripcion_Equipo, id_inscripcion=id)
    if request.method == 'POST':
        try:
            inscripcion.delete()
            return redirect('ver_inscripciones')
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    
    return render(request, 'Inscripcion_Equipo/borrar_Inscripcion_Equipo.html', {'inscripcion': inscripcion})

# ---------------------------------------------------------------
# VISTAS PARA INSTALACION_DEPORTIVA
# ---------------------------------------------------------------
def ver_Instalacion_Deportiva(request):
    instalaciones = Instalacion_Deportiva.objects.all().order_by('nombre_instalacion')
    return render(request, 'Instalacion_Deportiva/ver_Instalacion_Deportiva.html', {'instalaciones': instalaciones})

def agregar_Instalacion_Deportiva(request):
    if request.method == 'POST':
        try:
            instalacion = Instalacion_Deportiva(
                nombre_instalacion=request.POST['nombre_instalacion'],
                tipo_instalacion=request.POST['tipo_instalacion'],
                ubicacion=request.POST.get('ubicacion', ''),
                capacidad_personas=request.POST.get('capacidad_personas', 0),
                horario_disponible=request.POST.get('horario_disponible', 'No especificado'),
                costo_alquiler_hora=request.POST['costo_alquiler_hora'],
                es_techada=request.POST.get('es_techada') == 'on',
                descripcion_equipamiento=request.POST.get('descripcion_equipamiento', '')
            )
            instalacion.save()
            return redirect('ver_instalaciones')
        except Exception as e:
            return HttpResponse(f"Error al agregar la instalación: {str(e)}")
    
    return render(request, 'Instalacion_Deportiva/agregar_Instalacion_Deportiva.html')

def actualizar_Instalacion_Deportiva(request, id):
    instalacion = get_object_or_404(Instalacion_Deportiva, id_instalacion=id)
    if request.method == 'POST':
        try:
            instalacion.nombre_instalacion = request.POST['nombre_instalacion']
            instalacion.tipo_instalacion = request.POST['tipo_instalacion']
            instalacion.ubicacion = request.POST.get('ubicacion', instalacion.ubicacion)
            instalacion.capacidad_personas = request.POST.get('capacidad_personas', instalacion.capacidad_personas)
            instalacion.horario_disponible = request.POST.get('horario_disponible', instalacion.horario_disponible)
            instalacion.costo_alquiler_hora = request.POST['costo_alquiler_hora']
            instalacion.es_techada = request.POST.get('es_techada') == 'on'
            instalacion.descripcion_equipamiento = request.POST.get('descripcion_equipamiento', instalacion.descripcion_equipamiento)
            instalacion.save()
            return redirect('ver_instalaciones')
        except Exception as e:
            return HttpResponse(f"Error al actualizar la instalación: {str(e)}")
            
    return render(request, 'Instalacion_Deportiva/actualizar_Instalacion_Deportiva.html', {'instalacion': instalacion})

def borrar_Instalacion_Deportiva(request, id):
    instalacion = get_object_or_404(Instalacion_Deportiva, id_instalacion=id)
    if request.method == 'POST':
        try:
            instalacion.delete()
            return redirect('ver_instalaciones')
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
            
    return render(request, 'Instalacion_Deportiva/borrar_Instalacion_Deportiva.html', {'instalacion': instalacion})

# ---------------------------------------------------------------
# VISTAS PARA RESERVA_INSTALACION
# ---------------------------------------------------------------
def ver_Reserva_Instalacion(request):
    reservas = Reserva_Instalacion.objects.select_related('instalacion', 'deportista').all().order_by('-fecha_reserva', 'hora_inicio')
    return render(request, 'Reserva_Instalacion/ver_Reserva_Instalacion.html', {'reservas': reservas})

def agregar_Reserva_Instalacion(request):
    if request.method == 'POST':
        try:
            instalacion = get_object_or_404(Instalacion_Deportiva, pk=request.POST.get('instalacion'))
            deportista_obj = get_object_or_404(Deportista, pk=request.POST.get('deportista'))
            
            reserva = Reserva_Instalacion(
                instalacion=instalacion,
                deportista=deportista_obj,
                fecha_reserva=request.POST.get('fecha_reserva'),
                hora_inicio=request.POST.get('hora_inicio'),
                hora_fin=request.POST.get('hora_fin'),
                duracion_horas=request.POST.get('duracion_horas'),
                motivo_reserva=request.POST.get('motivo_reserva'),
                monto_pagado=request.POST.get('monto_pagado'),
                estado_reserva=request.POST.get('estado_reserva', 'Confirmada')
            )
            reserva.save()
            return redirect('ver_reservas')
        except Exception as e:
            return HttpResponse(f"Error al agregar la reserva: {str(e)}")
    
    instalaciones = Instalacion_Deportiva.objects.all().order_by('nombre_instalacion')
    deportistas = Deportista.objects.all().order_by('apellido', 'nombre')

    instalaciones_data = list(instalaciones.values())
    deportistas_data = list(deportistas.values())

    return render(request, 'Reserva_Instalacion/agregar_Reserva_Instalacion.html', {
        'instalaciones': instalaciones,
        'deportistas': deportistas,
        'instalaciones_data': instalaciones_data,
        'deportistas_data': deportistas_data,
    })

def actualizar_Reserva_Instalacion(request, id):
    reserva = get_object_or_404(Reserva_Instalacion, id_reserva=id)
    if request.method == 'POST':
        try:
            reserva.instalacion = get_object_or_404(Instalacion_Deportiva, pk=request.POST.get('instalacion'))
            reserva.deportista = get_object_or_404(Deportista, pk=request.POST.get('deportista'))
            reserva.fecha_reserva = request.POST.get('fecha_reserva', reserva.fecha_reserva)
            reserva.hora_inicio = request.POST.get('hora_inicio', reserva.hora_inicio)
            reserva.hora_fin = request.POST.get('hora_fin', reserva.hora_fin)
            reserva.duracion_horas = request.POST.get('duracion_horas', reserva.duracion_horas)
            reserva.motivo_reserva = request.POST.get('motivo_reserva', reserva.motivo_reserva)
            reserva.monto_pagado = request.POST.get('monto_pagado', reserva.monto_pagado)
            reserva.estado_reserva = request.POST.get('estado_reserva', 'Confirmada')
            reserva.save()
            return redirect('ver_reservas')
        except Exception as e:
            return HttpResponse(f"Error al actualizar la reserva: {str(e)}")
            
    instalaciones = Instalacion_Deportiva.objects.all().order_by('nombre_instalacion')
    deportistas = Deportista.objects.all().order_by('apellido', 'nombre')

    instalaciones_data = list(instalaciones.values())
    deportistas_data = list(deportistas.values())

    return render(request, 'Reserva_Instalacion/actualizar_Reserva_Instalacion.html', {
        'reserva': reserva,
        'instalaciones': instalaciones,
        'deportistas': deportistas,
        'instalaciones_data': instalaciones_data,
        'deportistas_data': deportistas_data,
    })

def borrar_Reserva_Instalacion(request, id):
    reserva = get_object_or_404(Reserva_Instalacion, id_reserva=id)
    if request.method == 'POST':
        try:
            reserva.delete()
            return redirect('ver_reservas')
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    
    return render(request, 'Reserva_Instalacion/borrar_Reserva_Instalacion.html', {'reserva': reserva})
