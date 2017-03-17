from basetest import BaseTest
import json
import time
script_hello = '''#!/bin/sh
echo "hello"
pwd
date
hostname
echo $@
'''

script_wait = '''#!/bin/sh
sleep 100
'''

job_conf_1 = json.dumps( { 
            "job_wdir" : "~/tmp" ,
            "job_name" : "test"  ,
            "time_limit" : 1 ,
            "partition" : "MIC" ,
            "scale_cores" : 2 ,
            "scale_memGB" : 30 ,
            "scale_Nodes" : 2 ,
            "jobfile_args" : "test1 test2" ,
        } )

#{u'status': {u'4900296.batch': u'Success', u'4900296': u'Success'}, u'tasks': {u'4900296.batch': u'1', u'4900296': u''}, u'name': {u'4900296.batch': u'batch', u'4900296': u'test'}, u'partition': {u'4900296.batch': u'', u'4900296': u'MIC'}, u'time': {u'4900296.batch': u'00:00:00', u'4900296': u'00:00:00'}, u'nodes': {u'4900296.batch': 0.0416666667, u'4900296': 2.0}, u'id': {u'4900296.batch': u'4900296.batch', u'4900296': u'4900296'}, u'exitcode': {u'4900296.batch': u'0:0', u'4900296': u'0:0'}}


class JobTest(BaseTest):

    def setUp(self):
        super( JobTest , self ).setUp()
        self.baseurl = "/job/%s/" % self.machine
        self.data = {"command" : "" }
        
        

    def setcommand(self,command):
        self.data["command"] = command
        self.errstr = "%s run : %s " % ( self.url , command )
        self.logger.debug("test api : %s" % self.errstr )

    def isSuccess(self,jobid,jobconf = None):
        jobconf = json.loads( jobconf )
        errstr = 'check if job %s success' % jobid
        self.assertEqual( self.mc.ret200() , True , errstr  )
        self.assertEqual( self.mc.output['status'][str(jobid)] , "Success" , errstr  )
        #self.assertEqual( self.mc.output['exitcode'][str(jobid)] , "0:0" , errstr  )
        if jobconf :
            if "job_name" in jobconf :
                self.assertEqual( self.mc.output['name'][str(jobid)], jobconf[ "job_name"] , errstr  )
            if  "partition"  in jobconf :
                self.assertEqual( self.mc.output['partition'][str(jobid)] , jobconf["partition"] , errstr  )

    def likeQueueRes(self , qr):
        """ check if a dict like this :
         {u'status': {}, u'nodelist': {}, u'name': {}, u'partition': {}, u'user'                    : {}, u'time': {}, u'nodes': {}, u'id': {}}
        """
        if not isinstance(qr,dict) : return False
        if not 'status' in qr : return False
        if not 'name' in qr : return False
        if not 'id' in qr : return False
        return True
        pass

    def testGetJob(self):
        """Test : GET /api/job/<machine>/
            return should be just like this :
        """
        errstr = 'GET /api/job/<machine>'
        self.logger.debug(errstr)
        self.mc.open( self.baseurl  , login=False)
        self.logger.debug(self.mc.data)
        self.assertEqual( self.mc.ret200() , False , errstr + ' without login' )
        self.mc.open(  self.baseurl )
        self.logger.debug(self.mc.data)
        self.assertEqual( self.mc.ret200() , True , errstr  )
        self.assertEqual( self.likeQueueRes(self.mc.output) , True , errstr  )

    def _testPostJob(self , script =  script_hello ,  file = None , conf = None , test = True):
        url = "/job/%s/" % self.machine
        data = { }
        if script :
            data["jobscript"] = script
        if file :
            if script:
                data["jobfilepath"] = file
            else :
                data["jobfile"] = file
        if conf :
            data["jobconf"] = conf
        errstr = 'POST /api/job/<machine>'
        if test:
            self.mc.open( url , data=data   , login=False)
            self.logger.debug(self.mc.data)
            self.assertEqual( self.mc.ret200() , False , errstr + ' without login' )
        self.mc.open( url , data=data   )
        self.logger.debug(self.mc.data)
        self.assertEqual( self.mc.ret200() , True , errstr  )
        jobid = int(self.mc.output['jobid'])        
        self.logger.debug("success submitted job : %s" % jobid)
        return jobid 
        pass
		
    def _testGetJobId(self , jobid , test = True):
        pass
        errstr = 'GET /api/job/<machine>/<id>'
        self.logger.debug(errstr)
        if test :
            self.mc.open( self.baseurl + str(jobid) , login=False)
            self.logger.debug(self.mc.data)
            self.assertEqual( self.mc.ret200() , False , errstr + ' without login' )
        self.mc.open(  self.baseurl + str(jobid) )
        self.logger.debug(self.mc.data)
        self.assertEqual( self.mc.ret200() , True , errstr  )
        #self.assertEqual( self.likeQueueRes(self.mc.output) , True , errstr  )


    def _testDeleteJob(self,jobid):
        errstr = 'DELETE /api/job/<machine>/<id>'
        self.logger.debug(errstr)
        self.mc.open( self.baseurl + str(jobid) , login=False , method = "DELETE")
        self.logger.debug(self.mc.data)
        self.assertEqual( self.mc.ret200() , False , errstr + ' without login' )
        self.mc.open(  self.baseurl + str(jobid) ,method = "DELETE")
        self.logger.debug(self.mc.data)
        self.assertEqual( self.mc.ret200() , True , errstr  )        
        pass
		
    def testJobWorkFlow(self):
        pass
        self._testPostJob()
        self._testPostJob( file = "~/test.sh" )
        self._testPostJob( file = "~/test.sh"  , conf  = job_conf_1 )
        self._testPostJob(  script = None, file = "~/test.sh" )
        jobid = self._testPostJob( script = script_wait  , conf  = job_conf_1 )
        self._testGetJobId(jobid)
        self._testDeleteJob(jobid)
        self._testGetJobId(jobid)
        status = self.mc.output["status"][str(jobid)]
        self.assertEqual( status , "Failed" , "testJobWorkFlow Failed"  )
        
    def testJobWorkFlow2(self):
        self._testPostJob( file = "~/test.sh"  , conf  = job_conf_1 )
        jobid = self._testPostJob( script = script_hello  , conf  = job_conf_1 , test = False )
        self._testGetJobId(jobid , test = False)
        status = self.mc.output["status"]
        status = status.get( str(jobid) ) if str(jobid) in status else {}
        while status == {} or status == 'Pending' or status == 'Running' :
            time.sleep(10)
            self._testGetJobId(jobid , test = False)
            status = self.mc.output["status"]
            status = status.get( str(jobid) ) if str(jobid) in status else {}
        self.isSuccess( jobid , jobconf = job_conf_1 )
              
        
        


		
