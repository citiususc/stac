# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:31:12 2014

@author: Adrián
"""

"""Fichero de pruebas unitarias. Primero se recogen las pruebas del test de Wilcoxon y a continuación se presentan
las pruebas para los tests no parmétricos de ranking, los tests POST-HOC y los tests paramétricos."""


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

	def test_resultado_wilcoxon(self):
		"""Verifica el resultado de la aplicación del test de Wilcoxon."""
		datos_devueltos = tnp.wilcoxon_test(datos0, 0.05)
		self.assertTrue(datos_devueltos["resultado"], "Error resultado")
		self.assertEqual(datos_devueltos["estadistico"], 19, "Error estadistico")
		self.assertEqual(datos_devueltos["suma rangos pos"], 86, "Error suma rangos positivos")
		self.assertEqual(datos_devueltos["suma rangos neg"], 19, "Error suma rangos negativos")
		self.assertEqual(datos_devueltos["punto critico"], 21, "Error punto crítico")

	def test_resultado_wilcoxon1(self):
		"""Verifica Exception en caso de que el número de algoritmos sea distinto de 2"""
		self.assertRaises(Exception,tnp.wilcoxon_test,datos1,0.05)

	def test_resultado_wilcoxon2(self):
		"""Verifica Exception en caso de que el número de conjuntos sea menor de 5"""
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
signficancia considerado es el más habitual: 0.05. Para la cuestión de si se trata de minimizar
o maximizar se considera un tipo 0 (minimización) y se crea una prueba adicional con el tipo 1
para el caso de los nombres y de los rankings, ya que es donde variaría el resultado."""
class TestFriedman(unittest.TestCase):

    def test_resultado_friedman(self):
		"""Verifica el resultado de la aplicación del test de Friedman."""
		datos_devueltos = tnp.friedman_test(nombres0, datos3, 0.05, 0)
		self.assertTrue(datos_devueltos["resultado"], "Error resultado")
		self.assertEqual(round(datos_devueltos["estadistico"],3), 16.225, "Error estadistico")
		self.assertEqual(round(datos_devueltos["p_valor"],3), 0.001, "Error p_valor")
		self.assertEqual(datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"], "Error ranking nombres")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["ranking"]], [1.729,2.521,2.521,3.229], "Error ranking numerico")

    def test_resultado_friedman_tipo1(self):
		"""Verifica el ranking de nombres y valores tratándose del caso de maximizar."""
		datos_devueltos = tnp.friedman_test(nombres0, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["nombres"], ["PDFC","IS-CHC+INN","NNEP","FH-GBML"], "Error ranking nombres")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["ranking"]], [1.771,2.479,2.479,3.271], "Error ranking numerico")


"""TestCase que contiene las pruebas a realizar sobre el test de Iman-Davenport. El nivel 
de signficancia considerado es el más habitual: 0.05. Solo se prueba p_valor y estadístico,
ya que son los valores que varían respecto a Friedman."""
class TestImanDavenport(unittest.TestCase):

    def test_resultado_iman_davenport(self):
		"""Verifica el valor del estadístico y el p_valor."""
		datos_devueltos = tnp.iman_davenport_test(nombres0, datos3, 0.05, 0)
		self.assertEqual(round(datos_devueltos["estadistico"],3), 6.691)
		self.assertEqual(round(datos_devueltos["p_valor"],3), 0.000)


