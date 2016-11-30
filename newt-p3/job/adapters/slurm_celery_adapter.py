"""Job Adapter Template File

IMPORTANT: NOT A FUNCTIONAL ADAPTER. FUNCTIONS MUST BE IMPLEMENTED

Notes:
    - Each of the functions defined below must return a json serializable
      object, json_response, or valid HttpResponse object
    - A json_response creates an HttpResponse object given parameters:
        - content: string with the contents of the response 
        - status: string with the status of the response 
        - status_code: HTTP status code 
        - error: string with the error message if there is one 
"""
from __future__ import absolute_import
from celery import shared_task , chain , chord
from common.response import json_response
import logging
import re
logger = logging.getLogger("newt." + __name__)
from common import slurmutil
#from common.slurmutil import GlobusHelper
from common.shell import run_command
import tempfile
from common.decorators import login_required , safty_task , unsafty_task
import socket
from file.adapters.celery_file_adapter import put_file_task
from django.contrib.auth.models import User
from job.adapters.job_models import HPCJob
import os
from pwd import getpwnam
import sys
from django.core.cache import cache


@login_required
def get_machines(request):
    """Returns the available machines that jobs can run on
    TO-DO : do a yhi for 
    Keyword arguments:
    request - Django HttpRequest
    """
    machines = {}
    #for (machine, attrs) in gridutil.GRID_RESOURCE_TABLE.iteritems(): not work on python3
    for (machine, attrs) in slurmutil.GRID_RESOURCE_TABLE.items():
        if attrs['jobmanagers'] != {}:
            machines[machine] = attrs['jobmanagers']
    return machines

@shared_task(bind=True , track_started=True )
def view_queue_task(self,task_env):
    return view_queue_task_unsafty(self,task_env )

@safty_task
def view_queue_task_unsafty(self,task_env ):
    mycmd = 'squeue'
    #mycmd = "ssh " + machine["hostname"]   +   " ' " + machine["qstat"]["bin"]  + " '"
    (output, error, retcode) = run_command( mycmd )
    if retcode !=0 :
        return json_response(status="ERROR", status_code=500, error="Unable to get queue: %s" % error)
    patt = re.compile(r'(?P<jobid>[^\s]+)\s+(?P<partition>[^\s]+)\s+(?P<job_name>[^\s]+)\s+(?P<user>[^\s]+)\s+(?P<state>[^\s]+)\s+(?P<time>[^\s]+)\s+(?P<nodes>\d+)\s+(?P<nodelist>.*)$')
    output = output.splitlines()
    output = [x.strip() for x in output]
    output = filter(lambda line: patt.match(line), output)
    output = map(lambda x: patt.match(x).groupdict(), output)
    #print( list(output)  )
    return list(output)

@login_required
def view_queue(request, machine_name):
    """Returns the current state of the queue in a list

    Keyword arguments:
    request -- Django HttpRequest
    machine_name -- name of the machine
    """
    pass
    machine = slurmutil.GRID_RESOURCE_TABLE.get(machine_name, None)
    if not machine:
        return json_response(status="ERROR", status_code=400, error="Invalid machine name: %s" % machine_name)
    taskenv = { "user" : request.user.username , "machine" : machine_name }
    rest = view_queue_task.delay( taskenv    )
    cache.set("async-" + rest.id , "AsyncJob" , 3600 )
    return json_response(status="ACCEPT", status_code=201, error="" , content=rest.id)

@shared_task(bind=True , track_started=True )
def submit_job_task(self , task_env , HPCJobid ):
    return submit_job_task_unsafty(self , task_env , HPCJobid )

