# -*- coding: utf-8 -*-
"""
.. Created on Mon Mar 31 17:11:34 2014

.. @author: Adrián
"""

import numpy as np
import scipy as sp
import scipy.stats as st

def anova_test(matriz_datos, alpha=0.05):
	"""Test paramétrico Anova.

    .. note:: Contrasta la hipótesis nula de que las medias de los resultados de
              dos o más algoritmos son iguales.

    Args:
        matriz_datos: lista de listas de float [N_conjuntos_datos * K_algoritmos]
            Lista que contiene una serie de listas que a su vez contienen los
            resultados en floats obtenidos por los distintos algoritmos.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) que se quiere
            utilizar para contrastar la hipótesis nula del test.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            resultado: boolean
                Resultado del test de contraste de hipótesis. True indica que se
                rechaza la hipótesis nula. False indica que no se rechaza.
            p_valor: float
                p-valor calculado para comparar (contrastar H0) con el nivel de
                significancia.
            estadistico: float
                Estadístico calculado durante el test. Sigue una distribución F.
            variaciones: lista de float [3]
                Lista de variaciones (variación total o respecto a la media general,
                variación dentro del tratamiento o variación del error y variación
                entre los tratamientos o algoritmos).
            grados_libertad: lista de float [3]
                Lista que contiene los grados de libertad totales, de los
                tratamientos y del error.
            cuadrados_medios: lista de float [3]
                Lista de contiene los cuadrados medios (variaciones / grados de libertad)
                totales, del tratamiento y del error.
            medias_algoritmos: lista de float [K_algoritmos]
                Media de los resultados obtenidos por cada uno de los algoritmos.
            media_general: float
                Media de medias de los algoritmos.

    References:
        1. Primitivo Reyes (Sept. 2007). *Análisis de Varianza Anova de una Vía* [Documento WWW]. URL http://www.icicm.com/files/AN_LISIS_DE_VARIANZA.doc
        2. Manuel Oviedo - Beatriz Pateiro. *Contraste sobre la igualdad de medias en dos o más poblaciones normales.*
        3. José Luis Vicente Villardón. *Introducción al Análisis de la Varianza* [Documento WWW]. URL http://biplot.usal.es/problemas/anova/ANOVA.html
    """

	#Número de conjuntos de datos.
	N = len(matriz_datos)
	#Número de algoritmos.
	K = len(matriz_datos[0])

	#Medias algoritmos.
	medias_algoritmos = []
	for i in range(len(matriz_datos[0])):
		medias_algoritmos.append(sp.mean([conjunto[i] for conjunto in matriz_datos]))

	#Media general.
	media_general = sp.mean(medias_algoritmos)

	#Variación total (respecto a la media general).
	SCT = 0
	#Variación dentro del tratamiento o variación del error (cada valor respecto a la
	#media de su tratamiento).
	SCE = 0
	#Variación entre los diferentes tratamientos o algoritmos (efecto de la media de cada
	#tratamiento respecto a la media general).
	SCTR = 0
	for i in range(len(matriz_datos[0])):
		x  = [conjunto[i] for conjunto in matriz_datos]
		for elem in x:
		    SCT = SCT + (elem-media_general)**2
		    SCE = SCE + (elem-medias_algoritmos[i])**2
		SCTR = SCTR + (len(x)*(medias_algoritmos[i]-media_general)**2)

	#Grados de libertad.
	GLT = (N*K)-1
	GLTR = K-1
	GLE = GLT - GLTR

	#Cuadrados medios (suma cuadrados / grados de libertad)
	CMT = SCT/GLT
	CMTR = SCTR/GLTR
	CME = SCE/GLE

	#Estadístico (para contrastar diferencia en las medias del factor de columna TR).
	F = CMTR/CME

	#Cáculo del p_valor.
	p_valor = 1 - st.f.cdf(F, GLTR, GLE)

	return {"resultado" : np.asscalar(p_valor < alpha), "p_valor" : p_valor, "estadistico" : F,
		    "variaciones" : [SCT,SCTR,SCE], "grados_libertad" : [GLT,GLTR,GLE],
		    "cuadrados_medios" : [CMT,CMTR,CME], "medias_algoritmos" : medias_algoritmos,
		    "media_general" : media_general}



