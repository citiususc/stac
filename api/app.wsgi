import sys, os

sys.path = ['/var/www/beta/api/'] + sys.path
os.chdir(os.path.dirname(__file__))

import bottle
from bottle import Bottle

import servicios # importa los servicios REST

application = bottle.default_app() # Carga la aplicacion por defecto con los servicios REST
root = Bottle()
root.mount('/beta/api/', application) # Mediante esta raiz podemos hacer que todos los servicios escuchen en /api
