# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 17:11:34 2014

@author: Adrián
"""

import scipy as sp
import scipy.stats as st

def anova_test(matriz_datos, alpha):
    
    """
    Hipótesis:
    
    Ho: No hay diferencia en las medias del factor de columna.
    Ha: Al menos una media del factor de columna es diferente.

    Ho: No hay diferencia en las medias de la variable de renglón.
    Ha: Al menos una media de la variable de renglón es diferente.
    """
    
    #Matriz para pruebas.
    matriz_datos = [[27,21,25],
                    [31,33,35],
                    [42,39,39],
                    [38,41,37],
                    [45,46,45]]
    
    #Número de conjuntos de datos.
    N = len(matriz_datos)
    #Número de algoritmos.
    K = len(matriz_datos[0])
    
    #Medias
    media_algoritmos = []
    for i in range(len(matriz_datos[0])):
        media_algoritmos.append(sp.mean([conjunto[i] for conjunto in matriz_datos]))
        
    media_conjunto_datos = []
    for conjunto in matriz_datos:
        media_conjunto_datos.append(sp.mean(conjunto))
    
    media_total = sp.mean(media_algoritmos)
    
    print media_algoritmos, media_conjunto_datos, media_total
    
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
    #Varianza dentro de los conjuntos de datos.
    SCBL = 0
    for j in range(N):
        SCBL = SCBL + (K*(media_conjunto_datos[j]-media_total)**2)
        
    #Grados de libertad.
    GLT = (N*K)-1
    GLTR = K-1
    GLBL = N-1
    GLE = GLT - GLTR
        
    #Cuadrados medios (suma cuadrados / grados de libertad)
    CMT = SCT/GLT
    CMTR = SCTR/GLTR
    CME = SCE/GLE
    CMBL = SCBL/GLBL
    
    #Estadísticos (para contrastar diferencia en las medias del factor de columna TR y en
    #en las medias de la variable de renglón BL)
    F1 = CMTR/CME
    F2 = CMBL/CME
    
    #Cáculo de los p_valores.
    st.fprob()