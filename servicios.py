# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 12:49:31 2014

@author: Adrián
"""

from bottle import route, run, response, request
import tests_no_parametricos as tnp
import re, os

def leer_datos(nombre_archivo):
    """
    Función que lee el fichero de datos que contiene los datos sobre los que se aplican los tests.

    Argumentos
    ----------
    nombre_archivo: string
        Nombre del archivo a abrir (con extensión)
        
    Salida
    ------
    tuple:
        palabra: string
            Palabra que sale antes de la primera coma
        nombres_conj_datos: list
            Nombres de los conjuntos de datos (diferentes).
        nombres_algoritmos: list
            Nombres de los algoritmos (diferentes).
        matriz_datos: list
            Lista de listas que contiene las listas de los diferentes conjuntos de datos.
    descripcion_error: string
        Cadena que contiene un mensaje de error. Será la única salida en caso de error
        
    Tipos de errores
    ----------------
    Nombre algoritmo repetido\n
    Nombre conjunto datos repetido\n
    Error dato linea (El dato no es un número válido)\n
    Error formato datos (La estructura de los datos presentados no es correcta)\n
    Deben existir al menos dos algoritmos\n
    """
    patron_numeros = re.compile('^\d+(\.{1}\d+)?$')
    descripcion_error = ""
    palabra = ""
    nombres_conj_datos = []
    nombres_algoritmos = []
    matriz_datos = []
    f = open(nombre_archivo,"r")
    numero_linea = 0
    error = 0
    while not error:
        linea = f.readline()
        if not linea:
            break
        tokens = re.split(",",linea)
        if numero_linea == 0:
            for i in range(len(tokens)):
                if i == 0:
                    palabra = tokens[i]
                else:
                    nombre = tokens[i].replace("\n","")
                    if nombres_algoritmos.count(nombre) == 0:
                        nombres_algoritmos.append(nombre)
                    else:
                        descripcion_error = "Nombre algoritmo repetido"
                        error = 1
                        break
        else:
            lista_datos = []
            for i in range(len(tokens)):
                if i == 0:
                    if nombres_conj_datos.count(tokens[i]) == 0:
                        nombres_conj_datos.append(tokens[i])
                    else:
                        descripcion_error = "Nombre conjunto datos repetido"
                        error = 1
                        break
                else:
                    m = patron_numeros.match(tokens[i])
                    if m:
                        dato = float(tokens[i])
                        lista_datos.append(dato)
                    else:
                        descripcion_error = "Error dato linea" , numero_linea
                        error = 1
                        break
            matriz_datos.append(lista_datos)
        numero_linea += 1

    numero_algoritmos = len(nombres_algoritmos)
    for i in matriz_datos:
        if len(i) != numero_algoritmos:
            descripcion_error = "Error formato datos"
            error = 1
            break
    if numero_algoritmos < 2:
        descripcion_error = "Deben existir al menos dos algoritmos"
        error = 1

    if not error:
        return palabra, nombres_conj_datos, nombres_algoritmos, matriz_datos
    else:
        return descripcion_error

#No funciona correctamente!
@route('/subir', method='POST')
def subir_fichero():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    subida = request.files.get('fichero')
    nombre, extension = os.path.splitext(subida.filename)
    if extension not in ('.csv'):
        return {"error:" : "Extension no permitida"}
    else:
        return {"nombre" : nombre, "extension" : extension}

@route('/wilcoxon', method="GET")
@route('/wilcoxon/<alpha:float>', method="GET")
def wilcoxon_test(alpha=0.05):
    """
    Servicio web para el test de los rangos signados de Wilcoxon
    
    Argumentos
    ----------
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de Wilcoxon
    fallo en el archivo: dict (JSON)
        Diccionario con la clave "fallo" que indica un fallo ocurrido durante la lectura del arhivo en la función "leer_datos"
    """
    datos = leer_datos("data_wilcoxon.csv")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    if isinstance(datos, tuple):
        resultado = tnp.wilcoxon_test(datos[3],alpha)
        return resultado
    else:
        return {"fallo" : datos}
        
@route('/friedman', method="GET")
@route('/friedman/<alpha:float>', method="GET")
@route('/friedman/<tipo:int>', method="GET")
@route('/friedman/<alpha:float>/<tipo:int>', method="GET")
def friedman_test(alpha=0.05, tipo=0):
    """
    Servicio web para el test de Friedman
    
    Argumentos
    ----------
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta
    tipo: string
        Indica si lo que se quiere es minimizar ("0") o maximizar ("1")
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de Friedman
    fallo en el archivo: dict (JSON)
        Diccionario con la clave "fallo" que indica un fallo ocurrido durante la lectura del arhivo en la función "leer_datos"
    """
    datos = leer_datos("data_wilcoxon.csv")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    if isinstance(datos, tuple):
        resultado = tnp.friedman_test(datos[2],datos[3],alpha,tipo)
        return resultado
    else:
        return {"fallo" : datos}

@route('/iman-davenport', method="GET")
@route('/iman-davenport/<alpha:float>', method="GET")
@route('/iman-davenport/<tipo:int>', method="GET")
@route('/iman-davenport/<alpha:float>/<tipo:int>', method="GET")
def iman_davenport_test(alpha=0.05, tipo=0):
    """
    Servicio web para el test de Iman-Davenport
    
    Argumentos
    ----------
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta
    tipo: string
        Indica si lo que se quiere es minimizar ("0") o maximizar ("1")
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de Iman-Davenport
    fallo en el archivo: dict (JSON)
        Diccionario con la clave "fallo" que indica un fallo ocurrido durante la lectura del arhivo en la función "leer_datos"
    """
    datos = leer_datos("data_wilcoxon.csv")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    if isinstance(datos, tuple):
        resultado = tnp.iman_davenport_test(datos[2],datos[3],alpha,tipo)
        return resultado
    else:
        return {"fallo" : datos}
        
@route('/rangos-alineados', method="GET")
@route('/rangos-alineados/<alpha:float>', method="GET")
@route('/rangos-alineados/<tipo:int>', method="GET")
@route('/rangos-alineados/<alpha:float>/<tipo:int>', method="GET")
def friedman_rangos_alineados_test(alpha=0.05, tipo=0):
    """
    Servicio web para el test de los Rangos Alineados de Friedman
    
    Argumentos
    ----------
    alpha: string
        Nivel de significancia. Probabilidad de rechazar la hipótesis nula siendo cierta
    tipo: string
        Indica si lo que se quiere es minimizar ("0") o maximizar ("1")
        
    Salida
    ------
    resultado: dict (JSON)
        Resultado devuelto al aplicar el test de los Rangos Alineados de Friedman
    fallo en el archivo: dict (JSON)
        Diccionario con la clave "fallo" que indica un fallo ocurrido durante la lectura del arhivo en la función "leer_datos"
    """
    datos = leer_datos("data_wilcoxon.csv")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    if isinstance(datos, tuple):
        resultado = tnp.friedman_rangos_alineados_test(datos[2],datos[3],alpha,tipo)
        return resultado
    else:
        return {"fallo" : datos}

run(reloader=True, host='localhost', port=8080)
