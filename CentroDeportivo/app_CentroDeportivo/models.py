from django.db import models

# ---------------------------------------
# MODELO: DEPORTISTA
# ---------------------------------------
class Deportista(models.Model):
    id_deportista = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1)
    email = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    deporte_principal = models.CharField(max_length=50)
    nivel_habilidad = models.CharField(max_length=50)
    fecha_registro = models.DateField()
    lesiones_previas = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ---------------------------------------
# MODELO: DEPORTE
# ---------------------------------------
class Deporte(models.Model):
    id_deporte = models.AutoField(primary_key=True)
    nombre_deporte = models.CharField(max_length=50)
    descripcion = models.TextField()
    num_jugadores_equipo = models.IntegerField()
    es_individual = models.BooleanField()
    reglas_basicas = models.TextField()
    tipo_superficie = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_deporte


# ---------------------------------------
# MODELO: EQUIPO
# ---------------------------------------
class Equipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre_equipo = models.CharField(max_length=100)
    deporte = models.ForeignKey(Deporte, on_delete=models.PROTECT, db_column='id_deporte')
    fecha_fundacion = models.DateField()
    entrenador = models.CharField(max_length=100)
    capitan = models.CharField(max_length=100)
    num_jugadores_actual = models.IntegerField()
    categoria_edad = models.CharField(max_length=50)
    colores_equipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_equipo


# ---------------------------------------
# MODELO: PARTIDO
# ---------------------------------------
class Partido(models.Model):
    id_partido = models.AutoField(primary_key=True)
    deporte = models.ForeignKey(Deporte, on_delete=models.PROTECT, db_column='id_deporte')
    fecha_partido = models.DateField()
    hora_partido = models.TimeField()
    lugar_partido = models.CharField(max_length=100)
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_local', on_delete=models.PROTECT, db_column='id_equipo_local')
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitante', on_delete=models.PROTECT, db_column='id_equipo_visitante')
    resultado_local = models.IntegerField()
    resultado_visitante = models.IntegerField()
    arbitro = models.CharField(max_length=100)

    def __str__(self):
        return f"Partido {self.id_partido}"


# ---------------------------------------
# MODELO: INSCRIPCIÓN DE EQUIPO
# ---------------------------------------
class Inscripcion_Equipo(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    deportista = models.ForeignKey(Deportista, on_delete=models.CASCADE, db_column='id_deportista')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo')
    fecha_inscripcion = models.DateField()
    rol_en_equipo = models.CharField(max_length=50)
    num_camiseta = models.IntegerField()
    es_titular = models.BooleanField()
    fecha_baja_equipo = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Inscripción {self.id_inscripcion}"


# ---------------------------------------
# MODELO: INSTALACIÓN DEPORTIVA
# ---------------------------------------
class Instalacion_Deportiva(models.Model):
    id_instalacion = models.AutoField(primary_key=True)
    nombre_instalacion = models.CharField(max_length=255)
    tipo_instalacion = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    capacidad_personas = models.IntegerField()
    costo_alquiler_hora = models.DecimalField(max_digits=10, decimal_places=2)
    es_techada = models.BooleanField()
    horario_disponible = models.TextField()
    descripcion_equipamiento = models.TextField()

    def __str__(self):
        return self.nombre_instalacion


# ---------------------------------------
# MODELO: RESERVA DE INSTALACIÓN
# ---------------------------------------
class Reserva_Instalacion(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    deportista = models.ForeignKey(Deportista, on_delete=models.CASCADE, db_column='id_deportista_reserva')
    instalacion = models.ForeignKey(Instalacion_Deportiva, on_delete=models.PROTECT, db_column='id_instalacion')
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    duracion_horas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    motivo_reserva = models.TextField()
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    estado_reserva = models.CharField(max_length=50)

    def __str__(self):
        return f"Reserva {self.id_reserva}"
