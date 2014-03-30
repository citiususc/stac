# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 12:49:31 2014

@author: Adrián
"""

from bottle import route, run, response, request
import scipy.stats as st
import itertools
import tests_no_parametricos as tnp
import csv, re, hashlib

lista_ficheros = {}

#Función para leer los datos de un fichero.
def leer_datos(archivo):
    patron_numeros = re.compile('^\d+(\.\d+)?([eE][+-]?\d+)?$')

    palabra = ""
    nombres_conj_datos = []
    nombres_algoritmos = []
    matriz_datos = []

    lector = csv.reader(archivo)

    numero_linea = 0

    for fila in lector:
        if len(fila)<3:
            raise Exception("Error formato datos.")
        if numero_linea == 0:
            for i in range(len(fila)):
                if i == 0:
                    palabra = fila[i]
                else:
                    if nombres_algoritmos.count(fila[i]) == 0:
                        nombres_algoritmos.append(fila[i])
                    else:
                        raise Exception("Nombre de algoritmo repetido.")
        else:
            numero_algoritmos = len(nombres_algoritmos)
            if len(fila) != numero_algoritmos + 1:
                raise Exception("Error formato datos")
            lista_datos = []
            for i in range(len(fila)):
                if i == 0:
                    if nombres_conj_datos.count(fila[i]) == 0:
                        nombres_conj_datos.append(fila[i])
                    else:
                        raise Exception("Nombre conjunto datos repetido.")
                else:
                    m = patron_numeros.match(fila[i])
                    if m:
                        dato = float(fila[i])
                        lista_datos.append(dato)
                    else:
                        raise Exception("Número \"" + fila[i] + "\" no valido en línea " + str(numero_linea+1) +".")
            matriz_datos.append(lista_datos)
        numero_linea = numero_linea + 1
        
    return {"palabra" : palabra, "nombres_conj_datos" : nombres_conj_datos, "nombres_algoritmos" : nombres_algoritmos,
        "matriz_datos" : matriz_datos}


#Función para generar el resumen hash MD5 de los ficheros.
def generar_md5(archivo):
    tam_bloque = 65536
    md5 = hashlib.md5()
    bufer = archivo.read(tam_bloque)
    while len(bufer) > 0:
        md5.update(bufer)
        bufer = archivo.read(tam_bloque)
    archivo.seek(0, 0);
    return md5.hexdigest()


#Servicio para la subida de ficheros.
@route('/fichero', method='POST')
def subir_fichero():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    subida = request.files.get('fichero')
    clave_hash = generar_md5(subida.file)
    for clave in lista_ficheros.keys():
        if clave == clave_hash:
            return {"fallo" : "El fichero con hash \"" + clave + "\" ya se encuentra el servidor."}
    try:
        datos = leer_datos(subida.file)
    except Exception, fallo:
        return {"fallo" : str(fallo)}
    lista_ficheros[clave_hash] = datos
    return {"clave" : clave_hash}


#Servicio para la consulta de ficheros.
@route('/fichero/<id_fichero>', method='GET')
def consultar_fichero(id_fichero):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    #Consulta del contenido de un fichero en concreto.
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningún fichero con esa clave."}
    return datos


#Servicio para el test de Wilcoxon.
@route('/wilcoxon/<id_fichero>', method="GET")
@route('/wilcoxon/<id_fichero>/<alpha:float>', method="GET")
def wilcoxon_test(id_fichero, alpha=0.05):
    """
    Servicio web para el test de los rangos signados de Wilcoxon
    
    Argumentos
    ----------
    id_fichero: string
        Identificador HASH MD5 del fichero sobre el que se quiere aplicar el test
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de Wilcoxon
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningún fichero con esa clave."}
    try:
        resultado = tnp.wilcoxon_test(datos["matriz_datos"],alpha)
    except Exception, fallo:
        return {"fallo" : str(fallo)}
    return resultado


