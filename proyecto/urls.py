from django.conf.urls import patterns, include, url
from django.contrib import admin
from colciencias.views import *
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proyecto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
  #  url((r'^estado/','colciencias.views.inicio')),
 	url(r'^estado/$', 'colciencias.views.busqueda'),
 	url(r'^CDR/$', 'colciencias.views.cdr'),
 	url(r'^Registros/$', 'colciencias.views.Consultacdr'),
 	 url(r'^verificarTransferencias/$',verificarTransferencias),
   # url(r'^CDR/$','colciencias.views.cdrs'),
)


#	 				  (r'^prueba/','colciencias.views.inicio'),
              #      (r'^admin/', include(admin.site.urls)),
#)
