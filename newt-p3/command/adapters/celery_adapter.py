from __future__ import absolute_import
from celery import shared_task
from common.shell import run_command
from common.response import json_response
from django.conf import settings
from celery.result import AsyncResult
import logging
from common.decorators import  login_required , safty_task
import time
from django.core.cache import cache
logger = logging.getLogger("newt." + __name__)


@shared_task(bind=True , track_started=True )
def execute_task(self , task_env, command  ):
    return execute_task_unsafy(self , task_env,  command  )

@safty_task
def execute_task_unsafy(self , task_env,  command  ):
    try :
        (output, error, retcode) = run_command(command , bash = True)
        response = { "content" : {
                'output': output,
                'error': error,
                'retcode': retcode
            } }
        return response
    except Exception as e:
        #return json_response(error="Could not run command: %s" % str(e), status="ERROR", status_code=500)
        return { "error" : "Could not run command: %s" % str(e),
                 "status":"ERROR", 
                 "status_code":500  }

@login_required
def execute(request, machine_name='', command=''   ):
    logger.debug( command )
    taskenv = { "user" : request.user.username , "machine" : machine_name }
    rest = execute_task.delay( taskenv  , command   )
    cache.set("async-" + rest.id , "AsyncJob" , 3600 )
    return json_response(status="ACCEPT", status_code=201, error="" , content=rest.id)
    #return celery_request(  request , execute_task , command , machine = machine_name  )



def get_systems(request):
    conf = settings.NEWT_CONFIG
    return [ x["NAME"]  for x in  conf['SYSTEMS'] ]

patterns = (
)




def extras_router(request, query):
    """Maps a query to a function if the pattern matches and returns result

    Keyword arguments:
    request -- Django HttpRequest
    query -- the query to be matched against
    """
    for pattern, func, req in patterns:
        match = pattern.match(query)
        if match and req:
            return func(request, **match.groupdict())
        elif match:
            return func(**match.groupdict())

    # Returns an Unimplemented response if no pattern matches
    return json_response(status="Unimplemented", 
                             status_code=501, 
                             error="", 
                             content="query: %s" % query)
