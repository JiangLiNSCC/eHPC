from __future__ import absolute_import
from celery import shared_task
from common.shell import run_command
from common.response import json_response
from django.conf import settings
from celery.result import AsyncResult
import logging
from common.decorators import machine_check , login_required
import time
logger = logging.getLogger("newt." + __name__)

#app = Celery()

@shared_task(bind=True , track_started=True )
def execute_task(self , command  , machine = None):
    try :
        (output, error, retcode) = run_command(command)
        response = {
                'output': output,
                'error': error,
                'retcode': retcode
            }
        return response
    except Exception as e:
        return json_response(error="Could not run command: %s" % str(e), status="ERROR", status_code=500)

from common.celeryutil import celery_request

def execute(request, machine_name='', command=''   ):
    return celery_request(  request , execute_task , command , machine = machine_name  )


@login_required
@machine_check
def execute_old(request, machine_name='', command='' , waittime = 0.03  ):
    try:
        logger.debug("Running command(ssh): %s  (@ %s)" % (command, machine_name))
        qid = request.POST.get('qid')
        async = request.POST.get('async')
        #print( 'async:' , async )
        if qid :
            rest = AsyncResult ( qid )
        else :
            rest = execute_task.delay( command , machine = machine_name   )
        if waittime > 0 : 
            time.sleep( waittime )
        if async == "False" or async == "false" :
            response = rest.get 
            return response
        cur_state = rest.state 
        if cur_state == "SUCCESS" :
            response =  rest.result
            return response
        elif cur_state == 'FAILURE':
            return json_response(error= "Command run failure : %s " % rest.result , status="ERROR", status_code=500)
        else :
            return json_response(error= "Command running on Celery worker : %s " % rest.result , status=cur_state, status_code=100 , content=rest.id)
    except Exception as e:
        logger.error("Could not run command: %s" % str(e))
        return json_response(error="Could not run command: %s" % str(e), status="ERROR", status_code=500)


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
