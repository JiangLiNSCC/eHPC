from __future__ import absolute_import
from celery import shared_task
from newt.celery import app
from common.shell import run_command
import re
import magic
import logging
from django.http import StreamingHttpResponse
from common.response import json_response
import tempfile
from common.decorators import login_required , safty_task
import os ,stat
from pwd import getpwnam , getpwuid
import socket
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger("newt." + __name__)
tempdir = settings.NEWT_CONFIG["TEMPDIR"]
localcookies = settings.NEWT_CONFIG["LOCALCOOKIES"]
machine_default = settings.NEWT_CONFIG["MACHINE_DEFAULT"]
def get_mime_type(machine_name=None, path=None, file_handle=None):
    if file_handle:
        try:
            content_type = magic.from_buffer(file_handle.read(1024), mime=True)
        except Exception as e:
            logger.warning("Could not get mime type %s" % str(e))
            content_type = 'application/octet-stream'
        file_handle.seek(0)
    elif path:
        try:
            content_type = magic.from_file(path)
        except Exception as e:
            logger.warning("Could not get mime type %s" % str(e))
            content_type = 'application/octet-stream'
    else:
        content_type = 'application/octet-stream'
    return content_type   

def is_readable( path , user):
    #print( path , user ) 
    try : 
       user_info = getpwnam( user )
       uid = user_info.pw_uid
       gid = user_info.pw_gid
       s = os.stat( path )
       mode = s[ stat.ST_MODE ]
       return (
        ((s[stat.ST_UID] == uid) and ( mode & stat.S_IRUSR >0 )) or
        ( (s[stat.ST_GID] == gid) and ( mode & stat.S_IRGRP >0 ) ) or
        ( mode & stat.S_IROTH )
       )
    except Exception as ex :
       return False

@shared_task(bind=True , track_started=True )
def download_path_task(self, taskenv , path ):
    return download_path_task_unsafty(self, taskenv , path )

@safty_task
def download_path_task_unsafty(self, taskenv , path ):
    src = path 
    temphost = taskenv["host"]
    #dest =  '/tmp/tmpfile/'+ self.request.id 
    cookie_file =  os.path.join( getpwuid(os.getuid()).pw_dir , localcookies)
    command = '''  curl -b %s  -T %s  "%s://%s:%s/api/file/%s/%s?local=True" ''' % ( cookie_file , src , 'http' , temphost , '8000' , machine_default  , self.request.id  )
    #(output, error, retcode) = run_command(" scp %s %s:%s " % (  src , temphost,  dest))
    (output, error, retcode) = run_command( command )
    if retcode != 0:
        return json_response(content=output, status="ERROR", status_code=500, error=error)
    return  self.request.id 
    pass


@login_required
def download_path(request, machine_name, path):
    #return json_response(status="ERROR",
    #                         status_code=500,
    #                         error="This API is forbidden yet. ")
    try:
        taskenv = { "user" : request.user.username , "machine" : machine_name , "host" :  settings.TASKENV_HOST }
        #if not os.path.isfile( path ) :
        #    return json_response(status="ERROR",
        #                     status_code=500,
        #                     error=" no such file ")
        #if not is_readable( path , request.user.username ): 
        #    return json_response(status="ERROR",
        #                     status_code=403,
        #                     error="file not readable ")
        if not os.path.isdir(tempdir):
            os.makedirs( tempdir )
            os.chmod( tempdir , stat.S_IWOTH + stat.S_IXOTH + stat.S_IROTH)
        if os.path.dirname(path) == '/' :
            tmpfile = os.path.join( tempdir , os.path.basename(path))
            logger.error("tempfile %s" % tmpfile )
            #if not is_readable( tmpfile , request.user.username ):
            #    return json_response(status="ERROR",
            #                 status_code=403,
            #                 error="file not readable ")
            # could download tmpfile ^ ^ 
            file_handle = open(tmpfile, 'r')
            content_type = get_mime_type(machine_name, tmpfile, file_handle)
            logger.debug("File download requested: %s" % path)
            if content_type is None:
                content_type = "application/octet-stream"
            return StreamingHttpResponse(file_handle, content_type=content_type)
        #file_handle = open(path, 'r')
        #content_type = get_mime_type(machine_name, path, file_handle)
        #logger.debug("File download requested: %s" % path)
        #if content_type is None:
        #    content_type = "application/octet-stream"
        #return StreamingHttpResponse(file_handle, content_type=content_type)
        rest = download_path_task.delay( taskenv , path   )
        cache.set("async-" + rest.id , "AsyncJob" , 3600 )
        return json_response(status="ACCEPT", status_code=201, error="" , content=rest.id)
    except Exception as e:
        logger.error("Could not get file %s" % str(e))
        return json_response(status="ERROR",
                             status_code=500,
                             error=str(e))


