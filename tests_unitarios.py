# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:31:12 2014

@author: Adrián
"""

"""Fichero de pruebas unitarias. Primero se recogen las pruebas del test de Wilcoxon y a continuación se presentan
las pruebas para los tests no parmétricos de ranking y los tests POST-HOC."""

import unittest
import tests_no_parametricos as tnp
import tests_parametricos as tp

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
signficancia considerado es el más habitual: 0.05."""
class TestWilcoxon(unittest.TestCase):

	def test_resultado(self):
		"""Verfifica si el test aplicado sobre los datos es o no estadísticamente significativo)."""
		datos_devueltos = tnp.wilcoxon_test(datos0, 0.05)
		self.assertEqual(datos_devueltos["resultado"], "True")

	def test_estadistico(self):
		"""Verifica del valor del estadístico."""
		datos_devueltos = tnp.wilcoxon_test(datos0, 0.05)
		self.assertEqual(datos_devueltos["estadistico"], 19)

	def test_rangos_pos(self):
		"""Verifica el valor de la suma de rangos positivos."""
		datos_devueltos = tnp.wilcoxon_test(datos0, 0.05)
		self.assertEqual(datos_devueltos["suma rangos pos"], 86)

	def test_rangos_neg(self):
		"""Verifica el valor de la suma de rangos negativos."""
		datos_devueltos = tnp.wilcoxon_test(datos0, 0.05)
		self.assertEqual(datos_devueltos["suma rangos neg"], 19)

	def test_punto_critico(self):
		"""Verifica que el valor del punto crítico es recogido correctamente de la tabla de Wilcoxon."""
		datos_devueltos = tnp.wilcoxon_test(datos0, 0.05)
		self.assertEqual(datos_devueltos["punto critico"], 21)

	def test_numero_algoritmos(self):
		"""Verifica que se lanza una excepción en caso de que el número de algoritmos sea distinto de 2."""
		self.assertRaises(Exception,tnp.wilcoxon_test,datos1,0.05)

	def test_numero_conjuntos(self):
		"""Verifica que se lanza una excepción en caso de que el número de conjuntos sea menor de 5."""
		self.assertRaises(Exception,tnp.wilcoxon_test,datos2,0.05)

