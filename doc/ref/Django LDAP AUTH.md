## 通过SHELL使用LDAP CLIENT 
检查 /etc/openldap/ldap.conf
```
TLS_CACERTDIR /etc/openldap/cacerts
URI ldap://lam-yhpc-server/
BASE dc=yhpc
```
检查 /etc/hosts
```
# Management Nodes
12.11.70.128 mn5-gn0 mn5 lam-yhpc-server
12.11.71.129 mn7-gn0 mn7 
12.11.70.136 mn14-gn0 mn14 lam-yhpc-backup
```
可以看到 ldap 认证是在内网管理服务器上的 mn5 。

ldap 本质是一个访问速度很快的数据库，关于其配置可以参考[此链接](http://blog.csdn.net/hitabc141592/article/details/22931179)。

在天河上，可以通过 ldap 的命令来测试。

```ldapsearch -x -b 'dc=yhpc' ```

通过此命令，可以看到天河上的LDAP 数据库里的很多信息。

要留意的是，ldapsearch 不需要提供验证信息。LDAP 默认供任何人可读。


```ldapsearch -x -b 'dc=yhpc'| grep nscc-gz_jiangli``` 

这里可以看到 我的账号相关的一些信息，其中最重要的是这一行：

```
dn: uid=nscc-gz_jiangli,ou=people,dc=yhpc
```
我可以用这个dn 信息来进行验证：
```
ldapwhoami -x -D 'uid=nscc-gz_jiangli,ou=people,dc=yhpc' -w '******'
```
成功后会返回
```
dn: uid=nscc-gz_jiangli,ou=people,dc=yhpc
```
不成功则返回
```
ldap_bind:Invalid credentials
```

## 在Python 中调用 LDAP
找来找去，还是[官方文档](https://www.python-ldap.org/doc/html/ldap.html#)有些用:

* 基本环境设定

```
import ldap
ldappath="ldap://lam-yhpc-server/"
l = ldap.initialize(ldappath)
```

* 查询

```
l.search_st('dc=yhpc',ldap.SCOPE_SUBTREE,'cn=nscc-gz_jiangli')
```
这里返回了很多有用信息，如 uid ,uidNumber , gidNumber , sn , homeDirectory , 等等 …… 


* 认证
这里演示一种简单的认证方式：
```
l.simple_bind_s('uid=nscc-gz_jiangli,ou=people,dc=yhpc', 'password***')
```
正确返回的结果是这个样子： ```(91,[])``` ，不明白是什么意思。
错误的话，则会抛出异常。 并返回 : ldap.INVALID_CREDENTIALS:{'desc':'Invalid credentials'}

然后，这时候，使用

``` l.whoami_s() ```

会返回 ： 
```
dn: uid=nscc-gz_jiangli,ou=people,dc=yhpc
```
而如果没有正确的登陆，则是返回''

利用 LDAP 应该还可以进行改密码，添加账户等等等等操作~ 

但目前这些操作应该已经足够完成 “登陆” ，这个基本操作了 ~！

## 在Django 中测试 LDAP .
- [ ] TODO 
这个需要在TH2 上进行测试
[可参考]( http://www.blogjava.net/Man/archive/2013/06/27/401013.html )
- [x] 需要 安装 python ldap ,  
- [ ] 需要 安装 django-auth-ldap 
- [ ] 按照天河的设置进行配置 。 

Python 3.5.1 

python ldap  竟然只有 python2 版本的， 不过GITHUB 里面有一个 LDAP3 来支持

依赖了 pyasn1
