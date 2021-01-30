from importlib.machinery import SourceFileLoader
import os
import sys
import imp


sys.path.insert(0, os.path.dirname(__file__))
#wsgi = SourceFileLoader('app.py', 'wsgi').load_module()
wsgi = imp.load_source('wsgi', 'app.py')
application = wsgi.app

#from app import app as app