@safty_task
def submit_job_task_unsafty(self , taskenv , HPCJobid ):
    pass
    try :
        job = HPCJob.objects.get( id = HPCJobid  )
    except ImportError :
        return sys.path
    if  job.jobid : 
        return json_response(status="ERROR",
                             status_code=500,
                             error="The Job have submit once : %s" % job.jobid )
    if job.state == "tempfile" :
        # mv jobfile to user dir 
        src = job.jobfile
        temphost = taskenv["host"]
        dest = os.path.join(  getpwnam( job.user.username ).pw_dir , 'newt' , str(job.id)  , os.path.basename( job.jobfile  ) )
        os.makedirs( os.path.dirname( dest ) )
        put_file_task( taskenv, temphost ,  src, dest )
        pass
        #dest = os.path.join(  getpwnam( job.user.username ).pw_dir , 'newt' , str(job.id)  , os.path.basename( job.jobfile  ) )
        if not  os.path.isfile( dest) :
            return json_response(status="ERROR",
                             status_code=500,
                             error="Cannot find tmpfile : %s" % dest )
        else :
            job.jobfile = dest 
            job.state = "unsubmit"
            job.save() # can not save as readonly
    qsub = "/usr/bin/sbatch"
    #cmd_str = ''' bash -c -l "%s %s %s"  ''' % (qsub, job.jobfile , job.jobfile_args )
    cmd_str = "%s %s %s" % (qsub, job.jobfile , job.jobfile_args)
    os.environ['PWD'] = os.path.dirname( job.jobfile  )
    os.chdir( os.path.dirname( job.jobfile  )  )
    (output, error, retcode) = run_command(cmd_str , bash = True)
    if retcode != 0:
        return json_response(status="ERROR", 
                             status_code=500, 
                             error="qsub failed with error: %s" % error)
    job.jobid = output.strip().split(' ')[-1]
    job.state = "submited"
    job.save() # can not save as readonly 
    return {"jobid":job.jobid}


@login_required
def submit_job(request, machine_name):
    """Submits a job to the queue

    Keyword arguments:
    request -- Django HttpRequest
    machine_name -- name of the machine
    """
    pass
    user = request.user # User.objects.get(username=username)
    job = HPCJob( user = user,jobfile = '' , machine = machine_name )
    if request.POST.get("jobfile", False):
        # Create command for sbatch on an existing slurm file
        job_file_path = request.POST.get("jobfile")
        job.jobfile = job_file_path
        job.state = "unsubmit"
        #cmd = "%s %s" % (qsub, job_file_path)
    elif request.POST.get("jobscript", False):
        # Create command for qsub from stdin data
        job_script = request.POST.get("jobscript").encode()
        # Creates a temporary job file
        tmp_job_file = tempfile.NamedTemporaryFile(prefix="newt_" , dir = '/tmp/jobfile' , delete = False)
        print(job_script)
        tmp_job_file.write(job_script)
        tmp_job_file.flush()
        tmp_job_file.close()
        job.jobfile = tmp_job_file.name
        job.state = "tempfile"
        #cmd = "%s %s" % (qsub, tmp_job_file.name)
        username = user.username #taskenv["user"]
        ngid = getpwnam( username ).pw_gid
        nuid = getpwnam( username ).pw_uid
        os.chown( job.jobfile  , nuid , ngid )
    else:
        return json_response(status="ERROR", 
                             status_code=400, 
                             error="No data received")
    #job = HPCJob( user = user,jobfile = jobfile , machine = machine_name )
    job.save()
    taskenv = { "user" : request.user.username , "machine" : machine_name }
    if job.state == "tempfile" :
        pass
        taskenv["host"] = socket.gethostname()
    rest = submit_job_task.delay( taskenv , job.id   )
    cache.set("async-" + rest.id , "AsyncJob" , 3600 )
    return json_response(status="ACCEPT", status_code=201, error="" , content=rest.id)


@shared_task(bind=True , track_started=True )
def get_info_task(self , taskenv , HPCJobid):
    return get_info_task_unsafty(self , taskenv , HPCJobid)

