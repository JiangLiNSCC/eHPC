#!/bin/sh
source /HOME/nscc-gz_jiangli/virtualenv/workonln2.sh 
#ps aux | grep celery | grep worker | awk '{print $2}' | xargs -i kill -9 {}
REDIS_SERVER=`/HOME/nscc-gz_jiangli/virtualenv/3.2.4/bin/redis-cli -p 26379 sentinel get-master-addr-by-name mymaster`
export REDIS_SERVER
cd /HOME/nscc-gz_jiangli/virtualenv/eHPC_ln9_dev/newt-p3
C_FORCE_ROOT=1   celery -A newt worker -Q ln3 -l info --maxtasksperchild=1    &> ../../logs/$HOSTNAME.worker



