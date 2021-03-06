from django.conf import settings
from importlib import import_module
import inspect

# Imports all the models from the class listed in settings.py
models_file = settings.NEWT_CONFIG['ADAPTERS']['JOB']['models']
if models_file:
    for name, model in inspect.getmembers(import_module(models_file), inspect.isclass):
        #print('need to load self module: %s' % model )
        locals()[name] = model
        #print( locals())

#class Job(import_module(models_file).HPCJob):
