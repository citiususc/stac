# -*- coding: utf-8 -*-
"""
Created on Tue Api 22 16:05:31 2014

@author: Adrián
"""

import csv, re, hashlib
from collections import *

class LimitedSizeDict(OrderedDict):
    """Un diccionario con tamaño máximo. Cuando llega al límite, elimina al
    elemento más antiguo del diccionario (FIFO).
    """
    
    def __init__(self, *args, **kwds):
        self.size_limit = kwds.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)


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
