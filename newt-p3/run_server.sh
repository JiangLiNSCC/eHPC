#!/bin/sh
source /HOME/nscc-gz_jiangli/virtualenv/py34env/bin/activate
REDIS_SERVER=`/HOME/nscc-gz_jiangli/virtualenv/3.2.4/bin/redis-cli -p 26379 sentinel get-master-addr-by-name mymaster`
export REDIS_SERVER
cd /HOME/nscc-gz_jiangli/virtualenv/eHPC_ln9_dev/newt-p3
gunicorn --worker-class=gevent -w 24   newt.wsgi -b 0.0.0.0:8000  &> ../../logs/log.$HOSTNAME.gunicorn