#Datos para relizar las pruebas de los tests no paramétricos de ranking. Los argumentos de estos tests siempre
#son (nombres_algoritmos, matriz_datos, alpha, tipo).
nombres0 = ["PDFC","NNEP","IS-CHC+INN","FH-GBML"]
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
signficancia considerado es el más habitual: 0.05. Para la cuestión de si se trata de
minimizar o maximizar, en todas las pruebas se asume un tipo 0 (minimización) y se crean
dos pruebas adicionales con el tipo 1 para el caso de los nombres y de los rankings, ya
que son los casos en que puede haber variaciones."""
class TestFriedman(unittest.TestCase):

    def test_resultado(self):
		"""Verifica si el test aplicado sobre los datos es o no estadísticamente significativo)."""
		datos_devueltos = tnp.friedman_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["resultado"], "True")

    def test_estadistico(self):
		"""Verifica el valor del estadístico."""
		datos_devueltos = tnp.friedman_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["estadistico"], 16.225)

    def test_p_valor(self):
		"""Verifica el p_valor."""
		datos_devueltos = tnp.friedman_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["p_valor"], 0.00102)

    def test_nombres_tipo0(self):
		"""Verifica el ranking de nombres tratándose del caso de minimizar."""
		datos_devueltos = tnp.friedman_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"])

    def test_nombres_tipo1(self):
		"""Verifica el ranking de nombres tratándose del caso de maximizar."""
		datos_devueltos = tnp.friedman_test(nombres0, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["nombres"], ["PDFC","IS-CHC+INN","NNEP","FH-GBML"])

    def test_ranking_tipo0(self):
		"""Verifica el ranking de valores obtenidos tratándose del caso de minimizar."""
		datos_devueltos = tnp.friedman_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["ranking"], [1.729,2.521,2.521,3.229])

    def test_ranking_tipo1(self):
		"""Verifica el ranking de valores obtenidos tratándose del caso de maximizar."""
		datos_devueltos = tnp.friedman_test(nombres0, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["ranking"], [1.771,2.479,2.479,3.271])


"""TestCase que contiene las pruebas a realizar sobre el test de Iman-Davenport. El nivel 
de signficancia considerado es el más habitual: 0.05. Solo se prueba p_valor y estadístico,
ya que el resto de casos se hacen en Friedman."""
class TestImanDavenport(unittest.TestCase):

    def test_estadistico(self):
		"""Verifica el valor del estadístico."""
		datos_devueltos = tnp.iman_davenport_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["estadistico"], 6.691)

    def test_p_valor(self):
		"""Verifica el p_valor."""
		datos_devueltos = tnp.iman_davenport_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["p_valor"], 0.000497)


"""TestCase que contiene las pruebas a realizar sobre el test de los Rangos Signados de
Friedman. El nivel de signficancia considerado es el más habitual: 0.05. Para la cuestión
de si se trata de minimizar o maximizar, en todas las pruebas se asume un tipo 0 (minimización)
y se crean dos pruebas adicionales con el tipo 1 para el caso de los nombres y de los rankings,
ya que son los casos en que puede haber variaciones."""
class TestFriedmanRangosAlineados(unittest.TestCase):

	def test_resultado(self):
		"""Verifica si el test aplicado sobre los datos es o no estadísticamente significativo)."""
		datos_devueltos = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["resultado"], "True")

	def test_estadistico(self):
		"""Verifica el valor del estadístico."""
		datos_devueltos = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["estadistico"], 22.26)

	def test_p_valor(self):
		"""Verifica el p_valor."""
		datos_devueltos = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["p_valor"], 0.000058)

	def test_nombres_tipo0(self):
		"""Verifica el ranking de nombres tratándose del caso de minimizar."""
		datos_devueltos = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"])

	def test_nombres_tipo1(self):
		"""Verifica el ranking de nombres tratándose del caso de maximizar."""
		datos_devueltos = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["nombres"], ["PDFC","NNEP","IS-CHC+INN","FH-GBML"])

	def test_ranking_tipo0(self):
		"""Verifica el ranking de valores obtenidos tratándose del caso de minimizar."""
		datos_devueltos = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["ranking"], [26.104, 50.021, 50.208, 67.667])

	def test_ranking_tipo1(self):
		"""Verifica el ranking de valores obtenidos tratándose del caso de maximizar."""
		datos_devueltos = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["ranking"], [29.333, 46.792, 46.979, 70.896])


"""TestCase que contiene las pruebas a realizar sobre el test de Quade. El nivel de
signficancia considerado es el más habitual: 0.05. Para la cuestión de si se trata de
minimizar o maximizar, en todas las pruebas se asume un tipo 0 (minimización) y se crean
dos pruebas adicionales con el tipo 1 para el caso de los nombres y de los rankings, ya 
que son los casos en que puede haber variaciones."""
class TestQuade(unittest.TestCase):

	def test_resultado(self):
		"""Verifica si el test aplicado sobre los datos es o no estadísticamente significativo)."""
		datos_devueltos = tnp.quade_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["resultado"], "True")

	def test_estadistico(self):
		"""Verifica el valor del estadístico."""
		datos_devueltos = tnp.quade_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["estadistico"], 11.752)

	def test_p_valor(self):
		"""Verifica el p_valor."""
		datos_devueltos = tnp.quade_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["p_valor"], 0.000003)

	def test_nombres_tipo0(self):
		"""Verifica el ranking de nombres tratándose del caso de minimizar."""
		datos_devueltos = tnp.quade_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"])

	def test_nombres_tipo1(self):
		"""Verifica el ranking de nombres tratándose del caso de maximizar."""
		datos_devueltos = tnp.quade_test(nombres0, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["nombres"], ["PDFC","NNEP","IS-CHC+INN","FH-GBML"])

	def test_ranking_tipo0(self):
		"""Verifica el ranking de valores obtenidos tratándose del caso de minimizar."""
		datos_devueltos = tnp.quade_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(datos_devueltos["ranking"], [1.518,2.408,2.462,3.612])

	def test_ranking_tipo1(self):
		"""Verifica el ranking de valores obtenidos tratándose del caso de maximizar."""
		datos_devueltos = tnp.quade_test(nombres0, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["ranking"], [1.388,2.538,2.592,3.482])


#Datos para relizar las pruebas de los tests no paramétricos de comparación POST-HOC (con método
#de control). Los argumentos de estos tests siempre son (test_principal, nombres, ranking, N, alpha).
nombres2 = ["PDFC","IS-CHC+INN","NNEP","FH-GBML"]
datos5 = [1.7708333333333333, 2.4791666666666665, 2.4791666666666665, 3.2708333333333335]

"""TestCase que contiene las pruebas a realizar sobre el mutitest de Bonferroni-Dunn. El nivel 
de signficancia considerado es el más habitual: 0.05."""
class TestBonferroni_Dunn(unittest.TestCase):

    def test_resultado(self):
    		"""Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
    		datos_devueltos = tnp.bonferroni_dunn_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["resultado"], ['True', 'False', 'False'])
    
    def test_valores_z(self):
    		"""Verifica el valor de los estadisticos correspondientes a las comparaciones."""
    		datos_devueltos = tnp.bonferroni_dunn_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["valores z"], [-4.025, -1.901, -1.901])
    
    def test_p_valores(self):
    		"""Verifica los p_valores."""
    		datos_devueltos = tnp.bonferroni_dunn_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["p_valores"], [5.7e-05, 0.057347, 0.057347])
    
    def test_alpha(self):
    		"""Verifica el valor de alpha."""
    		datos_devueltos = tnp.bonferroni_dunn_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["alpha"], 0.017)
    
    def test_nombres(self):
    		"""Verifica el orden de los nombres de los algoritmos."""
    		datos_devueltos = tnp.bonferroni_dunn_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["nombres"], ['FH-GBML', 'IS-CHC+INN', 'NNEP'])

    def test_metodo_control(self):
		"""Verifica que el método de control es el correcto."""
		datos_devueltos = tnp.bonferroni_dunn_test("friedman", nombres2, datos5, 24, 0.05)
		self.assertEqual(datos_devueltos["metodo de control"], "PDFC")    
    
    def test_p_valores_ajustados(self):
    		"""Verifica los p_valores ajustados."""
    		datos_devueltos = tnp.bonferroni_dunn_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["p_valores ajustados"], [0.000171, 0.172041, 0.172041])


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Holm. El nivel 
de signficancia considerado es el más habitual: 0.05."""
class TestHolm(unittest.TestCase):

    def test_resultado(self):
    		"""Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
    		datos_devueltos = tnp.holm_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["resultado"], ['True', 'False', 'False'])
    
    def test_valores_z(self):
    		"""Verifica el valor de los estadisticos correspondientes a las comparaciones."""
    		datos_devueltos = tnp.holm_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["valores z"], [-4.025, -1.901, -1.901])
    
    def test_p_valores(self):
    		"""Verifica los p_valores."""
    		datos_devueltos = tnp.holm_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["p_valores"], [5.7e-05, 0.057347, 0.057347])
    
    def test_alphas(self):
    		"""Verifica los valores alpha."""
    		datos_devueltos = tnp.holm_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["alphas"], [0.017, 0.025, 0.05])
    
    def test_nombres(self):
    		"""Verifica el orden de los nombres de los algoritmos."""
    		datos_devueltos = tnp.holm_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["nombres"], ['FH-GBML', 'IS-CHC+INN', 'NNEP'])

    def test_metodo_control(self):
		"""Verifica que el método de control es el correcto."""
		datos_devueltos = tnp.holm_test("friedman", nombres2, datos5, 24, 0.05)
		self.assertEqual(datos_devueltos["metodo de control"], "PDFC")    
    
    def test_p_valores_ajustados(self):
    		"""Verifica los p_valores ajustados."""
    		datos_devueltos = tnp.holm_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["p_valores ajustados"], [0.000171, 0.114694, 0.114694])


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Hochberg. El nivel 
de signficancia considerado es el más habitual: 0.05."""
class TestHochberg(unittest.TestCase):

    def test_resultado(self):
    		"""Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
    		datos_devueltos = tnp.hochberg_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["resultado"], ['True', 'False', 'False'])
    
    def test_valores_z(self):
    		"""Verifica el valor de los estadisticos correspondientes a las comparaciones."""
    		datos_devueltos = tnp.hochberg_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["valores z"], [-4.025, -1.901, -1.901])
    
    def test_p_valores(self):
    		"""Verifica los p_valores."""
    		datos_devueltos = tnp.hochberg_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["p_valores"], [5.7e-05, 0.057347, 0.057347])
    
    def test_alphas(self):
    		"""Verifica los valores alpha."""
    		datos_devueltos = tnp.hochberg_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["alphas"], [0.017, 0.025, 0.05])
    
    def test_nombres(self):
    		"""Verifica el orden de los nombres de los algoritmos."""
    		datos_devueltos = tnp.hochberg_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["nombres"], ['FH-GBML', 'IS-CHC+INN', 'NNEP'])

    def test_metodo_control(self):
		"""Verifica que el método de control es el correcto."""
		datos_devueltos = tnp.hochberg_test("friedman", nombres2, datos5, 24, 0.05)
		self.assertEqual(datos_devueltos["metodo de control"], "PDFC")    
    
    def test_p_valores_ajustados(self):
    		"""Verifica los p_valores ajustados."""
    		datos_devueltos = tnp.hochberg_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["p_valores ajustados"], [0.000171, 0.057347, 0.057347])


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Li. El nivel 
de signficancia considerado es el más habitual: 0.05."""
class TestLi(unittest.TestCase):

    def test_resultado(self):
    		"""Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
    		datos_devueltos = tnp.li_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["resultado"], ['True', 'True', 'False'])
    
    def test_valores_z(self):
    		"""Verifica el valor de los estadisticos correspondientes a las comparaciones."""
    		datos_devueltos = tnp.li_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["valores z"], [-4.025, -1.901, -1.901])
    
    def test_p_valores(self):
    		"""Verifica los p_valores."""
    		datos_devueltos = tnp.li_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["p_valores"], [5.7e-05, 0.057347, 0.057347])
    
    def test_nombres(self):
    		"""Verifica el orden de los nombres de los algoritmos."""
    		datos_devueltos = tnp.li_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["nombres"], ['FH-GBML', 'IS-CHC+INN', 'NNEP'])

    def test_metodo_control(self):
		"""Verifica que el método de control es el correcto."""
		datos_devueltos = tnp.li_test("friedman", nombres2, datos5, 24, 0.05)
		self.assertEqual(datos_devueltos["metodo de control"], "PDFC")    
    
    def test_p_valores_ajustados(self):
    		"""Verifica los p_valores ajustados."""
    		datos_devueltos = tnp.li_test("friedman", nombres2, datos5, 24, 0.05)
    		self.assertEqual(datos_devueltos["p_valores ajustados"], [6e-05, 0.057347, 0.057347])


