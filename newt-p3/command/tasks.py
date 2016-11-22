from __future__ import absolute_import
from celery import shared_task
from pwd import getpwnam
import time
import os
import encodings.idna 


@shared_task()
def add(x,y):
    return x+ y 

'''
@shared_task()
def sendmail(mail):
    print("+++++++++++++++++++++++++++")
    print('sending mail to %s...' % mail['to'] )
    time.sleep(2.0)
    print('mail sent.')
    print("---------------------------")
    return mail['to']
'''


'''
@shared_task()
def test_safty( username , cmd ) :
    ngid = getpwnam( username ).pw_gid
    nuid = getpwnam( username ).pw_uid
    #newpid = os.fork()
    print( ngid , nuid)
    newpid = 0 
    if newpid == 0 :
        #os.setegid( ngid) 
        #os.seteuid( nuid)
        os.setgid(ngid)
        os.setuid(nuid)
        output = os.popen( cmd )
        ret = output.read()
        return ret.encode('utf-8')
    return 'error'
'''
