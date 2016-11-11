from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HPCJob(models.Model):
    '''
    This models store the job infos in DB.
    jobfile : link to the file-obj in the File System
    jobfile_args : jobfile may have args
    user : link to user of the jobfile
    machine : the machine the job submit on ( ln3 / ln4 /ln6   )
    jobid : the jobid create by slurm
    status : the status got from slurm
    time_create : the time the job object create
    time_submit : the time the job submit 
    time_start : the time the job start to run
    time_end : the time the job end run
    time_limit : the time limit of the job to run
    time_hold : the time hold of the job

    partition : the partition the job run on 
    scale_cores : at least the num of cores should be used
    scale_memGB : at least the num of memory (GB) should be used
    scale_Nodes : at least the num of Nodes should be used

    actions : 
    * create obj : once create , [ user , *machine , time_create , ] is fixed.
    * submit : util submit  [ jobfile , partition , scale_* , info ] could be changed .
        once submit success , [ time_submit ] create , [status] could be got from slurm
    * finish run : once the job finished , all the infos could not change except the [info]. 
    
    status : [ unsubmit , pending , runing , hold , success , failed  ]

    functions :
    HPCJob.__init__
    HPCJob.submit
    HPCJob.get_status
    HPCJob.set( keyword = value  )
    HPCJob.fork( ... ...  ) create a new HPCJob from an exsit one 
    HPCJob.resubmit( ... ... ) auto fork and use the old jobfile again . 
    '''
    class Meta:
        app_label = 'job'
    jobfile = models.FilePathField()  #models.TextField()
    jobfile_args = models.CharField(max_length=128)
    job_wdir = models.FilePathField() # ADD , which dir to submit the job
    user = models.ForeignKey(User) # id_user
    machine = models.CharField(max_length=10)
    jobid = models.IntegerField( null=True  )
    exit_code = models.IntegerField( null=True  ) # exit_code
    job_name = models.CharField(max_length=255)  # job_name
    state = models.CharField(max_length=10) # status() convert state 
    time_create = models.DateTimeField( null=True , auto_now_add = True )
    time_submit = models.DateTimeField( null=True )
    time_start = models.DateTimeField( null=True)
    time_end = models.DateTimeField( null=True)
    time_hold = models.TimeField( null=True)
    time_limit = models.TimeField( null=True) # timelimit
    partition = models.CharField(max_length=255) # partition
    scale_cores = models.IntegerField( null=True,default=1)  #cpus_req
    scale_memGB = models.IntegerField( null=True,default = 0) # mem_req  
    scale_Nodes = models.IntegerField( null=True,default = 1) # nodes_alloc 
    info = models.TextField( ) # other infomations in json dict , such as software/app , ... 
    def __str__(self):
        return self.machine + ':' + str(self.jobid)
    #def __init__(self , user , jobfile) :
    #    self.user = user
    #    self.jobfile = jobfile 
