from common.response import json_response
from django.http import HttpRequest
import json
import inspect
from django.conf import settings
from pwd import getpwnam
import os
def login_required(view_func):
    """
    Use this for class based views (i.e. first argument is self)
    """
    def wrapper(*args, **kwargs):
        # If view_func is a class view, args=[self, request, ... ]
        # If view_func is a regular function args=[request, ...]
        if isinstance(args[0], HttpRequest):
            request = args[0]
        elif isinstance(args[1], HttpRequest):
            request = args[1]
        else:
            return json_response(status="ERROR", 
                                 status_code=500, 
                                 error="Missing request object") 

        if request.user.is_authenticated():
            return view_func(*args, **kwargs)
        else:
            return json_response(status="ERROR", 
                                 status_code=403, 
                                 error="You must be logged in to access this.",
                                 content=json.dumps({"login_url": "/api/auth/"}))
    return wrapper
def check_machine( machine ):
    pass


def machine_check( view_func  ):
    """
    Use this for api that call resource on machines 
    """
    def wrapper(*args,**kwargs):
        # If view_func is a class view, args=[self, request, machine_name , ... ]
        # If view_func is a regular function args=[request, machine_name ,  ...]
        if isinstance(args[0], HttpRequest):
            request = args[0]
            machine_name = args[1]
        elif isinstance(args[1], HttpRequest):
            request = args[1]
            machine_name = args[2]
        else:
            return json_response(status="ERROR",
                                 status_code=500,
                                 error="Missing request object")
        hostname = None
        conf = settings.NEWT_CONFIG
        if not isinstance(machine_name , str) :
            return json_response(status="ERROR",
                                 status_code=500,
                                 error="Missing machine name")
        for s in conf['SYSTEMS']:
            if machine_name==s['NAME']:
                hostname = s['HOSTNAME']
                break
        if hostname is None:
            return json_response(status="ERROR",
                                 status_code=404,
                                 error="Unrecognized system: %s" % machine_name)
        return view_func(*args, **kwargs)
    return wrapper


def safty_task( task_func ):
    def wrapper(*args,**kwargs):
        #return( args , kwargs )  
        if not isinstance(args[1] , dict) :
            return json_response(status="ERROR",
                                 status_code=500,
                                 error="not a safty task: no taskenv")
        if ( "user" not in args[1].keys()  ) or ( "machine" not in args[1].keys() ) : 
           return json_response(status="ERROR",
                                 status_code=500,
                                 error="not a safty task: no taskenv")
        # chuid :
        username = args[1]["user"]
        ngid = getpwnam( username ).pw_gid
        nuid = getpwnam( username ).pw_uid
        if nuid == 0 :
           return json_response(status="ERROR",
                                 status_code=500,
                                 error="dangerous action ! ")
        os.setgid(ngid)
        os.setuid(nuid)
        return [ username  ,  task_func( *args,**kwargs ) ] 
    return wrapper

def unsafty_task( task_func ):
    def wrapper(*args,**kwargs):
        #return( args , kwargs )  
        if not isinstance(args[1] , dict) :
            return json_response(status="ERROR",
                                 status_code=500,
                                 error="not a safty task: no taskenv")
        if ( "user" not in args[1].keys()  ) or ( "machine" not in args[1].keys() ) :
           return json_response(status="ERROR",
                                 status_code=500,
                                 error="not a safty task: no taskenv")
        # chuid :
        username = args[1]["user"]
        ngid = getpwnam( username ).pw_gid
        nuid = getpwnam( username ).pw_uid
        if nuid == 0 :
           return json_response(status="ERROR",
                                 status_code=500,
                                 error="dangerous action ! ")
        #os.setgid(ngid)
        #os.setuid(nuid)
        return [ username  ,  task_func( *args,**kwargs ) ]
    return wrapper
