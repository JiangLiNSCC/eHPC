from basetest import BaseTest
import time
import random
import string

def random_string( dig ):
    return ''.join(random.sample( string.ascii_letters + string.digits ,dig))

class FileTest(BaseTest):

    def testGetFileMachinePath(self):
        """Test :  GET /api/file/<machine>/<path>
           return should be just like :

           {u'status': u'OK', u'output': [ ... , 

{u'date(c)': 1479190687.7819555, u'uid': 0, u'perms': u'drwxr-xr-x', u'hardlinks': 15, u'name': u'usr', u'date(a)': 1489477508.7897112, u'gid': 0, u'size(B)': 4096, u'date(m)': 1473753526.0},
 , ...

,], u'status_code': 200, u'error': u''}
        """
        self.logger.debug( "test api: GET /api/file/<machine> " )
        testpath = "/"
        self.mc.open( "/file/%s/%s" % (self.machine , testpath),login=False  )
        self.logger.debug( self.mc.data  )
        errstr = 'GET /api/file/%s/%s  failed!'  % (self.machine , testpath)
        self.assertEqual( self.mc.ret200() , False , errstr + ' test not login')
        self.mc.open( "/file/%s/%s" % (self.machine , testpath ))
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , True , errstr )
        outputlen = len( self.mc.data['output'] )
        self.assertEqual( outputlen > 5 , True , errstr ) # opt , usr , lib , proc , dev , etc ...
        has_etc = False
        for itemi in self.mc.data['output'] :
            if itemi.get( 'name' , None) == 'etc' :
                has_etc = True
        self.assertEqual( has_etc , True , errstr )

    def testGetFileMachinePathNoPermission(self):
        """Test :  GET /api/file/<machine>/<path> with path no Permission
           return should be just like :
        """
        self.logger.debug( "test api: GET /api/file/<machine> (no Permission)" )
        testpath = "/proc/1/"
        errstr = 'GET /api/file/%s/%s  !' % (self.machine , testpath)
        self.mc.open( "/file/%s/%s" % (self.machine , testpath), )
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , True , errstr )
        testpath = "/proc/1/cwd"
        errstr = 'GET /api/file/%s%s  !' % (self.machine , testpath)
        self.mc.open( "/file/%s/%s" % (self.machine , testpath), )
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , False , errstr )


    def testGetFileMachinePathHome(self):
        """Test :  GET /api/file/<machine>/<path> with path no Permission
           return should be just like :
        """
        self.logger.debug( "test api: GET /api/file/<machine> (no Permission)" )
        testpath = "~"
        errstr = 'GET /api/file/%s/%s  !' % (self.machine , testpath)
        self.mc.open( "/file/%s/%s" % (self.machine , testpath), )
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , True , errstr )
    
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
        testdata = "Test API at %s" % str(time.time())
        filename = "~/eHPC_test_%s" % random_string(8)
        url = '/file/%s/%s' % ( self.machine , filename )
        errstr= 'PUT /api/%s' % url
        self.logger.debug( "test upload file : %s" % errstr )
        self.mc.open( url  , method = "PUT" , data = testdata  , login = False ) # t1
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , False , errstr )
        self.mc.open( url  , method = "PUT" , data = testdata   ) #t2
        self.logger.debug( self.mc.data  )
        self.assertEqual( self.mc.ret200() , True , errstr )
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
        self.logger.debug( 'Download 1 response: '+ self.mc.data  )
        self.assertEqual( self.mc.ret200() , True , errstr )
        if self.mc.retjson :
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


