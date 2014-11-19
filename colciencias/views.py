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
from forms import *
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import EmailMultiAlternatives
from datetime import datetime

import os
#dsd
codigo = 0
tipo = ''


# Este metodo permite
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
    if request.method == 'POST':
        codigo = request.POST.get('codigo','')
        if request.POST.get('boton','') == 'Consultar':
            validarSiif = TransferenciasSiif.objects.filter(convenio = codigo)
            if validarSiif:
                siif = TransferenciasSiif.objects.filter(convenio = codigo)
                siif.order_by('-entidad')
            validarPago = ProgramacionPago.objects.filter(convenio = codigo)
            if validarPago:
                pagos = ProgramacionPago.objects.filter(convenio = codigo)
                pagos.order_by('-entidad')
    return render_to_response('transferencias.html',{'pagos':pagos,'siif':siif},context_instance = RequestContext(request))

def cdr(request):
    if request.method == 'GET':
        

        if request.GET.get('boton','') == 'Consultar CDR':
            global codigo
            codigo = request.GET.get('ID','')
            
            datos = Proyecto.objects.filter(ID = codigo)
            # send_mail('Este mensaje es para decir que django ', 'Here is the message.', 'from@example.com',
            # ['camilo.28.tef@gmail.com'], fail_silently=False)
            # correo = EmailMessage("titulo", "contenido", to=['camilo.28.sec@gmail.com'])
            # correo.send()
            return render_to_response('estadoCDR.html',{'datos':datos},context_instance = RequestContext(request))

        if request.GET.get('boton','') == 'Registrar':
            return HttpResponseRedirect('/add/')

        if request.GET.get('boton','') == 'Imprimir':
            
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="CDR.pdf"'

            # Create the PDF object, using the response object as its "file."
            p = canvas.Canvas(response)

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # datos = Organizacion.objects.get(convenio_FK = codigo)
            convenio = Proyecto.objects.get(ID =codigo)
            imagen = os.path.realpath(os.path.dirname(__file__))
            p.drawImage(imagen + "/Imagenes/logo.png",50,750,width=200, height=50)

            p.setFont("Helvetica-Bold", 16)
            p.drawString(210, 700, "Informe Estado de Cuenta")

            p.setFont("Helvetica", 12)
            p.drawString(50,660, "Numero de Convenio: ")
            p.drawString(170,660, convenio.titulo)
            # p.drawString(50,660, "Numero de Proyecto: ")
            # p.drawString(170,660, convenio.duracion)
           
            p.showPage()
            p.save()
            return response
            
    datos = {}
    return render_to_response('estadoCDR.html',{'datos':datos},context_instance = RequestContext(request))    

def inicio(request):
    return render_to_response('index.html', context_instance = RequestContext(request))
    
def formulario(request):
    if request.method=='POST':
        formulario= OrganizacionForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
        return HttpResponseRedirect('/CDR')
    else:
        formulario = OrganizacionForm()
    return render_to_response('cdrs.html',{'formulario':formulario}, context_instance=RequestContext(request))

def formularioPro(request):
    if request.method=='POST':
        formulario= ProformaForm(request.POST, request.FILES)
        subject = 'Nueva Proforma agregada'
        text_content = 'Por favor ver la nueva proforma'
        html_content = '<h2>Proforma</2><p>Se ha adjuntado una nueva proforma al sistema por favor verificar<br>Sistema Colciencas 2014 </p>'
        from_email = '"origen" <infocolciencia@gmail.com>'
        to = 'camilo.28.sec@gmail.com'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()              
        if formulario.is_valid():
            formulario.save()
           
        return HttpResponseRedirect('/')
    else:
        formulario = ProformaForm()
    return render_to_response('proforma.html',{'formulario':formulario}, context_instance=RequestContext(request))

def expedir_cdr(request):
    cdrs = {}
    siif = {}
    if request.method == 'POST':
        
        if request.POST.get('boton','') == 'Consultar':
                cdrs = CDR.objects.filter(validado = True)

        if request.POST.get('boton','') == 'Imprimir': 

            codigo = request.POST.get('ID','')
            cdr = CDR.objects.get(ID =codigo)
            if int(cdr.organizacion.valor) != 0:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="CDR.pdf"'

                # Create the PDF object, using the response object as its "file."
                p = canvas.Canvas(response)

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                cdr = CDR.objects.get(ID =codigo)
                # datos = Organizacion.objects.get(convenio_FK = codigo)
                imagen = os.path.realpath(os.path.dirname(__file__))
                p.drawImage(imagen + "/Imagenes/logo.png",50,750,width=200, height=50)

                p.setFont("Helvetica-Bold", 16)
                p.drawString(210, 700, "Informe Estado de Cuenta")

                p.setFont("Helvetica", 12)
                p.drawString(50,660, "Numero de Convenio: ")
                p.drawString(170,660, cdr.ID)

                p.setFont("Helvetica", 12)
                p.drawString(50,640, "Nombre del Convenio: ")
                p.drawString(173,640, cdr.Proforma.ID)

                p.setFont("Helvetica", 12)
                p.drawString(50,620, "Fecha Inicio: $")
                p.drawString(132,620, str( cdr.Convenio.valorTotal))
                p.showPage()
                p.save()
                return response
        # return render_to_response('expedir_CDR.html',{'datos':datos},context_instance = RequestContext(request))
    return render_to_response('expedir_CDR.html',{'pagos':cdrs},context_instance = RequestContext(request))
           
