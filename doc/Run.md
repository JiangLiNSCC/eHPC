# 1. Run redis server  
redis-server 
# 2. Run celery worker
celery -A newt worker -l info 
# 3. Run django 

