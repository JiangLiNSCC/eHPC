from common.shell import run_command
from common.response import json_response
from celery.result import AsyncResult
import logging
logger = logging.getLogger("newt." + __name__)


def execute(request, machine_name, command):
    try:
        logger.debug("Running command: %s" % command)
        #print( command  + 's')
        res = run_command(command)
        (output, error, retcode) = run_command(command)
        response = {
            'output': output,
            'error': error,
            'retcode': retcode
        }
        #print( response)
        return response
    except Exception as e:
        logger.error("Could not run command: %s" % str(e))
        return json_response(error="Could not run command: %s" % str(e), status="ERROR", status_code=500)

def async_execute(request , machine_name , command):
    try:
        logger.debug("Running command: %s" % command)
        res = run_command.delay(command)
        #(output, error, retcode) = run_command(command)
        response = {
            'id': res.id,
        }
        return response
    except Exception as e:
        logger.error("Could not run command: %s" % str(e))
        return json_response(error="Could not run command: %s" % str(e), status="ERROR", status_code=500)

def async_check(request,machine_name,rid):
    try :
        res = AsyncResult( rid )
        response = {
             'status' : res.status ,
             'info'   : res.info   ,
        }
        return response
    except Exception as e :
        logger.error("Could not check aysnc command : %s" % str(e))
        return json_response(error="Could not check aysnc command: %s" % str(e), status="ERROR", status_code=500)



def get_systems(request):
    return ['localhost']

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
