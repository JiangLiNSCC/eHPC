#!/bin/sh

REDIS_SERVER=`/HOME/nscc-gz_jiangli/virtualenv/3.2.4/bin/redis-cli -p 26379 sentinel get-master-addr-by-name mymaster`
echo 'REDIS SERVER (MASTER ) ON  :' $REDIS_SERVER
while [ 's' == 's'  ] ; do
 REDIS_SERVER_NEW=`/HOME/nscc-gz_jiangli/virtualenv/3.2.4/bin/redis-cli -p 26379 sentinel get-master-addr-by-name mymaster`
 if [ "s$REDIS_SERVER" == "s$REDIS_SERVER_NEW" ] ; then
    a=a
 else
    echo [ "s$REDIS_SERVER" == "s$REDIS_SERVER_NEW" ] 
    REDIS_SERVER=$REDIS_SERVER_NEW
    echo 'change to :' $REDIS_SERVER  
    supervisorctl restart run_server
 fi
 sleep 3
done


