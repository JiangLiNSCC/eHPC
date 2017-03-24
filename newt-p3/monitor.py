#!/usr/bin/env python
import unittest
import os
import smtplib
from email.mime.text import MIMEText
import time
from six.moves import configparser 
import argparse
from newt.settings import NEWT_CONFIG

cf = configparser.ConfigParser() 
cf.read("../../config/test.conf")


def str2bool(bools):
    if bools.lower()  in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']:
        return True
    elif  bools.lower()  in ['false', '0', 'f', 'n', 'no', 'noop', 'not', 'fou', 'bu']:
        return False
    else :
        return None 

class NodeStatus(object):
    def cpu(self):
        cpuinfo = {}
        procinfo ={}
        nprocs = 0 
        with open('/proc/cpuinfo') as f:
            for line in f:
                if not line.strip():
                    # end of one processor
                    cpuinfo['proc%s' % nprocs] = procinfo
                    nprocs=nprocs+1
                    # Reset
                    procinfo={}
                else:
                    if len(line.split(':')) == 2:
                        procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                    else:
                        procinfo[line.split(':')[0].strip()] = ''
        return cpuinfo
    def loadavg(self):
        loadavg = {} 
        f = open("/proc/loadavg") 
        con = f.read().split() 
        f.close() 
        loadavg['lavg_1']=con[0] 
        loadavg['lavg_5']=con[1] 
        loadavg['lavg_15']=con[2] 
        loadavg['nr']=con[3] 
        loadavg['last_pid']=con[4] 
        return loadavg 
    def memory(self):
        meminfo={}
        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()
        return meminfo

    def net(self):
        ifstat = open('/proc/net/dev').readlines()
        ifstat = ifstat[2:]
        output = {}
        for interface in ifstat :
            infos = interface.split()
            name = infos[0].split(':')[0]
            receive = int( infos[1] )
            transmit = int( infos[9] )
            output[ name ] = { 'receive' : receive , 'transmit' : transmit }
        return output

    def netspeed(self , sleep =3 ):
        time1 = time.time()
        net1 = self.net()
        time.sleep(sleep)
        time2 = time.time()
        net2 = self.net()
        speed = {}
        for interface in net1 :
            speed[interface]={}
            for itemi in net1[ interface ]:
                speed[interface][itemi] = ( net2[interface][itemi] - net1[interface][itemi] ) / ( time2 -time1 )
        return speed

def cleanTmp( dirname  , timedeta = None , numlimit = None ):
    timenow = time.time()
    timelist = []
    count = 0 
    for parent, dirnames, filenames in os.walk(dirname):
        for filename in filenames :
            sfilename = os.path.join( parent , filename )
            fstat = os.stat(sfilename)
            deta = timenow - fstat.st_atime
            if timedeta and timedeta < deta :
                #print('try to remove file : %s' % filename )
                os.remove( sfilename  )
                count +=1
            else :
                timelist.append( deta)
    if numlimit and len(timelist) > numlimit :
        timelist.sort()
        setdeta = timelist[ numlimit ]
        return count + cleanTmp( dirname  , timedeta = setdeta )
    return count

def cleanSession( ):
    os.system('python manage.py clearsessions'  )
    pass


if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument('-s' ,'--session' , default = False , action='store_true' , dest = 'session' , help = 'clear session .'  )
    parser.add_argument('-t' ,'--tmp' ,'--temp', default = False , action='store_true' , dest = 'tmp' , help = 'clear tmpfile.' )
    parser.add_argument('-m','--monitor' , default= None ,dest='monitor' ,choices=('cpu','mem','net' , 'all'), help = 'monitor webserver status ' )
    args = parser.parse_args()
    if args.session:
        cleanSession()
    if args.tmp:
        #print( NEWT_CONFIG["TEMPDIR"] )
        count = cleanTmp( NEWT_CONFIG["TEMPDIR"] , 3600 , numlimit = 10000 )
        print('cleaned tmpfile : %s' % count)
    if args.monitor:
        ns=NodeStatus()
        if args.monitor == 'all' or args.monitor == 'cpu' :
            print( ns.loadavg() )
        if args.monitor == 'all' or args.monitor == 'mem' :
            print( ns.memory() )
        if args.monitor == 'all' or args.monitor == 'net' :
            print( ns.net() )
            print( ns.netspeed())

