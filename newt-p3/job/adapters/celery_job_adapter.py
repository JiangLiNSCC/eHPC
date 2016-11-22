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
from celery import shared_task
from celery.result import AsyncResult

from common.response import json_response
import logging
import re
logger = logging.getLogger("newt." + __name__)
from common import slurmutil
#from common.slurmutil import GlobusHelper
from common.shell import run_command
import tempfile
from common.decorators import login_required , safty_task

#from common.celeryutil import celery_request

@login_required
def get_machines(request):
    """Returns the available machines that jobs can run on
     such as the yhi but on different machines ? : TO-DO NEXT 
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
def view_queue_task(self , taskenv):
    return view_queue_task_unsafty(self , taskenv)    

@safty_task
def view_queue_task_unsafty(self , taskenv):
    """ Celery task for view_queue to call"""
    #mycmd = machine["qstat"]["bin"]
    mycmd = "/usr/bin/squeue"
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
    taskenv = { "user" : request.user.username , "machine" : machine_name }
    rest = view_queue_task.delay( taskenv   )
    return json_response(status="ACCEPT", status_code=201, error="" , content=rest.id)
    #machine = slurmutil.GRID_RESOURCE_TABLE.get(machine_name, None)
    #if not machine:
    #    return json_response(status="ERROR", status_code=400, error="Invalid machine name: %s" % machine_name)
    #env = slurmutil.get_cred_env(request.user)
    #mycmd = "ssh " + machine["hostname"]   +   " ' " + machine["qstat"]["bin"]  + " '"
    #mycmd = machine["qstat"]["bin"] 
    #return celery_request(  request , view_queue_task , machine = machine_name  )

@login_required
def submit_job(request, machine_name):
    """Submits a job to the queue

    Keyword arguments:
    request -- Django HttpRequest
    machine_name -- name of the machine
    """
    pass
    machine = slurmutil.GRID_RESOURCE_TABLE.get(machine_name, None)
    if not machine:
        return json_response(status="ERROR", status_code=400, error="Invalid machine name: %s" % machine_name)
    qsub = machine['qsub']['bin']
    env = slurmutil.get_cred_env(request.user)
    
    if request.POST.get("jobfile", False):
        # Create command for sbatch on an existing slurm file
        job_file_path = request.POST.get("jobfile")
        cmd = "%s %s" % (qsub, job_file_path)
    elif request.POST.get("jobscript", False):
        # Create command for qsub from stdin data
        job_script = request.POST.get("jobscript").encode()

        # Creates a temporary job file
        tmp_job_file = tempfile.NamedTemporaryFile(prefix="newt_")
        print(job_script)
        tmp_job_file.write(job_script)
        tmp_job_file.flush()

        # Stages the temporary job file and pass it as to stdin to qsub
        #flags += " -- %s" % tmp_job_file.name
        cmd = "%s %s" % (qsub, tmp_job_file.name)
    else:
        return json_response(status="ERROR", 
                             status_code=400, 
                             error="No data received")

    try:
        #runner = GlobusHelper(request.user)
        cmd_str = "ssh " + machine["hostname"]   +   '  " ' + cmd +' " '  
        print( cmd_str)
        (output, error, retcode) = run_command(cmd_str, env=env)
    except Exception as ex:
        return json_response(status="ERROR", 
                             status_code=500, 
                             error="qsub failed with error: %s" % str(ex))
    if retcode != 0:
        return json_response(status="ERROR", 
                             status_code=500, 
                             error="qsub failed with error: %s" % error)
    return {"jobid":output.strip().split(' ')[-1]}

    
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
    env = slurmutil.get_cred_env(request.user)
    mycmd = "ssh " + machine["hostname"]   +   " ' " + ' sacct -j  '  + job_id  + " '"
    (output, error, retcode) = run_command( mycmd )
    if retcode !=0 :
        return json_response(status="ERROR", status_code=500, error="Unable to get queue: %s" % error)
    patt = re.compile(r'(?P<jobid>[^\s]+)\s+(?P<jobname>[^\s]+)\s+(?P<partition>[^\s]+)\s+(?P<account>[^\s]+)\s+(?P<alloccpus>[^\s]+)\s+(?P<state>[^\s]+)\s+(?P<exitcode>.*)$')
    output = output.splitlines()
    output = [x.strip() for x in output]
    output = filter(lambda line: patt.match(line), output)
    output = list(map(lambda x: patt.match(x).groupdict(), output))[2:]
    #print( output  )
    return (output)



@login_required
def delete_job(request, machine_name, job_id):
    machine = slurmutil.GRID_RESOURCE_TABLE.get(machine_name, None)
    if not machine:
        return json_response(status="ERROR", status_code=400, error="Invalid machine name: %s" % machine_name)
    env = slurmutil.get_cred_env(request.user)
    mycmd = "ssh " + machine["hostname"]   +   " ' " + ' scancel  '  + job_id  + " '"
    (output, error, retcode) = run_command( mycmd )
    if retcode !=0 :
        return json_response(status="ERROR", status_code=500, error="Unable to get queue: %s" % error)
    return (output)


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
