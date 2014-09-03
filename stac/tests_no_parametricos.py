# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:33:54 2014

@author: Adrián
"""

import numpy as np
import scipy as sp
import scipy.stats as st

#Para cuando el tamaño muestral N sea menor o igual a 25, se puede hacer el test de Wilcoxon
#examinando la tabla que nos da los valores críticos (el intervalo) para cada valor de N y
#nivel de significancia (0.10,0.05,0.02,0.01,0.005,0.001) dado. Si tenemos en cuenta que T
#será el valor mínimo de (suma rangos positivos, suma rangos negativos), se utilizan los límites
#inferiores de los intervalos y el contraste será estadísticamente significativo si: T <= límite
#inferior correspondiente.
tabla_wilcoxon = {0.10:{5:0,6:2,7:3,8:5,9:8,10:10,11:13,12:17,13:21,14:25,15:30,16:35,17:41,
                    18:47,19:53,20:60,21:67,22:75,23:83,24:91,25:100},
                  0.05:{6:0,7:2,8:3,9:5,10:8,11:10,12:13,13:17,14:21,15:25,16:29,17:34,18:40,
                    19:46,20:52,21:58,22:65,23:73,24:81,25:89},
                  0.02:{7:0,8:1,9:3,10:5,11:7,12:9,13:12,14:15,15:19,16:23,17:27,18:32,19:37,
                    20:43,21:49,22:55,23:62,24:69,25:76},
                  0.01:{8:0,9:1,10:3,11:5,12:7,13:9,14:12,15:15,16:19,17:23,18:27,19:32,20:37,
                    21:42,22:48,23:54,24:61,25:68},
                  0.005:{9:0,10:1,11:3,12:5,13:7,14:9,15:12,16:15,17:19,18:23,19:27,20:32,
                    21:37,22:42,23:48,24:54,25:60},
                  0.001:{11:0,12:1,13:2,14:4,15:6,16:8,17:11,18:14,19:18,20:21,21:25,22:30,
                    23:35,24:40,25:45}}

def wilcoxon_test(matriz_datos, alpha=0.05):
    """Test de los Rangos Signados de Wilcoxon.

    .. note:: Contrasta la hipótesis nula de que las medianas de las diferencias de dos muestras (resultados de dos algoritmos)
              relacionadas son iguales. Para tamaños muestrales pequeños, se puede determinar mediante la comparación del
              estadístico con el valor crítico de la tabla de Wilcoxon. Para tamaños muestrales grandes (> 25), el test se puede
              aproximar con la distribución normal. Se deben tener al menos 5 conjuntos de datos cuyas diferencias sean distintas
              de 0.

    Args:
        matriz_datos: lista de listas de float [N_conjuntos_datos * K_algoritmos]
            Lista que contiene una serie de listas que a su vez contienen los resultados en floats obtenidos por los distintos
            algoritmos.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) que se quiere utilizar para contrastar la hipótesis nula del
            test.

    Returns:
        dict: diccionario que contiene los siguientes elementos (tamaño muestral <= 25)::

            resultado: boolean
                Resultado del test de contraste de hipótesis. True indica que se rechaza la hipótesis nula. False indica que no
                se rechaza.
            estadistico: float
                Estadístico T calculado durante el test, donde T = min(T_Mas,T_Men) y donde T_Mas = suma rangos positivos y
                T_Men = suma rangos negativos.
            suma rangos pos: float
                Suma de los rangos de las diferencias mayores que 0.
            suma rangos neg: float
                Suma de los rangos de las diferencias menores que 0.
            punto critico: float
                Límite inferior del intervalo de aceptación. El contraste será estadísticamente significativo si: T <= límite
                inferior correspondiente.

        dict: diccionario que contiene los siguientes elementos (tamaño muestral > 25)::

            resultado: boolean
                Resultado del test de contraste de hipótesis. True indica que se rechaza la hipótesis nula. False indica que no
                se rechaza.
            p_valor: float
                p-valor calculado para comparar (contrastar H0) con el nivel de significancia.
            estadistico: float
                Estadístico Z calculado durante el test. Sigue una distribución normal.
            suma rangos pos: float
                Suma de los rangos de las diferencias mayores que 0.
            suma rangos neg: float
                Suma de los rangos de las diferencias menores que 0.

    References:
        1. Manuel Oviedo - Beatriz Pateiro. *Test de los Rangos Signados de Wilcoxon para muestras apareadas.*
        2. Universidad de Salamanca (Jul. 2013). *Estadística para investigadores. Test no paramétricos: Test de Wilcoxon. Modulo
           6* [Vídeo]. URL https://www.youtube.com/watch?v=B_7Wt49dTos
        3. Wikipedia. *Prueba de los rangos con signo de Wilcoxon* [Documento WWW]. URL http://es.wikipedia.org/wiki/Prueba_de_los_rangos_con_signo_de_Wilcoxon
    """

    #El test de Wilcoxon compara dos algoritmos.
    if len(matriz_datos[0]) != 2:
        raise Exception("Test de Wilcoxon solo aplicable a dos algoritmos")

    #Paso de una matriz de conjuntos de datos a dos listas: lista "a", que contiene
    #los resultados de aplicar el primer algoritmo a los datos y una lista "b" que
    #contiene los resultados de aplicar el segundo algoritmo sobre los mismos datos.
    a = []
    b = []
    for lista_datos in matriz_datos:
        a.append(lista_datos[0])
        b.append(lista_datos[1])

    #Cálculo del número de veces que se aplican los dos algoritmos, es decir,
    #el número de individuos o datos sobre los que se aplican los algoritmos. El
    #tamaño de a y b deben ser iguales. Se conoce como tamaño muestral. Hay
    #dos muestras: a y b.
    N = len(a)

    #Cálculo de las diferencias sin signos y con signos. Se excluye el 0.
    diferencias = []
    signos = []
    for i in range(N):
        diferencia = a[i]-b[i]
        if diferencia != 0:
            diferencias.append(abs(diferencia))
            signos.append(diferencia)

    #Tamaño muestral después de eliminar las diferencias 0.
    N = len(diferencias)

    #El tamaño de la muestra  (sin ligaduras) debe ser al menos de 5.
    if N < 5:
        raise Exception("Menos de 5 conjuntos de datos sin ligaduras")

    #Rangos de orden 1,2,...,N. Cada elemento de copia tiene un rango asociado:
    #indice(elemento) + 1. Si hay empates se calcula la media del rango de cada
    #uno de los elementos repetidos.
    copia = list(diferencias)
    copia.sort()
    rangos = []
    for i in diferencias:
        rangos.append((copia.count(i)+copia.index(i)*2+1)/float(2))

    #Sumas de los rangos de las Di mayores que 0 y menores que 0.
    mayor0 = []
    menor0 = []
    for i in range(N):
        if signos[i] > 0:
            mayor0.append(rangos[i])
        else:
            menor0.append(rangos[i])
    T_Mas = sp.sum(mayor0)
    T_Men = sp.sum(menor0)

    #T es el valor mínimo de T_Mas y T_Men.
    T = min(T_Mas,T_Men)

    #Para tamaños muestrales pequeños, se puede determinar el test de Wilcoxon mediante la comparación
    #de T con el valor crítico de la tabla de Wilcoxon. Para tamaños muestrales grandes, el test se puede
    #aproximar con la distribución normal.
    if N <= 25:
        if alpha not in tabla_wilcoxon:
            raise Exception("Valor de alpha no contenido en la tabla de Wilcoxon")
        #Límite inferior del intervalo de aceptación.
        punto_critico = tabla_wilcoxon[alpha][N]

        return {"resultado" : np.asscalar(T <= punto_critico), "estadistico" : T, "suma rangos pos" : T_Mas,
        "suma rangos neg" : T_Men, "punto critico" : punto_critico}
    else:
        #Cálculo del valor Z
        Z = (T-((N*(N+1))/float(4)))/float(sp.sqrt((N*(N+1)*(2*N+1))/float(24)))

        #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo
        #como el estadístico Z.
        p_valor = 2*(1-st.norm.cdf(abs(Z)))

        return {"resultado" : np.asscalar(p_valor < alpha), "p_valor" : p_valor, "estadistico" : Z,
        "suma rangos pos" : T_Mas, "suma rangos neg" : T_Men}



def test_ranking(test, post_hoc, nombres_algoritmos, matriz_datos, N, alpha=0.05, tipo=0):
    """Función general que sirve para ejecutar test de ranking + POST-HOC sin acoplamiento."""

    #Cálculo del resultado del test de ranking elegido.
    resultado_ranking = test(nombres_algoritmos, matriz_datos, alpha, tipo)

    #Lista de tests POST-HOC de método de control (no multitests).
    post_hoc_metodo_control = ["bonferroni_dunn_test", "holm_test", "hochberg_test", "li_test", "finner_test"]

    #Si el test de ranking es estadísticamente significativo, se caculan los datos comunes del POST-HOC de comparación
    #múltiple o del POST-HOC con método de control y se calcula el resultado del mismo.
    if resultado_ranking["resultado"] == True:

        resultado_post_hoc = {}
        if post_hoc.__name__ in post_hoc_metodo_control:
            K, nombres, valores_z, p_valores, metodo_control = datos_comunes_tests(test.__name__, resultado_ranking["nombres"], resultado_ranking["ranking"], N)
            resultado_post_hoc = post_hoc(K, nombres, valores_z, p_valores, metodo_control, alpha)
        else:
            m, comparaciones, valores_z, p_valores = datos_comunes_multitests(test.__name__, resultado_ranking["nombres"], resultado_ranking["ranking"], N)
            resultado_post_hoc = post_hoc(m, comparaciones, valores_z, p_valores, alpha)

        return {"test_ranking" : resultado_ranking, "test_comparacion" : resultado_post_hoc}

    else:
        return {"test_ranking" : resultado_ranking}



def friedman_test(nombres_algoritmos, matriz_datos, alpha=0.05, tipo=0):
    """Test de Friedman.

    .. note:: Contrasta la hipótesis nula de que todos los algoritmos se comportan de forma similar, por lo que sus rankings deben
              de ser similares y por tanto se puedan considerar iguales todos los algoritmos. El estadístico se distribuye como
              una distribución chi-cuadrado con K-1 grados de libertad, siendo K el número de variables relacionadas (o número de algoritmos).
              Realiza comparaciones y asigna rankings dentro de cada conjunto de datos. Se asignan rankings medios en caso de empate.

    Args:
        nombres_algoritmos: lista de string [K_algoritmos]
            Lista que contiene los nombres de los algoritmos involucrados en el contraste.
        matriz_datos: lista de listas de float [N_conjuntos_datos * K_algoritmos]
            Lista que contiene una serie de listas que a su vez contienen los resultados en floats obtenidos por los distintos
            algoritmos.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) que se quiere utilizar para contrastar la hipótesis nula del
            test.
        tipo: int, optional (default = 0)
            Valor que indica si lo que se quiere es minimizar (0) o maximizar (1). Influye en la asignación de rankings.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            resultado: boolean
                Resultado del test de contraste de hipótesis. True indica que se rechaza la hipótesis nula. False indica que no
                se rechaza.
            p_valor: float
                p-valor calculado para comparar (contrastar H0) con el nivel de significancia.
            estadistico: float
                Estadístico de Friedman, que se distribuye como una distribución chi-cuadrado con K-1 grados de libertad, siendo
                K el número de variables relacionadas (o número de algoritmos).
            nombres: lista de string [K_algoritmos]
                Lista que contiene los nombres de los algoritmos involucrados en el contraste en el orden del ranking.
            ranking: lista de float [K_algoritmos]
                Lista que contiene los rankings medios (de todos los conjuntos de datos) de los algoritmos involucrados en el
                contraste ordenados de peor a mejor.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Número de algoritmos.
    K = len(nombres_algoritmos)

    #Número de conjuntos de datos (Número de veces que se aplican los algoritmos o número de
    #problemas).
    N = len(matriz_datos)

    #Asignación de rankings a los resultados obtenidos por cada algoritmo en cada problema.
    #Cada fila representa un conjunto de datos compuesto por los valores (rankings) asignados.
    #Los valores se asignan de forma ascencente: 1 al mejor resultado, 2 al segundo, etc. En
    #caso de empates, se asignan valores medios.
    rankings = []
    for conj_datos in matriz_datos:
        ranking_conj = []
        copia = list(conj_datos)
        #Ordenamos según el problema se tratase de maximizar o minimizar.
        copia.sort(reverse=tipo)
        for dato in conj_datos:
            ranking_conj.append((copia.count(dato)+copia.index(dato)*2+1)/float(2))
        rankings.append(ranking_conj)

    #Cálculo de los rankings medios de los algoritmos sobre los N problemas.
    rankings_medios = []
    for i in range(K):
        rankings_medios.append(sp.mean([fila[i] for fila in rankings]))

    #Cálculo del estadístico de Friedman, que se distribuye como una distribución chi-cuadrado
    #con K-1 grados de libertad, siendo K el número de variables relacionadas (o número de algoritmos).
    chi2 = ((12*N)/float((K*(K+1))))*((sp.sum(r**2 for r in rankings_medios))-((K*(K+1)**2)/float(4)))

    #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo como el estadístico
    #chi2.
    p_valor = 1 - st.chi2.cdf(chi2, K-1)

    #Cálculo del ranking de los nombres de los algoritmos (de acuerdo a los rankings medios obtenidos).
    ranking_nombres = []
    for i in sorted({nombres_algoritmos[i] : rankings_medios[i] for i in range(K)}.items(), key = lambda t:t[1]):
        ranking_nombres.append(i[0])

    #Ordenamiento de menor a mayor de los rankings medios obtenidos.
    rankings_medios.sort()

    return {"resultado" : np.asscalar(p_valor < alpha), "p_valor" : p_valor, "estadistico" : chi2,
    "nombres" : ranking_nombres, "ranking" : rankings_medios}



