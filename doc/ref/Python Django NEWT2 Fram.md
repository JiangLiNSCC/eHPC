NEWT2 为了增加模块化，在 Python Django 的基础上做了一些简单的设计 ：

项目文件夹架构示意：

* account/ 
* authnz/
    * \__init__.py
    * models.py
    * tests.py
    * urls.py
    * adapters/
        * \__init__.py
        * dbauth_adapters.py
        * myproxy_adapter.py
        * myproxy_backend.py
        * myproxy_models.py
        * template_adapter.py
* command/
* common/
    * \__init__.py
    * decorators.py
    * gridutil.py
    * response.py
    * shell.py
* file/
* job/
* newt/
    * \__init__.py
    * crossdomain.py
    * models.py
    * sample_local_settings.py
    * settings.py
    * tests.py
    * urls.py
    * views.py
    * wsgi.py
* status/
* store/
* manage.py

这里，项目名为newt ，其中 account,authnz,command,file,job,status,store 分别对应API 设计下面的七大模块，每个文件夹对应一个django app ， 另外一个 common 里面封装了一些工具供各个模块调用以及项目整体的配置。

## URI路由规则

项目各个模块的API 放到 /api/[模块名] 中：

newt/urls.py:
```
urlpatterns = patterns('',
    (r'^api/?$', RootView.as_view()),
    (r'^api/status', include('status.urls')),
    (r'^api/file', include('file.urls')),
    (r'^api/auth', include('authnz.urls')),
    (r'^api/command', include('command.urls')),
    (r'^api/store', include('store.urls')),
    (r'^api/account', include('account.urls')),
    (r'^api/job', include('job.urls')),
)
```

在各个模块里再将下面的URI 路由到对应的Pyhon Class ，通过as_view()方法来处理不同的HTTP VERB。

job/urls.py:
```
urlpatterns = patterns('command.views',
    (r'^/?$', JobRootView.as_view()),
    (r'^/(?P<machine>[^/]+)/$', JobQueueView.as_view()),
    (r'^/(?P<machine>[^/]+)/(?P<job_id>[^/]+)/$', JobDetailView.as_view()),
    (r'^(?P<query>.+)/$', ExtraJobView.as_view()),
)
```

然后在各个模块的views.py 里，对应不同URI的CLASS 来映射各个URI 到各个 函数

```
job_adapter = import_module(settings.NEWT_CONFIG['ADAPTERS']['JOB']['adapter'])
...
# /api/jobs/<machine>/
class JobQueueView(JSONRestView):
    def get(self, request, machine):
        return job_adapter.view_queue(request, machine)
    def post(self, request, machine):
        return job_adapter.submit_job(request, machine)
```

这里可以看出，最终函数的实现是在 job_adapter 的对应的函数里，这样是为了对应不同的系统环境调用不同的实现。
另外，　可以看到，这里的　JobQueueView　并非直接继承　Django 的View 基类，而是进行了一层封装的 JSONRestView 或  AuthJSONRestView 。

## ADAPTERS机制

如上所诉，NEWT 的项目采用了 ADAPTERS 的机制，以实现类似“可插拔”的效果。机制如下：

在app/views.py的各个View 类里，并没有去处理请求，而是通过return  job_adapter.**sub-function**(request,*) 外包出去了。

而在文件头，则如此这般指定了job_adapter为何物：
```
from importlib import import_module
job_adapter = import_module(settings.NEWT_CONFIG['ADAPTERS']['AUTH']['adapter'])
```

在项目的配置文件settings.py里，则设定了NEWT_CONFIG['ADAPTERS']：
```
NEWT_CONFIG = {
    'SYSTEMS': [
        {'NAME': 'localhost', 'HOSTNAME': 'localhost' },
    ],
    'ADAPTERS': {
        'STATUS': {
            'adapter': 'status.adapters.ping_adapter',
            'models': '',
        },
        'FILE': {
            'adapter': 'file.adapters.localfile_adapter',
            'models': "",
        }, 
        'AUTH': {
            'adapter': 'authnz.adapters.dbauth_adapter',
            'models': '',
        },
        ...
```

如此例，可以看出，```settings.NEWT_CONFIG['ADAPTERS']['AUTH']['adapter']``` 此时指的就是'authnz.adapters.dbauth_adapter',在对应的文件authnz/adapters/dbauth_adapter.py 里，就可以找到 view 里的函数的各种具体实现了。

而在*app*/adapters 里，一般不只一个实现，如authnz/adapters 下，有 dbauth_adapters.py ，myproxy_adapter.py 和 template_adapter.py 。

其中， template_adapter.py  只是个空白的模板，类似于API-FUNCTION 的说明了：

authnz/adapters/template_adapter.py
```
...
def login(request):
    """Logs the user in and returns the status

    Keyword arguments:
    request -- Django HttpRequest
    """
    pass

def logout(request):
...
```

而另两个文件则是针对不同情况的具体的代码实现了。

这样，在使用时，针对不同的系统环境，更改settings.py 里面设置，选择具体的实现即可。需要增加新的实现代码，则只需要在 app/adapters/ 里添加新的 *_adapter.py .

## 对View的封装

详细机制需参考 [Djang Doc : class based views](https://docs.djangoproject.com/en/1.9/topics/class-based-views/intro/)

由于在urls.py里面，对URI 的响应设定为 ***XXXView.as_view()*** ， 并在 views.py 里面进行了相关实现***class XXXView(JSONRestView):*** ;而且JSONRestView 在 newts/views.py 里面继承自Djiango 的 View Class , 并对其dispatch 函数进行了重载 : 
```
class JSONRestView(View):
    def dispatch(self, request, *args, **kwargs):
        """
        Override the dispatch method of the class view 
        """
        # Wrap the dispatch method, so that we autoencode JSON
        response = super(JSONRestView, self).dispatch(request, *args, **kwargs)
        # If this is not an HTTPResponseBase object (Base class for responses) 
        if not isinstance(response, HttpResponseBase):
            response = json_response(response)

        return response
    ...
```

根据Django 的机制，每一个 URI request ，因为指定了 由 View.as_view() 来处理， 会调用 dispatch 将其发给 HTTP VERB 对应的 函数如 get(.) 来处理，这里对view 的封装，是为了将结果统一转换为 统一的JSON 的格式 (通过 newt 自定义的 json_response )来完成。

另外，对于需要进行用户验证的URI request , 这里进一步封装了 ```class AuthJSONRestView(JSONRestView):``` ，这里封装了Django auth 装饰器    @login_required,以实现自动的用户验证

## common Tools

### gridutils.py 

NEWT 关于网格计算 Globus 的相关设置和调用的封装。我们目前没有试用Globus ，意义不大。

### decorators.py 
实现装饰器 login_reuired , Django 的auth 是有这个实现了，这里则提供了一个自己的实现(调用自己的  request.user.is_authenticated() )。

这个封装可能是为了更好更一致性的处理错误信息。

### shell.py
主要是为了封装 run_command(command, env=None, timeout=600) 用来方便的运行shell 命令。
首先，通过 shlex 来拆分命令。
然后，通过 Popen 来异步执行 命令，并通过信号量来设置超时时间。
这样保障在执行命令出错或者卡住时能够及时的退出。
