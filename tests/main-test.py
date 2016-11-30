import urllib2 , urllib
import json
import time
import random , string

base_url = "http://10.127.48.5:8000/api"
login_url = "/auth"
async_url = "/async"
async_first_wait_time = 1
async_wait_time = 100
login_data = {"username": "sysu_dwu_1" , "password" : "ae0a22c8b3695ce8"}
DEBUG_ASYNC = True
test_batchfile = "/HOME/sysu_dwu_1/apitests/pytest/job.sh"
test_batchstr = '''#!/bin/sh
#SBATCH -N 2
#SBATCH -p free
srun -p free -N 2 -n 4 hostname
whoami
'''
test_batchstr_long = '''#!/bin/sh
#SBATCH -N 2
#SBATCH -p free
srun -p free -N 2 -n 4 hostname
sleep 100
whoami
'''
class Client:
    def __init__(self , base_url = base_url  ,headers ={} , login_cookie = None , login_data = login_data):
        self.headers = headers
        #for (k,v) in headers :        
        self.base_url = base_url 
        self.login_cookie = login_cookie
        self.login_data = login_data
        self.async_wait_time = async_wait_time
    def login(self):
        tmpdata = self.open( login_url , data = self.login_data , login = False )
        self.login_cookie = 'newt_sessionid=' + tmpdata["output"]['newt_sessionid']
    def open(self , url , data = None , method = None , login = True  , async_get = True , async_wait = True , retjson = True):
        url = self.base_url + url
        if  data  :
            try :
                data = urllib.urlencode(data)
            except TypeError :
                pass
            req = urllib2.Request( url , data  )
        else : 
            req =  urllib2.Request(url)
        if login :
            if not self.login_cookie :
                self.login()
            req.add_header("Cookie" , self.login_cookie  )
        for (k,v) in self.headers :
            req.add_header( k , v  )
        if method :
            req.get_method = lambda:method
        try:
            resp = urllib2.urlopen(req)
            self.resp = resp
            rdata = resp.read()
            #rdata =  json.loads((rdata).decode('ascii'))
        except urllib2.HTTPError ,e :
            rdata=e.fp.read()
            #rdata =  json.loads((rdata).decode('ascii'))
            #print type(rdata)
        #rdata = resp.read()
        try :
            rdata =  json.loads((rdata).decode('ascii'))
            self.data = rdata
            self.status = self.data["status"]
            self.status_code = self.data["status_code"]
            self.output = self.data["output"]
        except ValueError :
            self.data = rdata
            try : 
                self.status_code = resp.getcode()
            except Exception :
                self.status_code = 403
            self.status = "unknown"
            self.output = self.data
            if self.status_code == 200 : self.status = "OK"
        if self.status_code == 201 and async_get: # It's a async task !
            #print async_url + '/' + self.output
            self.async_wait_time = async_wait_time
            time.sleep( async_first_wait_time  )
            if DEBUG_ASYNC : print "jump to async"
            self.open( async_url + '/' + self.output )
        if self.status_code == 100 and async_wait and self.async_wait_time > 0 : #  async task is running !
            time.sleep(1)
            self.async_wait_time -= 1 
            if DEBUG_ASYNC : print " async retry"
            self.open( async_url + '/' + self.output )
        if self.async_wait_time <= 0  :
            print "Error : aysnc connection time out !!!"
            self.async_wait_time = async_wait_time
        return self.data
    def ret200(self):
        return  self.status == "OK" and self.status_code == 200
    def ret403(self):  #
        return  self.status == "ERROR" and self.status_code == 403
    def ret500(self):
        return self.status == "ERROR" and self.status_code == 500
    def retError(self):
        return self.status == "ERROR"

def random_string( dig ):
    return ''.join(random.sample( string.ascii_letters + string.digits ,dig))

         
