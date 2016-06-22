> https://github.com/JiangLiNSCC/eHPC/blob/master/doc/ref/README.md

这里用来整理前期的调研参考资料 调研的内容：已有的规范，可参考的软件架构、模式等 负责人： 李江
预期：3周（截止7月1日，推荐6月26日前完成） 调研可参考的已有平台/资料 。后续可继续完善。调研的结果整理成文档总结到此文件夹中，如 doc/ref/NERSC.md 前期预计重点参考：
(过程中可能会发现更好的调研对象。)


- [x] [HPC Web Service API Reference ](
https://msdn.microsoft.com/en-us/library/windows/desktop/hh560258(v=vs.85).aspx)
    * Microsoft HPC Pack provides access to the HPC Job Scheduler Service by using an HTTP web service that is based on **the representational state transfer (REST) model.**
    * 应该有很多值得参考的 ！ 重点调研对象 ， 推荐由 **康游** 进行 

- [x] [codecademy](https://www.codecademy.com/)
    * 在线学习编程的网站，需熟悉了解其业务逻辑，如果能更一步了解其背后的架构设计最好。这部分资料比较分散，推荐由 **陈品** 进行
    * ref 1: [React.js在Codecademy中的实际应用]( http://www.infoq.com/cn/articles/reactjs-codecademy?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global)
    * ref 2:[前端设计笔记](http://www.ui.cn/detail/17817.html)
    * ref 3: [how-codecombat-was-built](http://stackshare.io/posts/how-codecombat-was-built)
    
- [x] [NERSC 的 API ](https://newt.nersc.gov/)   
    * 另一个重点调研对象，推荐由 **李江** 进行 



- [ ] 陈  [AGAVE-PLATFORM](http://agaveapi.co/slides/agave-platform) tacc

- [ ] 李 [GALAXY](...) 

- [ ] 钟 [EXTREME FACTORY COMPUTING STUDIO ](http://www.bull.com/print/node/144) 

NERSC 模块代码细读

- [ ] 李 authnz	Move auth -> authnz to avoid naming conflicts	a year ago

- [ ] 钟 command	Add login_required to various API calls	2 years ago

- [ ] 李 file	Add login_required to various API calls	2 years ago

- [ ] 陈 job	Add login_required to various API calls	2 years ago



NERSC 其他模块

* account	Add login_required to various API calls	2 years ago
* newt	Move auth -> authnz to avoid naming conflicts	a year ago
* status	Added newt logger to all adapters and views	2 years ago
* store	Add login_required to various API calls	2 years ago
* common	Move auth -> authnz to avoid naming conflicts	a year ago


## 其他参考资料 

* **the representational state transfer (REST) model.**
     * ref 0. [RESTful API WIKI](http://en.wikipedia.org/wiki/Representational_state_transfer)
     * ref 1. [RESTful API 设计指南](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)
     * 这部分还需要补充其他的资料，大家在自己调研的过程中发现好的材料请发给我看看。如有需要，我会在下次讨论后针对此项目写一个关于 RESTful API 的 文档。
* 类似网站
    *  [知乎： 有类似Codecademy的中文在线编程学习网站吗？](http://www.zhihu.com/question/22425402) 可以看看能不能找到同类产品的架构
    * [Fenby 国内的同类网站](http://36kr.com/p/207858.html)
    * [HPC on amazon ](http://www.hpcwire.com/2015/08/11/amazon-web-services-spotlights-hpc-options/)
* [负载均衡]( http://blog.chinaunix.net/uid-27022856-id-3236257.html)
* 认证
    * [在django中实现QQ登录](http://www.cnblogs.com/weisenz/archive/2012/09/06/2673456.html)
    * [Django OAuth 2.0 (RFC 6749) pluggable implementation.](https://github.com/metwit/django-fulmine)
    * [理解OAuth 2.0](http://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html)
    * [OAuth2.0认证和授权原理](http://justcoding.iteye.com/blog/1950270)
    * [支付宝的OAuth](https://doc.open.alipay.com/doc2/detail.htm?treeId=115&articleId=104110&docType=1)
* [Using Django](https://docs.djangoproject.com/en/1.9/topics/)

