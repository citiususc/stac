import sys, os, bottle

sys.path = ['/var/www/api/'] + sys.path
os.chdir(os.path.dirname(__file__))

from bottle import Bottle
import servicios # importa los servicios REST

application = bottle.default_app() # Carga la aplicacion por defecto con los servicios REST
root = Bottle()
root.mount('/api/', application) # Mediante esta raiz podemos hacer que todos los servicios escuchen en /api