def iman_davenport_test(nombres_algoritmos, matriz_datos, alpha=0.05, tipo=0):
    """Test de Iman-Davenport.

    .. note:: Contrasta la hipótesis nula de que todos los algoritmos se comportan de forma similar, por lo que sus rankings deben
              de ser similares y por tanto se puedan considerar iguales todos los algoritmos. Es una mejora del test de Friedman
              (para evitar el comportamiento conservativo de éste) por lo que presenta un estadístico más ajustado que se distribuye
              de acuerdo a una distribución f con (K-1) y (K-1)*(N-1) grados de libertad. Realiza comparaciones y asigna rankings
              dentro de cada conjunto de datos. Se asignan rankings medios en caso de empate.

    Args:
        nombres_algoritmos: lista de string [K_algoritmos]
            Lista que contiene los nombres de los algoritmos involucrados en el contraste.
        matriz_datos: lista de listas de float [N_conjuntos_datos * K_algoritmos]
            Lista que contiene una serie de listas que a su vez contienen los resultados en floats obtenidos por los distintos
            algoritmos.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) que se quiere utilizar para contrastar la hipótesis nula del
            test.
        tipo: int, optional (default = 0)
            Valor que indica si lo que se quiere es minimizar (0) o maximizar (1). Influye en la asignación de rankings.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            resultado: boolean
                Resultado del test de contraste de hipótesis. True indica que se rechaza la hipótesis nula. False indica que no
                se rechaza.
            p_valor: float
                p-valor calculado para comparar (contrastar H0) con el nivel de significancia.
            estadistico: float
                Estadístico de Iman-Davenport, que se distribuye de acuerdo a una distribución f con (K-1) y (K-1)*(N-1) grados de
                libertad.
            nombres: lista de string [K_algoritmos]
                Lista que contiene los nombres de los algoritmos involucrados en el contraste en el orden del ranking.
            ranking: lista de float [K_algoritmos]
                Lista que contiene los rankings medios (de todos los conjuntos de datos) de los algoritmos involucrados en el
                contraste ordenados de peor a mejor.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Número de algoritmos.
    K = len(nombres_algoritmos)

    #Número de conjuntos de datos (Número de veces que se aplican los algoritmos o número de
    #problemas).
    N = len(matriz_datos)

    # Cálculo del estadistico de Friedman.
    friedman = friedman_test(nombres_algoritmos, matriz_datos, alpha, tipo)
    chi2 = friedman["estadistico"]

    # Cálculo del estadistico de Iman-Davenport, que se distribuye de acuerdo a una distribución
    #f con (K-1) y (K-1)(N-1) grados de libertad.
    iman_davenport = ((N-1)*chi2)/float((N*(K-1)-chi2))

    #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo como el estadístico
    #iman_davenport.
    p_valor = 1 - st.f.cdf(iman_davenport, K-1, (K-1)*(N-1))

    return {"resultado" : np.asscalar(p_valor < alpha), "p_valor" : p_valor, "estadistico" : iman_davenport,
    "nombres" : friedman["nombres"], "ranking" : friedman["ranking"]}



def friedman_rangos_alineados_test(nombres_algoritmos, matriz_datos, alpha=0.05, tipo=0):
    """Test de los Rangos Alineados de Friedman.

    .. note:: Contrasta la hipótesis nula de que todos los algoritmos se comportan de forma similar, por lo que sus rankings deben
              de ser similares y por tanto se puedan considerar iguales todos los algoritmos. El estadístico se distribuye como
              una distribución chi-cuadrado con K-1 grados de libertad, siendo K el número de variables relacionadas (o número de algoritmos).
              Realiza comparaciones y asigna rankings teniendo en cuenta a todos los conjuntos de datos. Se asignan rankings medios
              en caso de empate. Suele emplearse cuando el número de algoritmos en la comparación es pequeño.

    Args:
        nombres_algoritmos: lista de string [K_algoritmos]
            Lista que contiene los nombres de los algoritmos involucrados en el contraste.
        matriz_datos: lista de listas de float [N_conjuntos_datos * K_algoritmos]
            Lista que contiene una serie de listas que a su vez contienen los resultados en floats obtenidos por los distintos
            algoritmos.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) que se quiere utilizar para contrastar la hipótesis nula del
            test.
        tipo: int, optional (default = 0)
            Valor que indica si lo que se quiere es minimizar (0) o maximizar (1). Influye en la asignación de rankings.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            resultado: boolean
                Resultado del test de contraste de hipótesis. True indica que se rechaza la hipótesis nula. False indica que no
                se rechaza.
            p_valor: float
                p-valor calculado para comparar (contrastar H0) con el nivel de significancia.
            estadistico: float
                Estadístico de los Rangos Alineados de Friedman, que se distribuye como una distribución chi-cuadrado con K-1 grados
                de libertad, siendo K el número de variables relacionadas (o número de algoritmos).
            nombres: lista de string [K_algoritmos]
                Lista que contiene los nombres de los algoritmos involucrados en el contraste en el orden del ranking.
            ranking: lista de float [K_algoritmos]
                Lista que contiene los rankings medios (de todos los conjuntos de datos) de los algoritmos involucrados en el
                contraste ordenados de peor a mejor.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Número de algoritmos.
    K = len(nombres_algoritmos)

    #Número de conjuntos de datos (Número de veces que se aplican los algoritmos o número de
    #problemas).
    N = len(matriz_datos)

    #Cálculo de las observaciones alienadas: Primero se halla el valor de localización, que es el
    #rendimiento medio alcanzado por cada algoritmo en cada conjunto de datos. Luego, se calculan
    #las diferencias entre el rendimiento obtenido por cada algoritmo con respecto al valor de localización.
    #Se repite para todos los algoritmos y conjuntos de datos.
    observaciones_alineadas = []
    for conj_datos in matriz_datos:
        fila_observaciones = []
        valor_localizacion = sp.mean(conj_datos)
        for dato in conj_datos:
            fila_observaciones.append(dato-valor_localizacion)
        observaciones_alineadas.append(fila_observaciones)

    # Creación de una lista a partir de la tabla observaciones_alineadas.
    tabla_a_lista = []
    for fila in observaciones_alineadas:
        for dato in fila:
            tabla_a_lista.append(dato)

    # Ordenación de la lista.
    tabla_a_lista.sort(reverse=tipo)

    #Asignación de rankings a los resultados obtenidos por cada algoritmo en cada problema.
    #Cada fila representa un conjunto de datos compuesto por los rankings asignados. Los
    #rankings se asignan de forma ascencente: 1 al mejor resultado, 2 al segundo, ... hasta
    #K*N. En caso de empates, se asignan valores medios.
    rankings = []
    for fila in observaciones_alineadas:
        ranking_conj = []
        for dato in fila:
            ranking_conj.append((tabla_a_lista.count(dato)+tabla_a_lista.index(dato)*2+1)/float(2))
        rankings.append(ranking_conj)

    #Cálculo de los rankings medios de los algoritmos sobre los N problemas y de la suma de los
    #ranking obtenidos por cada algoritmo.
    rankings_medios = []
    totales_algoritmos = []
    for i in range(K):
        rankings_medios.append(sp.mean([fila[i] for fila in rankings]))
        totales_algoritmos.append(sp.sum([fila[i] for fila in rankings]))

    #Cálculo de suma de los rankings obtenidos para cada conjunto de datos.
    totales_conjuntos = []
    for i in rankings:
        totales_conjuntos.append(sp.sum(i))

    #Cálculo del estadístico de los Rangos Alineados de Friedman.
    T = (K-1)*(sp.sum(total**2 for total in totales_algoritmos)-(K*N**2/float(4))*(K*N+1)**2)/float(((K*N*(K*N+1)*(2*K*N+1))/float(6))-(1/float(K))*sp.sum(total**2 for total in totales_conjuntos))

    #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo como el estadístico T.
    p_valor = 1 - st.chi2.cdf(T, K-1)

    #Cálculo del ranking de los nombres de los algoritmos (de acuerdo a los rankings medios obtenidos).
    ranking_nombres = []
    for i in sorted({nombres_algoritmos[i] : rankings_medios[i] for i in range(K)}.items(), key = lambda t:t[1]):
        ranking_nombres.append(i[0])

    #Ordenamiento de menor a mayor de los rankings medios obtenidos.
    rankings_medios.sort()

    return {"resultado" : np.asscalar(p_valor < alpha), "p_valor" : p_valor, "estadistico" : T,
    "nombres" : ranking_nombres, "ranking" : rankings_medios}



