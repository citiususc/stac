# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 12:49:31 2014

@author: Adrián
"""

import sys, os
sys.path = [os.path.dirname(__file__), os.path.dirname(os.path.dirname(__file__))] + sys.path
from bottle import route, run, response, request
import scipy.stats as st
import numpy as np
from stac import nonparametric_tests as npt
from utils import clean_missing_values
import json

def headers(func):
    def func_wrapper(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.content_type = "application/json"
        try :
            return json.dumps(func(*args, **kwargs))
        except Exception, error:
            return json.dumps({"error": error})
    return func_wrapper


@route('/wilcoxon', method="POST")
@route('/wilcoxon/<alpha:float>', method="POST")
@headers
def wilcoxon(alpha=0.05):
    values = clean_missing_values(request.json['values'])
    statistic, p_value = st.wilcoxon(values.values()[0], values.values()[1])
    result = np.asscalar(p_value<alpha)
    return {"result" : result, "statistic" : statistic, "p_value" : p_value}
    
	
@route('/mannwhitneyu/', method="POST")
@route('/mannwhitneyu/<alpha:float>', method="POST")
@headers
def mannwhitneyu(alpha=0.05):
    values = clean_missing_values(request.json['values'], delete_row=False)
    statistic, p_value = st.mannwhitneyu(values.values()[0], values.values()[1], use_continuity="false")
    result = np.asscalar(p_value*2<alpha)
    return {"result" : result, "statistic" : statistic, "p_value" : p_value*2}
    

def ranking(func):
    def func_wrapper(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.content_type = "application/json"
        statistic, p_value, rankings, names, comparisons, z_values, adj_p_values = func(*args, **kwargs)
        return {
            "ranking": {
                "statistic": statistic, 
                "p_value": p_value, 
                "rankings": rankings,
                "names": names
            },
            "post_hoc": {
                "comparisons": comparisons,
                "statistic": z_values,
                "p_value": adj_p_values
            }
        }
    return func_wrapper

@route('/friedman/', method="POST")
@route('/friedman/<alpha:float>', method="POST")
@route('/friedman/<post_hoc>', method="POST")
@route('/friedman/<post_hoc>/<alpha:float>', method="POST")
@headers
@ranking
def friedman(alpha=0.05, post_hoc="bonferroni_dunn_test"):
    values = clean_missing_values(request.json['values'])
    statistic, p_value, rankings, ranking_cmp = npt.friedman_test(*values.values())
    rankings, names = map(list, zip(*sorted(zip(rankings, values.keys()), key=lambda t: t[0])))
    ranks = {key: ranking_cmp[i] for i,key in enumerate(values.keys())}
    comparisons, z_values, _, adj_p_values = getattr(npt, post_hoc)(ranks)
    return statistic, p_value, rankings, names, comparisons, z_values, adj_p_values


#Servicio para el test de los Rangos Alineados de Friedman.
#@route('/rangos-alineados/<id_fichero>/<test_comparacion>', method="GET")
#@route('/rangos-alineados/<id_fichero>/<alpha:float>/<test_comparacion>', method="GET")
#@route('/rangos-alineados/<id_fichero>/<tipo:int>/<test_comparacion>', method="GET")
#@route('/rangos-alineados/<id_fichero>/<alpha:float>/<tipo:int>/<test_comparacion>', method="GET")
#@route('/rangos-alineados/<id_fichero>', method="GET")
#@route('/rangos-alineados/<id_fichero>/<alpha:float>', method="GET")
#@route('/rangos-alineados/<id_fichero>/<tipo:int>', method="GET")
#@route('/rangos-alineados/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
#def friedman_rangos_alineados(id_fichero, alpha=0.05, tipo=0, test_comparacion="bonferroni_dunn_test"):
#
#    response.headers['Access-Control-Allow-Origin'] = '*'
#    response.content_type = "application/json"
#    try:
#        datos = lista_ficheros[id_fichero]
#    except Exception:
#        return {"fallo" : "There is no file with that key."}
#    resultado = test_ranking(friedman_rangos_alineados_test, getattr(tnp, test_comparacion), datos["nombres_algoritmos"], datos["matriz_datos"], len(datos["matriz_datos"]), alpha, tipo)
#    return json.dumps(resultado)
#
#
##Servicio para el test Quade.
#@route('/quade/<id_fichero>/<test_comparacion>', method="GET")
#@route('/quade/<id_fichero>/<alpha:float>/<test_comparacion>', method="GET")
#@route('/quade/<id_fichero>/<tipo:int>/<test_comparacion>', method="GET")
#@route('/quade/<id_fichero>/<alpha:float>/<tipo:int>/<test_comparacion>', method="GET")
#@route('/quade/<id_fichero>', method="GET")
#@route('/quade/<id_fichero>/<alpha:float>', method="GET")
#@route('/quade/<id_fichero>/<tipo:int>', method="GET")
#@route('/quade/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
#def quade(id_fichero, alpha=0.05, tipo=0, test_comparacion="bonferroni_dunn_test"):
#
#    response.headers['Access-Control-Allow-Origin'] = '*'
#    response.content_type = "application/json"
#    try:
#        datos = lista_ficheros[id_fichero]
#    except Exception:
#        return {"fallo" : "There is no file with that key."}
#    resultado = test_ranking(quade_test, getattr(tnp, test_comparacion), datos["nombres_algoritmos"], datos["matriz_datos"], len(datos["matriz_datos"]), alpha, tipo)
#    return json.dumps(resultado)
#
#
##Servicio para el test de normalidad de Shapiro-Wilk.
#@route('/shapiro/<id_fichero>', method="GET")
#@route('/shapiro/<id_fichero>/<alpha:float>', method="GET")
#def shapiro(id_fichero, alpha=0.05):
#    response.headers['Access-Control-Allow-Origin'] = '*'
#    response.content_type = "application/json"
#    try:
#        datos = lista_ficheros[id_fichero]
#    except Exception:
#        return {"fallo" : "There is no file with that key."}
#    estadisticos_w = []
#    p_valores = []
#    resultados = []
#    for i in range(len(datos["matriz_datos"][0])):
#        try:
#            resultado_shapiro = st.shapiro([conjunto[i] for conjunto in datos["matriz_datos"]])
#            estadisticos_w.append(resultado_shapiro[0])
#            p_valores.append(resultado_shapiro[1])
#            #Si p_valor < alpha, se rechaza la hipótesis "True" de que la muestra provenga de una distribución normal.
#            resultados.append(resultado_shapiro[1]<alpha)
#        except Exception, fallo:
#            return {"fallo" : str(fallo)}
#    return json.dumps({"result" : resultados, "w" : estadisticos_w, "p_value" : p_valores, "dataset": datos["nombres_algoritmos"]})
#
#
##Servicio para el test de normalidad de Kolmogorov-Smirnov.
#@route('/kolmogorov/<id_fichero>', method="GET")
#@route('/kolmogorov/<id_fichero>/<alpha:float>', method="GET")
#def kolmogorov(id_fichero, alpha=0.05):
#    response.headers['Access-Control-Allow-Origin'] = '*'
#    response.content_type = "application/json"
#    try:
#        datos = lista_ficheros[id_fichero]
#    except Exception:
#        return {"fallo" : "There is no file with that key."}
#    estadisticos_d = []
#    p_valores = []
#    resultados = []
#    for i in range(len(datos["matriz_datos"][0])):
#        try:
#            resultado_kolmogorov = st.kstest([conjunto[i] for conjunto in datos["matriz_datos"]], 'norm')
#            estadisticos_d.append(resultado_kolmogorov[0])
#            p_valores.append(resultado_kolmogorov[1])
#            #Si p_valor < alpha, se rechaza la hipótesis "True" de que la muestra provenga de una distribución normal.
#            resultados.append(np.asscalar(resultado_kolmogorov[1]<alpha))
#        except Exception, fallo:
#            return {"fallo" : str(fallo)}
#    return json.dumps({"resultado" : resultados, "estadisticos_d" : estadisticos_d, "p_valores" : p_valores})
#
#
##Servicio para el test de normalidad de D'Agostino-Pearson.
#@route('/agostino/<id_fichero>', method="GET")
#@route('/agostino/<id_fichero>/<alpha:float>', method="GET")
#def agostino(id_fichero, alpha=0.05):
#    response.headers['Access-Control-Allow-Origin'] = '*'
#    response.content_type = "application/json"
#    try:
#        datos = lista_ficheros[id_fichero]
#    except Exception:
#        return {"fallo" : "There is no file with that key."}
#    try:
#        estadisticos_k2, p_valores = st.normaltest(datos["matriz_datos"],axis=0)
#        #Si p_valor < alpha, se rechaza la hipótesis "True" de que la muestra provenga de una distribución normal.
#        resultados = [np.asscalar(p_valores[i]<alpha) for i in range(len(p_valores))]
#    except Exception, fallo:
#        return {"fallo" : str(fallo)}
#    return json.dumps({"resultado" : resultados, "estadisticos_k2" : estadisticos_k2.tolist(), "p_valores" : p_valores.tolist()})
#
#
##Servicio para el test de homocedasticidad de Levene.
#@route('/levene/<id_fichero>', method="GET")
#@route('/levene/<id_fichero>/<alpha:float>', method="GET")
#def levene(id_fichero, alpha=0.05):
#    response.headers['Access-Control-Allow-Origin'] = '*'
#    response.content_type = "application/json"
#    try:
#        datos = lista_ficheros[id_fichero]
#    except Exception:
#        return {"fallo" : "There is no file with that key."}
#    argumentos = ()
#    for i in range(len(datos["matriz_datos"][0])):
#        argumentos = argumentos + ([conjunto[i] for conjunto in datos["matriz_datos"]],)
#    try:
#        estadistico_w, p_valor = st.levene(*argumentos)
#        #Si p_valor < alpha, se rechaza la hipótesis "True" de que las muestras de entrada provengan de poblaciones con
#        #varianzas similares.
#        resultado = np.asscalar(p_valor<alpha)
#    except Exception, fallo:
#        return {"fallo" : str(fallo)}
#    return json.dumps({"resultado" : resultado, "estadistico_w" : estadistico_w, "p_valor" : p_valor})
#
#
##Servicio para el test paramétrico T-Test.
#@route('/ttest/<id_fichero>', method="GET")
#@route('/ttest/<id_fichero>/<alpha:float>', method="GET")
#def ttest(id_fichero, alpha=0.05):
#    response.headers['Access-Control-Allow-Origin'] = '*'
#    response.content_type = "application/json"
#    try:
#        datos = lista_ficheros[id_fichero]
#    except Exception:
#        return {"fallo" : "There is no file with that key.."}
#    if len(datos["matriz_datos"][0]) != 2:
#        return {"fallo" : "Require only two samples."}
#    else:
#        argumentos = ()
#        for i in range(len(datos["matriz_datos"][0])):
#            argumentos = argumentos + ([conjunto[i] for conjunto in datos["matriz_datos"]],)
#        try:
#            estadistico_t, p_valor = st.ttest_ind(*argumentos)
#            #Si p_valor < alpha, se rechaza la hipótesis "True" de que las 2 muestras relacionadas o repetidas
#            #tienen idénticos valores promedio (esperados).
#            resultado = np.asscalar(p_valor<alpha)
#        except Exception, fallo:
#            return {"fallo" : str(fallo)}
#        return json.dumps({"resultado" : resultado, "estadistico_t" : estadistico_t.tolist(), "p_valor" : p_valor})
#
#
##Servicio para el test paramétrico ANOVA.
#@route('/anova/<id_fichero>', method="GET")
#@route('/anova/<id_fichero>/<alpha:float>', method="GET")
#def anova(id_fichero, alpha=0.05):
#    response.headers['Access-Control-Allow-Origin'] = '*'
#    response.content_type = "application/json"
#    try:
#        datos = lista_ficheros[id_fichero]
#    except Exception:
#        return {"fallo" : "There is no file with that key."}
#    res_anova = anova_test(datos["matriz_datos"],alpha)
#
#    res_comparacion = bonferroni_test(datos["nombres_algoritmos"],res_anova["medias_algoritmos"],res_anova["cuadrados_medios"][2],len(datos["matriz_datos"]),alpha)
#    return json.dumps({"test_anova" : res_anova, "test_comparacion" : res_comparacion})



if __name__ == '__main__':
    run(reloader=True, host='localhost', port=8080, quiet=True)

