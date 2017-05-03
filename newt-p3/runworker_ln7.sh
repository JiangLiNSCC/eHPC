#!/bin/sh
echo $HOSTNAME
if [ ${HOSTNAME:0:2} == 'cn' ]; then
    echo "cn"
    source /HOME/nscc-gz_jiangli/virtualenv/py34env/bin/activate
elif [ ${HOSTNAME:0:2} == 'ln' ]; then
    echo "ln"
    source /HOME/nscc-gz_jiangli/virtualenv/workonln2.sh
else
    echo "unknown"
fi
export LD_LIBRARY_PATH=/NSFCGZ/app/mysql/5.5.28/lib:$LD_LIBRARY_PATH
#source /HOME/nscc-gz_jiangli/virtualenv/workonln2.sh 
#ps aux | grep celery | grep worker | awk '{print $2}' | xargs -i kill -9 {}
REDIS_SERVER=`/HOME/nscc-gz_jiangli/virtualenv/3.2.4/bin/redis-cli -h cn16356 -p 26379 sentinel get-master-addr-by-name mymaster`
export REDIS_SERVER
cd /HOME/nscc-gz_jiangli/virtualenv/eHPC_ln9_dev/newt-p3
C_FORCE_ROOT=1   celery -A newt worker -Q ln7 -l info --maxtasksperchild=1    &> ../../logs/$HOSTNAME.worker



