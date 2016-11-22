 curl -X GET -b cookie.txt http://localhost:8000/api/command


 curl -X POST --data-urlencode 'command=bash -i -c "export PWD=/HOME/nscc-gz_jiangli;pwd"' -b cookie.txt http://localhost:8000/api/command/ln3
#{"error": "", "output": "39884b96-27b4-45c7-8457-f7742dcafb8d", "status": "ACCEPT", "status_code": 201}[nscc-gz_jiangli@cn16356 tests]$ 
#nscc-gz_jiangli@cn16356 tests]$ curl -X GET -b cookie.txt http://localhost:8000/api/async/39884b96-27b4-45c7-8457-f7742dcafb8d
#{"error": "", "output": {"retcode": 0, "error": "", "output": "/HOME/nscc-gz_jiangli/virtualenv/eHPC/newt-p3\n"}, "status": "OK", "status_code": 200}[nscc-gz_jiangli@cn16356 tests]$ 
