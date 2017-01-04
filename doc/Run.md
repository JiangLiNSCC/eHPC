# 1. Run redis server  
redis-server 

You can use the command `/WORK/app/redis/3.2.4/bin/redis-cli ping` to check if the redis-server was running.

# 2. Run celery worker
#celery -A newt worker -l info 

#C_FORCE_ROOT=1 celery -A newt worker -Q ln3 -l info 

C_FORCE_ROOT=1   celery -A newt worker -Q ln3 -l info --maxtasksperchild=1    &> ../../logs/ln2.worker  &

--maxtasksperchild=1   should be set , as the chroot can out recover !


# 3. Run django 

(py34env) [root@cn16356 newt-p3]# gunicorn --worker-class=gevent -w 24   newt.wsgi -b 0.0.0.0:8000  &> ../../logs/log.cn16356.gunicorn