@safty_task
def get_info_task_unsafty(self , taskenv , HPCJobid):
    job = HPCJob.objects.get( id = HPCJobid )
    job_id = job.jobid
    mycmd =  ' sacct -j  '  + str(job_id ) 
    (output, error, retcode) = run_command( mycmd  , bash = True )
    if retcode !=0 :
        return json_response(status="ERROR", status_code=500, error="Unable to get queue: %s" % error)
    patt = re.compile(r'(?P<jobid>[^\s]+)\s+(?P<jobname>[^\s]+)\s+(?P<partition>[^\s]+)\s+(?P<account>[^\s]+)\s+(?P<alloccpus>[^\s]+)\s+(?P<state>[^\s]+)\s+(?P<exitcode>.*)$')
    #return output
    output = output.splitlines()
    output = [x.strip() for x in output]
    output = filter(lambda line: patt.match(line), output)
    output = list(map(lambda x: patt.match(x).groupdict(), output))[2:]
    if output :
        job.partition = output[0]["partition"]
        job.exit_code = output[0]["exitcode"].split(':')[1]
        job.job_name = output[0]["jobname"]
        job.state = output[0]["state"]
        job.save()
    return output

    
@login_required
def get_info(request, machine_name, job_id):
    """Gets the information of a job, given the id

    Keyword arguments:
    machine_name -- name of the machine
    job_id -- the job id
    """
    pass
    machine = slurmutil.GRID_RESOURCE_TABLE.get(machine_name, None)
    if not machine:
        return json_response(status="ERROR", status_code=400, error="Invalid machine name: %s" % machine_name)
    taskenv = { "user" : request.user.username , "machine" : machine_name }
    try :
        job = HPCJob.objects.get(machine= machine_name ,jobid= job_id , user= request.user )
    except Exception as ex :
        return json_response(status="ERROR", status_code=400, error="get job error : %s" % ex)
    if job.state == "COMPLETED" or job.state == "FAILED" :
        return {"partition": job.state , "jobid": job.jobid, "state": job.state, "exitcode": job.exit_code, "jobname": job.job_name }
    rest = get_info_task.delay( taskenv , job.id   )
    cache.set("async-" + rest.id , "AsyncJob" , 3600 )
    return json_response(status="ACCEPT", status_code=201, error="" , content=rest.id)

@shared_task(bind=True , track_started=True )
def delete_job_task( self , taskenv , job_id  ):
    return delete_job_task_unsafty( self , taskenv , job_id  )

@safty_task
def delete_job_task_unsafty( self , taskenv , job_id  ):
    mycmd = ' scancel  '  + str( job_id ) 
    (output, error, retcode) = run_command( mycmd , bash = True )
    if retcode !=0 :
        return json_response(status="ERROR", status_code=500, error="Unable to get queue: %s" % error)
    return (output)

@login_required
def delete_job(request, machine_name, job_id):
    machine = slurmutil.GRID_RESOURCE_TABLE.get(machine_name, None)
    if not machine:
        return json_response(status="ERROR", status_code=400, error="Invalid machine name: %s" % machine_name)
    taskenv = { "user" : request.user.username , "machine" : machine_name }   
    rest = delete_job_task.delay( taskenv , job_id   )
    cache.set("async-" + rest.id , "AsyncJob" , 3600 )
    return json_response(status="ACCEPT", status_code=201, error="" , content=rest.id)
    #env = slurmutil.get_cred_env(request.user)
    #mycmd = "ssh " + machine["hostname"]   +   " ' " + ' scancel  '  + job_id  + " '"
    #(output, error, retcode) = run_command( mycmd )
    #if retcode !=0 :
    #    return json_response(status="ERROR", status_code=500, error="Unable to get queue: %s" % error)
    #return (output)


patterns = (
)

def extras_router(request, query):
    """Maps a query to a function if the pattern matches and returns result

    Keyword arguments:
    request -- Django HttpRequest
    query -- the query to be matched against
    """
    for pattern, func, req in patterns:
        match = pattern.match(query)
        if match and req:
            return func(request, **match.groupdict())
        elif match:
            return func(**match.groupdict())

    # Returns an Unimplemented response if no pattern matches
    return json_response(status="Unimplemented", 
                             status_code=501, 
                             error="", 
                             content="query: %s" % query)