def quade_test(nombres_algoritmos, matriz_datos, alpha=0.05, tipo=0):
    """Test de Quade.

    .. note:: Contrasta la hipótesis nula de que todos los algoritmos se comportan de forma similar, por lo que sus rankings deben
              de ser similares y por tanto se puedan considerar iguales todos los algoritmos. El estadístico se distribuye como una
              distribución F con (K-1) y (K-1)*(N-1) grados de libertad siendo K el número de variables relacionadas (o número de algoritmos)
              y N el número de conjuntos de datos. El test de Quade considera que algunos problemas son más difíciles o que los
              resultados que obtienen los algoritmos sobre ellos son más distantes (ponderación). Se asignan rankings medios en caso
              de empate.

    Args:
        nombres_algoritmos: lista de string [K_algoritmos]
            Lista que contiene los nombres de los algoritmos involucrados en el contraste.
        matriz_datos: lista de listas de float [N_conjuntos_datos * K_algoritmos]
            Lista que contiene una serie de listas que a su vez contienen los resultados en floats obtenidos por los distintos
            algoritmos.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) que se quiere utilizar para contrastar la hipótesis nula del
            test.
        tipo: int, optional (default = 0)
            Valor que indica si lo que se quiere es minimizar (0) o maximizar (1). Influye en la asignación de rankings.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            resultado: boolean
                Resultado del test de contraste de hipótesis. True indica que se rechaza la hipótesis nula. False indica que no
                se rechaza.
            p_valor: float
                p-valor calculado para comparar (contrastar H0) con el nivel de significancia.
            estadistico: float
                Estadístico de Quade, que se distribuye como una distribución F con (K-1) y (K-1)*(N-1) grados de libertad siendo K
                el número de variables relacionadas (o número de algoritmos) y N el número de conjuntos de datos.
            nombres: lista de string [K_algoritmos]
                Lista que contiene los nombres de los algoritmos involucrados en el contraste en el orden del ranking.
            ranking: lista de float [K_algoritmos]
                Lista que contiene los rankings medios (de todos los conjuntos de datos) de los algoritmos involucrados en el
                contraste ordenados de peor a mejor.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Número de algoritmos.
    K = len(nombres_algoritmos)

    #Número de conjuntos de datos (Número de veces que se aplican los algoritmos o número de
    #problemas).
    N = len(matriz_datos)

    #Asignación de rankings a los resultados obtenidos por cada algoritmo en cada problema de forma
    #similar al test de Friedman: cada fila representa un conjunto de datos compuesto por los
    #valores (rankings) asignados. Los valores se asignan de forma ascencente: 1 al mejor resultado,
    #2 al segundo, etc. En caso de empates, se asignan valores medios.
    rankings_resultados = []
    for conj_datos in matriz_datos:
        ranking_conj = []
        copia = list(conj_datos)
        #Ordenamos según el problema se tratase de maximizar o minimizar.
        copia.sort(reverse=tipo)
        for dato in conj_datos:
            ranking_conj.append((copia.count(dato)+copia.index(dato)*2+1)/float(2))
        rankings_resultados.append(ranking_conj)

    #Los rankings se asignan a los problemas de acuerdo al tamaño del rango de la muestra en cada
    #uno. El rango de la muestra en un problema es la diferencia entre la observación más alta y
    #la más baja en dicho problema. Se asigna el ranking 1 al conjunto con el menor rango, el 2 al
    #segundo con menor rango, etc. Se utilizan rankings medios en caso de empate.
    rankings_problemas = []
    rangos = []
    for conj_datos in matriz_datos:
        rangos.append(max(conj_datos)-min(conj_datos))
    copia = list(rangos)
    copia.sort()
    for rango in rangos:
        rankings_problemas.append((copia.count(rango)+copia.index(rango)*2+1)/float(2))

    #S, W.
    S = []
    W = []
    ranking_medio = (K+1)/float(2)
    contador_problemas = 0
    for ranking_conj in rankings_resultados:
        fila_s = []
        fila_w = []
        for i in range(K):
            fila_s.append(rankings_problemas[contador_problemas]*(ranking_conj[i]-ranking_medio))
            fila_w.append(rankings_problemas[contador_problemas]*ranking_conj[i])
        contador_problemas+=1
        S.append(fila_s)
        W.append(fila_w)

    #Sj, Wj.
    Sj = []
    Wj = []
    for i in range(K):
        Sj.append(sp.sum(fila[i] for fila in S))
        Wj.append(sp.sum(fila[i] for fila in W))

    #Rankings medios.
    rankings_medios = []
    for i in range(K):
        rankings_medios.append(Wj[i]/float((N*(N+1))/float(2)))

    #Términos A, B.
    A = N*(N+1)*(2*N+1)*K*(K+1)*(K-1)/float(72)
    B = sp.sum(x**2 for x in Sj)/float(N)

    #Cáculo del estadístico.
    T = (N-1)*B/float(A-B)

    #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo como el estadístico T.
    p_valor = 1 - st.f.cdf(T, K-1, (K-1)*(N-1))

    #Cálculo del ranking de los nombres de los algoritmos (de acuerdo a los rankings medios obtenidos).
    ranking_nombres = []
    for i in sorted({nombres_algoritmos[i] : rankings_medios[i] for i in range(K)}.items(), key = lambda t:t[1]):
        ranking_nombres.append(i[0])

    #Ordenamiento de menor a mayor de los rankings medios obtenidos.
    rankings_medios.sort()

    return {"resultado" : np.asscalar(p_valor < alpha), "p_valor" : p_valor, "estadistico" : T,
    "nombres" : ranking_nombres, "ranking" : rankings_medios}



def datos_comunes_tests(test_principal, nombres, ranking, N):
    """Cálculo de los datos comunes a los tests de comparación POST-HOC.

    .. note:: Función utilizada por todos los tests de comparación POST-HOC para obtener los datos comunes. Los estadísticos Z
              siguen una distribución normal. Los valores de los estadísticos cambian en función de si el test principal es
              Friedman o Iman-Davenport, Rangos Alineados de Friedman o Quade.

    Args:
        test_principal: {'friedman', 'iman-davenport', quade', 'rangos-alineados'}
            Nombre del test principal o test de ranking ejecutado.
        nombres: lista de string [K_algoritmos]
            Lista que contiene los nombres de los algoritmos involucrados en el contraste en el orden del ranking obtenido por el
            test principal.
        ranking: lista de float [K_algoritmos]
            Lista que contiene los rankings medios (de todos los conjuntos de datos) de los algoritmos involucrados en el
            contraste ordenados de peor a mejor obtenidos por el test principal.
        N: int
            Número de conjuntos de datos o problemas sobre los que se aplican los algoritmos.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            K: int
                Número de algoritmos (incluyendo método de control).
            nombres: lista de string [K-1]
                Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
            valores_z: lista de float [K-1]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K-1]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            metodo_control: string
                Método de control del test, por convención es el test de menor ranking.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Número de algoritmos K (incluyendo método de control).
    K = len(ranking)

    #Cálculo del estadístico Z (distribución normal). El valor cambia en función de si el
    #test principal es Friedman o Iman-Davenport, Rangos Alineados de Friedman o Quade.
    valores_z = []
    if test_principal == "friedman_test" or test_principal == "iman_davenport_test":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1))/float(6*N)))
    elif test_principal == "friedman_rangos_alineados_test":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(N+1))/float(6)))
    else:
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1)*((2*N)+1)*(K-1))/float(18*N*(N+1))))

    #Cálculo de los p_valores.
    p_valores = []
    for i in range(K-1):
        p_valores.append(2*(1-st.norm.cdf(abs(valores_z[i]))))

    #Método de control (Primero del ranking).
    metodo_control = nombres[0]

    #Ordenamiento de los nombres, valores_z y p_valores segun el p_valor.
    tabla = zip(nombres[1:],valores_z,p_valores)
    tabla.sort(key=lambda valor: valor[2])
    n, z, p = zip(*tabla)
    nombres = list(n)
    valores_z = list(z)
    p_valores = list(p)

    return K, nombres, valores_z, p_valores, metodo_control



