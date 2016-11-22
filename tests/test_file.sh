#/bin/sh
curl -X GET -b cookie.txt http://cn16356:8000/api/file/ln3/WORK/nscc-gz_jiangli/
curl -X GET -b cookie.txt http://cn16356:8000/api/file/ln3/WORK/nscc-gz_jiangli/modules.dep
#curl -X GET -b cookie.txt http://cn16356:8000/api/sync/5d9a156d-6bdd-40f4-a74b-9c3b0aa39988
curl -X GET -b cookie.txt http://cn16356:8000/api/file/ln3/WORK/nscc-gz_jiangli/modules.dep?download=True
curl -X PUT -b cookie.txt -T abcd  http://cn16356:8000/api/file/ln3/tmp/abcd

