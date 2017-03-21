from basetest import BaseTest


class AlwaysFalseTest(BaseTest):

    def testRoot(self):
        """Test : GET /api 
        """
        self.assertEqual( 1 , 2 , 'test 1 1 fail'  )
        self.logger.debug( "test always false" )



