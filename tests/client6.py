import six
from six.moves.urllib import request , parse
import json
import time
import random , string
import re
import logging
import logging.config
if six.PY3 :
    from http.client import HTTPException 
from six.moves.urllib.error import HTTPError
logging.config.fileConfig("logger.conf")
logger = logging.getLogger("test")

login_url = "/auth"
async_url = "/async"
async_first_wait_time = 1
async_wait_time = 100
DEBUG_ASYNC = True
USE_GLOBAL = True
global g__cookies
class newtAPIClient:

    def __init__(self , base_url = ""  ,headers ={} , login_cookie = None , login_data = ""):
        self.headers = headers
        self.base_url = base_url 
        self.login_cookie = login_cookie
        self.login_data = login_data
        self.async_wait_time = async_wait_time
        self.username = None
        global g__cookies
        try :
            if 'cookie' in  g__cookies :
                pass
                if self.login_data == None :
                    self.login_data = g__cookies['cookie']
        except NameError :
            g__cookies = {}

    def login(self):
        tmpdata = self.open( login_url , data = self.login_data , login = False )
        self.login_cookie = 'newt_sessionid=' + tmpdata["output"]['newt_sessionid']
        self.username = self.login_data["username"]
        global g__cookies
        try :
            g__cookies['cookie'] = self.login_cookie
        except NameError :
            g__cookies = {}
            g__cookies['cookie'] = self.login_cookie

    def open(self , url , data = None , method = None , login = True  , async_get = True , async_wait = True , retjson = True):
        url = self.base_url + url
        if  data :
            try :
                if  method != 'PUT' :
                    data = parse.urlencode(data).encode(encoding='UTF8')
                else :
                    data = data.encode('utf-8')
            except TypeError as ex:
                print(data)
                logger.debug( ex )
                pass
            req = request.Request( url , data  )
        else : 
            req =  request.Request(url)
        if login :
            if not self.login_cookie :
                self.login()
            req.add_header("Cookie" , self.login_cookie  )
        for (k,v) in self.headers :
            req.add_header( k , v  )
        if method :
            req.get_method = lambda:method
        try:
            resp = request.urlopen(req)
            self.resp = resp
            rdata = resp.read()
        except HTTPError as e :
            rdata=e.fp.read()
        except HTTPException as e :
            rdata = e.args[0]
        if not retjson :
            logger.debug(dict(resp))
            self.data = rdata
            self.status_code = resp.code
            self.status = "OK" if resp.code == 200 else  "ERROR"
            self.output = self.data
            return self.data
        #print(type(rdata))
        if isinstance( rdata , bytes):
            rdata = rdata.decode('utf-8')
        rdata_reg = re.search( '\{.+\}' ,rdata )
        rdata =  rdata if rdata_reg is None else rdata_reg.group()  
        try :
            rdata =  json.loads(rdata)
            self.data = rdata
            self.status = self.data["status"]
            self.status_code = self.data["status_code"]
            self.output = self.data["output"]
        except ValueError as exc:
            print( 'ValueError:' , exc , ' ; rdata:' , rdata)
            self.data = rdata
            try : 
                self.status_code = self.data["status_code"]
                self.status = self.data["status"]
            except Exception as exc :
                print(exc)
                logger.debug ("exe : %s" % exc)
                logger.debug( "rdata : %s" % rdata )
                try:
                    self.status_code = rdata["status_code"]
                    self.status = rdata["status"]
                except Exception as ex :
                    self.status_code = 200
                    self.status = 200
                self.status = "unknown"
            self.output = self.data
            if self.status_code == 200 : self.status = "OK"
        if self.status_code == 201 and async_get: # It's a async task !
            self.async_wait_time = async_wait_time
            time.sleep( async_first_wait_time  )
            if DEBUG_ASYNC : logger.debug( "jump to async")
            return self.open( async_url + '/' + self.output )
        if self.status_code == 100 and async_wait and self.async_wait_time > 0 : #  async task is running !
            time.sleep(1)
            self.async_wait_time -= 1 
            if DEBUG_ASYNC : logger.debug( " async retry")
            return self.open( async_url + '/' + self.output )
        if self.async_wait_time <= 0  :
            logger.error( "Error : aysnc connection time out !!!")
            self.async_wait_time = async_wait_time
        logger.debug( "return status  %s in( %s )  %s  secs"% (self.status_code  , async_wait  , self.async_wait_time ))
        return self.data

    def ret200(self):
        return  self.status == "OK" and self.status_code == 200

    def ret403(self):  #
        return  self.status == "ERROR" and self.status_code == 403

    def ret500(self):
        return self.status == "ERROR" and self.status_code == 500

    def retError(self):
        return self.status == "ERROR"

#def random_string( dig ):
#    return ''.join(random.sample( string.ascii_letters + string.digits ,dig))

         

