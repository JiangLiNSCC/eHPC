
set -x 
#### test auth
curl -X GET http://localhost:8000 | grep api
 curl -X GET http://localhost:8000/api
 curl -X GET http://localhost:8000/api/auth
 curl -X POST -d "username=test3&password=test3" -D cookie.txt http://localhost:8000/api/auth 
 curl -X GET -b cookie.txt http://localhost:8000/api/auth
 curl -b cookie.txt -X DELETE http://localhost:8000/api/auth
 curl -X GET -b cookie.txt http://localhost:8000/api/auth
 curl -X POST -d "username=test3&password=test3" -D cookie.txt http://localhost:8000/api/auth

