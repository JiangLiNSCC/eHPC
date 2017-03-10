from common.tools import ResultParser

slurm_convert_status = {
             'RUNNING' : 'Running' ,
             'COMPLETED' : 'Success' ,
             'CANCELLED' : 'Failed' ,
             'CONFIGURING' : 'Pending' ,
             'COMPLETING' : 'Success' ,
             'FAILED' : 'Failed' ,
             'NODE_FAIL' : 'Failed' ,
             'PENDING' : 'Pending' ,
             'SUSPENDED' : 'Suspended',
             'R' : 'Running' ,
             'CD' : 'Success' ,
             'CA' : 'Failed' ,
             'CF' : 'Pending' ,
             'CG' : 'Success' ,
             'F' : 'Failed' ,
             'NF' : 'Failed' ,
             'PD' : 'Pending' ,
             'S' : 'Suspended',
         } 

class SlurmStatResultParser( ResultParser ):
    filter = {
         'from' : [ 'NAME' , 'PARTITION' , 'JOBID' , 'NODELIST(REASON)' , 'ST' , 'USER' , 'TIME' , 'NODES'   ] ,
         'to'   : [ 'name' , 'partition' , 'id' , 'nodelist' , 'status' , 'user' , 'time' , 'nodes' ] ,
        
    }
    convert = {
         'status' : slurm_convert_status ,
         'nodes' : lambda x : int(x) ,

    }

class SlurmAcctResultParser( ResultParser ):
    filter = {
        'from' : [ 'JobID' , 'NTasks' , 'Elapsed' , 'Partition' , 'JobName' , 'State', 'AllocCPUS', 'ExitCode'  ] ,
        'to'   : [ 'id' , 'tasks' , 'time' , 'partition' , 'name' , 'status' , 'nodes' , 'exitcode'],
    }
    convert = {
        'status' :  slurm_convert_status , 
        'nodes' : lambda x : int(x)/24,
    }


class HPCJobHandler(object):
    args_parser = None
    args_default = {
        "partition" : "" , 
        "time_limit" : None ,
        "scale_cores" : 1 ,
        "scale_memGB" : 0 ,
        "scale_Nodes" : 1 ,
}
    @classmethod
    def gen_args(cls , job):
        arg_list=[]
        for argi in cls.args_parser :
            if job.__dict__[ argi  ] and job.__dict__[ argi  ] != cls.args_default.get( argi  , None) :
                if callable( cls.args_parser[ argi  ] ) :
                    arg_list.append( cls.args_parser[ argi  ]( job )   )
                else :
                    arg_list.append( cls.args_parser[ argi  ] % job.__dict__[ argi  ]   )
        return "".join(arg_list)

class SlurmHPCJobHandler(HPCJobHandler):
    args_parser = {
        "job_wdir" : " -D %s " ,
        "job_name" : " -J %s ",
        "partition" : " -p %s " ,
        "time_limit" : " -t %s " ,
        "scale_cores" : " -n %s " ,
        "scale_memGB" : lambda job :  " --mem=%s "  % ( job.scale_memGB * 1024 )  ,
        "scale_Nodes" : " -N %s " ,
    }
      


