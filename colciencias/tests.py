from django.test import TestCase
from django.test import * 
from colciencias.models import *

# Create your tests here.
class OrganizacionTestCase(TestCase):
    def setUp(self):
        Organizacion.objects.create(ID="23",nombre="Intergrupo", NIT="1287654", convenio_FK="23")
       
#

