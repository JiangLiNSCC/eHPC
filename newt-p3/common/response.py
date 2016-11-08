from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
#import simplejson as json
import json

def json_response(content="", status="OK", status_code=200, error=""):
    """
    Returns an HTTP response with standard JSON envelope

    Keyword arguments:
        content -- string with the contents of the response 
        status -- string with the status of the response 
        status_code -- HTTP status code 
                       (See http://goo.gl/DKyBHK for status codes)
        error -- string with the error message if there is one 
    """
    #if isinstance(content, dict):
    #    
    wrapper = {
        'status': status,
        'status_code': status_code,
        'output': content,
        'error': error
    }
    #print( type( wrapper) , wrapper )
    response = json.dumps((wrapper)) 
    #response = json.dumps((wrapper), cls=DjangoJSONEncoder, indent=4) 
    return HttpResponse(response, content_type='application/json', status=status_code)
