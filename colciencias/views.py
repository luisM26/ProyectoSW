from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from colciencias.models import *
from django.core.context_processors import csrf
from django.shortcuts import render
from django.template import RequestContext
from reportlab.pdfgen import canvas
from colciencias.forms import *
import smtplib
import random
from django.contrib.auth import login, authenticate, logout
from django.core.mail import EmailMessage
from django.core.mail import send_mail

tipo = ''
codigo = ''

def busqueda(request):
    if request.method == 'GET':
        if request.GET.get('boton','') == 'Consultar':
            cod = request.GET.get('codigo','')
            tip = request.GET.get('tipo','')
            tipo = tip
            codigo = cod
            datos = Convenio.objects.filter(numConvenio = cod, tipoConvenio = tip)

            return render_to_response('estado.html',{'datos':datos},context_instance = RequestContext(request))

        if request.GET.get('boton','') == 'Generar PDF':
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

            # Create the PDF object, using the response object as its "file."
            p = canvas.Canvas(response)

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.drawString(100, 100, 'estado.html')

            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            return response
    datos = {}
    return render_to_response('estado.html',{'datos':datos},context_instance = RequestContext(request))

def cdr(request):
    if request.method == 'GET':
        if request.GET.get('boton','') == 'Consultar CDR':
            cod = request.GET.get('ID','')
            tip = request.GET.get('lineaTematica','')
            tipo = tip
            codigo = cod
            datos = Proyecto.objects.filter(ID = cod)
            send_mail('Este mensaje es para decir que django ', 'Here is the message.', 'from@example.com',
            ['camilo.28.tef@gmail.com'], fail_silently=False)
            correo = EmailMessage("titulo", "contenido", to=['camilo.28.sec@gmail.com'])
            correo.send()
            #Organizacion.objects.create(ID="2",nombre="PSL", NIT="1287654", convenio_FK="EL Refran")
            return render_to_response('estadoCDR.html',{'datos':datos},context_instance = RequestContext(request))

        if request.GET.get('boton','') == 'agregar CDR':
                return HttpResponseRedirect('/admin/colciencias/organizacion/add/')

        if request.GET.get('boton','') == 'Generar PDF':
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

            # Create the PDF object, using the response object as its "file."
            p = canvas.Canvas(response)

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.drawString(100, 100, 'estadocdr.html')

            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            return response
    datos = {}
    return render_to_response('estadoCDR.html',{'datos':datos},context_instance = RequestContext(request))

def Consultacdr(request):
            Becario.objects.all()
            return render_to_response('registros.html',context_instance = RequestContext(request))


