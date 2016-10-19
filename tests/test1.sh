set -x 
curl -X GET http://localhost:8000 | grep api
 curl -X GET http://localhost:8000/api
 curl -X GET http://localhost:8000/api/auth
 curl -X POST -d "username=test3&password=test3" -D cookie.txt http://localhost:8000/api/auth 
 curl -X GET -b cookie.txt http://localhost:8000/api/auth
 curl -b cookie.txt -X DELETE http://localhost:8000/api/auth
 curl -X GET -b cookie.txt http://localhost:8000/api/auth
 curl -X POST -d "username=test3&password=test3" -D cookie.txt http://localhost:8000/api/auth
 curl -X GET -b cookie.txt http://localhost:8000/api/job/
 curl -X GET -b cookie.txt http://localhost:8000/api/job/localhost/

 curl -X POST -d "command=ls /" -b cookie.txt http://localhost:8000/api/command/local

 # need to chmod the *.sh file in job dir
 curl -X POST -d "jobscript=sleep 10;date;sleep 100;date" -b cookie.txt http://localhost:8000/api/job/localhost/ 
 newjob=`curl -X POST -d "jobscript=date" -b cookie.txt http://localhost:8000/api/job/localhost/ `
 jobid=`echo $newjob | awk -F\" '{print $12 }'`
 sleep 5
 curl -X GET -b cookie.txt http://localhost:8000/api/job/localhost/$jobid/

  newjob=`curl -X POST -d "jobscript=sleep 100 ; date " -b cookie.txt http://localhost:8000/api/job/localhost/ `
 jobid=`echo $newjob | awk -F\" '{print $12 }'`
 # sleep 5
 curl -X GET -b cookie.txt http://localhost:8000/api/job/localhost/$jobid/
 curl -X DELETE -b cookie.txt http://localhost:8000/api/job/localhost/$jobid/
 curl -X GET -b cookie.txt http://localhost:8000/api/job/localhost/$jobid/
 
