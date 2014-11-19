#
from django import forms
from django.forms import ModelForm
from colciencias.models import *	

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class OrganizacionForm(ModelForm):
    class Meta:
        model = Organizacion
      	convenio='convenio_FK'
        fields = ('ID','nombre', 'NIT', convenio, 'valor')
      #  exclude = ["numConvenio", "nombre","tipoConvenio", "RP", "proyectoInversion_FK" , "fechaInicio", "fechaSuscripcion", "fechaLegalizacion", "fechaFInalizacion","areaResponsable","supervisor","plazo", "objeto"]



class ProformaForm(ModelForm):
    class Meta:
        model = Proforma
        fields =  ('ID','fechaCargue','descripcion','archivo')


class AnexoForm(ModelForm):
    class Meta:
        model = Anexo
        fields =  ('ID','fechaCargue','descripcion','archivo','convenio_FK')
