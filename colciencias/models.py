from django.db import models
from django.contrib import admin


class ProyectoInversion(models.Model):
    ID = models.CharField(max_length=20 , primary_key=True)
    recursos = models.CharField(max_length=100)
    metas = models.TextField()
    vigencia = models.CharField(max_length=10)
    #def __init__(self):
        #super(proyectoInversion, self).__init__()
        #

class TransferenciasSiif(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    convenio = models.CharField(max_length=30)
    fecha = models.DateField()
    valorTransferencia = models.FloatField()
    autoridad = models.CharField(max_length=30)
    entidad = models.CharField(max_length=30)
     #def __init__(self):
        #super(siif, self).__init__()
        #

class ProgramacionPago(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    convenio = models.CharField(max_length=30)
    fecha = models.DateField()
    valorTransferencia = models.FloatField()
    autoridad = models.CharField(max_length=30)
    entidad = models.CharField(max_length=30)
     #def __init__(self):
        #super(siif, self).__init__()
        #

class Convenio(models.Model):
    numConvenio = models.CharField(max_length=30 , primary_key=True)
    nombre = models.CharField(max_length=50)
    tipoConvenio = models.CharField(max_length=30)
    valorTotal = models.FloatField()
    RP = models.CharField(max_length=50)
    proyectoInversion_FK = models.ForeignKey(ProyectoInversion)
    fechaInicio = models.DateField()
    fechaSuscripcion = models.DateField()
    fechaLegalizacion = models.DateField()
    fechaFInalizacion = models.DateField()
    areaResponsable = models.CharField(max_length=30)
    supervisor = models.CharField(max_length=100)
    plazo = models.DateField()
    objeto = models.CharField(max_length=100)
    #def __init__(self):
        #super(Convenio, self).__init__()
        #

class Organizacion(models.Model):
    ID = models.CharField(max_length=20 , primary_key=True)
    nombre = models.CharField(max_length=100)
    NIT = models .CharField(max_length=20)
    convenio_FK = models.ForeignKey(Convenio)
    #def __init__(self):
        #super(organizacion, self).__init__()
        #

class Aporte(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    fecha = models.DateField()
    valor = models.FloatField()
    validado = models.CharField(max_length=10)
    esProgramado = models.CharField(max_length=10)
    organizacion_FK = models.ForeignKey(Organizacion , null=True)
    convenio_FK = models.ForeignKey(Convenio)
    #def __init__(self):
        #super(Aporte, self).__init__()
        #

class Becario(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=30)
    cumpleRequisitos = models.CharField(max_length=10)
    informacionBecario = models.TextField()
    informacionTesis = models.TextField()
    convenio_FK = models.ForeignKey(Convenio)
    #def __init__(self):
        #super(Becario, self).__init__()
        #

class Seguimiento(models.Model):
    ID = models.OneToOneField(Becario, primary_key=True)
    fecha = models.DateField()
    semestre = models.IntegerField()
    valorMatricula = models.FloatField()
    NumMatriculasAprobadas = models.IntegerField()
    #def __init__(self):
        #super(Seguimiento, self).__init__()
        #

class Desembolso(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    fechaSolicitud = models.DateField()
    valor = models.FloatField()
    girado = models.CharField(max_length=100)
    fechaGiro = models.DateField()
    condiciones = models.TextField()
    organizacion_FK = models.ForeignKey(Organizacion , null=True)
    becario_FK = models.ForeignKey(Becario)
    #def __init__(self):
        #super(Desembolso, self).__init__()
        #

class Proyecto(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    duracion = models.FloatField()
    lineaTematica = models.CharField(max_length=50)
    lugarEjecucion = models.CharField(max_length=50)
    titulo = models.CharField(max_length=100)
    CDR = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)
    justificacionEstado = models.TextField()
    convenio_FK = models.ForeignKey(Convenio)
    desembolso_FK = models.ForeignKey(Desembolso)
    #def __init__(self):
        #super(Proyecto, self).__init__()
        #

class Novedad(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    tipoNovedad = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    convenio_FK = models.ForeignKey(Convenio , null=True)
    proyecto_FK = models.ForeignKey(Proyecto , null=True)
    #def __init__(self):
        #super(Novedad, self).__init__()
        #

class Anexo(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    fechaCargue = models.DateField()
    descripcion = models.TextField()
    archivo = models.FileField()
    desembolso_FK = models.ForeignKey(Desembolso , null=True)
    convenio_FK = models.ForeignKey(Convenio , null=True)
    proyecto_FK = models.ForeignKey(Proyecto , null=True)
    #def __init__(self):
        #super(Anexo, self).__init__()
        #


class Notificacion(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    #def __init__(self):
        #super(Notificacion, self).__init__()
        #

class Notificacion_Proyecto(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    destinatario = models.CharField(max_length=30)
    mensaje = models.TextField()
    notificacion_FK = models.ForeignKey(Notificacion)
    proyecto_FK = models.ForeignKey(Proyecto)
    #def __init__(self):
        #super(Notificacion_Proyecto, self).__init__()
        #

class Notificacion_Convenio(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    destinatario = models.CharField(max_length=30)
    mensaje = models.TextField()
    notificacion_FK = models.ForeignKey(Notificacion)
    convenio_FK = models.ForeignKey(Convenio)
    #def __init__(self):
        #super(Notificacion_Proyecto, self).__init__()
        #
class Estado(models.Model):
    ID = models.CharField(max_length=30 , primary_key=True)
    convenio = models.CharField(max_length=30) 
    transferido = models.FloatField()
    transferir = models.FloatField()
    pagados = models.FloatField()
    noComprometidos = models.FloatField()
    noGirados = models.FloatField()
    comprometidos = models.FloatField()
    comprometer = models.FloatField()
    porPagar = models.FloatField()
    transferidoColciencias = models.FloatField()
    transferirColciencias = models.FloatField()
    transferidoOtrasEntidades = models.FloatField()
    girosOtrasEntidades = models.FloatField()
    #def __init__(self):
        #super(estado, self).__init__()
        #