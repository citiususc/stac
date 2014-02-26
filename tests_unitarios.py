# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:31:12 2014

@author: Adrián
"""

"""Fichero de pruebas unitarias. Primero se recogen las pruebas del test de Wilcoxon y a continuación se presentan
las pruebas para los tests no parmétricos de ranking."""

import unittest
from .tests_no_parametricos import wilcoxon_test, friedman_test, iman_davenport_test, friedman_rangos_alineados_test

#Datos para relizar las pruebas del test de Wilcoxon. Los argumentos del test son (matriz_datos, alpha).
#Caso normal N<25 y >= 5 y número de algoritmos = 2.
datos0 = [[78,78],
[24,24],
[64,62],
[45,48],
[64,68],
[52,56],
[30,25],
[50,44],
[64,56],
[50,40],
[78,68],
[22,36],
[84,68],
[40,20],
[90,58],
[72,32]]
#Caso anormal número de algoritmos > 2.
datos1 = [[78,78,0],
[24,24,0],
[64,62,0],
[45,48,0],
[64,68,0],
[52,56,0],
[30,25,0],
[50,44,0],
[64,56,0],
[50,40,0],
[78,68,0],
[22,36,0],
[84,68,0],
[40,20,0],
[90,58,0],
[72,32,0]]
#Caso anormal número de conjuntos de datos sin ligaduras < 5.
datos2 = [[78,78],
[24,24],
[64,62],
[45,48]]

"""TestCase que contiene las pruebas a realizar sobre el test de Wilcoxon. El nivel de
signficancia considerado es el más habitual: 0.05. Se asume que si las pruebas no fallan
ocurrirá lo mismo con otros niveles de significancia."""
class TestWilcoxon(unittest.TestCase):

	def test_resultado(self):
		"""Prueba para verfificar el resultado obtenido (si el test aplicado sobre los datos
		es o no estadísticamente significativo)."""
		datos_devueltos = wilcoxon_test(datos0, 0.05)
		self.assertEqual(datos_devueltos["resultado"], "True")

	def test_estadistico(self):
		"""Prueba para verificar del valor del estadístico."""
		datos_devueltos = wilcoxon_test(datos0, 0.05)
		self.assertEqual(datos_devueltos["estadistico"], 19)

	def test_rangos_pos(self):
		"""Prueba para verificar el valor de la suma de rangos positivos."""
		datos_devueltos = wilcoxon_test(datos0, 0.05)
		self.assertEqual(datos_devueltos["suma rangos pos"], 86)

	def test_rangos_neg(self):
		"""Prueba para verificar el valor de la suma de rangos negativos."""
		datos_devueltos = wilcoxon_test(datos0, 0.05)
		self.assertEqual(datos_devueltos["suma rangos neg"], 19)

	def test_punto_critico(self):
		"""Prueba para verificar que el valor del punto crítico es recogido correctamente
		del diccionario con la tabla de Wilcoxon."""
		datos_devueltos = wilcoxon_test(datos0, 0.05)
		self.assertEqual(datos_devueltos["punto critico"], 21)

	def test_numero_algoritmos(self):
		"""Prueba para verificar que se devuelve fallo en caso de que el número de
		algoritmos sea distinto de 2, en cuyo caso el valor devuelto será un diccionario
		con la clave fallo."""
		datos_devueltos = wilcoxon_test(datos1, 0.05)
		self.assertDictEqual(datos_devueltos, {"fallo" : "Test de Wilcoxon solo aplicable a dos algoritmos"})

	def test_numero_conjuntos(self):
		"""Prueba para verificar que se devuelve fallo en caso de que el número de
		conjuntos sea menor de 5, en cuyo caso el valor devuelto será un diccionario
		con la clave fallo."""
		datos_devueltos = wilcoxon_test(datos2, 0.05)
		self.assertDictEqual(datos_devueltos, {"fallo" : "Menos de 5 conjuntos de datos sin ligaduras"})

#Datos para relizar las pruebas de los tests no paramétricos de ranking. Los argumentos de estos tests siempre
#son (nombres_algoritmos, matriz_datos, alpha, tipo)
nombres = ["PDFC","NNEP","IS-CHC+INN","FH-GBML"]
datos3 = [[0.752,0.773,0.785,0.795],
[0.727,0.748,0.724,0.713],
[0.736,0.716,0.585,0.638],
[0.994,0.861,0.880,0.791],
[0.508,0.553,0.575,0.515],
[0.535,0.536,0.513,0.471],
[0.967,0.871,0.954,0.532],
[0.831,0.807,0.819,0.768],
[0.745,0.702,0.719,0.705],
[0.709,0.572,0.669,0.607],
[0.722,0.728,0.725,0.732],
[0.967,0.947,0.953,0.960],
[0.832,0.752,0.802,0.691],
[0.998,0.992,0.482,0.910],
[0.963,0.963,0.954,0.926],
[0.982,0.953,0.932,0.630],
[0.978,0.773,0.834,0.849],
[0.854,0.787,0.841,0.779],
[0.965,0.984,0.995,0.947],
[0.924,0.887,0.861,0.804],
[0.929,0.942,0.931,0.921],
[0.837,0.643,0.602,0.554],
[0.972,0.956,0.944,0.922],
[0.958,0.959,0.964,0.964]]

"""TestCase que contiene las pruebas a realizar sobre el test de Friedman. El nivel de
signficancia considerado es el más habitual: 0.05. Se asume que si las pruebas no fallan
ocurrirá lo mismo con otros niveles de significancia. Para la cuestión de si se trata de
minimizar o maximizar, en todas las pruebas se asume un tipo 0 (minimización) y se crean
dos pruebas adicionales con el tipo 1 para el caso de los nombres y de los rankings, ya
que son los casos en que puede haber variaciones."""
class TestFriedman(unittest.TestCase):

    def test_resultado(self):
		"""Prueba para verfificar el resultado obtenido (si el test aplicado sobre los datos
		es o no estadísticamente significativo)."""
		datos_devueltos = friedman_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["resultado"], "True")

    def test_estadistico(self):
		"""Prueba para verificar del valor del estadístico."""
		datos_devueltos = friedman_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["estadistico"], 16.225)

    def test_p_valor(self):
		"""Prueba para verificar el p_valor."""
		datos_devueltos = friedman_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["p_valor"], 0.00102)

    def test_nombres_tipo0(self):
		"""Prueba para verificar el ranking de nombres tratándose del caso de
		minimizar."""
		datos_devueltos = friedman_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"])

    def test_nombres_tipo1(self):
		"""Prueba para verificar el ranking de nombres tratándose del caso de
		maximizar."""
		datos_devueltos = friedman_test(nombres, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["nombres"], ["PDFC","IS-CHC+INN","NNEP","FH-GBML"])

    def test_ranking_tipo0(self):
		"""Prueba para verificar el ranking de valores obtenidos tratándose del caso de
		minimizar."""
		datos_devueltos = friedman_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["ranking"], [1.729,2.521,2.521,3.229])

    def test_ranking_tipo1(self):
		"""Prueba para verificar el ranking de valores obtenidos tratándose del caso de
		maximizar."""
		datos_devueltos = friedman_test(nombres, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["ranking"], [1.771,2.479,2.479,3.271])


"""TestCase que contiene las pruebas a realizar sobre el test de Iman-Davenport. El nivel 
de signficancia considerado es el más habitual: 0.05. Se asume que si las pruebas no
fallan ocurrirá lo mismo con otros niveles de significancia. Solo se prueba p_valor y
estadístico, ya que el resto de casos se hacen en Friedman."""
class TestImanDavenport(unittest.TestCase):

    def test_estadistico(self):
		"""Prueba para verificar del valor del estadístico."""
		datos_devueltos = iman_davenport_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["estadistico"], 6.691)

    def test_p_valor(self):
		"""Prueba para verificar el p_valor."""
		datos_devueltos = iman_davenport_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["p_valor"], 0.000497)


"""TestCase que contiene las pruebas a realizar sobre el test de los Rangos Signados de
Friedman. El nivel de signficancia considerado es el más habitual: 0.05. Se asume que si
las pruebas no fallan ocurrirá lo mismo con otros niveles de significancia. Para la 
cuestión de si se trata de minimizar o maximizar, en todas las pruebas se asume un 
tipo 0 (minimización) y se crean dos pruebas adicionales con el tipo 1 para el caso de 
los nombres y de los rankings, ya que son los casos en que puede haber variaciones."""
class TestFriedmanRangosAlineados(unittest.TestCase):

	def test_resultado(self):
		"""Prueba para verfificar el resultado obtenido (si el test aplicado sobre los datos
		es o no estadísticamente significativo)."""
		datos_devueltos = friedman_rangos_alineados_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["resultado"], "True")

	def test_estadistico(self):
		"""Prueba para verificar del valor del estadístico."""
		datos_devueltos = friedman_rangos_alineados_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["estadistico"], 22.26)

	def test_p_valor(self):
		"""Prueba para verificar el p_valor."""
		datos_devueltos = friedman_rangos_alineados_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["p_valor"], 0.000058)

	def test_nombres_tipo0(self):
		"""Prueba para verificar el ranking de nombres tratándose del caso de
		minimizar."""
		datos_devueltos = friedman_rangos_alineados_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"])

	def test_nombres_tipo1(self):
		"""Prueba para verificar el ranking de nombres tratándose del caso de
		maximizar."""
		datos_devueltos = friedman_rangos_alineados_test(nombres, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["nombres"], ["PDFC","NNEP","IS-CHC+INN","FH-GBML"])

	def test_ranking_tipo0(self):
		"""Prueba para verificar el ranking de valores obtenidos tratándose del caso de
		minimizar."""
		datos_devueltos = friedman_rangos_alineados_test(nombres, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["ranking"], [26.104, 50.021, 50.208, 67.667])

	def test_ranking_tipo1(self):
		"""Prueba para verificar el ranking de valores obtenidos tratándose del caso de
		maximizar."""
		datos_devueltos = friedman_rangos_alineados_test(nombres, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["ranking"], [29.333, 46.792, 46.979, 70.896])

if __name__ == '__main__':
	unittest.main()

