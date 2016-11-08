from celery.result import AsyncResult
import logging
import time
from common.response import json_response
logger = logging.getLogger("newt." + __name__)
def celery_request(  request , task_func ,  *args , **kwargs ):
    ''' *args , **kwargs must have the keyword machine !  '''
    try:
        logger.debug("Running celery_request: %s  " % task_func.__name__ )
        qid = request.POST.get('qid')
        async = request.POST.get('async')
        if qid :
            rest = AsyncResult ( qid )
        else :
            # rest = task.delay( command , machine = machine_name   )
            rest = task_func.delay( *args , **kwargs )
        waittime = 0.03 # should be load from settings . TO-DO 
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
            return json_response(error= "Worker run failure : %s " % rest.result , status="ERROR", status_code=500)
        else :
            return json_response(error= "Worker running: %s " % rest.result , status=cur_state, status_code=100 , content=rest.id)
    except Exception as e:
        logger.error("Error: %s" % str(e))
        return json_response(error="Error: %s" % str(e), status="ERROR", status_code=500)