#if __name__ == '__main__' :
if True:
    mc = Client()
    #print mc.open("/auth",login=False,data = login_data)
    DEBUG_ALL = True
    machine_name = 'ln3'
    count_pass = 0
    count_notpass = 0
    def print_PASS() :
        global count_pass
        print '\033[1;32m'
        print("PASS")
        print '\033[0m'
        count_pass += 1
    def print_NOTPASS() :
        global count_notpass
        print '\033[1;31m'
        print("NOTPASS")
        print '\033[0m'
        count_notpass += 1
    def test_get_root():
        print "test api: GET /api (1 test)"
        rep =  mc.open("" , login=False)
        if DEBUG_ALL : print mc.data
        if mc.ret200() : print_PASS()
        else : print_NOTPASS()
    def test_post_auth():
        print "test api: POST /api/auth (2 test)"
        rep = mc.open("/auth" , login=False , data = login_data)
        if DEBUG_ALL : print mc.data
        if mc.ret200() and mc.output["auth"] == True : print_PASS()
        else : print_NOTPASS()
        rep = mc.open("/auth" , login=False , data = {'username':'x' , 'password': 'y'})
        if DEBUG_ALL  : print mc.data
        if mc.ret200() and mc.output["auth"] == False : print_PASS()
        else : print_NOTPASS()
    def test_get_auth():
        print "test api: GET /api/auth (2 test)"
        rep = mc.open("/auth" , login=False )
        if DEBUG_ALL  : print mc.data
        if mc.ret200() and mc.output["auth"] == False : print_PASS()
        else : print_NOTPASS()
        rep = mc.open("/auth" , login=True )
        if DEBUG_ALL  : print mc.data
        if mc.ret200() and mc.output["auth"] == True : print_PASS()
        else : print_NOTPASS()
    def test_delete_auth():
        print "test api: DELETE /api/auth (2 test)"    
        rep = mc.open("/auth" , login=True , method = "DELETE" )
        if DEBUG_ALL  : print mc.data
        if mc.ret200()  : print_PASS()
        else : print_NOTPASS()
        rep = mc.open("/auth" , login=True )
        if DEBUG_ALL  : print mc.data
        if mc.ret200() and mc.output["auth"] == False : print_PASS()
        else : print_NOTPASS()
        mc.login() # re-login 
        rep = mc.open("/auth" , login=True )
        if DEBUG_ALL  : print mc.data
        if mc.ret200() and mc.output["auth"] == True : print_PASS()
        else : print_NOTPASS()
    def test_get_file_machine_path():
        print "test api: GET /api/file/<machine>/<path>" 
        rep = mc.open("/file/" + machine_name + '/' , login=True  )
        if DEBUG_ALL  : print mc.data
        if mc.ret200()  : print_PASS()
        else : print_NOTPASS()
        # Try not login 
        rep = mc.open("/file/" + machine_name + '/' , login=False  )
        if DEBUG_ALL  : print mc.data
        if mc.ret403()  : print_PASS()
        else : print_NOTPASS()
        # Try path not readable
        rep = mc.open("/file/" + machine_name + '/proc/1/'  )
        if DEBUG_ALL  : print mc.data
        if mc.retError()  : print_PASS()
        else : print_NOTPASS()
    def test_get_file_machine_path_download():
        print "test api: GET /api/file/<macchine>/<path>?download=True"
        rep = mc.open("/file/" + machine_name + '/etc/resolv.conf?download=True'   )
        if DEBUG_ALL  : print mc.data , mc.status_code
        if mc.ret200()  : 
            rep = mc.open("/file/" + machine_name + '/' + mc.data["output"] + '?download=True'   )
            if DEBUG_ALL  : print mc.data , mc.status_code
            print_PASS()
        else : print_NOTPASS()
        rep = mc.open("/file/" + machine_name + '/root/.bashrc?download=True'   )
        if DEBUG_ALL  : print mc.data , mc.status_code , mc.resp.geturl()
        if mc.retError()  : print_PASS()
        else : print_NOTPASS()
    def test_put_file_machine_path():
        print "test api: PUT /api/file/<macchine>/<path>"
        testdata = str(time.time())
        filename = 'eHPC_test_' +  random_string(8) 
        rep = mc.open("/file/" + machine_name + '/tmp/' + filename , method = "PUT" , data = testdata  , login = False )
        if DEBUG_ALL  : print mc.data , mc.status_code
        if mc.ret403()  : print_PASS()
        else : print_NOTPASS()
        rep = mc.open("/file/" + machine_name + '/root/' + filename , method = "PUT" , data = testdata   )
        if DEBUG_ALL  : print mc.data , mc.status_code
        if not mc.ret200()  : print_PASS()
        else : print_NOTPASS()
        rep = mc.open("/file/" + machine_name + '/tmp/' + filename , method = "PUT" , data = testdata   )
        if DEBUG_ALL  : print mc.data , mc.status_code
        if mc.ret200()  : print_PASS()
        else : print_NOTPASS()
    def test_post_command_machine():
        print "test api: POST /api/command/<macchine>"
        rep = mc.open("/command/" + machine_name , login=False , data = {"command" : "date" })
        if DEBUG_ALL : print mc.data
        if mc.ret403() : print_PASS()
        else : print_NOTPASS() 
        rep = mc.open("/command/" + machine_name  , data = {"command" : '''bash  -c -l  "pwd;hostname;env" ''' })
        if DEBUG_ALL : print mc.data
        if mc.ret200()  : print_PASS()
        else : print_NOTPASS() 
        rep = mc.open("/command/" + machine_name  , data = {"command" : "touch /root/a" })
        if DEBUG_ALL : print mc.data
        if mc.ret200() and mc.data["output"]["retcode"] !=0  : print_PASS()
        else : print_NOTPASS()
        rep = mc.open("/command/" + machine_name  , data = {"command" : "ls /root" })
        if DEBUG_ALL : print mc.data
        if mc.ret200() and mc.data["output"]["retcode"] !=0   : print_PASS()
        else : print_NOTPASS()
    def test_post_job_machine():
        print "test api: POST /api/job/<machine>" 
        rep = mc.open("/job/" + machine_name + '/' , data = {"jobfile" : test_batchfile })
        if DEBUG_ALL : print mc.data
        if mc.ret200()  : print_PASS()
        else : print_NOTPASS()
        rep = mc.open("/job/" + machine_name + '/' , data = {"jobscript" : test_batchstr })
        if DEBUG_ALL : print mc.data
        if mc.ret200()  : print_PASS()
        else : print_NOTPASS()
        rep = mc.open("/job/" + machine_name + '/', login=False , data = {"jobfile" : test_batchfile })
        if DEBUG_ALL : print mc.data
        if mc.ret403()  : print_PASS()
        else : print_NOTPASS()
    def test_get_job_machine():
        print "test api: GET /api/job/<machine>"       
        rep = mc.open("/job/" + machine_name + '/' )
        if DEBUG_ALL : print mc.data
        if mc.ret200()  : print_PASS()
        else : print_NOTPASS() 
        rep = mc.open("/job/" + machine_name + '/' , login=False)
        if DEBUG_ALL : print mc.data
        if mc.ret403()  : print_PASS()
        else : print_NOTPASS()
        rep = mc.open("/job/" + machine_name + '/' , data = {"jobscript" : test_batchstr_long })
        if mc.ret200()  : 
            myjobid = mc.data["output"]["jobid"]
            print "submit job: " , myjobid
            time.sleep( 5 )
            rep = mc.open("/job/" + machine_name + '/' + str(myjobid) + '/')
            if DEBUG_ALL : print mc.data
            if mc.ret200()  : 
                # check output 
                print_PASS()
            else : print_NOTPASS()
        
        
    def test_delete_job_machine():
        print "test api: DELETE /api/job/<machine>"
        rep = mc.open("/job/" + machine_name + '/' , data = {"jobscript" : test_batchstr_long })
        if mc.ret200()  :
            myjobid = mc.data["output"]["jobid"]
            print "submited job: " , myjobid
            rep = mc.open("/job/" + machine_name + '/' + str(myjobid) + '/' , method = "DELETE" )
            if DEBUG_ALL : print mc.data
            if mc.ret200()  :
                # check output
                print_PASS()
                return 
            else : print_NOTPASS()
        print_NOTPASS()
        pass 
    def test_run( cmd ):
        print " run cmd :  %s" % cmd
        rep = mc.open("/command/" + machine_name  , data = {"command" : cmd })
        if DEBUG_ALL : print mc.data
        if mc.ret200()  : 
            print ( mc.data["output"]["output"] )
        else : print_NOTPASS()
