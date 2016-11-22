from django.contrib import auth
import logging
import re
from ldap3 import Server , Connection 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.conf import settings
logger = logging.getLogger("newt." + __name__)

def is_logged_in(request):
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


def get_status(request):
    return is_logged_in(request)


def login(request):
    user = None
    try:
        username = request.POST['username']
        password = request.POST['password']
        ldap_host = 'mn5-gn0' # TO-DO , Should be get from settings .
        server = Server( ldap_host )
        connstr = 'uid=%s,ou=people,dc=yhpc' % username  #dn:uid=nscc-gz_jiangli,ou=people,dc=yhpc
        conn = Connection(server, connstr , password , auto_bind=True)
        if conn.extend.standard.who_am_i() != ( 'dn:' + connstr  ) :
            return is_logged_in(request)            
        try:
            myuser = User.objects.get(username=username)
        except ObjectDoesNotExist :
            email = ""
            #email = "%s@%s" % (username, settings.NEWT_DOMAIN)
            try:
                myuser = User.objects.create_user(username, email)
                myuser.set_password(password)
            except Exception as ex:
                logger.error(ex)
                raise ex
        myuser.backend = 'django.contrib.auth.backends.ModelBackend'
        user = myuser #auth.login(request, myuser)           
    except Exception as ex :
        logger.debug("Login error : %s" % ex)
        pass
    logger.debug("Attemping to log in user: %s" % username)
    if user is not None:
        auth.login(request, user)
        logger.info("Successfully logged in user: %s" % username)
    return is_logged_in(request)

def logout(request):
    logger.info("Successfully logged out user: %s" % request.user.username)

    auth.logout(request)

    return is_logged_in(request)

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
