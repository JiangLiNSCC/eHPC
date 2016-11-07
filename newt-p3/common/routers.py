class MyRouter(object):
    def route_for_task( self,task,args=None ,kwargs=None ) :
        if 'machine' in kwargs :
            #print( args , kwargs )
            return { 'exchange':'ln' , 'exchange_type':'topic','routing_key':'ln.' + kwargs["machine"] }

