from common.shell import run_command
from common.response import json_response
from django.conf import settings

import logging
logger = logging.getLogger("newt." + __name__)


def execute(request, machine_name, command):
    conf = settings.NEWT_CONFIG
    try:
        hostname = None
        for s in conf['SYSTEMS']:
            if machine_name==s['NAME']:
                hostname = s['HOSTNAME']
                break

        if hostname is None:
            return json_response(status="ERROR",
                                 status_code=404,
                                 error="Unrecognized system: %s" % machine_name)
        #user = request.POST.get('sudo_user')
        logger.debug("Running command(ssh): %s  (@ %s)" % (command, machine_name))
        #command = "sudo -u %s %s " % (user, command)
        command =  'ssh %s " %s " ' % (hostname, command)
        (output, error, retcode) = run_command(command)
        response = {
            'output': output,
            'error': error,
            'retcode': retcode
        }
        return response
    except Exception as e:
        logger.error("Could not run command: %s" % str(e))
        return json_response(error="Could not run command: %s" % str(e), status="ERROR", status_code=500)


def get_systems(request):
    conf = settings.NEWT_CONFIG
    return [ x["NAME"]  for x in  conf['SYSTEMS'] ]

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
