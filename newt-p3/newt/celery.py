from __future__ import absolute_import #,unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newt.settings')

from django.conf import settings  # noqa

app = Celery('proj')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
#app.config_from_object('django.conf:settings' ) #, namespace='CELERY')
app.config_from_object('newt.celery_settings' )
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#app.conf.update(
#    result_expires = 3600 ,
#    result_serializer = "pickle" , 
#    accept_content = ['pickle' , 'json']
#)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