#Servicio para el test de Friedman.
@route('/friedman/<id_fichero>/<test_comparacion>', method="GET")
@route('/friedman/<id_fichero>/<alpha:float>/<test_comparacion>', method="GET")
@route('/friedman/<id_fichero>/<tipo:int>/<test_comparacion>', method="GET")
@route('/friedman/<id_fichero>/<alpha:float>/<tipo:int>/<test_comparacion>', method="GET")
@route('/friedman/<id_fichero>', method="GET")
@route('/friedman/<id_fichero>/<alpha:float>', method="GET")
@route('/friedman/<id_fichero>/<tipo:int>', method="GET")
@route('/friedman/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def friedman_test(id_fichero, alpha=0.05, tipo=0, test_comparacion="bonferroni_dunn_test"):
    """
    Servicio web para el test de Friedman.
    
    Argumentos
    ----------
    id_fichero: string
        Identificador HASH MD5 del fichero sobre el que se quiere aplicar el test.
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta.
    tipo: string
        Indica si lo que se quiere es minimizar ("0") o maximizar ("1").
    test_comparacion: string
        Test POST-HOC a aplicar si el test de ranking encuentra diferencias
        significativas.
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de Friedman y si procede el resultado de
        aplicar el test de comparación.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningún fichero con esa clave."}
    res_ranking = tnp.friedman_test(datos["nombres_algoritmos"],datos["matriz_datos"],alpha,tipo)
    if res_ranking["resultado"] == "True":
        print len(datos["matriz_datos"])
        res_comparacion = getattr(tnp, test_comparacion)("friedman",res_ranking["nombres"],res_ranking["ranking"],len(datos["matriz_datos"]),alpha)
        return {"test_ranking" : res_ranking, "test_comparacion" : res_comparacion}
    return {"test_ranking" : res_ranking}


#Servicio para el test de Iman-Davenport.
@route('/iman-davenport/<id_fichero>/<test_comparacion>', method="GET")
@route('/iman-davenport/<id_fichero>/<alpha:float>/<test_comparacion>', method="GET")
@route('/iman-davenport/<id_fichero>/<tipo:int>/<test_comparacion>', method="GET")
@route('/iman-davenport/<id_fichero>/<alpha:float>/<tipo:int>/<test_comparacion>', method="GET")
@route('/iman-davenport/<id_fichero>', method="GET")
@route('/iman-davenport/<id_fichero>/<alpha:float>', method="GET")
@route('/iman-davenport/<id_fichero>/<tipo:int>', method="GET")
@route('/iman-davenport/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def iman_davenport_test(id_fichero, alpha=0.05, tipo=0, test_comparacion="bonferroni_dunn_test"):
    """
    Servicio web para el test de Iman-Davenport.
    
    Argumentos
    ----------
    id_fichero: string
        Identificador HASH MD5 del fichero sobre el que se quiere aplicar el test.
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta.
    tipo: string
        Indica si lo que se quiere es minimizar ("0") o maximizar ("1").
    test_comparacion: string
        Test POST-HOC a aplicar si el test de ranking encuentra diferencias
        significativas.
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de Iman-Davenport y si procede el resultado
        de aplicar el test de comparación.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningún fichero con esa clave."}
    res_ranking = tnp.iman_davenport_test(datos["nombres_algoritmos"],datos["matriz_datos"],alpha,tipo)
    if res_ranking["resultado"] == "True":
        res_comparacion = getattr(tnp, test_comparacion)("iman-davenport",res_ranking["nombres"],res_ranking["ranking"],len(datos["matriz_datos"]),alpha)
        return {"test_ranking" : res_ranking, "test_comparacion" : res_comparacion}
    return {"test_ranking" : res_ranking}


#Servicio para el test de los Rangos Alineados de Friedman.
@route('/rangos-alineados/<id_fichero>/<test_comparacion>', method="GET")
@route('/rangos-alineados/<id_fichero>/<alpha:float>/<test_comparacion>', method="GET")
@route('/rangos-alineados/<id_fichero>/<tipo:int>/<test_comparacion>', method="GET")
@route('/rangos-alineados/<id_fichero>/<alpha:float>/<tipo:int>/<test_comparacion>', method="GET")
@route('/rangos-alineados/<id_fichero>', method="GET")
@route('/rangos-alineados/<id_fichero>/<alpha:float>', method="GET")
@route('/rangos-alineados/<id_fichero>/<tipo:int>', method="GET")
@route('/rangos-alineados/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def friedman_rangos_alineados_test(id_fichero, alpha=0.05, tipo=0, test_comparacion="bonferroni_dunn_test"):
    """
    Servicio web para el test de los Rangos Alineados de Friedman.
    
    Argumentos
    ----------
    id_fichero: string
        Identificador HASH MD5 del fichero sobre el que se quiere aplicar el test.
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta.
    tipo: string
        Indica si lo que se quiere es minimizar ("0") o maximizar ("1").
    test_comparacion: string
        Test POST-HOC a aplicar si el test de ranking encuentra diferencias
        significativas.
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de los Rangos Alineados de Friedman y si
        procede el resultado de aplicar el test de comparación.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningún fichero con esa clave."}
    res_ranking = tnp.friedman_rangos_alineados_test(datos["nombres_algoritmos"],datos["matriz_datos"],alpha,tipo)
    if res_ranking["resultado"] == "True":
        res_comparacion = getattr(tnp, test_comparacion)("rangos-alineados",res_ranking["nombres"],res_ranking["ranking"],len(datos["matriz_datos"]),alpha)
        return {"test_ranking" : res_ranking, "test_comparacion" : res_comparacion}
    return {"test_ranking" : res_ranking}


#Servicio para el test Quade.
@route('/quade/<id_fichero>/<test_comparacion>', method="GET")
@route('/quade/<id_fichero>/<alpha:float>/<test_comparacion>', method="GET")
@route('/quade/<id_fichero>/<tipo:int>/<test_comparacion>', method="GET")
@route('/quade/<id_fichero>/<alpha:float>/<tipo:int>/<test_comparacion>', method="GET")
@route('/quade/<id_fichero>', method="GET")
@route('/quade/<id_fichero>/<alpha:float>', method="GET")
@route('/quade/<id_fichero>/<tipo:int>', method="GET")
@route('/quade/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def quade_test(id_fichero, alpha=0.05, tipo=0, test_comparacion="bonferroni_dunn_test"):
    """
    Servicio web para el test de Quade
    
    Argumentos
    ----------
    id_fichero: string
        Identificador HASH MD5 del fichero sobre el que se quiere aplicar el test
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta
    tipo: string
        Indica si lo que se quiere es minimizar ("0") o maximizar ("1")
    test_comparacion: string
        Test POST-HOC a aplicar si el test de ranking encuentra diferencias
        significativas.
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de Quade y si procede el resultado de
        aplicar el test de comparación.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningún fichero con esa clave."}
    res_ranking = tnp.quade_test(datos["nombres_algoritmos"],datos["matriz_datos"],alpha,tipo)
    if res_ranking["resultado"] == "True":
        res_comparacion = getattr(tnp, test_comparacion)("quade",res_ranking["nombres"],res_ranking["ranking"],len(datos["matriz_datos"]),alpha)
        return {"test_ranking" : res_ranking, "test_comparacion" : res_comparacion}
    return {"test_ranking" : res_ranking}


#Servicio para el test de normalidad de Shapiro-Wilk.
@route('/shapiro/<id_fichero>', method="GET")
@route('/shapiro/<id_fichero>/<alpha:float>', method="GET")
def shapiro_test(id_fichero, alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningún fichero con esa clave."}
    estadisticos_w = []
    p_valores = []
    resultados = []
    for i in range(len(datos["matriz_datos"][0])):
        resultado_shapiro = st.shapiro([conjunto[i] for conjunto in datos["matriz_datos"]])
        estadisticos_w.append(resultado_shapiro[0])
        p_valores.append(resultado_shapiro[1])
        #Si p_valor < alpha, se rechaza la hipótesis "True" de que la muestra provenga de una distribución normal.
        resultados.append(str(resultado_shapiro[1]<alpha))
    return {"resultado" : resultados, "estadisticos_w" : estadisticos_w, "p_valores" : p_valores}


#Servicio para el test de normalidad de Kolmogorov-Smirnov.
@route('/kolmogorov/<id_fichero>', method="GET")
@route('/kolmogorov/<id_fichero>/<alpha:float>', method="GET")
def kolmogorov_test(id_fichero, alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningún fichero con esa clave."}
    estadisticos_d = []
    p_valores = []
    resultados = []
    for i in range(len(datos["matriz_datos"][0])):
        resultado_kolmogorov = st.kstest([conjunto[i] for conjunto in datos["matriz_datos"]],'norm')
        estadisticos_d.append(resultado_kolmogorov[0])
        p_valores.append(resultado_kolmogorov[1])
        #Si p_valor < alpha, se rechaza la hipótesis "True" de que la muestra provenga de una distribución normal.
        resultados.append(str(resultado_kolmogorov[1]<alpha))
    return {"resultado" : resultados, "estadisticos_d" : estadisticos_d, "p_valores" : p_valores}


#Servicio para el test de normalidad de D'Agostino-Pearson.
@route('/agostino/<id_fichero>', method="GET")
@route('/agostino/<id_fichero>/<alpha:float>', method="GET")
def agostino_test(id_fichero, alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningún fichero con esa clave."}
    estadisticos_k2, p_valores = st.normaltest(datos["matriz_datos"],axis=0)
    #Si p_valor < alpha, se rechaza la hipótesis "True" de que la muestra provenga de una distribución normal.
    resultados = [str(p_valores[i]<alpha) for i in range(len(p_valores))]
    return {"resultado" : resultados, "estadisticos_k2" : estadisticos_k2.tolist(), "p_valores" : p_valores.tolist()}


#Servicio para el test de homocedasticidad de Levene.
@route('/levene/<id_fichero>', method="GET")
@route('/levene/<id_fichero>/<alpha:float>', method="GET")
def agostino_test(id_fichero, alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningún fichero con esa clave."}
    print list(itertools.chain.from_iterable(datos["matriz_datos"]))
    for muestra in datos["matriz_datos"]:
        estadisticos_w, p_valores = st.levene(muestra[i] for i in range(len(datos["matriz_datos"])))
    #Si p_valor < alpha, se rechaza la hipótesis "True" de que las muestras de entrada provengan de poblaciones con
    #varianzas similares.
    resultados = [str(p_valores[i]<alpha) for i in range(len(p_valores))]
    return {"resultado" : resultados, "estadisticos_w" : estadisticos_w, "p_valores" : p_valores}


run(reloader=True, host='localhost', port=8080)
