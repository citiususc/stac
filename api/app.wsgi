import sys, os

sys.path = [os.path.dirname(__file__), os.path.dirname(os.path.dirname(__file__))] + sys.path
os.chdir(os.path.dirname(__file__))

import bottle
from bottle import Bottle

import services # importa los servicios REST

application = bottle.default_app() # Carga la aplicacion por defecto con los servicios REST
root = Bottle()
root.mount('/api/', application) # Mediante esta raiz podemos hacer que todos los servicios escuchen en /api
