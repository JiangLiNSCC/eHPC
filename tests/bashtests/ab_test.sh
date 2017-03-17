# test POST /api/auth

ab -c 100 -n 100 -p ./ab.1.post  -T 'application/x-www-form-urlencoded'  http://cn16356:8000/api/auth

# test GET /api/auth
ab -c 20 -n 1000 -C "newt_sessionid=n3zi83tonups8xfziohkxvo8yd56v5wh;csrftoken=oHDjI3aNkHy1lLwD7qe56XT58noXahsQU6C0nO3Y2l3NFXhBQEowpkQSA3JSYvRp;"  http://cn16356:8000/api/auth

# test GET /api/file/<path>

ab -c 20 -n 10000 -C "newt_sessionid=n3zi83tonups8xfziohkxvo8yd56v5wh;csrftoken=oHDjI3aNkHy1lLwD7qe56XT58noXahsQU6C0nO3Y2l3NFXhBQEowpkQSA3JSYvRp;"  http://cn16356:8000/api/file/ln3/WORK/nscc-gz_jiangli/

# * test GET /api/file/<path-FILE> just the same as the above one 

ab -c 20 -n 10000 -C "newt_sessionid=n3zi83tonups8xfziohkxvo8yd56v5wh;csrftoken=oHDjI3aNkHy1lLwD7qe56XT58noXahsQU6C0nO3Y2l3NFXhBQEowpkQSA3JSYvRp;"  http://cn16356:8000/api/file/ln3/WORK/nscc-gz_jiangli/modules.dep

# test GET /api/file/<path-FILE>?download=True . test download
ab -c 20 -n 100 -C "newt_sessionid=n3zi83tonups8xfziohkxvo8yd56v5wh;"  http://cn16356:8000/api/file/ln3/WORK/nscc-gz_jiangli/modules.dep?download=True
