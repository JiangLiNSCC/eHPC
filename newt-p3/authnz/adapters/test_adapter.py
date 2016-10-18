"""Auth Adapter Template File

IMPORTANT: NOT A FUNCTIONAL ADAPTER. FUNCTIONS MUST BE IMPLEMENTED

Notes:
    - Each of the functions defined below must return a json serializable
      object, json_response, or valid HttpResponse object
    - A json_response creates an HttpResponse object given parameters:
        - content: string with the contents of the response 
        - status: string with the status of the response 
        - status_code: HTTP status code 
        - error: string with the error message if there is one 
"""
from django.contrib import auth
from common.response import json_response
import logging
import re
logger = logging.getLogger("newt." + __name__)
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

def get_status(request):
    """Returns the current user status

    Keyword arguments:
    request -- Django HttpRequest
    """
    if (request.user is not None) and (request.user.is_authenticated()):
        output=dict(auth=True,
                    username=request.user.username,
                    session_lifetime=request.session.get_expiry_age(),
                    newt_sessionid=request.session.session_key)
    else:
        output=dict(auth=False,
                    username=None,
                    session_lifetime=0,
                    newt_sessionid=None)
    return output
    pass


def login(request):
    """Logs the user in and returns the status

    Keyword arguments:
    request -- Django HttpRequest
    """
    username = request.POST.get('username') #.encode("utf-8")
    password = request.POST.get('password') #.encode("utf-8")
    if ( 1 == 1) :
        try:
            myuser = User.objects.get(username=username)
        except ObjectDoesNotExist:
            # This isn't actually used anywhere, but you might make this smarter
            email = "%s@%s" % (username, settings.NEWT_DOMAIN)
            try:
                myuser = User.objects.create_user(username, email)
            except Exception as ex:
                logger.error(ex)
                raise ex
    myuser.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, myuser)
    return get_status(request)
    pass
    

def logout(request):
    """Logs the user out and returns the status

    Keyword arguments:
    request -- Django HttpRequest
    """
    auth.logout(request)
    return get_status(request)
    pass


"""A tuple list in the form of:
    (
        (compiled_regex_exp, associated_function, request_required),
        ...
    )

    Note: The compiled_regex_exp must have named groups corresponding to
          the arguments of the associated_function
    Note: if request_required is True, the associated_function must have
          request as the first argument

    Example:
        patterns = (
            (re.compile(r'/usage/(?P<path>.+)$'), get_usage, False),
            (re.compile(r'/image/(?P<query>.+)$'), get_image, False),
            (re.compile(r'/(?P<path>.+)$'), get_resource, False),
        )
"""
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
