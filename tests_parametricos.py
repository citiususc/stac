# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 17:11:34 2014

@author: Adrián
"""

import scipy as sp
import scipy.stats as st

def anova_test(matriz_datos, alpha):
    
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
    
    return {"resultado" : str(p_valor<alpha), "p_valor" : p_valor, "estadistico" : F,
            "variaciones" : [SCT,SCTR,SCE], "grados_libertad" : [GLT,GLTR,GLE],
            "cuadrados_medios" : [CMT,CMTR,CME], "medias_algoritmos" : medias_algoritmos,
            "media_general" : media_general}



def bonferroni_test(nombres_algoritmos, N, medias_algoritmos, cuadrado_medio_error, alpha):
    
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
        resultado.append(p_valores[i]<alpha2)
        
    #Cálculo de los p_valores ajustados.
    p_valores_ajustados = []
    for i in range(m):
        v = m*p_valores[i]
        p_valores_ajustados.append(min(v,1))
        
    #Para seralizar JSON.
    resultado = [str(x) for x in resultado]
    
    return {"valores_t" : valores_t, "p_valores" : p_valores, "comparaciones" : comparaciones, "alpha" : alpha2,
            "resultado" : resultado, "p_valores ajustados" : p_valores_ajustados}



datos = [[27,21,25],[31,33,35],[42,39,39],[38,41,37],[45,46,45]]
print anova_test(datos, 0.05)
print bonferroni_test(["A","B","C"],5,[36.600000000000001, 36.0, 36.200000000000003],67.166666666666671,0.05)