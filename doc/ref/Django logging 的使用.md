
>[官方文档](https://docs.djangoproject.com/en/1.9/topics/logging/)

Django 提供了 logging 模块，来方便运行日志的生成。logging 本身也是 [python 的基本模块](https://docs.python.org/3/library/logging.html#logrecord-attributes)，Django 里有些重载。

# 配置 settings.py
一个来自 NERSC NEWT API 2.0 的范例如下： 
```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'full': {
            'format': '[%(levelname)s] %(asctime)s %(name)s : %(message)s'
        },
        'brief': {
            'format': '[%(levelname)s] %(message)s'
        },
        'message_only': {
            'format': '%(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'full'
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(_LOGDIR, 'django.log'),
            'formatter': 'full',
            'maxBytes': 1000000,
            'backupCount': 3
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'newt': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
```
可以看到，对于logging 来说，除了 version 和 disable_existing_loggers 这两个属性，重要的设置有这几个：
* formatters
* filters
* handlers
* loggers

### formatters 
如此例子，通过python 的格式字符串和 [LogRecord 元素](https://docs.python.org/3/library/logging.html#logrecord-attributes) 来创建不同的 LOG 格式

如此例中的 'full' 格式 ，设定为：
```
            'format': '[%(levelname)s] %(asctime)s %(name)s : %(message)s'
```
某一个结果示例如下：
```
[INFO] 2016-06-23 21:11:43,965 newt.authna.adapters.dbauth_dapter : Successfully logged in user: tonge
```

**可缺省，缺省的LOG 格式就只有 %(message)s**

对于一般的开发调试，范例里的full 格式已经相当好用。在这里可以将模块名设定到levelname ，这样就可以知道具体信息的来源代码了。

### filters

>A filter is used to provide additional control over which log records are passed from logger to handler.

官网上的说明也很少，会用到这里的情况比较少，控制好LOG LEVEL 应该就够了

**可缺省**

### handlers 

LOG 信息的处理核心， 可以设置不同的处理核心。


* LEVEL 设定处理的LOG 信息的等级。这个也可以在 logger 里设定，而且觉得在logger 里设定更合适 。Python 定义的等级从低到高有下面几种：
    * EBUG: Low level system information for debugging purposes
    * INFO: General system information
    * WARNING: Information describing a minor problem that has occurred.
    * ERROR: Information describing a major problem that has occurred.
    * CRITICAL: Information describing a critical problem that has occurred.
* formatter 结合上层的 formatter 设定字符串格式
* filters 设定过滤器，和长层的 filters 配合使用的
* class 具体的消息的处理方式：
    * 'logging.StreamHandler' 这个就是在标准输出里显示了
    *  logging.handlers.RotatingFileHandler', ‘滚动的’文件记录
        * filename , 设定log 文件名
        * maxBytes 和  backupCount 应该是和滚动相关的设定 
    * 'django.utils.log.AdminEmailHandler' 发邮件！ 一般用于严重的问题，有空可以试一下~！  
### loggers

具体的日志记录实体的类型 .
>A logger is the entry point into the logging system. Each logger is a named bucket to which messages can be written for processing.

>A logger is configured to have a log level. This log level describes the severity of the messages that the logger will handle. Python defines the following log levels

在这里大概就是将需要的日志进行下分类，并调用不同的handler 来处理，同时可以控制日志输出级别。

如此例中，设定了一下处理[django-request 的log ](https://docs.djangoproject.com/en/1.9/topics/logging/#django-request) 和项目自己生产的log : newt.xxx 

# 使用

知道了配置的这这那那，使用直接看看示例就很明白了
```
import logging
logger = logging.getLogger("newt." + __name__)
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)

    logger.debug("Attemping to log in user: %s" % username)

    if user is not None:
        auth.login(request, user)
        logger.info("Successfully logged in user: %s" % username)

    return is_logged_in(request)
```

通过 getLogger ，设定了具体的logger 并通过 __name__ 在levelname 里留在了模块路径的痕迹。

logger.debug() 和 logger.info() 则用以生成对应级别的 log message , 同理还会有 logger.warning() , logger.error() , logger.critical()

另外，还有两个特殊的调用：
>* logger.log(): Manually emits a logging message with a specific log level.
>* logger.exception(): Creates an ERROR level logging message wrapping the current exception stack frame.

