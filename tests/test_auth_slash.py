from basetest import BaseTest


class RootTest(BaseTest):

    def testRoot(self):
        """Test : GET /api 
            return should be just like this : 
            {u'status': u'OK', u'output': {u'text': u'Welcome to eHPC ', u'version': u'0.0.2'}, u'status_code': 200, u'error': u''}
        """
        self.assertEqual( 1 , 1 , 'test 1 1 fail'  )
        self.logger.debug( "test api: GET /api (1 test)" )
        self.mc.open("" , login=False)
        self.logger.debug(self.mc.data)
        self.assertEqual( self.mc.ret200() , True , 'GET /api Failed!')


class AuthTest(BaseTest):

    def testPostAuthNotLogin(self):
        """Test : POST /api/auth without data
           return should be just like :
           {u'status': u'OK', u'output': {u'username': None, u'session_lifetime': 0, u'auth': False, u'newt_sessionid': None}, u'status_code': 200, u'error': u''}
        """
        self.logger.debug( "test api: POST /api/auth " )
        self.mc.open( "/auth/" , login=False  )
        self.logger.debug( self.mc.data  )
        errstr = 'POST /api/auth (not login) failed!'
        self.assertEqual( self.mc.ret200() , True , errstr )
        self.assertEqual( self.mc.data['output']['auth'] , False , errstr )
        self.assertEqual( self.mc.data['output']['username'] , None , errstr )

    def testPostAuthLoginTrue(self):
        """Test : POST /api/auth with correct data
           return should be just like :
           {u'status': u'OK', u'output': {u'username': u'nscc-gz_jiangli', u'session_lifetime': 1209600, u'auth': True, u'newt_sessionid': u'ukf1yy2zywzo78lyrpwrqfu3666l4c3k'}, u'status_code': 200, u'error': u''}
        """
        self.logger.debug( "test api: POST /api/auth data={username = username , password = password }" )
        self.mc.open( "/auth/" , login=False , data = self.login_data )
        self.logger.debug( self.mc.data  )
        errstr = 'POST /api/auth (login) failed!'
        self.assertEqual( self.mc.ret200() , True , errstr + ', not return 200' )
        self.assertEqual( self.mc.data['output']['auth'] , True , errstr + ', not output auth True' )
        self.assertEqual( self.mc.data['output']['username'] , self.username , errstr  + ', not get correct username')


    def testPostAuthLoginFalse(self):
        """Test : POST /api/auth with wrong data
           return should be just like :
           {u'status': u'OK', u'output': {u'username': None, u'session_lifetime': 0, u'auth': False, u'newt_sessionid': None}, u'status_code': 200, u'error': u''}
        """
        self.mc.open( "/auth/" , login=False , data = {'username':'x' , 'password' : 'y'} )
        self.logger.debug( "test api: POST /api/auth data={username = 'x' , password = 'y' }" )
        self.logger.debug( self.mc.data  )
        errstr = 'POST /api/auth (login) failed!'
        self.assertEqual( self.mc.ret200() , True , errstr + ', not return 200' )
        self.assertEqual( self.mc.data['output']['auth'] , False , errstr + ', not output auth False' )
        self.assertEqual( self.mc.data['output']['username'] , None , errstr )

        

    def testGetAuthLoginFalse(self):
        """Test : GET /api/auth without login
           Should return like : {u'status': u'OK', u'output': {u'username': None, u'session_lifetime': 0, u'auth': False, u'newt_sessionid': None}, u'status_code': 200, u'error': u''} 
        """
        self.logger.debug("Test : GET /api/auth without login")
        self.mc.open( "/auth/" , login=False  )
        self.logger.debug( self.mc.data)
        #({u'status': u'OK', u'output': {u'username': None, u'session_lifetime': 0, u'auth': False, u'newt_sessionid': None}, u'status_code': 200, u'error': u''}, u'OK')
        errstr = 'GET /api/auth (not login) failed!'
        self.assertEqual( self.mc.ret200() , True , errstr + ', not return 200' )
        self.assertEqual( self.mc.data['output']['auth'] , False , errstr + ', output auth error' )
        self.assertEqual( self.mc.data['output']['username'] , None , errstr  + ', output username error')


    def testGetAuthLoginTrue(self):
        """Test : GET /api/auth without login
           Should return like : {u'status': u'OK', u'output': {u'username': None, u'session_lifetime': 0, u'auth': False, u'newt_sessionid': None}, u'status_code': 200, u'error': u''}
        """
        self.logger.debug("Test : GET /api/auth with login")
        self.mc.open( "/auth/" ,  )
        self.logger.debug( self.mc.data)
        #({u'status': u'OK', u'output': {u'username': None, u'session_lifetime': 0, u'auth': False, u'newt_sessionid': None}, u'status_code': 200, u'error': u''}, u'OK')
        errstr = 'GET /api/auth ( login) failed!'
        self.assertEqual( self.mc.ret200() , True , errstr + ', not return 200' )
        self.assertEqual( self.mc.data['output']['auth'] , True , errstr + ', output auth error' )
        self.assertEqual( self.mc.data['output']['username'] , self.username , errstr  + ', output username error')

    def testDeleteAuth(self):
        """Test : Delete /api/auth 
           After Delete the cookie should not be used.
           {u'status': u'OK', u'output': {u'username': None, u'session_lifetime': 0, u'auth': False, u'newt_sessionid': None}, u'status_code': 200, u'error': u''}
        """
        self.logger.debug("Test : DELETE /api/auth ")
        self.mc.open( "/auth/" , login=True , method = "DELETE"  )
        self.logger.debug( self.mc.data)
        errstr = 'DELETE /api/auth (login) failed!'
        self.assertEqual( self.mc.ret200() , True , errstr + ', not return 200' )
        self.assertEqual( self.mc.data['output']['auth'] , False , errstr + ', not output auth False' )
        self.assertEqual( self.mc.data['output']['username'] , None , errstr )
        self.mc.open( "/auth/" , login=True   )
        self.logger.debug("Test :  /api/auth with cookie after logout ")
        self.logger.debug( self.mc.data)
        self.assertEqual( self.mc.ret200() , True , errstr + ', not return 200' )
        self.assertEqual( self.mc.data['output']['auth'] , False , errstr + ', not output auth False' )
        self.assertEqual( self.mc.data['output']['username'] , None , errstr )
        self.mc.login() # re-login
        self.logger.debug("relogin after test logout")
        self.logger.debug( self.mc.data)
        self.assertEqual( self.mc.ret200() , True , errstr + ', not return 200' )
        self.assertEqual( self.mc.data['output']['auth'] , True , errstr + ', not output auth False' )