#Datos para relizar las pruebas de los tests no paramétricos de comparación POST-HOC (multitest).
#Los argumentos de estos tests siempre son (test_principal, nombres, ranking, N, alpha).
nombres1 = ["C4.5","1NN","NaiveBayes","Kernel","CN2"]
datos4 = [2.100,3.250,2.200,4.333,3.117]

"""TestCase que contiene las pruebas a realizar sobre el mutitest de Nemenyi (Bonferroni-Dunn
multitest). El nivel de signficancia considerado es el más habitual: 0.05."""
class TestNemenyi(unittest.TestCase):

    def test_resultado(self):
		"""Verifica si los tests aplicados sobre todas las hipótesis (multitest) son o no significativos."""
		datos_devueltos = tnp.nemenyi_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["resultado"], ['True','True','True','True','False','False','False','False','False','False'])

    def test_comparaciones(self):
		"""Verifica la lista de posibles comparaciones (m = K(K-1)/2)."""
		datos_devueltos = tnp.nemenyi_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["comparaciones"], ['C4.5 vs Kernel','NaiveBayes vs Kernel','Kernel vs CN2','C4.5 vs 1NN','1NN vs Kernel','1NN vs NaiveBayes','C4.5 vs CN2','NaiveBayes vs CN2','1NN vs CN2','C4.5 vs NaiveBayes'])

    def test_valores_z(self):
		"""Verifica el valor de los estadisticos correspondientes a las distintas comparaciones."""
		datos_devueltos = tnp.nemenyi_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["valores z"], [-5.47,-5.225,2.979,-2.817,-2.653,2.572,-2.491,-2.246,0.326,-0.245])

    def test_p_valores(self):
		"""Verifica los p_valores."""
		datos_devueltos = tnp.nemenyi_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["p_valores"], [0.0,0.0,0.002896,0.004849,0.007983,0.010112,0.012734,0.024692,0.744589,0.806496])

    def test_alpha(self):
		"""Verifica el valor de alpha."""
		datos_devueltos = tnp.nemenyi_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["alpha"], 0.005)

    def test_p_valores_ajustados(self):
		"""Verifica los p_valores ajustados."""
		datos_devueltos = tnp.nemenyi_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["p_valores ajustados"], [0.0,2e-06,0.028959,0.048488,0.079828,0.101123,0.127337,0.246923,1.0,1.0])


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Holm. El nivel de signficancia
considerado es el más habitual: 0.05."""
class TestHolmMultitest(unittest.TestCase):

    def test_resultado(self):
		"""Verifica si los tests aplicados sobre todas las hipótesis (multitest) son o no significativos."""
		datos_devueltos = tnp.holm_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["resultado"], ['True','True','True','True','True','False','False','False','False','False'])

    def test_comparaciones(self):
		"""Verifica la lista de posibles comparaciones (m = K(K-1)/2)."""
		datos_devueltos = tnp.holm_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["comparaciones"], ['C4.5 vs Kernel','NaiveBayes vs Kernel','Kernel vs CN2','C4.5 vs 1NN','1NN vs Kernel','1NN vs NaiveBayes','C4.5 vs CN2','NaiveBayes vs CN2','1NN vs CN2','C4.5 vs NaiveBayes'])

    def test_valores_z(self):
		"""Verifica el valor de los estadisticos correspondientes a las distintas comparaciones."""
		datos_devueltos = tnp.holm_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["valores z"], [-5.47,-5.225,2.979,-2.817,-2.653,2.572,-2.491,-2.246,0.326,-0.245])

    def test_p_valores(self):
		"""Verifica los p_valores."""
		datos_devueltos = tnp.holm_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["p_valores"], [0.0,0.0,0.002896,0.004849,0.007983,0.010112,0.012734,0.024692,0.744589,0.806496])

    def test_alphas(self):
		"""Verifica los valores alphas."""
		datos_devueltos = tnp.holm_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["alphas"], [0.005,0.006,0.006,0.007,0.008,0.01,0.013,0.017,0.025,0.05])

    def test_p_valores_ajustados(self):
		"""Verifica los p_valores ajustados."""
		datos_devueltos = tnp.holm_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["p_valores ajustados"], [0.0,2e-06,0.023167,0.033941,0.047897,0.050562,0.050935,0.074077,1.0,1.0])


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Hochberg. El nivel de 
signficancia considerado es el más habitual: 0.05."""
class TestHochbergMultitest(unittest.TestCase):

    def test_resultado(self):
		"""Verifica si los tests aplicados sobre todas las hipótesis (multitest) son o no significativos."""
		datos_devueltos = tnp.hochberg_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["resultado"], ['True','True','True','True','True','False','False','False','False','False'])

    def test_comparaciones(self):
		"""Verifica la lista de posibles comparaciones (m = K(K-1)/2)."""
		datos_devueltos = tnp.hochberg_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["comparaciones"], ['C4.5 vs Kernel','NaiveBayes vs Kernel','Kernel vs CN2','C4.5 vs 1NN','1NN vs Kernel','1NN vs NaiveBayes','C4.5 vs CN2','NaiveBayes vs CN2','1NN vs CN2','C4.5 vs NaiveBayes'])

    def test_valores_z(self):
		"""Verifica el valor de los estadisticos correspondientes a las distintas comparaciones."""
		datos_devueltos = tnp.hochberg_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["valores z"], [-5.47,-5.225,2.979,-2.817,-2.653,2.572,-2.491,-2.246,0.326,-0.245])

    def test_p_valores(self):
		"""Verifica los p_valores."""
		datos_devueltos = tnp.hochberg_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["p_valores"], [0.0,0.0,0.002896,0.004849,0.007983,0.010112,0.012734,0.024692,0.744589,0.806496])

    def test_alphas(self):
		"""Verifica los valores alphas."""
		datos_devueltos = tnp.hochberg_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["alphas"], [0.005,0.006,0.006,0.007,0.008,0.01,0.013,0.017,0.025,0.05])

    def test_p_valores_ajustados(self):
		"""Verifica los p_valores ajustados."""
		datos_devueltos = tnp.hochberg_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["p_valores ajustados"], [0.0,2e-06,0.023167,0.033941,0.047897,0.050562,0.050935,0.074077,0.806496,0.806496])


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Li. El nivel de 
signficancia considerado es el más habitual: 0.05."""
class TestLiMultitest(unittest.TestCase):

    def test_resultado(self):
		"""Verifica si los tests aplicados sobre todas las hipótesis (multitest) son o no significativos."""
		datos_devueltos = tnp.li_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["resultado"], ['True','True','True','True','True','True','True','True','True','False'])

    def test_comparaciones(self):
		"""Verifica la lista de posibles comparaciones (m = K(K-1)/2)."""
		datos_devueltos = tnp.li_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["comparaciones"], ['C4.5 vs Kernel','NaiveBayes vs Kernel','Kernel vs CN2','C4.5 vs 1NN','1NN vs Kernel','1NN vs NaiveBayes','C4.5 vs CN2','NaiveBayes vs CN2','1NN vs CN2','C4.5 vs NaiveBayes'])

    def test_valores_z(self):
		"""Verifica el valor de los estadisticos correspondientes a las distintas comparaciones."""
		datos_devueltos = tnp.li_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["valores z"], [-5.47,-5.225,2.979,-2.817,-2.653,2.572,-2.491,-2.246,0.326,-0.245])

    def test_p_valores(self):
		"""Verifica los p_valores."""
		datos_devueltos = tnp.li_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["p_valores"], [0.0,0.0,0.002896,0.004849,0.007983,0.010112,0.012734,0.024692,0.744589,0.806496])

    def test_p_valores_ajustados(self):
		"""Verifica los p_valores ajustados."""
		datos_devueltos = tnp.li_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["p_valores ajustados"], [0.0,1e-06,0.014745,0.024445,0.039619,0.049664,0.061743,0.113166,0.793726,0.806496])


#Datos para relizar las pruebas de los tests paramétricos ANOVA y Bonferroni POST-HOC (multitest).
#Los argumentos para el test de ANOVA son (matriz_datos, alpha).
#Para el test de Bonferroni son (nombres_algoritmos, medias_algoritmos, cuadrado_medio_error, N, alpha)
nombres3 = ["A","B","C"]
datos6 = [[27,21,25],[31,33,35],[42,39,39],[38,41,37],[45,46,45]]

"""TestCase que contiene las pruebas a realizar sobre el test ANOVA. El nivel de
signficancia considerado es el más habitual: 0.05."""
class TestAnova(unittest.TestCase):

	def test_resultado(self):
		"""Verifica si el test aplicado sobre los datos es o no estadísticamente significativo)."""
		datos_devueltos = tp.anova_test(datos6, 0.05)
		self.assertEqual(datos_devueltos["resultado"], "False")

	def test_estadistico(self):
		"""Verifica el valor del estadístico."""
		datos_devueltos = tp.anova_test(datos6, 0.05)
		self.assertEqual(round(datos_devueltos["estadistico"],3), 0.007)

	def test_p_valor(self):
		"""Verifica el p_valor."""
		datos_devueltos = tp.anova_test(datos6, 0.05)
		self.assertEqual(round(datos_devueltos["p_valor"],6), 0.993080)

	def test_variaciones(self):
		"""Verifica los valores de las variaciones total, tratamiento y error (SCT, SCTR, SCE)."""
		datos_devueltos = tp.anova_test(datos6, 0.05)
		self.assertEqual([round(valor,3) for valor in datos_devueltos["variaciones"]], [806.933,0.933,806.000])

	def test_grados_libertad(self):
		"""Verifica los valores de los grados de libertad (GLT, GLTR, GLE)."""
		datos_devueltos = tp.anova_test(datos6, 0.05)
		self.assertEqual(datos_devueltos["grados_libertad"], [14,2,12])

	def test_cuadrados_medios(self):
		"""Verifica los valores de los cuadrados medios (CMT, CMTR, CME)."""
		datos_devueltos = tp.anova_test(datos6, 0.05)
		self.assertEqual([round(valor,3) for valor in datos_devueltos["cuadrados_medios"]], [57.638,0.467,67.167])

	def test_medias_algoritmos(self):
		"""Verifica las medias de los K tratamientos o algoritmos."""
		datos_devueltos = tp.anova_test(datos6, 0.05)
		self.assertEqual([round(valor,3) for valor in datos_devueltos["medias_algoritmos"]], [36.600,36.000,36.200])

	def test_media_general(self):
		"""Verifica la media general (media de medias de los tratamientos o algoritmos)."""
		datos_devueltos = tp.anova_test(datos6, 0.05)
		self.assertEqual(round(datos_devueltos["media_general"],3), 36.267)


"""TestCase que contiene las pruebas a realizar sobre el test POST-HOC Bonferroni. El nivel de
signficancia considerado es el más habitual: 0.05."""
class TestBonferroni(unittest.TestCase):

    def test_resultado(self):
    		"""Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
    		datos_devueltos = tp.bonferroni_test(nombres3, [36.600,36.000,36.200], 67.167, 5, 0.05)
    		self.assertEqual(datos_devueltos["resultado"], ['False', 'False', 'False'])
    
    def test_valores_t(self):
    		"""Verifica el valor de los estadisticos correspondientes a las comparaciones."""
    		datos_devueltos = tp.bonferroni_test(nombres3, [36.600,36.000,36.200], 67.167, 5, 0.05)
    		self.assertEqual([round(valor,3) for valor in datos_devueltos["valores_t"]], [0.116,0.077,0.039])
    
    def test_p_valores(self):
    		"""Verifica los p_valores."""
    		datos_devueltos = tp.bonferroni_test(nombres3, [36.600,36.000,36.200], 67.167, 5, 0.05)
    		self.assertEqual([round(valor,6) for valor in datos_devueltos["p_valores"]], [0.454880,0.469880,0.484928])
    
    def test_alpha(self):
    		"""Verifica el valor de alpha."""
    		datos_devueltos = tp.bonferroni_test(nombres3, [36.600,36.000,36.200], 67.167, 5, 0.05)
    		self.assertEqual(round(datos_devueltos["alpha"],3), 0.017)
    
    def test_comparaciones(self):
    		"""Verifica la lista de posibles comparaciones (m = K(K-1)/2)."""
    		datos_devueltos = tp.bonferroni_test(nombres3, [36.600,36.000,36.200], 67.167, 5, 0.05)
    		self.assertEqual(datos_devueltos["comparaciones"], ['A vs B','A vs C','B vs C'])
    
    def test_p_valores_ajustados(self):
    		"""Verifica los p_valores ajustados."""
    		datos_devueltos = tp.bonferroni_test(nombres3, [36.600,36.000,36.200], 67.167, 5, 0.05)
    		self.assertEqual(datos_devueltos["p_valores_ajustados"], [1,1,1])


if __name__ == '__main__':
    unittest.main()
