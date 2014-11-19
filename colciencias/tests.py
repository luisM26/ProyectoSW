from django.test import TestCase
from colciencias.models import *
from selenium import webdriver
from django.core.urlresolvers import reverse
from selenium.webdriver.support.ui import Select
from datetime import datetime

class test(TestCase):

	def setUp(self):
	  a = ConvenioSol.objects.create(numConvenio="1",nombre="convenio1",estado="aprobado",valorTotal = "1000",supervisor = "juan")
	  b = ConvenioSol.objects.create(numConvenio="2",nombre="convenio2",estado="legalizado",valorTotal = "3000",supervisor = "beto")
	  c = Ffjc.objects.create(ID="1", fecha=datetime.now(),valor = "20000")
	  d = Ffjc.objects.create(ID="2", fecha=datetime.now(),valor = "50000")
	  e = Giro.objects.create(ID="1", num="7",fecha=datetime.now(),numSol="3",valor = "40000")
	  f = Giro.objects.create(ID="2", num="8",fecha=datetime.now(),numSol="4",valor = "80000")
	  # g = Proyecto.objects.create(ID="1",duracion="20",lugarEjecucion="cali",estado="aprobado")
	  # h = Proyecto.objects.create(ID="2",duracion="60",lugarEjecucion="medellin",estado="no aprobado")
	  # i = Organizacion.objects.create(ID="1",nombre="ecopetrol",NIT="12")
	  # j = Organizacion.objects.create(ID="2",nombre="cooficafe",NIT="100")
	  # k = Proforma.objects.create(ID="1",fechaCargue=datetime.now(),descripcion="descripcion")
	  # l = Proforma.objects.create(ID="2",fechaCargue=datetime.now(),descripcion="otra descripcion")

	def testCrearNovedad(self):
		convenio = ConvenioSol.objects.get(estado="aprobado")
		convenio1 = ConvenioSol.objects.get(nombre="convenio2")
		centinela = False

		if convenio1.estado == "legalizado":
			centinela = True

		self.assertEqual(convenio.supervisor,"juan")
		self.assertEqual(centinela,True)

	def testProgramarGiros(self):
		giro = Giro.objects.get(numSol="3")
		giro1 = Giro.objects.get(ID="2")
		centinela = False

		if giro1.numSol == "4":
			centinela = True

		self.assertEqual(giro.valor,"40000")
		self.assertEqual(centinela,True)

	def testActualizarDatos(self):
		ffjc = Ffjc.objects.get(ID="2")
		ffjc1 = Ffjc.objects.get(ID="1")

		self.assertEqual(ffjc.valor,"50000")
		self.assertEqual(ffjc1.valor,"20000")

	# def testSolicitarCdr(sef):
	# 	proforma = Proforma.objects.get(ID="1")
	# 	Proforma1 = Proforma.objects.get(descripcion="otra descripcion")

	# 	self.assertEqual(proforma.descripcion,"descripcion")
	# 	self.assertEqual(Proforma1.ID,"2")


	# def setUp(self):
	# 	 Orgonanizacion.objects.create('ID'="1", 'nombre'= "LION", 'NIT'="123456", 'convenio_FK'="1", 'valor'="4567")


	# def test_Organizaciones_Creadas(self):
 #        lion = Orgonanizacion.objects.get(nombre="lion")
	# def setUp(self):
	# 	self.driver = webdriver.Firefox()

	# def testEstadoCuenta(self):
 #   		self.driver.get("http://localhost:8000/estado/")
 #   		self.driver.maximize_window()
   		
 #   		select = Select(self.driver.find_element_by_name("tipo"))
 #   		select.select_by_index(1)

 #   		self.driver.find_element_by_id('id_codigo').send_keys("2")
	# 	self.driver.find_element_by_id('id_consultar').click()
	# 	response = self.client.get('/')
	# 	self.assertEqual(response.status_code, 200)

	# # def testGenerarPdf(self):
	# # 	self.driver.get("http://localhost:8000/estado/")
	# # 	self.driver.maximize_window()

	# # 	select = Select(self.driver.find_element_by_name("tipo"))
	# # 	select.select_by_index(1)

	# # 	self.driver.find_element_by_id('id_codigo').send_keys("2")
		
 # #   		self.driver.find_element_by_id('id_consultar').click()
	# # 	self.driver.find_element_by_id('pdf').click()
	# # 	response = self.client.get('/')
	# # 	self.assertEqual(response.status_code, 200)

	# def testVerificarTransferencia(self):
	# 	self.driver.get("http://localhost:8000/verificarTransferencias/")
	# 	self.driver.maximize_window()
	# 	self.driver.find_element_by_id('id_codigo').send_keys("1")
	# 	self.driver.find_element_by_id('id_consultar').click()
	# 	response = self.client.get('/')
	# 	self.assertEqual(response.status_code, 200)

	# def tearDown(self):
	# 	self.driver.quit

