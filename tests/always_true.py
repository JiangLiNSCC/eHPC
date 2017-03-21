from basetest import BaseTest


class AlwaysTrueTest(BaseTest):

    def testRoot(self):
        """Test : aways true 
        """
        self.assertEqual( 1 , 1 , 'test 1 1 fail'  )
        self.logger.debug( "test always true!" )
        #self.mc.open("" , login=False)
        #self.logger.debug(self.mc.data)
        #self.assertEqual( self.mc.ret200() , True , 'GET /api Failed!')



