# 1. Run redis server  
redis-server 

You can use the command `/WORK/app/redis/3.2.4/bin/redis-cli ping` to check if the redis-server was running.

# 2. Run celery worker
celery -A newt worker -l info 
# 3. Run django 
