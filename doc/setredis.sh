#!/bin/sh
echo $1
# $1 REDISMASTER 
# $2 BEHAVIOR : [ ]
cd /HOME/nscc-gz_jiangli/virtualenv/config/redis
REDISDIR=/HOME/nscc-gz_jiangli/virtualenv/3.2.4/bin
testping=`$REDISDIR/redis-cli ping`
if [ s$testping  != sPONG ] ; then
  echo "Try to start redis server master "
  (
  cd /HOME/nscc-gz_jiangli/virtualenv/config/redis
  pwd # cp redis.conf $HOSTNAME.redis.conf
  #  nohup ../../3.2.4/bin/redis-server $HOSTNAME.redis.conf &>../../logs/log.redis.$HOSTNAME &
  )
  pwd
  testping2=`$REDISDIR/redis-cli ping`
  if [ s$testping2  != sPONG ] ; then
    echo "Could not start redis on" $HOSTNAME
    exit 100
  fi
  #if [ s$1 -ne s$HOSTNAME ] ; then
  #  echo "set to slave"
  #fi
else 
  echo "REDIS IS RUNNING ON " $HOSTNAME
  roleinfo=`$REDISDIR/redis-cli info | grep  role | cut -b 6-8 `
  echo $roleinfo
  if [ s$1 != s$HOSTNAME ] ; then
     echo " if it is slave"
     if [ "s$roleinfo" == "ssla" ] ; then
         echo "Slave node OK!"
         #exit 0
     else
         echo "Try to change node to slave!"
         $REDISDIR/redis-cli slaveof cn16356 6379
         roleinfo2=`$REDISDIR/redis-cli info | grep  role | cut -b 6-8 `
         if [ "s$roleinfo" != "ssla" ] ; then
            echo "Can not turn node " $HOSTNAME "to slave"
            exit 400
         fi
     fi
     echo "Try to check sentinel"
     testping_sent=`$REDISDIR/redis-cli -p 26379 ping`
     if [ s$testping_sent  != sPONG ] ; then
        echo "Try to start sentinel"
        (
        cd /HOME/nscc-gz_jiangli/virtualenv/config/redis
        cp sentinel.conf $HOSTNAME.sentinel.conf
        nohup ../../3.2.4/bin/redis-sentinel $HOSTNAME.sentinel.conf &>../../logs/log.$HOSTNAME.sentinel &
        wait 3
        )
     fi
     echo "Try to check sentinel master"
     REDIS_SERVER=`/HOME/nscc-gz_jiangli/virtualenv/3.2.4/bin/redis-cli -p 26379 sentinel get-master-addr-by-name mymaster`
     REDIS_SERVER_IP=`echo $REDIS_SERVER | awk '{print $1}'`
     REDIS_SERVER_NAME=`ssh $REDIS_SERVER_IP hostname `
     if [ s$REDIS_SERVER_NAME == s$1 ] ; then
         echo "REDIS SERVER MASTER OK"
         exit 0
     else
         echo "Error: Not Match master"
         exit 600
     fi
  else
     echo " if it is master" 
     echo "${roleinfo}" "master"
     if [ "s$roleinfo" == "smas" ] ; then
         echo "Master node OK!"
         exit 0
     else
         echo "Error: Master node is error role!"
         exit 200
     fi
  fi
fi




