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


class TestWilcoxon(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el test de Wilcoxon. El nivel de
    signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.datos_devueltos = tnp.wilcoxon_test(datos0, 0.05)

    def test_resultado(self):
        """Verfifica si el test aplicado sobre los datos es o no estadísticamente significativo)."""
        self.assertTrue(self.datos_devueltos["resultado"])

    def test_estadistico(self):
        """Verifica del valor del estadístico."""
        self.assertEqual(self.datos_devueltos["estadistico"], 19)

    def test_rangos_pos(self):
        """Verifica el valor de la suma de rangos positivos."""
        self.assertEqual(self.datos_devueltos["suma rangos pos"], 86)

    def test_rangos_neg(self):
        """Verifica el valor de la suma de rangos negativos."""
        self.assertEqual(self.datos_devueltos["suma rangos neg"], 19)

    def test_punto_critico(self):
        """Verifica que el valor del punto crítico es recogido correctamente de la tabla de Wilcoxon."""
        self.assertEqual(self.datos_devueltos["punto critico"], 21)

    def test_resultado_wilcoxon1(self):
        """Verifica Exception en caso de que el número de algoritmos sea distinto de 2."""
        self.assertRaises(Exception,tnp.wilcoxon_test,datos1,0.05)

    def test_resultado_wilcoxon2(self):
        """Verifica Exception en caso de que el número de conjuntos sea menor de 5."""
        self.assertRaises(Exception,tnp.wilcoxon_test,datos2,0.05)

    def test_resultado_wilcoxon3(self):
        """Verifica Exception en caso de que alpha no esté contenido en la tabla de Wilcoxon."""
        self.assertRaises(Exception,tnp.wilcoxon_test,datos1,0.03)


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


class TestFriedman(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el test de Friedman. El nivel de
    signficancia considerado es el más habitual: 0.05. Para la cuestión de si se trata de minimizar
    o maximizar se considera un tipo 0 (minimización) y se crea una prueba adicional con el tipo 1
    para el caso de los nombres y de los rankings, ya que es donde variaría el resultado."""

    @classmethod
    def setUpClass(cls):
        cls.datos_devueltos = tnp.friedman_test(nombres0, datos3, 0.05, 0)

    def test_resultado(self):
        """Verifica si el test aplicado sobre los datos es o no estadísticamente significativo)."""
        self.assertTrue(self.datos_devueltos["resultado"])

    def test_estadistico(self):
        """Verifica el valor del estadístico."""
        self.assertEqual(round(self.datos_devueltos["estadistico"],3), 16.225)

    def test_p_valor(self):
        """Verifica el p_valor."""
        self.assertEqual(round(self.datos_devueltos["p_valor"],3), 0.001)

    def test_nombres_tipo0(self):
        """Verifica el ranking de nombres tratándose del caso de minimizar."""
        self.assertEqual(self.datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"])

    def test_ranking_tipo0(self):
        """Verifica el ranking de valores obtenidos tratándose del caso de minimizar."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["ranking"]], [1.729,2.521,2.521,3.229])

    def test_nombres_tipo1(self):
        """Verifica el ranking de nombres tratándose del caso de maximizar."""
        datos_nombres_tipo1 = tnp.friedman_test(nombres0, datos3, 0.05, 1)["nombres"]
        self.assertEqual(datos_nombres_tipo1, ["PDFC","IS-CHC+INN","NNEP","FH-GBML"])

    def test_ranking_tipo1(self):
        """Verifica el ranking de valores obtenidos tratándose del caso de maximizar."""
        datos_ranking_tipo1 = tnp.friedman_test(nombres0, datos3, 0.05, 1)["ranking"]
        self.assertEqual([round(valor,3) for valor in datos_ranking_tipo1], [1.771,2.479,2.479,3.271])


class TestImanDavenport(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el test de Iman-Davenport. El nivel
    de signficancia considerado es el más habitual: 0.05. Sólo se prueba p_valor y estadístico,
    ya que son los valores que varían respecto a Friedman."""

    @classmethod
    def setUpClass(cls):
        cls.datos_devueltos = tnp.iman_davenport_test(nombres0, datos3, 0.05, 0)

    def test_estadistico(self):
        """Verifica el valor del estadístico."""
        self.assertEqual(round(self.datos_devueltos["estadistico"],3), 6.691)

    def test_p_valor(self):
        """Verifica el p_valor."""
        self.assertEqual(round(self.datos_devueltos["p_valor"],3), 0.000)


class TestFriedmanRangosAlineados(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el test de los Rangos Alineados de Friedman.
    El nivel de signficancia considerado es el más habitual: 0.05. Para la cuestión de si se trata de
    minimizar o maximizar se considera un tipo 0 (minimización) y se crea una prueba adicional con el
    tipo 1 para el caso de los nombres y de los rankings, ya que es donde variaría el resultado."""

    @classmethod
    def setUpClass(cls):
        cls.datos_devueltos = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 0)

    def test_resultado(self):
        """Verifica si el test aplicado sobre los datos es o no estadísticamente significativo)."""
        self.assertTrue(self.datos_devueltos["resultado"])

    def test_estadistico(self):
        """Verifica el valor del estadístico."""
        self.assertEqual(round(self.datos_devueltos["estadistico"],3), 22.26)

    def test_p_valor(self):
        """Verifica el p_valor."""
        self.assertEqual(round(self.datos_devueltos["p_valor"],3), 0.000)

    def test_nombres_tipo0(self):
        """Verifica el ranking de nombres tratándose del caso de minimizar."""
        self.assertEqual(self.datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"])

    def test_ranking_tipo0(self):
        """Verifica el ranking de valores obtenidos tratándose del caso de minimizar."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["ranking"]], [26.104, 50.021, 50.208, 67.667])

    def test_nombres_tipo1(self):
        """Verifica el ranking de nombres tratándose del caso de maximizar."""
        datos_nombres_tipo1 = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 1)["nombres"]
        self.assertEqual(datos_nombres_tipo1, ["PDFC","NNEP","IS-CHC+INN","FH-GBML"])

    def test_ranking_tipo1(self):
        """Verifica el ranking de valores obtenidos tratándose del caso de maximizar."""
        datos_ranking_tipo1 = tnp.friedman_rangos_alineados_test(nombres0, datos3, 0.05, 1)["ranking"]
        self.assertEqual([round(valor,3) for valor in datos_ranking_tipo1], [29.333, 46.792, 46.979, 70.896])


class TestQuade(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el test de Quade. El nivel de signficancia
    considerado es el más habitual: 0.05. Para la cuestión de si se trata de minimizar o maximizar se
    considera un tipo 0 (minimización) y se crea una prueba adicional con el tipo 1 para el caso de los
    nombres y de los rankings, ya que es donde variaría el resultado."""

    @classmethod
    def setUpClass(cls):
        cls.datos_devueltos = tnp.quade_test(nombres0, datos3, 0.05, 0)

    def test_resultado(self):
        """Verifica si el test aplicado sobre los datos es o no estadísticamente significativo)."""
        self.assertTrue(self.datos_devueltos["resultado"])

    def test_estadistico(self):
        """Verifica el valor del estadístico."""
        self.assertEqual(round(self.datos_devueltos["estadistico"],3), 11.752)

    def test_p_valor(self):
        """Verifica el p_valor."""
        self.assertEqual(round(self.datos_devueltos["p_valor"],3), 0.000)

    def test_nombres_tipo0(self):
        """Verifica el ranking de nombres tratándose del caso de minimizar."""
        self.assertEqual(self.datos_devueltos["nombres"], ["FH-GBML","IS-CHC+INN","NNEP","PDFC"])

    def test_ranking_tipo0(self):
        """Verifica el ranking de valores obtenidos tratándose del caso de minimizar."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["ranking"]], [1.518,2.408,2.462,3.612])

    def test_nombres_tipo1(self):
        """Verifica el ranking de nombres tratándose del caso de maximizar."""
        datos_nombres_tipo1 = tnp.quade_test(nombres0, datos3, 0.05, 1)["nombres"]
        self.assertEqual(datos_nombres_tipo1, ["PDFC","NNEP","IS-CHC+INN","FH-GBML"])

    def test_ranking_tipo1(self):
        """Verifica el ranking de valores obtenidos tratándose del caso de maximizar."""
        datos_ranking_tipo1 = tnp.quade_test(nombres0, datos3, 0.05, 1)["ranking"]
        self.assertEqual([round(valor,3) for valor in datos_ranking_tipo1], [1.388,2.538,2.592,3.482])


#Datos para relizar las pruebas de los tests no paramétricos de comparación POST-HOC (con método de control).
#Los argumentos de la función para hallar los datos comunes de los tests son: (test_principal, nombres, ranking, N).
#Para la ejecución de los propios tests son siempre los siguientes: (K, nombres, valores_z, p_valores, metodo_control, alpha).
nombres2 = ["PDFC","IS-CHC+INN","NNEP","FH-GBML"]
datos5 = [1.7708333333333333, 2.4791666666666665, 2.4791666666666665, 3.2708333333333335]


class TestDatosComunesTests(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el la función que genera los datos comunes  a los
    tests POST-HOC con método de control."""

    @classmethod
    def setUpClass(cls):
        cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control = tnp.datos_comunes_tests("friedman_test", nombres2, datos5, 24)

    def test_K(self):
        """Verfifica que el valor de K devuelto es el correcto."""
        self.assertEqual(self.K,4)

    def test_nombres(self):
        """Verifica que los nombres de los algoritmos están ordenados según los p_valores."""
        self.assertEqual(self.nombres, ['FH-GBML', 'IS-CHC+INN', 'NNEP'])

    def test_valores_z(self):
        """Verifica que los valores_z o estadísticos están calculados de forma correcta y ordenados según los p_valores."""
        self.assertEqual([round(valor,3) for valor in self.valores_z], [-4.025, -1.901, -1.901])

    def test_p_valores(self):
        """Verifica que los p_valores están calculados de forma correcta y ordenados según su valor."""
        self.assertEqual([round(valor,3) for valor in self.p_valores], [0.000, 0.057, 0.057])

    def test_metodo_control(self):
        """Verifica que el método de control devuelto sea el primero del ranking proporcionado."""
        self.assertEqual(self.metodo_control, "PDFC")


class TestBonferroni_Dunn(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el POST-HOC (método control) de Bonferroni-Dunn. El nivel
    de signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control = tnp.datos_comunes_tests("friedman_test", nombres2, datos5, 24)
        cls.datos_devueltos = tnp.bonferroni_dunn_test(cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [True, False, False])

    def test_alpha(self):
        """Verifica el valor de alpha."""
        self.assertEqual(round(self.datos_devueltos["alpha"],3), 0.017)

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [0.000, 0.172, 0.172])


class TestHolm(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el POST-HOC (método control) de Holm. El nivel
    de signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control = tnp.datos_comunes_tests("friedman_test", nombres2, datos5, 24)
        cls.datos_devueltos = tnp.holm_test(cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [True, False, False])

    def test_alphas(self):
        """Verifica los valores alpha."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["alphas"]], [0.017, 0.025, 0.05])

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [0.000, 0.115, 0.115])


class TestHochberg(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el POST-HOC (método control) de Hochberg. El nivel
    de signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control = tnp.datos_comunes_tests("friedman_test", nombres2, datos5, 24)
        cls.datos_devueltos = tnp.hochberg_test(cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [True, False, False])

    def test_alphas(self):
        """Verifica los valores alpha."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["alphas"]], [0.017, 0.025, 0.05])

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [0.000, 0.057, 0.057])


class TestLi(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el POST-HOC (método control) de Li. El nivel
    de signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control = tnp.datos_comunes_tests("friedman_test", nombres2, datos5, 24)
        cls.datos_devueltos = tnp.li_test(cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [True, False, False])

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [0.000, 0.057, 0.057])


class TestFinner(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el POST-HOC (método control) de Finner. El nivel
    de signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control = tnp.datos_comunes_tests("friedman_test", nombres2, datos5, 24)
        cls.datos_devueltos = tnp.finner_test(cls.K, cls.nombres, cls.valores_z, cls.p_valores, cls.metodo_control, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [True, True, False])

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [0.0, 0.085, 0.085])

    def test_alphas(self):
        """Verifica los valores alpha."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["alphas"]], [0.143, 0.074, 0.05])


#Datos para relizar las pruebas de los tests no paramétricos de comparación POST-HOC (multitest).
#Los argumentos de la función para hallar los datos comunes de los tests son: (test_principal, nombres, ranking, N).
#Para la ejecución de los propios tests son siempre los siguientes: (m, comparaciones, valores_z, p_valores, alpha).
nombres1 = ["C4.5","1NN","NaiveBayes","Kernel","CN2"]
datos4 = [2.100,3.250,2.200,4.333,3.117]


class TestDatosComunesMultiTests(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el la función que genera los datos comunes  a los
    multitests POST-HOC (múltiples comparaciones)."""

    @classmethod
    def setUpClass(cls):
        cls.m, cls.comparaciones, cls.valores_z, cls.p_valores = tnp.datos_comunes_multitests("friedman_test", nombres1, datos4, 30)

    def test_m(self):
        """Verfifica que el valor de m (número de comparaciones) devuelto es el correcto."""
        self.assertEqual(self.m,10)

    def test_comparaciones(self):
        """Verifica que los nombres de las comparaciones están ordenadas según los p_valores."""
        self.assertEqual(self.comparaciones, ['C4.5 vs Kernel','NaiveBayes vs Kernel','Kernel vs CN2','C4.5 vs 1NN','1NN vs Kernel','1NN vs NaiveBayes','C4.5 vs CN2','NaiveBayes vs CN2','1NN vs CN2','C4.5 vs NaiveBayes'])

    def test_valores_z(self):
        """Verifica que los valores_z o estadísticos están calculados de forma correcta y ordenados según los p_valores."""
        self.assertEqual([round(valor,3) for valor in self.valores_z], [-5.470,-5.225,2.979,-2.817,-2.653,2.572,-2.491,-2.246,0.326,-0.245])

    def test_p_valores(self):
        """Verifica que los p_valores están calculados de forma correcta y ordenados según su valor."""
        self.assertEqual([round(valor,3) for valor in self.p_valores], [0.000,0.000,0.003,0.005,0.008,0.010,0.013,0.025,0.745,0.806])


class TestNemenyi(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el POST-HOC mutitest de Nemenyi (Bonferroni-Dunn
    multitest). El nivel de signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.m, cls.comparaciones, cls.valores_z, cls.p_valores = tnp.datos_comunes_multitests("friedman_test", nombres1, datos4, 30)
        cls.datos_devueltos = tnp.nemenyi_multitest(cls.m, cls.comparaciones, cls.valores_z, cls.p_valores, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [True,True,True,True,False,False,False,False,False,False])

    def test_alpha(self):
        """Verifica el valor de alpha."""
        self.assertEqual(round(self.datos_devueltos["alpha"],3), 0.005)

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [0.0,0.000,0.029,0.048,0.080,0.101,0.127,0.247,1.0,1.0])


class TestHolmMultitest(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el POST-HOC mutitest de Holm. El nivel de signficancia
    considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.m, cls.comparaciones, cls.valores_z, cls.p_valores = tnp.datos_comunes_multitests("friedman_test", nombres1, datos4, 30)
        cls.datos_devueltos = tnp.holm_multitest(cls.m, cls.comparaciones, cls.valores_z, cls.p_valores, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [True,True,True,True,True,False,False,False,False,False])

    def test_alphas(self):
        """Verifica los valores alpha."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["alphas"]], [0.005,0.006,0.006,0.007,0.008,0.01,0.013,0.017,0.025,0.05])

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [0.0,0.000,0.023,0.034,0.048,0.051,0.051,0.074,1.0,1.0])


class TestHochbergMultitest(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el POST-HOC mutitest de Hochberg. El nivel de
    signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.m, cls.comparaciones, cls.valores_z, cls.p_valores = tnp.datos_comunes_multitests("friedman_test", nombres1, datos4, 30)
        cls.datos_devueltos = tnp.hochberg_multitest(cls.m, cls.comparaciones, cls.valores_z, cls.p_valores, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [True,True,True,True,True,False,False,False,False,False])

    def test_alphas(self):
        """Verifica los valores alpha."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["alphas"]], [0.005,0.006,0.006,0.007,0.008,0.01,0.013,0.017,0.025,0.05])

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [0.0,0.000,0.023,0.034,0.048,0.051,0.051,0.074,0.806,0.806])


class TestFinnerMultitest(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el POST-HOC mutitest de Finner. El nivel de
    signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.m, cls.comparaciones, cls.valores_z, cls.p_valores = tnp.datos_comunes_multitests("friedman_test", nombres1, datos4, 30)
        cls.datos_devueltos = tnp.finner_multitest(cls.m, cls.comparaciones, cls.valores_z, cls.p_valores, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [True,True,True,True,True,True,True,True,False,False])

    def test_alphas(self):
        """Verifica los valores alpha."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["alphas"]], [0.401,0.226,0.157,0.12,0.098,0.082,0.071,0.062,0.055,0.05])

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [0.0,0.0,0.01,0.012,0.016,0.017,0.018,0.031,0.781,0.806])


class TestShafferMultitest(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el POST-HOC mutitest de Shaffer. El nivel de
    signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.m, cls.comparaciones, cls.valores_z, cls.p_valores = tnp.datos_comunes_multitests("friedman_test", nombres1, datos4, 30)
        cls.datos_devueltos = tnp.shaffer_multitest(cls.m, cls.comparaciones, cls.valores_z, cls.p_valores, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [True,True,True,True,True,True,False,False,False,False])

    def test_alphas(self):
        """Verifica los valores alpha."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["alphas"]], [0.005,0.008,0.008,0.008,0.008,0.013,0.013,0.017,0.025,0.05])

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [0.0,0.0,0.017,0.029,0.048,0.048,0.051,0.074,1.0,1.0])


#Datos para relizar las pruebas de los tests paramétricos ANOVA y Bonferroni POST-HOC (multitest).
#Los argumentos para el test de ANOVA son (matriz_datos, alpha).
#Para el test de Bonferroni son (nombres_algoritmos, medias_algoritmos, cuadrado_medio_error, N, alpha)
nombres3 = ["A","B","C"]
datos6 = [[27,21,25],[31,33,35],[42,39,39],[38,41,37],[45,46,45]]


class TestAnova(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el test ANOVA. El nivel de
    signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.datos_devueltos = tp.anova_test(datos6,0.05)

    def test_resultado(self):
        """Verifica si el test aplicado sobre los datos es o no estadísticamente significativo)."""
        self.assertFalse(self.datos_devueltos["resultado"])

    def test_estadistico(self):
        """Verifica el valor del estadístico."""
        self.assertEqual(round(self.datos_devueltos["estadistico"],3), 0.007)

    def test_p_valor(self):
        """Verifica el p_valor."""
        self.assertEqual(round(self.datos_devueltos["p_valor"],3), 0.993)

    def test_variaciones(self):
        """Verifica las variaciones o varianzas (totales, tratamiento y error)."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["variaciones"]], [806.933,0.933,806.000])

    def test_grados_libertad(self):
        """Verifica los grados de libertad (totales, tratamiento y error)."""
        self.assertEqual(self.datos_devueltos["grados_libertad"], [14,2,12])

    def test_cuadrados_medios(self):
        """Verifica los cuadrados medios (variaciones / grados de libertad)."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["cuadrados_medios"]], [57.638,0.467,67.167])

    def test_medias_algoritmos(self):
        """Verifica el valor medio de los datos obtenidos por cada algoritmo."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["medias_algoritmos"]], [36.600,36.000,36.200])

    def test_media_general(self):
        """Verifica la media de las medias de los algoritmos."""
        self.assertEqual(round(self.datos_devueltos["media_general"],3), 36.267)


class TestBonferroni(unittest.TestCase):
    """TestCase que contiene las pruebas a realizar sobre el test POST-HOC Bonferroni. El nivel de
    signficancia considerado es el más habitual: 0.05."""

    @classmethod
    def setUpClass(cls):
        cls.datos_devueltos = tp.bonferroni_test(nombres3, [36.600,36.000,36.200], 67.167, 5, 0.05)

    def test_resultado(self):
        """Verifica si los tests aplicados sobre todas las hipótesis son o no significativos."""
        self.assertEqual(self.datos_devueltos["resultado"], [False,False,False])

    def test_alpha(self):
        """Verifica el valor de alpha."""
        self.assertEqual(round(self.datos_devueltos["alpha"],3), 0.017)

    def test_comparaciones(self):
        """Verifica que los nombres de las comparaciones están ordenadas según los p_valores."""
        self.assertEqual(self.datos_devueltos["comparaciones"], ['A vs B','A vs C','B vs C'])

    def test_valores_t(self):
        """Verifica que los valores_t o estadísticos están calculados de forma correcta y ordenados según los p_valores."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["valores_t"]], [0.116,0.077,0.039])

    def test_p_valores(self):
        """Verifica que los p_valores están calculados de forma correcta y ordenados según su valor."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores"]], [0.455,0.470,0.485])

    def test_p_valores_ajustados(self):
        """Verifica los p_valores ajustados."""
        self.assertEqual([round(valor,3) for valor in self.datos_devueltos["p_valores_ajustados"]], [1,1,1])


if __name__ == '__main__':
    unittest.main()
