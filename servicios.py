# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 12:49:31 2014

@author: Adrián
"""

from bottle import route, run, response, request
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
            raise Exception("Error formato datos")
        if numero_linea == 0:
            for i in range(len(fila)):
                if i == 0:
                    palabra = fila[i]
                else:
                    if nombres_algoritmos.count(fila[i]) == 0:
                        nombres_algoritmos.append(fila[i])
                    else:
                        raise Exception("Nombre de algoritmo repetido")
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
                        raise Exception("Nombre conjunto datos repetido")
                else:
                    m = patron_numeros.match(fila[i])
                    if m:
                        dato = float(fila[i])
                        lista_datos.append(dato)
                    else:
                        raise Exception("Numero \"" + fila[i] + "\" no valido en linea " + str(numero_linea+1))
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
            return {"fallo" : "El fichero con hash \"" + clave + "\" ya se encuentra el servidor"}
    try:
        datos = leer_datos(subida.file)
    except Exception, error:
        return {"fallo" : str(error)}
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
        return {"fallo" : "No existe ningun fichero con esa clave"}
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
        return {"fallo" : "No existe ningun fichero con esa clave"}
    try:
        resultado = tnp.wilcoxon_test(datos["matriz_datos"],alpha)
    except Exception, error:
        return {"fallo" : str(error)}
    return resultado


#Servicio para el test de Friedman.
@route('/friedman/<id_fichero>', method="GET")
@route('/friedman/<id_fichero>/<alpha:float>', method="GET")
@route('/friedman/<id_fichero>/<tipo:int>', method="GET")
@route('/friedman/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def friedman_test(id_fichero, alpha=0.05, tipo=0):
    """
    Servicio web para el test de Friedman
    
    Argumentos
    ----------
    id_fichero: string
        Identificador HASH MD5 del fichero sobre el que se quiere aplicar el test
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta
    tipo: string
        Indica si lo que se quiere es minimizar ("0") o maximizar ("1")
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de Friedman
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningun fichero con esa clave"}
    resultado = tnp.friedman_test(datos["nombres_algoritmos"],datos["matriz_datos"],alpha,tipo)
    return resultado


#Servicio para el test de Iman-Davenport.
@route('/iman-davenport/<id_fichero>', method="GET")
@route('/iman-davenport/<id_fichero>/<alpha:float>', method="GET")
@route('/iman-davenport/<id_fichero>/<tipo:int>', method="GET")
@route('/iman-davenport/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def iman_davenport_test(id_fichero, alpha=0.05, tipo=0):
    """
    Servicio web para el test de Iman-Davenport
    
    Argumentos
    ----------
    id_fichero: string
        Identificador HASH MD5 del fichero sobre el que se quiere aplicar el test
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta
    tipo: string
        Indica si lo que se quiere es minimizar ("0") o maximizar ("1")
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de Iman-Davenport
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningun fichero con esa clave"}
    resultado = tnp.iman_davenport_test(datos["nombres_algoritmos"],datos["matriz_datos"],alpha,tipo)
    return resultado


#Servicio para el test de los Rangos Alineados de Friedman.
@route('/rangos-alineados/<id_fichero>', method="GET")
@route('/rangos-alineados/<id_fichero>/<alpha:float>', method="GET")
@route('/rangos-alineados/<id_fichero>/<tipo:int>', method="GET")
@route('/rangos-alineados/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def friedman_rangos_alineados_test(id_fichero, alpha=0.05, tipo=0):
    """
    Servicio web para el test de los Rangos Alineados de Friedman
    
    Argumentos
    ----------
    id_fichero: string
        Identificador HASH MD5 del fichero sobre el que se quiere aplicar el test
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta
    tipo: string
        Indica si lo que se quiere es minimizar ("0") o maximizar ("1")
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de los Rangos Alineados de Friedman
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningun fichero con esa clave"}
    resultado = tnp.friedman_rangos_alineados_test(datos["nombres_algoritmos"],datos["matriz_datos"],alpha,tipo)
    return resultado


#Servicio para el test Quade.
@route('/quade/<id_fichero>', method="GET")
@route('/quade/<id_fichero>/<alpha:float>', method="GET")
@route('/quade/<id_fichero>/<tipo:int>', method="GET")
@route('/quade/<id_fichero>/<alpha:float>/<tipo:int>', method="GET")
def quade_test(id_fichero, alpha=0.05, tipo=0):
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
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de Quade
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    try:
        datos = lista_ficheros[id_fichero]
    except Exception:
        return {"fallo" : "No existe ningun fichero con esa clave"}
    resultado = tnp.quade_test(datos["nombres_algoritmos"],datos["matriz_datos"],alpha,tipo)
    return resultado


#Servicio para el test de Bonferroni-Dunn.
@route('/bonferroni-dunn/<test_principal>/<nombres>/<ranking>/<n:int>', method="GET")
@route('/bonferroni-dunn/<test_principal>/<nombres>/<ranking>/<n:int>/<alpha:float>', method="GET")
def bonferroni_dunn_test(test_principal,nombres,ranking,n,alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    nombres = nombres.split(",")
    ranking = [float(x) for x in ranking.split(",")]
    resultado = tnp.bonferroni_dunn_test(test_principal,nombres,ranking,n,alpha)
    return resultado


#Servicio para el test de Holm.
@route('/holm/<test_principal>/<nombres>/<ranking>/<n:int>', method="GET")
@route('/holm/<test_principal>/<nombres>/<ranking>/<n:int>/<alpha:float>', method="GET")
def holm_test(test_principal,nombres,ranking,n,alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    nombres = nombres.split(",")
    ranking = [float(x) for x in ranking.split(",")]
    resultado = tnp.holm_test(test_principal,nombres,ranking,n,alpha)
    return resultado


#Servicio para el test de Li.
@route('/li/<test_principal>/<nombres>/<ranking>/<n:int>', method="GET")
@route('/li/<test_principal>/<nombres>/<ranking>/<n:int>/<alpha:float>', method="GET")
def li_test(test_principal,nombres,ranking,n,alpha=0.05):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    nombres = nombres.split(",")
    ranking = [float(x) for x in ranking.split(",")]
    resultado = tnp.li_test(test_principal,nombres,ranking,n,alpha)
    return resultado

run(reloader=True, host='localhost', port=8080)
