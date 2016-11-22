class MyRouter(object):
    def route_for_task( self,task,args=None ,kwargs=None ) :
        if isinstance( args[0] , dict ) :
            if "user" in args[0].keys() and "machine" in args[0].keys() :
                return { 'exchange':'ln' , 'exchange_type':'topic','routing_key':'ln.' + args[0]["machine"] }
        #print (args , kwargs)
        #if 'machine' in kwargs :
        #    #print( args , kwargs )
        #    return { 'exchange':'ln' , 'exchange_type':'topic','routing_key':'ln.' + kwargs["machine"] }