@shared_task(bind=True , track_started=True )
def put_file_task( *args , **kwargs ):
    return safty_task( put_file_task_unsafty )( *args , **kwargs)
#@safty_task


def put_file_task_unsafty(self, task_env, temphost ,  src, dest): 
    #  safy task . cp , ...  , rm tmp file , return 
    cookie_file =  os.path.join( getpwuid(os.getuid()).pw_dir , localcookies)
    command_src = ''' curl -X GET -s -b %s  "%s://%s:%s/api/file/%s/%s?&download=True" -o %s ''' % ( cookie_file  , 'http' , temphost , '8000' , machine_default ,src , dest   )
    #(output, error, retcode) = run_command(" scp %s:%s %s " % ( temphost,  src, dest))
    (output, error, retcode) = run_command( command_src )
    if retcode != 0:
        return json_response(content=output, status="ERROR", status_code=500, error=error)
    #(output, error, retcode) = run_command(" ssh %s rm  %s " % ( temphost,  src))
    #if retcode != 0:
    #    return json_response(content=output, status="ERROR", status_code=500, error=error)
    return {'location': dest}
    pass

@login_required   
def put_file(request, machine, path , local = False):
    data = request.read()
    # Write data to temporary location
    # TODO: Get temporary path from settings.py 
    #tmp_file = tempfile.NamedTemporaryFile(prefix="newt_" ) )
    #print( request.FILES )
    tmp_file = tempfile.NamedTemporaryFile(prefix="newt_" , dir = tempdir, delete = False )
    tmp_file.write(data)
    tmp_file.file.flush()
    tmp_file.close()
    if not local :   
        src = tmp_file.name
        dest = path   # TO-DO need to check path is ok . 
        temphost = socket.gethostname()
        taskenv = { "user" : request.user.username , "machine" : machine }
        # CHOWN 
        #username = taskenv["user"]
        #ngid = getpwnam( username ).pw_gid
        #nuid = getpwnam( username ).pw_uid
        #os.chown( src  , nuid , ngid )
        rest = put_file_task.delay( taskenv , temphost ,  src, dest   )
        cache.set("async-" + rest.id , "AsyncJob" , 3600 )
        return json_response(status="ACCEPT", status_code=201, error="" , content=rest.id)
    else : 
        os.rename( tmp_file.name , os.path.join( tempdir  , path ))
        return {'location' : tmp_file.name }

#@shared_task(bind=True , track_started=True )
@app.task( bind=True , track_started=True ) # @safty_task
def get_dir_task(*args , **kwargs):
    return safty_task( get_dir_task_unsafty)( *args , **kwargs   )

def get_dir_task_unsafty( self , task_env , path ):
    # decorder chown 
    try :
        if os.path.isfile(path) :
            dirlist = [ os.path.basename(path) ]
            path = os.path.dirname(path)
        elif os.path.isdir(path) :
            dirlist = os.listdir(path)
        else :
            return json_response(status="ERROR", status_code=500, error="path is not a directory" )
        output = []
        for filei in dirlist :
            i_stat = os.stat( os.path.join( path , filei ) )
            output.append({
                'name' : filei ,
                'date(m)' : i_stat.st_mtime , # last modify
                'date(a)' : i_stat.st_atime , # last access
                'date(c)' : i_stat.st_ctime , # create 
                'size(B)': i_stat.st_size,
                'perms' : stat.filemode(  i_stat.st_mode ) ,
                'hardlinks' : i_stat.st_nlink ,
                'uid' : i_stat.st_uid ,
                'gid' : i_stat.st_gid ,
            })
        return(output)
    except Exception as e:
        logger.error("Could not get directory %s" % str(e))
        return json_response(status="ERROR", status_code=500, error="Could not get directory: %s" % str(e))
    



@login_required   
def get_dir(request, machine_name, path):
    try:
        pass
        if ( not os.path.isdir( path ) ) and ( not os.path.isfile( path )):
            return json_response(status="ERROR", status_code=500, error="path is not a directory" )
        # need no more check , just test open the celery task to read dir 
        taskenv = { "user" : request.user.username , "machine" : machine_name }
        rest = get_dir_task.delay( taskenv , path   )
        cache.set("async-" + rest.id , "AsyncJob" , 3600 )
        return json_response(status="ACCEPT", status_code=201, error="" , content=rest.id)
    except Exception as e:
        logger.error("Could not get directory %s" % str(e))
        return json_response(status="ERROR", status_code=500, error="Could not get directory: %s" % str(e))
    
      
def get_systems(request):
    return { 'ln3' : ['HOME' , 'WORK' ] , 'ln4' : ['HOME' , 'VIP'] , 'LN6' : ['HOME' , 'NSFCGZ']  }
    # TO-DO should be read from common-config-file 
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
