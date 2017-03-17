from basetest import BaseTest
import time
import random
import string

def random_string( dig ):
    return ''.join(random.sample( string.ascii_letters + string.digits ,dig))

class FileTest(BaseTest):

   
    def testFileUpDown(self):
        """Test Servel API and one time : Upload a File , Download a File , Delete a File
         T1  PUT /api/<machine>/<file> Not Login
         t2  PUT /api/<machine>/<file>  Login
         t3  PUT /api/<machine>/<file>  Login but error path
         t4  Download /api/<machine>/<file> Not Login
         t5  Download /api/<machine>/<file> Login
         t5+  Download /api/<machine>/token Login
         t6  Download /api/<machine>/<file> Login but error path  
           
        """
        self.logger.debug( "test api: Upload , Download , Delete " )
        testdata0 = "Test API at %s" % str(time.time())
        testdata = testdata0 * 100000
        filename = "~/eHPC_test_%s" % random_string(8)
        url = '/file/%s/%s' % ( self.machine , filename )
        errstr= 'PUT /api/%s' % url
        self.logger.debug( "test upload file : %s" % errstr )
        #self.mc.open( url  , method = "PUT" , data = testdata  , login = False ) # t1
        #self.logger.debug( self.mc.data  )
        #self.assertEqual( self.mc.ret200() , False , errstr )
        self.mc.open( url  , method = "PUT" , data = testdata   ) #t2
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , False , errstr )
        testdata = testdata0 * 40000
        self.mc.open( url  , method = "PUT" , data = testdata   )
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , True , errstr )
        return True
        self.mc.open( '/file/%s/%s' % ( self.machine , '/root/errorfile' )  , method = "PUT" , data = testdata   ) #t3
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , False , errstr )
        url="%s?download=True" % url
        errstr= 'GET /api/%s' % url
        self.logger.debug( "test download file : %s" % errstr )
        self.mc.open( url  , login = False ) #t4
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , False , errstr )
        self.mc.open( url   ) #5
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , True , errstr )
        self.mc.open( '/file/%s/%s?download=True' % ( self.machine ,  self.mc.data["output"] ) , retjson = False  ) #5 +
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , True , errstr )
        gotdata = self.mc.data if isinstance( self.mc.data , str ) else self.mc.data.decode('utf-8')
        self.assertEqual( gotdata , testdata  , errstr )
        # try to delete 
        self.mc.open( "/command/%s" %  self.machine , data = {"command" : "rm %s" % filename}  )
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , True , errstr )
        self.mc.open( '/file/%s/%s?download=True' % ( self.machine , '/root/a' )     ) #t6
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , False , errstr )
        
        
        

        
#if False : 


