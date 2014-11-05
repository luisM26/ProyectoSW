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
import os

codigo = 0
tipo = ''

def busqueda(request):
    if request.method == 'POST':
        if request.POST.get('boton','') == 'Consultar':
            global codigo
            codigo = request.POST.get('codigo','')
            global tipo
            tipo = request.POST.get('tipo','')
            validar = Convenio.objects.filter(numConvenio = codigo, tipoConvenio = tipo)
            if validar:
                convenio = Convenio.objects.get(numConvenio = codigo, tipoConvenio = tipo)
                datos = Estado.objects.get(convenio = codigo)
                datos.transferido = float(convenio.valorTotal)
                datos.transferir = float(datos.transferir) - float(convenio.valorTotal)
                datos.comprometer = float(datos.comprometer) - float(convenio.valorTotal)
                datos.porPagar = float(datos.comprometidos) - float(datos.pagados)
                return render_to_response('estado.html',{'datos':datos,'convenios':convenio},context_instance = RequestContext(request))
            else:
                datos = {}
                return render_to_response('estado.html',{'datos':datos},context_instance = RequestContext(request))

        if request.POST.get('boton','') == 'Generar PDF':
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="estadoCuenta.pdf"'

            # Create the PDF object, using the response object as its "file."
            p = canvas.Canvas(response)

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            convenio = Convenio.objects.get(numConvenio =codigo, tipoConvenio = tipo)
            datos = Estado.objects.get(convenio = codigo)
            imagen = os.path.realpath(os.path.dirname(__file__))
            p.drawImage(imagen + "/Imagenes/logo.png",50,750,width=200, height=50)

            p.setFont("Helvetica-Bold", 16)
            p.drawString(210, 700, "Informe Estado de Cuenta")

            p.setFont("Helvetica", 12)
            p.drawString(50,660, "Numero de Convenio: ")
            p.drawString(170,660, convenio.numConvenio)

            p.setFont("Helvetica", 12)
            p.drawString(50,640, "Nombre del Convenio: ")
            p.drawString(173,640, convenio.nombre)

            p.setFont("Helvetica", 12)
            p.drawString(50,620, "Fecha Inicio: $")
            p.drawString(132,620, str(convenio.fechaInicio))

            p.setFont("Helvetica", 12)
            p.drawString(50,600, "Fecha Fin: $")
            p.drawString(120,600, str(convenio.fechaFInalizacion))

            p.setFont("Helvetica", 12)
            p.drawString(50,580, "Valor Transferido: $")
            p.drawString(160,580, str(convenio.valorTotal))

            p.setFont("Helvetica", 12)
            p.drawString(50,560, "Saldo Por Transferir: $")
            p.drawString(175,560, str(float(datos.transferir) - float(convenio.valorTotal)))

            p.setFont("Helvetica", 12)
            p.drawString(50,540, "Recursos Comprometidos: $")
            p.drawString(204,540, str(datos.comprometidos))

            p.setFont("Helvetica", 12)
            p.drawString(50,520, "Saldo Por Comprometer: $")
            p.drawString(195,520, str(float(datos.comprometer) - float(convenio.valorTotal)))

            p.setFont("Helvetica", 12)
            p.drawString(50,500, "Saldo Por Pagar Sobre Recursos Comprometidos: $")
            p.drawString(330,500, str(float(datos.comprometidos) - float(datos.pagados)))

            p.setFont("Helvetica", 12)
            p.drawString(50,480, "Recursos Pagados: $")
            p.drawString(170,480, str(datos.pagados))

            p.setFont("Helvetica", 12)
            p.drawString(50,460, "Recursos No Comprometidos: $")
            p.drawString(225,460, str(datos.noComprometidos))

            p.setFont("Helvetica", 12)
            p.drawString(50,440, "Recursos No Girados: $")
            p.drawString(180,440, str(datos.noGirados))

            if float(datos.transferidoColciencias) != 0:
                p.setFont("Helvetica", 12)
                p.drawString(50,400, "Valor Transferido Por Colciencias: $")
                p.drawString(245,400, str(datos.transferidoColciencias))

                p.setFont("Helvetica", 12)
                p.drawString(50,380, "Saldo Por Transferir Colciencias: $")
                p.drawString(240,380, str(datos.transferirColciencias))

                p.setFont("Helvetica", 12)
                p.drawString(50,360, "Valor Transferido Por Otras Entidades: $")
                p.drawString(270,360, str(datos.transferidoOtrasEntidades))

                p.setFont("Helvetica", 12)
                p.drawString(50,340, "Saldo De Giros Por Recibir De Otras Entidades: $")
                p.drawString(320,340, str(datos.girosOtrasEntidades))

            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            return response

    datos = {}
    return render_to_response('estado.html',{'datos':datos},context_instance = RequestContext(request))

def verificarTransferencias(request):
    pagos = {}
    siif = {}
    if request.method == 'GET':
        codigo = request.GET.get('codigo','')
        if request.GET.get('boton','') == 'Consultar':
            validarSiif = TransferenciasSiif.objects.filter(convenio = codigo)
            if validarSiif:
                siif = TransferenciasSiif.objects.filter(convenio = codigo)
                siif.order_by('-convenio')
            validarPago = ProgramacionPago.objects.filter(convenio = codigo)
            if validarPago:
                pagos = ProgramacionPago.objects.filter(convenio = codigo)
                pagos.order_by('-convenio')
    return render_to_response('transferencias.html',{'pagos':pagos,'siif':siif},context_instance = RequestContext(request))


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


