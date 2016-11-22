curl -X GET -b cookie.txt http://cn16356:8000/api/job/ln3/


curl -X POST -b cookie.txt -d "jobfile=/HOME/nscc-gz_jiangli/tests/testhost.sh" http://localhost:8000/api/job/ln3/

curl -X POST -b cookie.txt -d 'jobscript=#!/bin/shhostname
pwd' http://localhost:8000/api/job/ln3/


