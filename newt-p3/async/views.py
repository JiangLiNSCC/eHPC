#from django.shortcuts import render
from newt.views import JSONRestView
from common.response import json_response
from django.conf import settings
import urllib
# Create your views here.
from celery.result import AsyncResult
from django.core.cache import cache

class AsyncView(JSONRestView):
    def get(self, request,async_id):
        #logger.debug("Entering %s:%s" % (self.__class__.__name__, __name__))
        rest = AsyncResult ( async_id )
        if rest.state == 'PENDING' :
            check_cache = cache.get("async-" + async_id , "None" )
            if check_cache == "None" :
                return json_response(status="ERROR",          
                             status_code=500, 
                             error="Could not got such a AsyncResult . Error id or out of date ! ", 
                             content="query: %s" )
            else :
                return json_response(error= "Command is waitting for worker "  , status= rest.state , status_code=100 , content=rest.id)
        elif rest.state == 'FAILURE':
            return json_response(error= "async task failure : %s " % rest.result , status="ERROR", status_code=500)
        elif rest.state == "SUCCESS" :
            if rest.result[0] == request.user.username:
                return rest.result[1]
            else :
                return json_response(error= "Error : Not Your task. "  , status= "ERROR" , status_code=550 )
        else :
            return json_response(error= "Command running on task worker : %s " % rest.result , status= rest.state , status_code=100 , content=rest.id)
        

class ExtraAsyncView(JSONRestView):
    def get(self, request, query):
        return  json_response(status="Unimplemented", 
                             status_code=501, 
                             error="", 
                             content="query: %s" % query)