def bonferroni_test(nombres_algoritmos, medias_algoritmos, cuadrado_medio_error, N, alpha=0.05):
	"""Test POST-HOC (comparaciones múltiples) de Anova: Bonferroni.

    .. note:: Este tests compara las medias de todos los algoritmos entre sí. Se utiliza
              una vez se tenga constancia gracias al análisis de varianzas Anova de que
              existen diferencias significativas entre las medias de los algoritmos.
              Cada p-valor asociado con la hipótesis H_i se compara con un alpha ajustado
              a todas las comparaciones: :math:`p_i < \\frac{\\alpha}{m}`, donde m se
              corresponde con el número de comparaciones: :math:`m = \\frac{(K*(K-1))}{2}`.

    Args:
        nombres_algoritmos: lista de string [K_algoritmos]
            Lista que contiene los nombres de los algoritmos involucrados en el contraste.
        medias_algoritmos: lista de float [K_algoritmos]
            Lista que contiene la media de los resultados obtenidos por cada uno de los
            algoritmos en el test de análisis de varianzas (Anova).
        cuadrado_medio_error: float
            Varianza dentro del tratamiento o algoritmo o del error (se obtiene del test
            de análisis de varianzas Anova)
        N: int
            Número de conjuntos de datos que se corresponden con el número de problemas sobre
            los que se aplica el test de análisis de varianzas Anova.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) que se quiere utilizar para
            contrastar la hipótesis nula del test.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            resultado: lista de boolean [m_comparaciones]
                Lista que contiene los resultados del test de contraste de hipótesis. True indica
                que se rechaza la hipótesis nula. False indica que no se rechaza.
            p_valores: lista de float [m_comparaciones]
                Lista de p-valores ordenada según los valor (de más a menos significancia o de menor
                a mayor) calculados para comparar (contrastar las H0 de igualdad de medias) con el
                nivel de significancia ajustado.
            valores_t: lista de float [m_comparaciones]
                Lista ordenada (según p_valores) de estadísticos calculados durante el test. Siguen
                una distribución F con (N*K)-K grados de libertad.
            comparaciones: lista de string [m_comparaciones]
                Lista ordenada (según p_valores) que contiene los nombres de las comparaciones realizadas
                en el test port ejemplo: "Alg1 vs Alg2".
            alpha: float
                Nivel de significancia (probabilidad de error tipo 1) ajustado a las m comparaciones.
            p_valores_ajustados: lista de float [m_comparaciones]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia
                proporcionado sin ajustar

    References:
        1. Manuel Oviedo - Beatriz Pateiro. *Contraste sobre la igualdad de medias en dos o más poblaciones normales.*
    """

	#Número de algoritmos K.
	K = len(medias_algoritmos)

	#Número posible de comparaciones.
	m = (K*(K-1))/2

	#Nombres de las comparaciones.
	comparaciones = []
	for i in range(K-1):
		for j in range(i+1,K):
			comparaciones.append(nombres_algoritmos[i] + " vs " + nombres_algoritmos[j])

	#Cálculo del estadístico T (distribución t de student).
	valores_t = []
	for i in range(K-1):
		for j in range(i+1,K):
			valores_t.append((abs(medias_algoritmos[i]-medias_algoritmos[j]))/float(sp.sqrt(cuadrado_medio_error)*sp.sqrt(2/float(N))))

	#Cálculo de los p_valores.
	p_valores = []
	for i in range(m):
		p_valores.append(1-st.t.cdf(valores_t[i],(N*K)-K))

	#Ordenamiento de las comparaciones, valores_t y p_valores segun el p_valor.
	tabla = zip(comparaciones,valores_t,p_valores)
	tabla.sort(key=lambda valor: valor[2])
	c, z, p = zip(*tabla)
	comparaciones = list(c)
	valores_t = list(z)
	p_valores = list(p)

	#Nuevo alpha.
	alpha2 = alpha/float(m)

	#Cálculo de los resultados.
	resultado = []
	for i in range(m):
		resultado.append(np.asscalar(p_valores[i]<alpha2))

	#Cálculo de los p_valores ajustados.
	p_valores_ajustados = []
	for i in range(m):
		v = m*p_valores[i]
		p_valores_ajustados.append(min(v,1))

	return {"valores_t" : valores_t, "p_valores" : p_valores, "comparaciones" : comparaciones, "alpha" : alpha2,
			"resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}