def bonferroni_dunn_test(K, nombres, valores_z, p_valores, metodo_control, alpha=0.05):
    """Test POST-HOC de Bonferroni-Dunn.

    .. note:: El contraste de las hipótesis se realiza comparando cada p_valor con :math:`\\frac{\\alpha}{(K-1)}.` Si el p_valor
              es menor que dicho alpha ajustado se rechaza la hipótesis nula.

    Args:
        K: int
            Número de algoritmos (incluyendo método de control).
        nombres: lista de string [K-1]
            Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
        valores_z: lista de float [K-1]
            Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
        p_valores: lista de float [K-1]
            p-valores calculados para comparar con los niveles de significancia ajustados.
        metodo_control: string
            Método de control del test, por convención es el test de menor ranking.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) del test de ranking principal.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            valores_z: lista de float [K-1]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K-1]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            metodo de control: string
                Método de control del test, por convención es el test de menor ranking.
            nombres: lista de string [K-1]
                Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
            alpha: float
                Nivel de significancia ajustado.
            resultado: lista de boolean [K-1]
                Resultado de los tests de contraste de hipótesis. True es que se rechaza la hipótesis nula y False que no se
                rechaza.
            p_valores_ajustados: lista de float [K-1]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia proporcionado sin ajustar.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Nuevo alpha.
    alpha2 = alpha/float(K-1)

    #Cálculo de los resultados.
    resultado = []
    for i in range(K-1):
        resultado.append(np.asscalar(p_valores[i]<alpha2))

    #Cálculo de los p_valores_ajustados.
    p_valores_ajustados = []
    for i in range(K-1):
        v = (K-1)*p_valores[i]
        p_valores_ajustados.append(min(v,1))

    return {"valores_z" : valores_z, "p_valores" : p_valores, "metodo_control" : metodo_control, "nombres" : nombres,
    "alpha" : alpha2, "resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}



def holm_test(K, nombres, valores_z, p_valores, metodo_control, alpha=0.05):
    """Test POST-HOC de Holm.

    .. note:: Compara cada p_valor (empezando por el más significativo) con :math:`\\frac{\\alpha}{(K-i)},` donde i in range(1,K).
              Si se rechaza una hipótesis continúa contrastando. En el caso de que una hipótesis se rechace se rechazan todas las demás.

    Args:
        K: int
            Número de algoritmos (incluyendo método de control).
        nombres: lista de string [K-1]
            Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
        valores_z: lista de float [K-1]
            Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
        p_valores: lista de float [K-1]
            p-valores calculados para comparar con los niveles de significancia ajustados.
        metodo_control: string
            Método de control del test, por convención es el test de menor ranking.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) del test de ranking principal.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            valores_z: lista de float [K-1]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K-1]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            metodo de control: string
                Método de control del test, por convención es el test de menor ranking.
            nombres: lista de string [K-1]
                Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
            alphas: lista de float [K-1]
                Niveles de significancia ajustados.
            resultado: lista de boolean [K-1]
                Resultado de los tests de contraste de hipótesis. True es que se rechaza la hipótesis nula y False que no se
                rechaza.
            p_valores_ajustados: lista de float [K-1]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia proporcionado sin ajustar.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Valores alphas.
    alphas = []
    for i in range(1,K):
        alphas.append(alpha/float(K-i))

    #Cálculo de los resultados.
    resultado = [False]*(K-1)
    for i in range(K-1):
        if p_valores[i] < alphas[i]:
            resultado[i] = True
        else:
            break

    #Cálculo de los p_valores_ajustados.
    p_valores_ajustados = []
    for i in range(K-1):
        v = max([(K-(j+1))*p_valores[j] for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))

    return {"valores_z" : valores_z, "p_valores" : p_valores, "metodo_control" : metodo_control, "nombres" : nombres,
    "alphas" : alphas, "resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}



def hochberg_test(K, nombres, valores_z, p_valores, metodo_control, alpha=0.05):
    """Test POST-HOC de Hochberg.

    .. note:: Compara en la dirección opuesta a Holm. En el momento que encuentra una hipótesis que pueda aceptar, acepta todas
              las demás.

    Args:
        K: int
            Número de algoritmos (incluyendo método de control).
        nombres: lista de string [K-1]
            Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
        valores_z: lista de float [K-1]
            Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
        p_valores: lista de float [K-1]
            p-valores calculados para comparar con los niveles de significancia ajustados.
        metodo_control: string
            Método de control del test, por convención es el test de menor ranking.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) del test de ranking principal.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            valores_z: lista de float [K-1]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K-1]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            metodo de control: string
                Método de control del test, por convención es el test de menor ranking.
            nombres: lista de string [K-1]
                Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
            alphas: lista de float [K-1]
                Niveles de significancia ajustados.
            resultado: lista de boolean [K-1]
                Resultado de los tests de contraste de hipótesis. True es que se rechaza la hipótesis nula y False que no se
                rechaza.
            p_valores_ajustados: lista de float [K-1]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia proporcionado sin ajustar.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Valores alphas.
    alphas = []
    for i in range(K-1,0,-1):
        alphas.append(alpha/float(i))

    #Cálculo de los resultados.
    resultado = [True]*(K-1)
    for i in range(K-2,-1,-1):
        if p_valores[i] > alphas[i]:
            resultado[i] = False
        else:
            break

    #Cálculo de los p_valores_ajustados (La pág. 137 pone max. Si no se pone min no da lo mismo
    #que la pág. 142).
    p_valores_ajustados = []
    for i in range(K-1):
        p_valores_ajustados.append(min([(K-j)*p_valores[j-1] for j in range(K-1,i,-1)]))

    return {"valores_z" : valores_z, "p_valores" : p_valores, "metodo_control" : metodo_control, "nombres" : nombres,
    "alphas" : alphas, "resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}



def li_test(K, nombres, valores_z, p_valores, metodo_control, alpha=0.05):
    """Test POST-HOC de Li.

    .. note:: Rechaza todas las hipótesis si el p_valor menos significativo es menor que alpha. En otro caso, acepta dicha
              hipótesis y rechaza cualquier hipótesis restante cuyo p_valor sea menor que un valor calculado.

    Args:
        K: int
            Número de algoritmos (incluyendo método de control).
        nombres: lista de string [K-1]
            Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
        valores_z: lista de float [K-1]
            Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
        p_valores: lista de float [K-1]
            p-valores calculados para comparar con los niveles de significancia ajustados.
        metodo_control: string
            Método de control del test, por convención es el test de menor ranking.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) del test de ranking principal.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            valores_z: lista de float [K-1]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K-1]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            metodo de control: string
                Método de control del test, por convención es el test de menor ranking.
            nombres: lista de string [K-1]
                Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
            resultado: lista de boolean [K-1]
                Resultado de los tests de contraste de hipótesis. True es que se rechaza la hipótesis nula y False que no se
                rechaza.
            p_valores_ajustados: lista de float [K-1]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia proporcionado sin ajustar.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Cálculo de los resultados.
    resultado = [True]*(K-1)
    if p_valores[K-2] > alpha:
        resultado[K-2] =  False
        valor = ((1-p_valores[K-2])/float(1-alpha))*alpha
        for i in range(K-2):
            if p_valores[i] > valor:
                resultado[i] = False

    #Cálculo de los p_valores_ajustados.
    p_valores_ajustados = []
    for i in range(K-1):
        p_valores_ajustados.append(p_valores[i]/float(p_valores[i]+1-p_valores[K-2]))

    return {"valores_z" : valores_z, "p_valores" : p_valores, "metodo_control" : metodo_control,
    "nombres" : nombres, "resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}



def finner_test(K, nombres, valores_z, p_valores, metodo_control, alpha=0.05):
    """Test POST-HOC de Finner.

    .. note:: Sigue un proceso igual al test de Holm pero cada p-valor asociado con la hipótesis H_i se compara como:
              :math:`p_i <= \\frac{\\alpha}{1-(1-\\alpha)^{(k-1)/i}}.`

    Args:
        K: int
            Número de algoritmos (incluyendo método de control).
        nombres: lista de string [K-1]
            Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
        valores_z: lista de float [K-1]
            Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
        p_valores: lista de float [K-1]
            p-valores calculados para comparar con los niveles de significancia ajustados.
        metodo_control: string
            Método de control del test, por convención es el test de menor ranking.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) del test de ranking principal.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            valores_z: lista de float [K-1]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K-1]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            metodo de control: string
                Método de control del test, por convención es el test de menor ranking.
            nombres: lista de string [K-1]
                Nombres de los algoritmos (con los que el método de control se compara) ordenados según los p_valores.
            alphas: lista de float [K-1]
                Niveles de significancia ajustados.
            resultado: lista de boolean [K-1]
                Resultado de los tests de contraste de hipótesis. True es que se rechaza la hipótesis nula y False que no se
                rechaza.
            p_valores_ajustados: lista de float [K-1]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia proporcionado sin ajustar.

    References:
        1. H. Finner, "On a monotonicity problem in step-down multiple test procedures", Journal of the American Statistical Association 88 (1993) 920–923
    """

    #Valores alphas.
    alphas = []
    for i in range(1,K):
        alphas.append(1-(1-alpha)**((K-1)/float(i)))

    #Cálculo de los resultados.
    resultado = [False]*(K-1)
    for i in range(K-1):
        if p_valores[i] <= alphas[i]:
            resultado[i] = True
        else:
            break

    #Cálculo de los p_valores ajustados.
    p_valores_ajustados = []
    for i in range(K-1):
        v = max([1-(1-p_valores[j])**((K-1)/float(j+1)) for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))

    return {"valores_z" : valores_z, "p_valores" : p_valores, "metodo_control" : metodo_control, "nombres" : nombres,
    "alphas" : alphas, "resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}



def datos_comunes_multitests(test_principal, nombres, ranking, N):
    """Cálculo de los datos comunes a los multitests de comparación POST-HOC.

    .. note:: Función utilizada por todos los multitests de comparación POST-HOC para obtener los datos comunes. Los estadísticos
              Z siguen una distribución normal. Los valores de los estadísticos cambian en función de si el test principal es
              Friedman o Iman-Davenport, Rangos Alineados de Friedman o Quade. Se realizan m comparaciones, donde :math:`m = \\frac{(K*(K-1))}{2}`.

    Args:
        test_principal: {'friedman', 'iman-davenport', quade', 'rangos-alineados'}
            Nombre del test principal o test de ranking ejecutado.
        nombres: lista de string [K_algoritmos]
            Lista que contiene los nombres de los algoritmos involucrados en el contraste en el orden del ranking obtenido por el
            test principal.
        ranking: lista de float [K_algoritmos]
            Lista que contiene los rankings medios (de todos los conjuntos de datos) de los algoritmos involucrados en el
            contraste ordenados de peor a mejor obtenidos por el test principal.
        N: int
            Número de conjuntos de datos o problemas sobre los que se aplican los algoritmos.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            m: int
                Número de comparaciones.
            comparaciones: lista de string [K*(K-1)/2]
                Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
            valores_z: lista de float [K*(K-1)/2]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K*(K-1)/2]
                p-valores calculados para comparar con los niveles de significancia ajustados.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Número de algoritmos K.
    K = len(ranking)

    #Número posible de comparaciones.
    m = (K*(K-1))/2

    #Nombres de las comparaciones.
    comparaciones = []
    for i in range(K-1):
        for j in range(i+1,K):
            comparaciones.append(nombres[i] + " vs " + nombres[j])

    #Cálculo del estadístico Z (distribución normal). El valor cambia en función de si el
    #test principal es Friedman o Iman-Davenport, Rangos Alineados de Friedman o Quade.
    valores_z = []
    if test_principal == "friedman_test" or test_principal == "iman_davenport_test":
        for i in range(K-1):
            for j in range(i+1,K):
                valores_z.append((ranking[i]-ranking[j])/sp.sqrt((K*(K+1))/float(6*N)))
    elif test_principal == "friedman_rangos_alineados_test":
        for i in range(K-1):
            for j in range(i+1,K):
                valores_z.append((ranking[i]-ranking[j])/sp.sqrt((K*(N+1))/float(6)))
    else:
        for i in range(K-1):
            for j in range(i+1,K):
                valores_z.append((ranking[i]-ranking[j])/sp.sqrt((K*(K+1)*((2*N)+1)*(K-1))/float(18*N*(N+1))))

    #Cálculo de los p_valores.
    p_valores = []
    for i in range(m):
        p_valores.append(2*(1-st.norm.cdf(abs(valores_z[i]))))

    #Ordenamiento de las comparaciones, valores_z y p_valores segun el p_valor.
    tabla = zip(comparaciones,valores_z,p_valores)
    tabla.sort(key=lambda valor: valor[2])
    c, z, p = zip(*tabla)
    comparaciones = list(c)
    valores_z = list(z)
    p_valores = list(p)

    return m, comparaciones, valores_z, p_valores



def nemenyi_multitest(m, comparaciones, valores_z, p_valores, alpha=0.05):
    """MultiTest POST-HOC de Nemenyi (Bonferroni-Dunn).

    .. note:: El contraste de las hipótesis se realiza comparando cada p_valor con :math:`\\frac{\\alpha}{m},` donde :math:`m = \\frac{(K*(K-1))}{2}`.
              Si el p_valor es menor que dicho alpha ajustado se rechaza la hipótesis nula.

    Args:
        m: int
            Número de comparaciones.
        comparaciones: lista de string [K*(K-1)/2]
            Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
        valores_z: lista de float [K*(K-1)/2]
            Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
        p_valores: lista de float [K*(K-1)/2]
            p-valores calculados para comparar con los niveles de significancia ajustados.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) del test de ranking principal.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            valores_z: lista de float [K*(K-1)/2]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K*(K-1)/2]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            comparaciones: lista de string [K*(K-1)/2]
                Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
            alpha: float
                Nivel de significancia ajustado.
            resultado: lista de boolean [K*(K-1)/2]
                Resultado de los tests de contraste de hipótesis. True es que se rechaza la hipótesis nula y False que no se
                rechaza.
            p_valores_ajustados: lista de float [K*(K-1)/2]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia proporcionado sin ajustar.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Nuevo alpha.
    alpha2 = alpha/float(m)

    #Cálculo de los resultados.
    resultado = []
    for i in range(m):
        resultado.append(np.asscalar(p_valores[i]<alpha2))

    #Cálculo de los p_valores_ajustados.
    p_valores_ajustados = []
    for i in range(m):
        v = m*p_valores[i]
        p_valores_ajustados.append(min(v,1))

    return {"valores_z" : valores_z, "p_valores" : p_valores, "comparaciones" : comparaciones, "alpha" : alpha2,
    "resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}



def holm_multitest(m, comparaciones, valores_z, p_valores, alpha=0.05):
    """MultiTest POST-HOC de Holm.

    .. note:: Compara cada p_valor (empezando por el más significativo) con :math:`\\frac{\\alpha}{(m+1-i)},` donde i in range(1,m+1) y
              :math:`m = \\frac{(K*(K-1))}{2}.` Si se rechaza una hipótesis continúa contrastando. En el caso de que una hipótesis se
              rechace se rechazan todas las demás.

    Args:
        m: int
            Número de comparaciones.
        comparaciones: lista de string [K*(K-1)/2]
            Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
        valores_z: lista de float [K*(K-1)/2]
            Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
        p_valores: lista de float [K*(K-1)/2]
            p-valores calculados para comparar con los niveles de significancia ajustados.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) del test de ranking principal.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            valores_z: lista de float [K*(K-1)/2]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K*(K-1)/2]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            comparaciones: lista de string [K*(K-1)/2]
                Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
            alphas: array de float [K*(K-1)/2]
                Niveles de significancia ajustados
            resultado: lista de boolean [K*(K-1)/2]
                Resultado de los tests de contraste de hipótesis. True es que se rechaza la hipótesis nula y False que no se
                rechaza.
            p_valores_ajustados: lista de float [K*(K-1)/2]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia proporcionado sin ajustar.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Valores alphas.
    alphas = []
    for i in range(1,m+1):
        alphas.append(alpha/float(m+1-i))

    #Cálculo de los resultados.
    resultado = [False]*m
    for i in range(m):
        if p_valores[i] < alphas[i]:
            resultado[i] = True
        else:
            break

    #Cálculo de los p_valores_ajustados.
    p_valores_ajustados = []
    for i in range(m):
        v = max([(m-j)*p_valores[j] for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))

    return {"valores_z" : valores_z, "p_valores" : p_valores, "comparaciones" : comparaciones, "alphas" : alphas,
    "resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}



def hochberg_multitest(m, comparaciones, valores_z, p_valores, alpha=0.05):
    """MultiTest POST-HOC de Hochberg.

    .. note:: Compara en la dirección opuesta a Holm. En el momento que encuentra una hipótesis que pueda aceptar, acepta todas
              las demás. m es el número de comparaciones o contrastes, :math:`m = \\frac{(K*(K-1))}{2}.`

    Args:
        m: int
            Número de comparaciones.
        comparaciones: lista de string [K*(K-1)/2]
            Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
        valores_z: lista de float [K*(K-1)/2]
            Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
        p_valores: lista de float [K*(K-1)/2]
            p-valores calculados para comparar con los niveles de significancia ajustados.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) del test de ranking principal.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            valores_z: lista de float [K*(K-1)/2]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K*(K-1)/2]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            comparaciones: lista de string [K*(K-1)/2]
                Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
            alphas: array de float [K*(K-1)/2]
                Niveles de significancia ajustados
            resultado: lista de boolean [K*(K-1)/2]
                Resultado de los tests de contraste de hipótesis. True es que se rechaza la hipótesis nula y False que no se
                rechaza.
            p_valores_ajustados: lista de float [K*(K-1)/2]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia proporcionado sin ajustar.

    References:
        1. Salvador García, Francisco Herrera. *Statistical Analysis of Experiments in Data Mining and Computational Intelligence
           Computational Intelligence.*
    """

    #Valores alphas.
    alphas = []
    for i in range(m,0,-1):
        alphas.append(alpha/float(i))

    #Cálculo de los resultados.
    resultado = [True]*m
    for i in range(m-1,-1,-1):
        if p_valores[i] > alphas[i]:
            resultado[i] = False
        else:
            break

    #Cálculo de los p_valores_ajustados (La pág. 137 pone max. Si no se pone min no da lo mismo
    #que la pág. 142).
    p_valores_ajustados = []
    for i in range(m):
        p_valores_ajustados.append(min([(m+1-j)*p_valores[j-1] for j in range(m,i,-1)]))

    return {"valores_z" : valores_z, "p_valores" : p_valores, "comparaciones" : comparaciones, "alphas" : alphas,
    "resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}



def finner_multitest(m, comparaciones, valores_z, p_valores, alpha=0.05):
    """MultiTest POST-HOC de Finner.

    .. note:: Sigue un proceso igual al test de Holm pero cada p-valor asociado con la hipótesis H_i se compara como:
              :math:`p_i <= \\frac{\\alpha}{1-(1-\\alpha)^{m/i}}.`

    Args:
        m: int
            Número de comparaciones.
        comparaciones: lista de string [K*(K-1)/2]
            Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
        valores_z: lista de float [K*(K-1)/2]
            Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
        p_valores: lista de float [K*(K-1)/2]
            p-valores calculados para comparar con los niveles de significancia ajustados.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) del test de ranking principal.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            valores_z: lista de float [K*(K-1)/2]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K*(K-1)/2]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            comparaciones: lista de string [K*(K-1)/2]
                Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
            alphas: array de float [K*(K-1)/2]
                Niveles de significancia ajustados
            resultado: lista de boolean [K*(K-1)/2]
                Resultado de los tests de contraste de hipótesis. True es que se rechaza la hipótesis nula y False que no se
                rechaza.
            p_valores_ajustados: lista de float [K*(K-1)/2]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia proporcionado sin ajustar.

    References:
        1. H. Finner, "On a monotonicity problem in step-down multiple test procedures", Journal of the American Statistical Association 88 (1993) 920–923
    """

    #Valores alphas.
    alphas = []
    for i in range(1,m+1):
        alphas.append(1-(1-alpha)**(m/float(i)))

    #Cálculo de los resultados.
    resultado = [False]*m
    for i in range(m):
        if p_valores[i] <= alphas[i]:
            resultado[i] = True
        else:
            break

    #Cálculo de los p_valores_ajustados.
    p_valores_ajustados = []
    for i in range(m):
        v = max([1-(1-p_valores[j])**(m/float(j+1)) for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))

    return {"valores_z" : valores_z, "p_valores" : p_valores, "comparaciones" : comparaciones, "alphas" : alphas,
    "resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}



def S(K):
    """Función auxiliar del test de Shaffer.

    .. note:: Calcula la secuencia de número máximo de hipótesis que pueden ser ciertas en una comparación secuencial entre 'K'
              distribuciones.

    Args:
        k: int
            Número de distribuciones a comparar entre sí.

    Returns:
        lista de int
            Secuencia del número hipótesis que pueden ser ciertas.

    References:
        1. J.P. Shaffer. Modified sequentially rejective multiple test procedures. Journal of the American Statistical Association, 81(395):826–831, 1986.
    """

    if K == 0 or K == 1:
        return {0}
    else:
        result = set()
        for j in reversed(range(1, K+1)):
            tmp = S(K - j)
            for s in tmp:
                result = result.union({sp.special.binom(j, 2) + s})
        return list(result)



def shaffer_multitest(m, comparaciones, valores_z, p_valores, alpha=0.05):
    """MultiTest POST-HOC de Shaffer.

    .. note:: Sigue un proceso igual al test de holm multi-test pero cada p-valor asociado con la hipótesis H_i se compara como
              :math:`p_i <= \\frac{\\alpha}{t_i},` donde t_i es el número máximo de hipótesis posibles suponiendo que las (j-1)
              anteriores han sido rechazadas.

    Args:
        m: int
            Número de comparaciones.
        comparaciones: lista de string [K*(K-1)/2]
            Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
        valores_z: lista de float [K*(K-1)/2]
            Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
        p_valores: lista de float [K*(K-1)/2]
            p-valores calculados para comparar con los niveles de significancia ajustados.
        alpha: float, optional (default = 0.05)
            Nivel de significancia (probabilidad de error tipo 1) del test de ranking principal.

    Returns:
        dict: diccionario que contiene los siguientes elementos::

            valores_z: lista de float [K*(K-1)/2]
                Estadísticos calculados durante el test. Siguen una normal (0, 1) y están ordenados según los p_valores.
            p_valores: lista de float [K*(K-1)/2]
                p-valores calculados para comparar con los niveles de significancia ajustados.
            comparaciones: lista de string [K*(K-1)/2]
                Nombres de las hipótesis contrastadas. Por ejemplo "algoritmoA vs algoritmoB".
            alphas: array de float [K*(K-1)/2]
                Niveles de significancia ajustados
            resultado: lista de boolean [K*(K-1)/2]
                Resultado de los tests de contraste de hipótesis. True es que se rechaza la hipótesis nula y False que no se
                rechaza.
            p_valores_ajustados: lista de float [K*(K-1)/2]
                p-valores ajustados, los cuales pueden ser comparados con el nivel de significancia proporcionado sin ajustar.

    References:
        1. J.P. Shaffer. Modified sequentially rejective multiple test procedures. Journal of the American Statistical Association, 81(395):826–831, 1986.
    """

    #Número máximo de hipótesis posibles.
    K = int((1 + sp.sqrt(1+4*m*2))/2)
    A = S(K)
    t = []

    #Valores alphas.
    alphas = []
    for i in range(1,m+1):
        t.insert(i-1,max([a for a in A if a <= m-i+1]))
        alphas.append(alpha/float(t[i-1]))

    #Cálculo de los resultados.
    resultado = [False]*m
    for i in range(m):
        if p_valores[i] <= alphas[i]:
            resultado[i] = True
        else:
            break

    #Cálculo de los p_valores ajustados.
    p_valores_ajustados = []
    for i in range(m):
        v = max([t[j]*p_valores[j] for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))

    return {"valores_z" : valores_z, "p_valores" : p_valores, "comparaciones" : comparaciones, "alphas" : alphas,
            "resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}
