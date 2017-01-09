from django.contrib import auth
import logging
import re
from ldap3 import Server , Connection 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import JsonResponse, QueryDict
from common.response import json_response
import datetime
logger = logging.getLogger("newt." + __name__)

from itsdangerous import URLSafeTimedSerializer as utsr
import base64

#from django.conf import settings as django_settings

class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(security_key.encode('utf-8'))
    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
	    #print serializer.loads(token, salt=self.salt)
        return serializer.loads(token, salt=self.salt)

token_confirm = Token(settings.SECRET_KEY)    # 定义为全局变量






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


def check_email( email ):
    try :
        uqs = User.objects.filter( email = email  )
    except :
        return True
    state = True
    for user in uqs :
        if user.is_active == True :
            state =  False
            continue
        td = (datetime.datetime.utcnow() - user.date_joined.replace(tzinfo=None)).seconds
        if td > 3600 :
            user.delete()
    return state

def signup(request):
    print( request.path , request.get_host())
    #put = QueryDict(request.body, encoding=request.encoding)
    #print( put.get('email') )
    #return 'OK'
    try:
        put = QueryDict(request.body, encoding=request.encoding)
        username = put.get('username')
        email = put.get('email')
        password = put.get('password')
        if not check_email(email) :
            return " Email has been used ! "
        try :
            user = User.objects.create_user(username=username, password=password, email=email)
        except :
            return " Could not create such user ! "
        user.is_active = False
        user.set_password(password)
        user.save()
        token = token_confirm.generate_validate_token(username)
        message = "\n".join([u'{0},欢迎注册'.format(username), u'请访问该链接，完成用户验证:',
                             '/'.join([ request.get_host() , 'api/auth', 'active', token])])
        user.email_user( subject = 'sgin ehpc ' , message= message )
        #user.delete()
        return "use email to active the user in 1 hour !"
        # check email
        #user , create  = User.objects.get_or_create(email=email)
    except Exception as ex:
        logger.error(ex)
        raise ex
    pass

def active(request , token):
    try:
        username = token_confirm.confirm_validate_token(token)
        print( username )
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            user.delete()
        return json_response(status="Error",
                             status_code=500,
                             error="The link is out of time",
                             content=" The link is out of time ! ")
        #return render(request, 'message.html', {
        #    'message': u'对不起，验证链接已经过期，请重新<a href=\"' + unicode(django_settings.DOMAIN) + u'/signup\">注册</a>'})
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return json_response(status="Error",
                             status_code=500,
                             error="No such user",
                             content=" No such user ")
    if not  check_email( user.email ) :
        return json_response(status="Error",
                             status_code=500,
                             error="email is used",
                             content=" email is used ")
    user.is_active = True
    user.save()
    return json_response(status="OK",
                             status_code=200,
                             error="",
                             content="active ok!")
    #message = u'验证成功，请进行<a href=\"' + unicode(django_settings.DOMAIN) + u'/login\">登录</a>操作'
    #return render(request, 'message.html', {'message': message})
    pass

def active_perm(request):
    pass


def check_ldap( username , password ):
    try :
        ldap_host = 'mn5-gn0' # TO-DO , Should be get from settings .
        server = Server( ldap_host )
        connstr = 'uid=%s,ou=people,dc=yhpc' % username  #dn:uid=nscc-gz_jiangli,ou=people,dc=yhpc
        conn = Connection(server, connstr , password , auto_bind=True)
        if conn.extend.standard.who_am_i() != ( 'dn:' + connstr  ) :
            return False
        else:
            return True
    except Exception as ex:
        logger.error(ex)
        raise ex



def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        print(username , password)
        try :
            user = auth.authenticate(username='testuser1', password='sbiasbia')
            #user = User.objects.get(username = username)
            #print ("check" , user.check_password( 'sbiasbia' )  , password , user)
            #if not user.check_password(password) :
            #    return "Login Error ! please check username and Password"
        except:
            return "Login Error ! please check Username and password"
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            logger.info("Successfully logged in user: %s" % username)
        return is_logged_in(request)
    except Exception as ex:
        logger.error(ex)
        raise ex

    #     ldap_host = 'mn5-gn0' # TO-DO , Should be get from settings .
    #     server = Server( ldap_host )
    #     connstr = 'uid=%s,ou=people,dc=yhpc' % username  #dn:uid=nscc-gz_jiangli,ou=people,dc=yhpc
    #     conn = Connection(server, connstr , password , auto_bind=True)
    #     if conn.extend.standard.who_am_i() != ( 'dn:' + connstr  ) :
    #         return is_logged_in(request)
    #     try:
    #         myuser = User.objects.get(username=username)
    #     except ObjectDoesNotExist :
    #         email = ""
    #         #email = "%s@%s" % (username, settings.NEWT_DOMAIN)
    #         try:
    #             myuser = User.objects.create_user(username, email)
    #             myuser.set_password(password)
    #         except Exception as ex:
    #             logger.error(ex)
    #             raise ex
    #     myuser.backend = 'django.contrib.auth.backends.ModelBackend'
    #     user = myuser #auth.login(request, myuser)
    # except Exception as ex :
    #     logger.debug("Login error : %s" % ex)
    #     pass
    # logger.debug("Attemping to log in user: %s" % username)
    # if user is not None:
    #     auth.login(request, user)
    #     logger.info("Successfully logged in user: %s" % username)
    # return is_logged_in(request)

def logout(request):
    logger.info("Successfully logged out user: %s" % request.user.username)

    auth.logout(request)

    return is_logged_in(request)

patterns = (
#    (r'^/(?P<token>[^/]+)$', active, True),
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
