# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 12:49:31 2014

@author: Adrián
"""

from bottle import route, run, response, request
import scipy.stats as st
import numpy as np
from stac import tests_no_parametricos as tnp
from stac import *
from utils import LimitedSizeDict, leer_datos, generar_md5
import json

lista_ficheros = LimitedSizeDict(size_limit=5)


#Servicio para la subida de ficheros.
@route('/file', method='POST')
def post_file():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    subida = request.files.get('file')
    clave_hash = generar_md5(subida.file)
    for clave in lista_ficheros.keys():
        if clave == clave_hash:
            return {"hash" : clave_hash}
    try:
        datos = leer_datos(subida.file)
    except Exception, fallo:
        return {"fallo" : str(fallo)}
    lista_ficheros[clave_hash] = datos
    
    return {"hash" : clave_hash}


#Servicio para la consulta de ficheros.
@route('/file/<id_fichero>', method='GET')
def get_file(id_fichero):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    #Consulta del contenido de un fichero en concreto.
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key."}
    return datos


#Servicio para el test de Wilcoxon.
@route('/wilcoxon/<id_fichero>', method="GET")
@route('/wilcoxon/<id_fichero>/<alpha:float>', method="GET")
def wilcoxon(id_fichero, alpha=0.05):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.content_type = "application/json"
	try:
		datos = lista_ficheros[id_fichero]
	except Exception:
		return {"error" : "There is no file with that key."}
	try:
		statistic, p_value = st.wilcoxon([v[0] for v in datos["matriz_datos"]], [v[1] for v in datos["matriz_datos"]])
		result = np.asscalar(p_value<alpha)
	except Exception, fallo:
		return {"error" : str(fallo)}
	return json.dumps({"result" : result, "statistic" : statistic, "p_value" : p_value})
	
@route('/mannwhitneyu/<id_fichero>', method="GET")
@route('/mannwhitneyu/<id_fichero>/<alpha:float>', method="GET")
def mannwhitneyu(id_fichero, alpha=0.05):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.content_type = "application/json"
	try:
		datos = lista_ficheros[id_fichero]
	except Exception:
		return {"error" : "There is no file with that key."}
	try:
		statistic, p_value = st.mannwhitneyu([v[0] for v in datos["matriz_datos"]], [v[1] for v in datos["matriz_datos"]], "false")
		result = np.asscalar(p_value*2<alpha)
	except Exception, fallo:
		return {"error" : str(fallo)}
	return json.dumps({"result" : result, "statistic" : statistic, "p_value" : p_value*2})


#Servicio para el test de Friedman.
@route('/friedman/<id_fichero>/<test_comparacion>', method="GET")
@route('/friedman/<id_fichero>/<alpha:float>/<test_comparacion>', method="GET")
@route('/friedman/<id_fichero>/<tipo:int>/<test_comparacion>', method="GET")
@route('/friedman/<id_fichero>/<alpha:float>/<tipo:int>/<test_comparacion>', method="GET")
@route('/friedman/<id_fichero>', method="GET")
@route('/friedman/<id_fichero>/<alpha:float>', method="GET")
@route('/friedman/<id_fichero>/<tipo:int>', method="GET")
@route('/friedman/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def friedman(id_fichero, alpha=0.05, tipo=0, test_comparacion="bonferroni_dunn_test"):

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key."}
    resultado = test_ranking(friedman_test, getattr(tnp, test_comparacion), datos["nombres_algoritmos"], datos["matriz_datos"], len(datos["matriz_datos"]), alpha, tipo)
    return json.dumps(resultado)


#Servicio para el test de Iman-Davenport.
@route('/iman-davenport/<id_fichero>/<test_comparacion>', method="GET")
@route('/iman-davenport/<id_fichero>/<alpha:float>/<test_comparacion>', method="GET")
@route('/iman-davenport/<id_fichero>/<tipo:int>/<test_comparacion>', method="GET")
@route('/iman-davenport/<id_fichero>/<alpha:float>/<tipo:int>/<test_comparacion>', method="GET")
@route('/iman-davenport/<id_fichero>', method="GET")
@route('/iman-davenport/<id_fichero>/<alpha:float>', method="GET")
@route('/iman-davenport/<id_fichero>/<tipo:int>', method="GET")
@route('/iman-davenport/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def iman_davenport(id_fichero, alpha=0.05, tipo=0, test_comparacion="bonferroni_dunn_test"):

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key."}
    resultado = test_ranking(iman_davenport_test, getattr(tnp, test_comparacion), datos["nombres_algoritmos"], datos["matriz_datos"], len(datos["matriz_datos"]), alpha, tipo)
    return json.dumps(resultado)


#Servicio para el test de los Rangos Alineados de Friedman.
@route('/rangos-alineados/<id_fichero>/<test_comparacion>', method="GET")
@route('/rangos-alineados/<id_fichero>/<alpha:float>/<test_comparacion>', method="GET")
@route('/rangos-alineados/<id_fichero>/<tipo:int>/<test_comparacion>', method="GET")
@route('/rangos-alineados/<id_fichero>/<alpha:float>/<tipo:int>/<test_comparacion>', method="GET")
@route('/rangos-alineados/<id_fichero>', method="GET")
@route('/rangos-alineados/<id_fichero>/<alpha:float>', method="GET")
@route('/rangos-alineados/<id_fichero>/<tipo:int>', method="GET")
@route('/rangos-alineados/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def friedman_rangos_alineados(id_fichero, alpha=0.05, tipo=0, test_comparacion="bonferroni_dunn_test"):

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key."}
    resultado = test_ranking(friedman_rangos_alineados_test, getattr(tnp, test_comparacion), datos["nombres_algoritmos"], datos["matriz_datos"], len(datos["matriz_datos"]), alpha, tipo)
    return json.dumps(resultado)


#Servicio para el test Quade.
@route('/quade/<id_fichero>/<test_comparacion>', method="GET")
@route('/quade/<id_fichero>/<alpha:float>/<test_comparacion>', method="GET")
@route('/quade/<id_fichero>/<tipo:int>/<test_comparacion>', method="GET")
@route('/quade/<id_fichero>/<alpha:float>/<tipo:int>/<test_comparacion>', method="GET")
@route('/quade/<id_fichero>', method="GET")
@route('/quade/<id_fichero>/<alpha:float>', method="GET")
@route('/quade/<id_fichero>/<tipo:int>', method="GET")
@route('/quade/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def quade(id_fichero, alpha=0.05, tipo=0, test_comparacion="bonferroni_dunn_test"):

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key."}
    resultado = test_ranking(quade_test, getattr(tnp, test_comparacion), datos["nombres_algoritmos"], datos["matriz_datos"], len(datos["matriz_datos"]), alpha, tipo)
    return json.dumps(resultado)


#Servicio para el test de normalidad de Shapiro-Wilk.
@route('/shapiro/<id_fichero>', method="GET")
@route('/shapiro/<id_fichero>/<alpha:float>', method="GET")
def shapiro(id_fichero, alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key."}
    estadisticos_w = []
    p_valores = []
    resultados = []
    for i in range(len(datos["matriz_datos"][0])):
        try:
            resultado_shapiro = st.shapiro([conjunto[i] for conjunto in datos["matriz_datos"]])
            estadisticos_w.append(resultado_shapiro[0])
            p_valores.append(resultado_shapiro[1])
            #Si p_valor < alpha, se rechaza la hipótesis "True" de que la muestra provenga de una distribución normal.
            resultados.append(resultado_shapiro[1]<alpha)
        except Exception, fallo:
            return {"fallo" : str(fallo)}
    return json.dumps({"result" : resultados, "w" : estadisticos_w, "p_value" : p_valores, "dataset": datos["nombres_algoritmos"]})


#Servicio para el test de normalidad de Kolmogorov-Smirnov.
@route('/kolmogorov/<id_fichero>', method="GET")
@route('/kolmogorov/<id_fichero>/<alpha:float>', method="GET")
def kolmogorov(id_fichero, alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key."}
    estadisticos_d = []
    p_valores = []
    resultados = []
    for i in range(len(datos["matriz_datos"][0])):
        try:
            resultado_kolmogorov = st.kstest([conjunto[i] for conjunto in datos["matriz_datos"]], 'norm')
            estadisticos_d.append(resultado_kolmogorov[0])
            p_valores.append(resultado_kolmogorov[1])
            #Si p_valor < alpha, se rechaza la hipótesis "True" de que la muestra provenga de una distribución normal.
            resultados.append(np.asscalar(resultado_kolmogorov[1]<alpha))
        except Exception, fallo:
            return {"fallo" : str(fallo)}
    return json.dumps({"resultado" : resultados, "estadisticos_d" : estadisticos_d, "p_valores" : p_valores})


#Servicio para el test de normalidad de D'Agostino-Pearson.
@route('/agostino/<id_fichero>', method="GET")
@route('/agostino/<id_fichero>/<alpha:float>', method="GET")
def agostino(id_fichero, alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key."}
    try:
        estadisticos_k2, p_valores = st.normaltest(datos["matriz_datos"],axis=0)
        #Si p_valor < alpha, se rechaza la hipótesis "True" de que la muestra provenga de una distribución normal.
        resultados = [np.asscalar(p_valores[i]<alpha) for i in range(len(p_valores))]
    except Exception, fallo:
        return {"fallo" : str(fallo)}
    return json.dumps({"resultado" : resultados, "estadisticos_k2" : estadisticos_k2.tolist(), "p_valores" : p_valores.tolist()})


#Servicio para el test de homocedasticidad de Levene.
@route('/levene/<id_fichero>', method="GET")
@route('/levene/<id_fichero>/<alpha:float>', method="GET")
def levene(id_fichero, alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key."}
    argumentos = ()
    for i in range(len(datos["matriz_datos"][0])):
        argumentos = argumentos + ([conjunto[i] for conjunto in datos["matriz_datos"]],)
    try:
        estadistico_w, p_valor = st.levene(*argumentos)
        #Si p_valor < alpha, se rechaza la hipótesis "True" de que las muestras de entrada provengan de poblaciones con
        #varianzas similares.
        resultado = np.asscalar(p_valor<alpha)
    except Exception, fallo:
        return {"fallo" : str(fallo)}
    return json.dumps({"resultado" : resultado, "estadistico_w" : estadistico_w, "p_valor" : p_valor})


#Servicio para el test paramétrico T-Test.
@route('/ttest/<id_fichero>', method="GET")
@route('/ttest/<id_fichero>/<alpha:float>', method="GET")
def ttest(id_fichero, alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key.."}
    if len(datos["matriz_datos"][0]) != 2:
        return {"fallo" : "Require only two samples."}
    else:
        argumentos = ()
        for i in range(len(datos["matriz_datos"][0])):
            argumentos = argumentos + ([conjunto[i] for conjunto in datos["matriz_datos"]],)
        try:
            estadistico_t, p_valor = st.ttest_ind(*argumentos)
            #Si p_valor < alpha, se rechaza la hipótesis "True" de que las 2 muestras relacionadas o repetidas
            #tienen idénticos valores promedio (esperados).
            resultado = np.asscalar(p_valor<alpha)
        except Exception, fallo:
            return {"fallo" : str(fallo)}
        return json.dumps({"resultado" : resultado, "estadistico_t" : estadistico_t.tolist(), "p_valor" : p_valor})


#Servicio para el test paramétrico ANOVA.
@route('/anova/<id_fichero>', method="GET")
@route('/anova/<id_fichero>/<alpha:float>', method="GET")
def anova(id_fichero, alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "There is no file with that key."}
    res_anova = anova_test(datos["matriz_datos"],alpha)

    res_comparacion = bonferroni_test(datos["nombres_algoritmos"],res_anova["medias_algoritmos"],res_anova["cuadrados_medios"][2],len(datos["matriz_datos"]),alpha)
    return json.dumps({"test_anova" : res_anova, "test_comparacion" : res_comparacion})



if __name__ == '__main__':
    run(reloader=True, host='localhost', port=8080, quiet=True)

