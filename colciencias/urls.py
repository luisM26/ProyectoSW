from django.conf.urls import patterns, include, url
from django.contrib import admin
from colciencias.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proyecto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^estado/','colciencias.views.busqueda', name= estado),
    url(r'^verificarTransferencias/','colciencias.views.verificarTransferencias', name= transferencias),
    url(r'^CDR/$', 'colciencias.views.cdr'),
    url(r'^inicio/$', 'colciencias.views.inicio'),
 	url(r'^Registros/$', 'colciencias.views.Consultacdr'),

)