def gestionarConvenioEnSolicitud(request):
    if request.method == 'POST':
        if request.POST.get('boton','') == 'Aceptar':
            datos = []
            i = 1
            while(i != (float(request.POST.get('org',''))+1)):
                datos.append(i)
                i = i + 1
            return render_to_response('gestionarSolicitud.html',{'datos':datos},context_instance = RequestContext(request))

        if request.POST.get('boton','') == 'Registrar':
            num = request.POST.get('num','')
            fecha = datetime.now()
            numInver = request.POST.get('numInv','')
            anio = request.POST.get('anio','')
            numRp = request.POST.get('numrp','')
            fechaRp = request.POST.get('fechaRp','')
            valorTotal = float(request.POST.get('total',''))
            valorPorOrg = request.POST.get('discri','')
            registro = ConvenioSol(numConvenio = num,valorTotal=valorTotal,RP=numRp)
            registro.save()
            return render_to_response('gestionarSolicitud.html',context_instance = RequestContext(request))

        if request.POST.get('boton','') == 'Guardar':
            valor = request.POST.get('valor','')
            numOrd = request.POST.get('numOr','')
            fecha = request.POST.get('fechaGir','')
            numSol = request.POST.get('numSol','')
            registro = Giro(valor=valor,numSol=numSol,num=numOrd)
            registro.save()

            ffjc = request.POST.get('ffjc','')

            if ffjc == 'colciencias':
                fecha = request.POST.get('fechaffjc','')
                valor = request.POST.get('valorRec','')
                pdf = request.POST.get('filePdf','')
                regis = Ffjc(valor=valor)
                regis.save()


    return render_to_response('gestionarSolicitud.html',context_instance = RequestContext(request))

def gestionarConvenioRegistro(request):
    if request.method == 'POST':
        if request.POST.get('boton','') == 'Registrar':
            num = request.POST.get('numCon','')
            objeto = request.POST.get('objeto','')
            valor = float(request.POST.get('valor',''))
            fechaSus = request.POST.get('fechaSus','')
            fechaLeg = request.POST.get('fechaLeg','')
            fechaIni = request.POST.get('fechaIni','')
            fechaFin = request.POST.get('fechaFin','')
            plazo = request.POST.get('plazo','')
            area = request.POST.get('area','')
            supervisor = request.POST.get('supervisor','')
            pdf = request.POST.get('file','')
            registro = ConvenioSol(numConvenio=num,valorTotal=valor,areaResponsable=area,supervisor=supervisor
                ,objeto=objeto)
            registro.save()

    return render_to_response('gestionarRegistro.html',context_instance = RequestContext(request))
    
def formularioAnexo(request):
    if request.method=='POST':
        formulario3= AnexoForm(request.POST, request.FILES)
        if formulario3.is_valid():
            formulario3.save()
        return HttpResponseRedirect('/')
    else:
        formulario3 = AnexoForm()
    return render_to_response('anexo.html',{'formulario3':formulario3}, context_instance=RequestContext(request))

def programarDesembolso(request):
    cdrs = {}
    exa={} 
    if request.method == 'POST':
        
        if request.POST.get('boton','') == 'Consultar':
               cdrs = Convocatoria.objects.filter(validado = True)

        return render_to_response('Desembolsos.html',{'pagos':cdrs},context_instance = RequestContext(request))
        
        if request.POST.get('boton','') == 'ir':
            codigo= request.POST.get('codigo','')
            exa = Convocatoria.objects.filter(ID = codigo)
        return render_to_response('Desembolsos.html',{'pagos':exa},context_instance = RequestContext(request))   

        if request.POST.get('boton','') == 'Aceptar':
            datos = []
            i = 1
            while(i != (float(request.POST.get('desem',''))+1)):
                datos.append(i)
                i = i + 1
            return render_to_response('Desembolsos.html',{'pagos':cdrs,'datos':datos},context_instance = RequestContext(request))
    
        if request.POST.get('boton','') == 'Registrar':
            num = request.POST.get('numrp','')
            fecha = request.POST.get('fecha','')
            valorTotal = float(request.POST.get('total',''))
            condicion= request.POST.get('cond','')
            registro = Desembolso(ID = num,fechaSolicitud=fecha,valor=valorTotal, condiciones= condicion)
            registro.save()
        return render_to_response('Desembolsos.html',context_instance = RequestContext(request))
    return render_to_response('Desembolsos.html',{'pagos':cdrs},context_instance = RequestContext(request))