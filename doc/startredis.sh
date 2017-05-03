#!/bin/sh
REDISMASTER=$HOSTNAME
REDISDIR=/HOME/nscc-gz_jiangli/virtualenv/3.2.4/bin
testping=`$REDISDIR/redis-cli ping`
if [ s$testping  != sPONG ] ; then
#   echo "Try to start redis server master "
#   (
#   cd /HOME/nscc-gz_jiangli/virtualenv/config/redis
#  pwd # cp redis.conf $HOSTNAME.redis.conf
#  #  nohup ../../3.2.4/bin/redis-server $HOSTNAME.redis.conf &>../../logs/log.redis.$HOSTNAME &
#   )
#   pwd
#
  echo "Try to start redis on master "
  ./setredis.sh $REDISMASTER
  if [ $? -ne 0 ] ; then
    echo "cloud not start redis master"
    exit 100
  fi
else 
echo "redis MASTER is RUNNING"
fi

for machine in `cat redishosts`
do
   echo $machine
   ssh $machine  ${PWD}/setredis.sh $REDISMASTER
done