"""TestCase que contiene las pruebas a realizar sobre el test de los Rangos Alineados de Friedman.
El nivel de signficancia considerado es el más habitual: 0.05. Para la cuestión de si se trata de
minimizar o maximizar se considera un tipo 0 (minimización) y se crea una prueba adicional con el
tipo 1 para el caso de los nombres y de los rankings, ya que es donde variaría el resultado."""
class TestFriedmanRangosAlineados(unittest.TestCase):

	def test_resultado_friedman_rangos_alineados(self):
		"""Verifica el resultado de la aplicación del test de los Rangos Alineados de Friedman."""
		datos_devueltos = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 0)
		self.assertTrue(datos_devueltos["resultado"], "Error resultado")
		self.assertEqual(round(datos_devueltos["estadistico"],3), 22.26, "Error estadistico")
		self.assertEqual(round(datos_devueltos["p_valor"],3), 0.000, "Error p_valor")
		self.assertEqual(datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"], "Error ranking nombres")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["ranking"]], [26.104, 50.021, 50.208, 67.667], "Error ranking numerico")

	def test_resultado_friedman_rangos_alineados_tipo1(self):
		"""Verifica el ranking de nombres y valores tratándose del caso de maximizar."""
		datos_devueltos = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["nombres"], ["PDFC","NNEP","IS-CHC+INN","FH-GBML"], "Error ranking nombres")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["ranking"]], [29.333, 46.792, 46.979, 70.896], "Error ranking numerico")


"""TestCase que contiene las pruebas a realizar sobre el test de Quade. El nivel de signficancia
considerado es el más habitual: 0.05. Para la cuestión de si se trata de minimizar o maximizar se
considera un tipo 0 (minimización) y se crea una prueba adicional con el tipo 1 para el caso de los
nombres y de los rankings, ya que es donde variaría el resultado."""
class TestQuade(unittest.TestCase):

	def test_resultado_quade(self):
		"""Verifica el resultado de la aplicación del test de los Rangos Alineados de Friedman."""
		datos_devueltos = tnp.quade_test(nombres0, datos3, 0.05, 0)
		self.assertTrue(datos_devueltos["resultado"], "Error resultado")
		self.assertEqual(round(datos_devueltos["estadistico"],3), 11.752, "Error estadistico")
		self.assertEqual(round(datos_devueltos["p_valor"],3), 0.000, "Error p_valor")
		self.assertEqual(datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"], "Error ranking nombres")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["ranking"]], [1.518,2.408,2.462,3.612], "Error ranking numerico")

	def test_resultado_quade_tipo1(self):
		"""Verifica el ranking de nombres y valores tratándose del caso de maximizar."""
		datos_devueltos = tnp.quade_test(nombres0, datos3, 0.05, 1)
		self.assertEqual(datos_devueltos["nombres"], ["PDFC","NNEP","IS-CHC+INN","FH-GBML"], "Error ranking nombres")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["ranking"]], [1.388,2.538,2.592,3.482], "Error ranking numerico")


