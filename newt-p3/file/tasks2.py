from __future__ import absolute_import
from celery import shared_task
import time
@shared_task()
def add2(x,y):
    return x+ y 

@shared_task()
def sendmail2(mail):
    print("+++++++++++++++++++++++++++")
    print('sending mail to %s...' % mail['to'] )
    time.sleep(2.0)
    print('mail sent.')
    print("---------------------------")
    return mail['to']