import sys         
if __name__ == '__main__' :
    tests = {
        'auth' : [ 
            test_get_root , 
            test_get_auth,
            test_delete_auth,],
        'file' : [
            test_get_file_machine_path,          
            test_get_file_machine_path_download,
            test_put_file_machine_path,
            ],
        'job' : [
            test_post_command_machine,
            test_post_job_machine,
            test_get_job_machine,
            test_delete_job_machine,
            ],
     }
    if  sys.argv[1] == 'run' :
        test_run( sys.argv[2] )
        exit()
    if len( sys.argv ) < 2  or sys.argv[ 1 ] == 'all' :
        pass ;
        print ("test all ")
        testlist = [x for j in tests.values() for x in j ]
    elif sys.argv[1]   in tests.keys() :
        testlist = tests[ sys.argv[1] ]
        if len( sys.argv ) > 2 and  sys.argv[2].isdigit() and int(sys.argv[2]) < len( testlist )  :
            testlist = [ testlist[ int(sys.argv[2]) ]  ]        
        pass ;
        print ("test :" , sys.argv[1])
    else :
        print( "Usage: python main.py [all/<test name >]" )
        print( "<test name > could be : " , tests.keys())
        exit()
        #testlist = tests[ sys.argv[1] ]
    for eachtest in testlist :
        eachtest()
    #test_get_root()
    #test_post_auth()
    #test_get_auth()
    #test_delete_auth()
    #test_get_file_machine_path()
    #test_get_file_machine_path_download()
    #test_put_file_machine_path()
    #test_post_command_machine()
    #test_post_job_machine()    
    #test_get_job_machine()
    #test_delete_job_machine()
    print "Total PASS : " , count_pass
    print "Total NOT PASS : " , count_notpass



