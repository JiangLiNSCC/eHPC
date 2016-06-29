# Python Django File

Nersc 的 File 模块里主要要实现这四个功能：

* GET /api/file  
    *  **get_systems()**
    *  查看状态
* GET /api/file/<machine_name>/<path> 
    * **get_dir(request, machine_name, path)**
    * 列出信息（ls）
* GET /api/file/<machine_name>/<path>?view=False
    * **download_path(request, machine_name, path)**
    * 下载
* PUT /api/file/<machine_name>/<path> 
    * **put_file(request, machine_name, path)**
    * 上传

Adapter 提供了两种实现：
* localfile 本地的文件系统 
* globus 通过Gird FTP 访问的文件系统 

## localfile adapter
本地实现，很简单:
* get_systems(request) 直接     return ['localhost']
* get_dir() 直接调用 ls -al 命令，然后通过对结果进行正则字符串的匹配来形成结果返回。
* put_file ， 分了两部分进行，创建临时文件，将request 里的data 写到 临时文件，然后将临时文件复制到指定的path .
    * 这个实现没有清除临时文件的操作，可能会导致内存被大量占用，只是一个最简单的实现。
    * 这里也没有任何的权限控制之类的东西
*  download_path() ， 直接用 open 打开文件， 然后将句柄传给  StreamingHttpResponse 。另外，通过magic （类linux 的file 命令）来判断文件的类型
    * 不知道对服务器资源的占用，以及断点续传等等怎么样。
    * 只是一个很简单的处理 

## GLOBUS adapter
调用GLOBUS GridFTP 的存储，而非本地的存储。
* get_systems(request) 直接    return gridutil.GRID_RESOURCE_TABLE.keys() ； 
    * 在 gridutil 的 GRID_RESOURCE_TABLE 里面配置了 GLOBUS 的网格计算资源，如：
```
 dict(
    edison=dict(
        hostname='edisongrid.nersc.gov', 
        jobmanagers=dict(fork=dict(url="edisongrid.nersc.gov/jobmanager"), 
                         batch=dict()),
        gridftp_servers=['edisongrid.nersc.gov'],
        qstat=dict(bin='/project/projectdirs/osp/newt_tools/qs_moab.sh',scheduler='qs'),
        qsub=dict(bin='/opt/torque/4.1.4/bin/qsub',scheduler='pbs'),
        qdel=dict(bin='/opt/torque/4.1.4/bin/qdel',scheduler='pbs'),
    ),
    ... 
```
* get_dir() 与 直接ls 不同的是使用 GridFTP 的命令 来获取目录信息：
    * 核心是 ：  ```run_command(gridutil.GLOBUS_CONF['LOCATION'] + "bin/uberftp -ls %s" % path,  env=env) ``` 后续的字符串处理类似。
    * 在调用 run_command 前 ， 是通过相关的 Grid 工具生成 env 和在 GridFTP 上的文件 PATH 
* put_file ，与localfile 不同的是，在创建 tempfile 后， 创建 GridFTP 需要的 env 和 dest , 通过 GridFTP 的 copy 命令
    * run_command(gridutil.GLOBUS_CONF['LOCATION'] + "bin/globus-url-copy %s %s" % (src, dest), env=env)
*  download_path() ， 先用GridFTP 工具将 文件复制到临时文件，然后将tempfile提交给 StreamingHttpResponse

## 天河实现版本 ？

* 本地使用的话？
    * 需要考虑 用户权限的验证？

* 异地使用的话？（在可以访问TH2 的云环境上使用）
    * 通过SSL FTP 来实现？ 

## Playground 

- [ ] test use sftp to move  file 