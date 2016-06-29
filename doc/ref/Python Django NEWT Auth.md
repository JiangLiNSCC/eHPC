# Python Django Auth 

NERSC 的认证需要实现这三个功能 ： 

* GET /api/auth
    * get_status(request)
    * 查询账户认证状态
* POST /api/auth 
    * login(request) 
    * 登陆账户
* DELET /api/auth 
    * logout(request)
    * 登出账户

Adapter 提供了两种实现：
* dbauth 基于 django 数据库的认证 
* myproxy 通过 SSL proxy 来进行认证 

这里大量使用了Django 关于认证的基本框架 ，有很多东西可参考：


## dbauth adapter
本地实现，基本都是调用Djanog 已有的东西，中间加上通过 logger 来进行日志记录:
* get_status(request)
    *  调用 request.user.is_authenticated() 进行认证
    *  状态信息在 request 里面基本都有了 
*  login()
    * 调用     user = auth.authenticate(username=username, password=password)
进行登录
* logout()
    * 调用 auth.logout(request) 来进行登出  

## myproxy adapter
get_status 和 logout 的实现和 dbauth 一致 ，login 将 直接调用 auth 改成了 mpb.authenticate(username=username, password=password) ， mpb 为按照 django 的规范，重载的认证后端。
认证流程：
1. 尝试 通过  username 和 password 创建 SSL.connection，并获取认证数据  ， 出错则抛出异常退出
2. 生成认证请求，和privatekey 
3. 通过conn 获取认证码 
4. 检查 User 是否存在 
5. 根据 认证信息创建 Cred 对象 并存到数据库 
6. 将Cred 对象放到 Session 中
7. myuser.backend = 'django.contrib.auth.backends.ModelBackend' 

这里大量调用了 ```from OpenSSL import crypto, SSL```里面的东西和也调用了django 自己的认证系统，对这个过程并不是太理解，但应该是自己建立了公钥、秘钥，用以认证的过程。 

## 天河实现版本 ？

* 如何封装 LDAP ?

* 如何结合public key 来进行认证 ？


## Playground 

- [x] test django auth 
- [ ] test use ldap
- [ ] test sign up use public key 

>- [ ] x