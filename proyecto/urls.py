from django.conf.urls import patterns, include, url
from django.contrib import admin
from colciencias.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proyecto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^estado/$', busqueda),
    url(r'^verificarTransferencias/$',verificarTransferencias),
 	url(r'^CDR/$', 'colciencias.views.cdr', name='CDR'),
 	#url(r'^Registros/$', 'colciencias.views.Consultacdr'), 
 	#url(r'^inicio/$', 'colciencias.views.inicio'),  	
 	url(r'^$', 'colciencias.views.inicio', name='home'),
 	url(r'^add/$', formulario, name='add'),
 	url(r'^cargar/$', formularioPro, name='proforma'),
 	url(r'^expedir/$', expedir_cdr, name='expedir'),
 	url(r'^crearConvenio/$', 'colciencias.views.gestionarConvenioEnSolicitud'),
 	url(r'^actualizarDatos/$', 'colciencias.views.gestionarConvenioRegistro'),
 	url(r'^anexo/$', formularioAnexo, name='anexo'),
 	url(r'^programarDesembolso/$', programarDesembolso, name='desembolso'),

)
