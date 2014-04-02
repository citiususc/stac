# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 17:11:34 2014

@author: Adrián
"""

import scipy as sp
import scipy.stats as st

def anova_test(matriz_datos, alpha):
    
    """
    Hipótesis (¿Dos vías?):
    
    Ho: No hay diferencia en las medias del factor de columna (algoritmos).
    Ha: Al menos una media del factor de columna es diferente.

    Ho: No hay diferencia en las medias de la variable de renglón (conjuntos de datos).
    Ha: Al menos una media de la variable de renglón es diferente.
    """
    
    #Número de conjuntos de datos.
    N = len(matriz_datos)
    #Número de algoritmos.
    K = len(matriz_datos[0])
    
    #Medias algoritmos (medias del factor de columna).
    media_algoritmos = []
    for i in range(len(matriz_datos[0])):
        media_algoritmos.append(sp.mean([conjunto[i] for conjunto in matriz_datos]))
    
    #Medias de conjuntos de datos (medias de la variable renglón).
    media_conjunto_datos = []
    for conjunto in matriz_datos:
        media_conjunto_datos.append(sp.mean(conjunto))
    
    #Media de medias o media total.
    media_total = sp.mean(media_algoritmos)
    
    #Varianzas: total, dentro de los algoritmos, entre algoritmos.
    SCT = 0
    SCE = 0
    SCTR = 0
    for i in range(len(matriz_datos[0])):
        x  = [conjunto[i] for conjunto in matriz_datos]
        for elem in x:
            SCT = SCT + (elem-media_total)**2
            SCE = SCE + (elem-media_algoritmos[i])**2
        SCTR = SCTR + (N*(media_algoritmos[i]-media_total)**2)
    #Varianza entre conjuntos de datos.
    SCBL = 0
    for j in range(N):
        SCBL = SCBL + (K*(media_conjunto_datos[j]-media_total)**2)
        
    #Grados de libertad.
    GLT = (N*K)-1
    GLTR = K-1
    GLBL = N-1
    GLE = GLT - GLTR
        
    #Cuadrados medios (suma cuadrados / grados de libertad)
    #CMT = SCT/GLT
    CMTR = SCTR/GLTR
    CME = SCE/GLE
    CMBL = SCBL/GLBL
    
    #Estadísticos (para contrastar diferencia en las medias del factor de columna TR y en
    #en las medias de la variable de renglón BL)
    F1 = CMTR/CME
    F2 = CMBL/CME
    
    #Cáculo de los p_valores.
    p_valor_F1 = 1 - st.f.cdf(F1, GLTR, GLE)
    p_valor_F2 = 1 - st.f.cdf(F2, GLBL, GLE)
    print 1 - st.f.cdf(178.9, 2, 12)
    
    #Resultados.
    resultados = [str(p_valor_F1 < alpha), str(p_valor_F2 < alpha)]
    
    return {"resultados" : resultados, "p_valores" : [p_valor_F1, p_valor_F2], "estadisticos" : [F1,F2],
            "cuadrados_medios" : [CMTR,CMBL], "cuadrado_medio_error" : CME, "medias_algoritmos" : media_algoritmos,
            "medias_conjuntos" : media_conjunto_datos, "media_global" : media_total}



def bonferroni_test(nombres_algoritmos, nombres_conj_datos, medias_algoritmos, cuadrado_medio_error, alpha):
    
    #Número de algoritmos K.
    K = len(medias_algoritmos)
    
    #Número de conjuntos de datos N.
    N = len(nombres_conj_datos)

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
    
    print comparaciones
    print valores_t
    print p_valores
    

datos = [[0.752,0.773,0.785,0.795],
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
#print anova_test(datos, 0.05)
bonferroni_test(["PDFC","NNEP","IS-CHC+INN","FH-GBML"],["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"],[0.84937499999999977, 0.8085416666666666, 0.79345833333333315, 0.75516666666666665],0.022017531250000003,0.05)