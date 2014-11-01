from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponse
from colciencias.models import *

def buscarMostrar(request):
	if request.method == 'POST':
		codigo = request.POST['codigo']
		tipo = request.POST['tipo']

		resultado = Convenio.objects.filter(numConvenio = codigo, tipoConvenio = tipo)

	return render_to_response('estadoCuenta.html',{'lista':lista}, context_instance=RequestContext(request))

def inicio(request):
    return render_to_response('estadoCuenta.html')

def cdr(request):
	