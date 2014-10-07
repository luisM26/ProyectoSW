from django.db import models

class Estado(models.Model):
    justificacionEstado = models.CharField(max_length=200)
    estado = models.CharField(max_length=20)

class ConvocatoriaProyecto(models.Model):
    duracion = models.IntegerField()
    estado = models.ForeignKey(Estado)
    titulo = models.CharField(max_length=100)
    cdr = models.CharField(max_length=50)
    lugarEjecucion = models.CharField(max_length=50)
    lineaTematica = models.CharField(max_length=50)

class entidadParticipante(models.Model):
    entidad = models.CharField(max_length=50)

class ConvocatorioConvenioContrato(models.Model):
    numConvenio = models.IntegerField()
    tipoConvenio = models.CharField(max_length=20)
    supervisor = models.CharField(max_length=50)
    areaResponsable = models.CharField(max_length=50)
    valorTotal = models.IntegerField()