#Datos para relizar las pruebas de los tests no paramétricos de comparación POST-HOC (con método
#de control). Los argumentos de estos tests siempre son (test_principal, nombres, ranking, N, alpha).
nombres2 = ["PDFC","IS-CHC+INN","NNEP","FH-GBML"]
datos5 = [1.7708333333333333, 2.4791666666666665, 2.4791666666666665, 3.2708333333333335]


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Bonferroni-Dunn. El nivel 
de signficancia considerado es el más habitual: 0.05."""
class TestBonferroni_Dunn(unittest.TestCase):

	def test_resultado_bonferroni_dunn(self):
		"""Verifica el resultado de la aplicación del test POST_HOC de Bonferroni-Dunn."""
		datos_devueltos = tnp.bonferroni_dunn_test("friedman", nombres2, datos5, 24, 0.05)
		self.assertEqual(datos_devueltos["resultado"], [True, False, False], "Error resultados")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["valores z"]], [-4.025, -1.901, -1.901], "Error estadisticos")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores"]], [0.000, 0.057, 0.057], "Error p_valores")
		self.assertEqual(round(datos_devueltos["alpha"],3), 0.017, "Error alpha")
		self.assertEqual(datos_devueltos["nombres"], ['FH-GBML', 'IS-CHC+INN', 'NNEP'], "Error orden nombres")
		self.assertEqual(datos_devueltos["metodo de control"], "PDFC", "Error metodo control")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores ajustados"]], [0.000, 0.172, 0.172], "Error p_valores ajustados")


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Holm. El nivel 
de signficancia considerado es el más habitual: 0.05."""
class TestHolm(unittest.TestCase):

	def test_resultado_holm(self):
		"""Verifica el resultado de la aplicación del test POST_HOC de Holm."""
		datos_devueltos = tnp.holm_test("friedman", nombres2, datos5, 24, 0.05)
		self.assertEqual(datos_devueltos["resultado"], [True, False, False], "Error resultados")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["valores z"]], [-4.025, -1.901, -1.901], "Error estadisticos")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores"]], [0.000, 0.057, 0.057], "Error p_valores")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["alphas"]], [0.017, 0.025, 0.05], "Error alphas")
		self.assertEqual(datos_devueltos["nombres"], ['FH-GBML', 'IS-CHC+INN', 'NNEP'], "Error orden nombres")
		self.assertEqual(datos_devueltos["metodo de control"], "PDFC", "Error metodo control")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores ajustados"]], [0.000, 0.115, 0.115], "Error p_valores ajustados")


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Hochberg. El nivel 
de signficancia considerado es el más habitual: 0.05."""
class TestHochberg(unittest.TestCase):

	def test_resultado_hochberg(self):
		"""Verifica el resultado de la aplicación del test POST_HOC de Hochberg."""
		datos_devueltos = tnp.hochberg_test("friedman", nombres2, datos5, 24, 0.05)
		self.assertEqual(datos_devueltos["resultado"], [True, False, False], "Error resultados")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["valores z"]], [-4.025, -1.901, -1.901], "Error estadisticos")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores"]], [0.000, 0.057, 0.057], "Error p_valores")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["alphas"]], [0.017, 0.025, 0.05], "Error alphas")
		self.assertEqual(datos_devueltos["nombres"], ['FH-GBML', 'IS-CHC+INN', 'NNEP'], "Error orden nombres")
		self.assertEqual(datos_devueltos["metodo de control"], "PDFC", "Error metodo control")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores ajustados"]], [0.000, 0.057, 0.057], "Error p_valores ajustados")


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Li. El nivel 
de signficancia considerado es el más habitual: 0.05."""
class TestLi(unittest.TestCase):

	def test_resultado_li(self):
		"""Verifica el resultado de la aplicación del test POST_HOC de Li."""
		datos_devueltos = tnp.li_test("friedman", nombres2, datos5, 24, 0.05)
		self.assertEqual(datos_devueltos["resultado"], [True, True, False], "Error resultados")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["valores z"]], [-4.025, -1.901, -1.901], "Error estadisticos")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores"]], [0.000, 0.057, 0.057], "Error p_valores")
		self.assertEqual(datos_devueltos["nombres"], ['FH-GBML', 'IS-CHC+INN', 'NNEP'], "Error orden nombres")
		self.assertEqual(datos_devueltos["metodo de control"], "PDFC", "Error metodo control")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores ajustados"]], [0.000, 0.057, 0.057], "Error p_valores ajustados")


