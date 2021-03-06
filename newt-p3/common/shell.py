from __future__ import absolute_import
from celery import shared_task

from subprocess import PIPE, Popen
import shlex
import re
import string
import os

import logging
import signal
from django.utils.encoding import smart_str



logger = logging.getLogger("newt."+__name__)


class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

# initialization code
try:
    signal.signal(signal.SIGALRM, alarm_handler)
except ValueError as e:
    logger.warning('setting alarm handler failed: "%s"' %e)

#@shared_task
def run_command(command, env=None, timeout=600 , decode ='utf-8' , bash = False ):
    #args = shlex.split(smart_str(command))
    if bash :
        #command =  ''' bash -c -l ' %s '  ''' % command  # [ 'bash' , '-c' , '-l' , ' " ' + command + ' " ' ]
        env_backup = os.environ.copy()
        for i in os.environ.keys() :
            os.unsetenv( i )
        args = [ "bash" , "-c" , "-l" , command ]
    else :
        args = shlex.split(smart_str(command))
    try:
        p = Popen(args, stdout=PIPE, stderr=PIPE, env=env)
    except OSError as  ex:
        logger.error('running command failed: "%s", OSError "%s"' %(' '.join(args), ex))
        raise ex
    
    
    output = ""
    error = ""
    retcode = 0


    # Timeout the call if the proc is hung. Default is 10 min (tweak the value?)
    signal.alarm(timeout)
    try:
        # Note - we can't rely on p.poll() to return a value since this deadlocks when the buffer fills up
        # p.communicate() will always returns on process completion
        (output, error) = p.communicate()
        retcode=p.poll()
        signal.alarm(0)  # reset the alarm
    except Alarm:
        # logger.error('process reached deadline without returning')
        logger.error('command "%s", reached deadline try to terminate' % (command))
        os.kill(p.pid, signal.SIGKILL)
        raise RuntimeError('command "%s", reached deadline and was terminated' % (command))
    if retcode != 0:
        # May not want to expose user to error
        #os.strerror(retcode)
        logger.warning('command "%s", exit: %d <br> %s' % (command, retcode, error))
    return (output.decode( decode ), error.decode( decode  ), retcode)
