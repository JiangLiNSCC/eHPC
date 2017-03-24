#!/usr/bin/env python
import unittest
import os
import smtplib
from email.mime.text import MIMEText
import time
from six.moves import configparser 
import argparse

cf = configparser.ConfigParser() 
cf.read("../../config/test.conf")

worker_list = cf.get('manager' ,'workers' ).split()  #[ 'ln2' ]
server_list = cf.get('manager' ,'servers' ).split()  #[ 'cn16356' ]

conf = {
  'email' : True ,  # -e --email
  'email_level' : cf.get('manager' ,'conf_email_level' ) , # -l --level  info 1 , warnning  2, error 3  ; if 3 > email_level , sent email_error  
  'restart' : False , # -r -- restart
  'test'  : cf.get('manager' ,'conf_test' ) , # -t --test
}

LEVEL_SET = {
'INFO' : 1 ,
'WARNNING' : 2 ,
'ERROR' : 3 ,
'info' : 1 ,
'warnning' : 2 ,
'info' : 3 ,
}

def str2bool(bools):
    if bools.lower()  in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']:
        return True
    elif  bools.lower()  in ['false', '0', 'f', 'n', 'no', 'noop', 'not', 'fou', 'bu']:
        return False
    else :
        return None 


conf['email'] = str2bool( cf.get('manager' ,'conf_email' ) )
conf['restart'] = str2bool( cf.get('manager' ,'conf_restart' ) )

def run_discover():
    if conf['test'] == 'discover' :
        uts = unittest.TestLoader().discover('.')
    else :
        utl = unittest.TestLoader()
        uts = utl.loadTestsFromName(conf['test'] )
    return unittest.TextTestRunner().run(uts)
   


def email(title , content , level = 'INFO' ):
    conf_level = LEVEL_SET.get( conf['email_level']  )
    self_level = LEVEL_SET.get( level )
    title += ' at ' + time.asctime( time.localtime( time.time() ))
    if not conf['email'] or self_level < conf_level :
        print("self level : %s ; conf level : %s  ; %s %s" % (level , conf['email_level'] ,  self_level , conf_level))
        print("mail to admin %s (NOT SEND):\n %s" %(title , content))
        exit(0)
        return 0
    mail_host = cf.get('manager' ,'mail_host' )
    mail_user = cf.get('manager' ,'mail_user' )
    mail_pass = cf.get('manager' ,'mail_pass' )
    receivers = cf.get('manager' ,'mail_recivers' ).split()
    msg = MIMEText(content)
    msg['Subject'] = title
    msg['From'] = mail_user
    msg['To'] = ','.join(receivers)
    smtp = smtplib.SMTP( mail_host )
    smtp.login( mail_user , mail_pass )
    smtp.sendmail( mail_user , receivers , msg.as_string())
    smtp.close()
    print("mail to admin %s :\n %s" %(title , content))
    exit(0)

def test_node_status( node   ):
    ret = os.system('timeout 5s ssh %s hostname ' % node)
    return ret == 0 

def msg_result( msg , result ):
    for erri in result.errors :
        msg.append( str(erri[0]) )    
        msg.append( str(erri[1]) )
    for erri in result.failures :
        msg.append( str(erri[0]) )
        msg.append( str(erri[1]) )
    
def restart( node , ctype = 'worker'):
    if ctype == 'worker' :
        command = 'timeout 300s ssh %s restart_worker.sh' % node
    elif ctype == 'server' :
        command = 'timeout 300s ssh %s restart_server.sh' % node
    print('run command : %s' % command )
    ret = os.system( command )
    return ret 



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e' ,'--email' , default = conf['email'] , action='store_true' , dest = 'email' , help = 'Send email , default is [ %s ] .' %  conf['email'] )
    parser.add_argument('-ne' ,'--noemail' , default = conf['email'] , action='store_false' , dest = 'email' , help = 'not Send email but just print logs .' )
    parser.add_argument('-l','--level' , default= conf['email_level'] ,dest='level' ,choices=('INFO','ERROR','WARNNING'), help = 'which level will send email [%s] ' % conf['email_level'] )
    parser.add_argument('-r' ,'--restart' , default = conf['restart'] , action='store_true' , dest = 'restart' , help = 'Try restart if test fail, default is [ %s] .' %  conf['restart'] )
    parser.add_argument('-nr' ,'--norestart' , default = conf['restart'] , action='store_false' , dest = 'restart' , help = 'Not Try restart if test fail' )
    parser.add_argument('-t','--test' , default= conf['test'] ,dest='test' , help = 'which test will be used.  [%s] ' % conf['test'] )
    args = parser.parse_args()
    conf['email'] = args.email
    conf['restart']= args.restart
    conf['email_level'] = args.level
    conf['test'] = args.test
    result = run_discover() 
    msg = []
    if result.wasSuccessful()  :
        print("PASSED THE TEST!")
        pass # email ok
        email("newt ok" , "passed all!" , level = 'INFO');
    else :
        msg_result( msg , result)
        avail_workers = []
        avail_servers = []
        for nodei in worker_list :
            print('test worker : %s' % nodei )
            if test_node_status( nodei   )  :
                print("worker " , nodei , ' available.')
                avail_workers.append( nodei )
        pass
        for nodei in server_list :
            print('test server : %s' % nodei )
            if test_node_status( nodei   ) :
                print( "server " ,nodei , ' available.')
                avail_servers.append( nodei )
        #avail_workers , avail_servers = [] ,[]
        msg.append( "avail_servers : " + str( avail_servers )  )
        msg.append( "avail workers : " + str( avail_workers))
        if not  conf['restart'] :
            msg.append('No restart tried by conf restart = %s ' % conf['restart'])
            email( 'newt Error!','\n'.join(msg ) , level = 'ERROR')
        if avail_workers == [] and avail_servers == [] :
            msg.append('No available nodes for workers and nodes ')
            email( 'newt Error!','\n'.join(msg ) , level = 'ERROR')
        else :
            print('Test to restart the node')
            restart_status = False
            if avail_workers :
                pass
                print('try to restart workers on %s' % avail_workers[0])
                if restart( avail_workers[0] , ctype = 'worker' ) == 0 :
                    restart_status = True
                    msg.append( "restart worker on %s success." % avail_workers[0] )
                else :
                    msg.append( "restart worker on %s failed." % avail_workers[0] )
            if avail_servers :
                pass
                #print('try to restart workers on %s' % avail_servers[0])
                if restart( avail_servers[0] , ctype = 'server' ) == 0  :
                    restart_status = True
                    msg.append( "restart server on %s success." % avail_servers[0] )
                else :
                    msg.append( "restart server on %s Failed." % avail_servers[0] )
            #print('restart OK OR NOT!' , restart_status )
            if restart_status :
                pass
                msg.append('restart OK, RETRY the API now')
                result2 = run_discover()
                msg_result(msg , result2)
                if result2.wasSuccessful()  :
                    pass
                    msg.append("test after restart passed!")
                    email( 'newt Warnning!','\n'.join(msg ) , level = 'WARNNING')
                else:
                    pass
                    msg.append("test after restart NOT passed!")
                    email( 'newt Error!','\n'.join(msg ) , level = 'ERROR')
            else :
                pass
                msg.append('All restart failed' )
                email( 'newt Error!','\n'.join(msg ) , level ='ERROR')
 
            
                

