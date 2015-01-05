

import numpy as np
import scipy as sp
import scipy.stats as st

def anova_test(matriz_datos, alpha=0.05):

    N = len(matriz_datos)

    K = len(matriz_datos[0])

    medias_algoritmos = []
    for columna in zip(*matriz_datos):
        medias_algoritmos.append(sp.mean(columna))

    media_general = sp.mean(medias_algoritmos)

    SCT = 0

    SCE = 0

    SCTR = 0
    for i in range(len(matriz_datos[0])):
    	x  = [conjunto[i] for conjunto in matriz_datos]
    	for elem in x:
    	    SCT = SCT + (elem-media_general)**2
    	    SCE = SCE + (elem-medias_algoritmos[i])**2
    	SCTR = SCTR + (len(x)*(medias_algoritmos[i]-media_general)**2)

    GLT = (N*K)-1
    GLTR = K-1
    GLE = GLT - GLTR

    CMT = SCT/GLT
    CMTR = SCTR/GLTR
    CME = SCE/GLE

    F = CMTR/CME

    p_valor = 1 - st.f.cdf(F, GLTR, GLE)

    return {"resultado" : np.asscalar(p_valor < alpha), "p_valor" : p_valor, "estadistico" : F,
    	    "variaciones" : [SCT,SCTR,SCE], "grados_libertad" : [GLT,GLTR,GLE],
    	    "cuadrados_medios" : [CMT,CMTR,CME], "medias_algoritmos" : medias_algoritmos,
    	    "media_general" : media_general}



def bonferroni_test(nombres_algoritmos, medias_algoritmos, cuadrado_medio_error, N, alpha=0.05):

	K = len(medias_algoritmos)

	m = (K*(K-1))/2

	comparaciones = []
	for i in range(K-1):
		for j in range(i+1,K):
			comparaciones.append(nombres_algoritmos[i] + " vs " + nombres_algoritmos[j])

	valores_t = []
	for i in range(K-1):
		for j in range(i+1,K):
			valores_t.append((abs(medias_algoritmos[i]-medias_algoritmos[j]))/float(sp.sqrt(cuadrado_medio_error)*sp.sqrt(2/float(N))))

	p_valores = []
	for i in range(m):
		p_valores.append(1-st.t.cdf(valores_t[i],(N*K)-K))

	tabla = zip(comparaciones,valores_t,p_valores)
	tabla.sort(key=lambda valor: valor[2])
	c, z, p = zip(*tabla)
	comparaciones = list(c)
	valores_t = list(z)
	p_valores = list(p)

	alpha2 = alpha/float(m)

	resultado = []
	for i in range(m):
		resultado.append(np.asscalar(p_valores[i]<alpha2))

	p_valores_ajustados = []
	for i in range(m):
		v = m*p_valores[i]
		p_valores_ajustados.append(min(v,1))

	return {"valores_t" : valores_t, "p_valores" : p_valores, "comparaciones" : comparaciones, "alpha" : alpha2,
			"resultado" : resultado, "p_valores_ajustados" : p_valores_ajustados}
