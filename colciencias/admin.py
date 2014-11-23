from django.contrib import admin
from colciencias.models import *

class OrganizacionAdmin (admin.ModelAdmin):
    list_display = ('ID', 'nombre', 'NIT')
    search_fields = ('nombre',) 

 

class ConvenioAdmin (admin.ModelAdmin):
    list_display = ('numConvenio', 'nombre', 'tipoConvenio')
    search_fields = ('nombre',) 




admin.site.register(ProyectoInversion)
admin.site.register(Convenio,ConvenioAdmin)
admin.site.register(Organizacion,OrganizacionAdmin)
admin.site.register(Aporte)
admin.site.register(Becario)
admin.site.register(Seguimiento)
admin.site.register(Desembolso)
admin.site.register(Proyecto)
admin.site.register(Novedad)
admin.site.register(Anexo)
admin.site.register(Notificacion)
admin.site.register(Notificacion_Proyecto)
admin.site.register(Notificacion_Convenio)
admin.site.register(Estado)
admin.site.register(TransferenciasSiif)
admin.site.register(ProgramacionPago)
admin.site.register(Proforma)
admin.site.register(CDR)
admin.site.register(Giro)
admin.site.register(Ffjc)
admin.site.register(ConvenioSol)
admin.site.register(Convocatoria)