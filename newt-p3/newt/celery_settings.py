# Django settings for newt project.
import os

import djcelery
djcelery.setup_loader()
BROKER_URL= 'redis://cn16356:6379/0'
CELERY_RESULT_BACKEND = 'redis://cn16356:6379/0'
from kombu import Queue,Exchange
CELERY_DEFAULT_QUEUE = 'default'
default_exchange = Exchange( 'default' , type='direct' )
#ln_exchange = Exchange('ln' , type='topic')
CELERY_QUEUES=(
 Queue('default',Exchange('default'),routing_key='task.#'),
 Queue('ln3' ,Exchange('ln'), routing_key='ln.ln3'),
 Queue('ln4',Exchange('ln'),routing_key='ln.ln4'),
)

#class MyRouter(object):
#    def route_for_task( self,task,args=None ,kwargs=None ) :
#        if task == 'command.adapters.celery_adapter.execute_task' :
#            print( args , kwargs )
#            return { 'exchange':'ln' , 'exchange_type':'topic','routing_key':'ln.' + kwargs["machine"] }

CELERY_ROUTES = ( 'common.routers.MyRouter'  )

#CELERY_ROUTES={
# 'command.adapters.celery_adapter.execute_task':{
#  'queue':'ln3' ,
#  'routing_key' : 'ln.ln3',
# },
#}

CELERY_DEFAULT_EXCHANGE='tasks'
CELERY_DEFAULT_EXCHANGE_TYPE='topic'
CELERY_DEFAULT_ROUTING_KEY='task.default'