#Datos para relizar las pruebas de los tests no paramétricos de comparación POST-HOC (multitest).
#Los argumentos de estos tests siempre son (test_principal, nombres, ranking, N, alpha).
nombres1 = ["C4.5","1NN","NaiveBayes","Kernel","CN2"]
datos4 = [2.100,3.250,2.200,4.333,3.117]


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Nemenyi (Bonferroni-Dunn
multitest). El nivel de signficancia considerado es el más habitual: 0.05."""
class TestNemenyi(unittest.TestCase):

	def test_resultado_nemenyi_multitest(self):
		"""Verifica el resultado de la aplicación del multitest POST_HOC de Nemenyi."""
		datos_devueltos = tnp.nemenyi_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["resultado"], [True,True,True,True,False,False,False,False,False,False], "Error resultados")
		self.assertEqual(datos_devueltos["comparaciones"], ['C4.5 vs Kernel','NaiveBayes vs Kernel','Kernel vs CN2','C4.5 vs 1NN','1NN vs Kernel','1NN vs NaiveBayes','C4.5 vs CN2','NaiveBayes vs CN2','1NN vs CN2','C4.5 vs NaiveBayes'], "Error comparaciones")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["valores z"]], [-5.47,-5.225,2.979,-2.817,-2.653,2.572,-2.491,-2.246,0.326,-0.245], "Error estadisticos")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores"]], [0.0,0.0,0.003,0.005,0.008,0.010,0.013,0.025,0.745,0.806], "Error p_valores")
		self.assertEqual(round(datos_devueltos["alpha"],3), 0.005, "Error alpha")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores ajustados"]], [0.0,0.000,0.029,0.048,0.080,0.101,0.127,0.247,1.0,1.0], "Error p_valores ajustados")


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Holm. El nivel de signficancia
considerado es el más habitual: 0.05."""
class TestHolmMultitest(unittest.TestCase):

	def test_resultado_holm_multitest(self):
		"""Verifica el resultado de la aplicación del multitest POST_HOC de Holm."""
		datos_devueltos = tnp.holm_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["resultado"], [True,True,True,True,True,False,False,False,False,False], "Error resultados")
		self.assertEqual(datos_devueltos["comparaciones"], ['C4.5 vs Kernel','NaiveBayes vs Kernel','Kernel vs CN2','C4.5 vs 1NN','1NN vs Kernel','1NN vs NaiveBayes','C4.5 vs CN2','NaiveBayes vs CN2','1NN vs CN2','C4.5 vs NaiveBayes'], "Error comparaciones")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["valores z"]], [-5.47,-5.225,2.979,-2.817,-2.653,2.572,-2.491,-2.246,0.326,-0.245], "Error estadisticos")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores"]], [0.0,0.0,0.003,0.005,0.008,0.010,0.013,0.025,0.745,0.806], "Error p_valores")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["alphas"]], [0.005,0.006,0.006,0.007,0.008,0.01,0.013,0.017,0.025,0.05], "Error alphas")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores ajustados"]], [0.0,0.000,0.023,0.034,0.048,0.051,0.051,0.074,1.0,1.0], "Error p_valores ajustados")


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Hochberg. El nivel de 
signficancia considerado es el más habitual: 0.05."""
class TestHochbergMultitest(unittest.TestCase):

	def test_resultado_hochberg_multitest(self):
		"""Verifica el resultado de la aplicación del multitest POST_HOC de Hochberg."""
		datos_devueltos = tnp.hochberg_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["resultado"], [True,True,True,True,True,False,False,False,False,False], "Error resultados")
		self.assertEqual(datos_devueltos["comparaciones"], ['C4.5 vs Kernel','NaiveBayes vs Kernel','Kernel vs CN2','C4.5 vs 1NN','1NN vs Kernel','1NN vs NaiveBayes','C4.5 vs CN2','NaiveBayes vs CN2','1NN vs CN2','C4.5 vs NaiveBayes'], "Error comparaciones")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["valores z"]], [-5.47,-5.225,2.979,-2.817,-2.653,2.572,-2.491,-2.246,0.326,-0.245], "Error estadisticos")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores"]], [0.0,0.0,0.003,0.005,0.008,0.010,0.013,0.025,0.745,0.806], "Error p_valores")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["alphas"]], [0.005,0.006,0.006,0.007,0.008,0.01,0.013,0.017,0.025,0.05], "Error alphas")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores ajustados"]], [0.0,0.000,0.023,0.034,0.048,0.051,0.051,0.074,0.806,0.806], "Error p_valores ajustados")


"""TestCase que contiene las pruebas a realizar sobre el mutitest de Li. El nivel de 
signficancia considerado es el más habitual: 0.05."""
class TestLiMultitest(unittest.TestCase):

	def test_resultado_li_multitest(self):
		"""Verifica el resultado de la aplicación del multitest POST_HOC de li."""
		datos_devueltos = tnp.li_multitest("friedman", nombres1, datos4, 30, 0.05)
		self.assertEqual(datos_devueltos["resultado"], [True,True,True,True,True,True,True,True,True,False], "Error resultados")
		self.assertEqual(datos_devueltos["comparaciones"], ['C4.5 vs Kernel','NaiveBayes vs Kernel','Kernel vs CN2','C4.5 vs 1NN','1NN vs Kernel','1NN vs NaiveBayes','C4.5 vs CN2','NaiveBayes vs CN2','1NN vs CN2','C4.5 vs NaiveBayes'], "Error comparaciones")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["valores z"]], [-5.47,-5.225,2.979,-2.817,-2.653,2.572,-2.491,-2.246,0.326,-0.245], "Error estadisticos")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores"]], [0.0,0.0,0.003,0.005,0.008,0.010,0.013,0.025,0.745,0.806], "Error p_valores")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores ajustados"]], [0.0,0.000,0.015,0.024,0.040,0.050,0.062,0.113,0.794,0.806], "Error p_valores ajustados")


#Datos para relizar las pruebas de los tests paramétricos ANOVA y Bonferroni POST-HOC (multitest).
#Los argumentos para el test de ANOVA son (matriz_datos, alpha).
#Para el test de Bonferroni son (nombres_algoritmos, medias_algoritmos, cuadrado_medio_error, N, alpha)
nombres3 = ["A","B","C"]
datos6 = [[27,21,25],[31,33,35],[42,39,39],[38,41,37],[45,46,45]]


"""TestCase que contiene las pruebas a realizar sobre el test ANOVA. El nivel de
signficancia considerado es el más habitual: 0.05."""
class TestAnova(unittest.TestCase):

	def test_resultado_anova(self):
		"""Verifica el resultado de la aplicación del test ANOVA."""
		datos_devueltos = tp.anova_test(datos6, 0.05)
		self.assertFalse(datos_devueltos["resultado"], "Error resultado")
		self.assertEqual(round(datos_devueltos["estadistico"],3), 0.007, "Error estadistico")
		self.assertEqual(round(datos_devueltos["p_valor"],3), 0.993, "Error p_valor")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["variaciones"]], [806.933,0.933,806.000], "Error variaciones")
		self.assertEqual(datos_devueltos["grados_libertad"], [14,2,12], "Error grados libertad")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["cuadrados_medios"]], [57.638,0.467,67.167], "Error cuadrados medios")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["medias_algoritmos"]], [36.600,36.000,36.200], "Error medias algoritmos")
		self.assertEqual(round(datos_devueltos["media_general"],3), 36.267, "Error media general")


"""TestCase que contiene las pruebas a realizar sobre el test POST-HOC Bonferroni. El nivel de
signficancia considerado es el más habitual: 0.05."""
class TestBonferroni(unittest.TestCase):

	def test_resultado_bonferroni(self):
		"""Verifica el resultado de la aplicación del test POST_HOC de Bonferroni."""
		datos_devueltos = tp.bonferroni_test(nombres3, [36.600,36.000,36.200], 67.167, 5, 0.05)
		self.assertEqual(datos_devueltos["resultado"], [False,False,False], "Error resultados")
		self.assertEqual(datos_devueltos["comparaciones"], ['A vs B','A vs C','B vs C'], "Error comparaciones")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["valores_t"]], [0.116,0.077,0.039], "Error estadisticos")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores"]], [0.455,0.470,0.485], "Error p_valores")
		self.assertEqual([round(valor,3) for valor in datos_devueltos["p_valores_ajustados"]], [1,1,1], "Error p_valores ajustados")
		self.assertEqual(round(datos_devueltos["alpha"],3), 0.017, "Error alpha")


if __name__ == '__main__':
    unittest.main()
