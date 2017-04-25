from common.response import json_response
import logging
logger = logging.getLogger("newt." + __name__)
from common.shell import run_command
import re
#from bson.objectid import ObjectId
from subprocess import Popen, PIPE
from django.conf import settings
from datetime import datetime
import pytz
import tempfile
import os
from common.decorators import login_required 
from common.response import json_response , worker_json_response

@login_required
def get_machines(request):
    """Returns the available machines that jobs can run on

    Keyword arguments:
    request - Django HttpRequest
    """
    return {"localhost": {}}

@login_required
def view_queue(request, machine_name):
    """Returns the current state of the queue in a list

    Keyword arguments:
    request -- Django HttpRequest
    machine_name -- name of the machine
    """
    (output, error, retcode) = run_command('ps -eo "%U %p %P %r %y %x %c %a"')
    #patt = re.compile(r'(?P<user>[^\s]+)\s+(?P<jobid>\d+)\s+(?P<ppid>\d+)\s+(?P<pgid>\d+)\s+(?P<sess>\d+)\s+(?P<jobc>\d+)\s+(?P<status>[^\s]+)\s+(?P<tt>[^\s]+)\s+(?P<timeuse>[^\s]+)\s+(?P<command>.+)')
    patt = re.compile(r'(?P<user>[^\s]+)\s+(?P<jobid>\d+)\s+(?P<ppid>\d+)\s+(?P<pgid>\d+)\s+(?P<tty>[^\s]+)\s+(?P<time>[^\s]+)(?P<command>.+)')
    processes = output.splitlines()[1:]
    #print( processes )
    processes = list(map(lambda x: patt.match(x).groupdict(), processes))
    outjs = { 'status' : {} ,  'name' : {} , 'partition' : {} , 'user' : {} , 'time' : {} , 'id' : {} }
    for ari in processes :
        arid = ari['jobid']
        outjs['status'][arid] = 'Running'
        outjs['name'][arid] = ari['command'].split()[0]
        outjs['partition'][arid] = 'local'
        outjs['user'][arid] = ari['user']
        outjs['time'][arid] = ari['time']
        outjs['id'][arid] = ari['jobid']
    #return worker_json_response( outjs )
    return outjs
    #return worker_json_response(list(output))

@login_required
def submit_job(request, machine_name):
    """Submits a job to the queue

    Keyword arguments:
    request -- Django HttpRequest
    machine_name -- name of the machine
    """
    # Get data from POST
    jobfilepath = request.POST.get("jobfilepath", None  )
    if request.POST.get("jobfile", False):
        with open( os.path.expanduser(  request.POST.get("jobfile")), 'r') as f :
            try :
                jobjobfile = f.read()
            except Exception as e:
                return json_response(status="ERROR", 
                                 status_code=400, 
                                 error="Unable to open job file. Be sure you gave an absolute path.")
    elif request.POST.get("jobscript", False):
        data = request.POST.get("jobscript")
        tmp_job_file = tempfile.NamedTemporaryFile(prefix="newt_" , dir =settings.NEWT_CONFIG["TEMPDIR"] , delete = False)
        tmp_job_file.write(data.encode())
        tmp_job_file.flush()
        tmp_job_file.close()
        jobjobfile =tmp_job_file.name
    else:
        return json_response(status="ERROR", 
                             status_code=400, 
                             error="No data received")

    # Generate unique outfile name
    tmpname = tempfile.mktemp( dir = settings.NEWT_CONFIG['TEMPDIR'] )
    print("tmpname : ", tmpname)
    tmp_job_name = os.path.basename( tmpname )  # str(ObjectId())

    # Get job emulator path
    job_emu = settings.PROJECT_DIR + "/job/adapters/emulate_job_run.sh"

    # Run job with the commands in data
    job = Popen([job_emu, tmp_job_name, request.user.username, jobjobfile], stdout=PIPE)

    # Get/return the job_id from stdout
    job_id = job.stdout.readline().rstrip().decode('utf-8')
    logger.debug("Spawned process: %s" % job_id)
    return {"jobid": job_id}    

@login_required
def get_info(request, machine_name, job_id):
    """Gets the information of a job, given the id

    Keyword arguments:
    request -- Django HttpRequest
    machine_name -- name of the machine
    job_id -- the job id
    """
    try:
        job_out = open("/tmp/newt_processes/%s.log" % job_id, 'r')
        lines = job_out.read().splitlines()
        job_out.close()
    except Exception as e:
        return {
            "jobid": job_id,
            "user": "",
            "status": "queue",
            "time_start": "",
            "time_end": "",
            "time_used": "",
            "output": ""
        }
    output = "\n".join(lines[1:])
    info = lines[0].split("; ")
    time_start = datetime.fromtimestamp(float(info[3]), tz=pytz.timezone("utc"))
    time_end = "" if info[2] == "999" else datetime.fromtimestamp(float(info[4]), tz=pytz.timezone("utc"))
    if info[2] == "999":
        time_used = datetime.utcnow().replace(tzinfo=pytz.timezone(("utc"))) - time_start
    else:
        time_used = time_end - time_start
    info = {
        "jobid": info[0],
        "user": info[1],
        "status": "running" if info[2] == "999" else info[2],
        "time_start": str(time_start),
        "time_end": str(time_end),
        "time_used": str(time_used),
        "output": output
    }
    return info    

@login_required
def delete_job(request, machine_name, job_id):
    """Gets the information of a job, given the id

    Keyword arguments:
    request -- Django HttpRequest
    machine_name -- name of the machine
    job_id -- the job id
    """
    (output, error, retcode) = run_command("kill %s" % job_id)
    if retcode != 0:
        return json_response(status="ERROR",
                             status_code=500,
                             error=error)
    return {"output": output}

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
