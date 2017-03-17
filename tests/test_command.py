from basetest import BaseTest


class CommandTest(BaseTest):

    def setUp(self):
        super( CommandTest , self ).setUp()
        self.url = "/command/%s/" % self.machine
        self.data = {"command" : "" } 

    def setcommand(self,command):
        self.data["command"] = command
        self.errstr = "%s run : %s " % ( self.url , command )
        self.logger.debug("test api : %s" % self.errstr )

    def testPostCommand(self):
        """Test : POST /api/command/<machine>/ 
            return should be just like this : 
        """
        self.setcommand('echo hello'  )
        self.mc.open(  self.url , data = self.data , login=False)
        self.logger.debug(self.mc.data)
        self.assertEqual( self.mc.ret200() , False , self.errstr + ' without login' )
        self.mc.open(  self.url , data = self.data )
        self.logger.debug(self.mc.data)
        self.assertEqual( self.mc.ret200() , True , self.errstr  )
        assertRest = { 'output': 'hello\n', 'error': '', 'retcode': 0  }
        self.assertEqual( self.mc.output , assertRest , self.errstr  )
        self.setcommand('touch /root/a'  )
        self.mc.open(  self.url , data = self.data )
        self.logger.debug(self.mc.data)
        self.assertEqual( self.mc.ret200() , True , self.errstr  )
        self.assertNotEqual( self.mc.output["retcode"] , 0 , self.errstr  )
        self.assertNotEqual( self.mc.output["error"] , "" , self.errstr  )




