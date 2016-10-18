#from django.conf.urls import patterns ,url
from django.conf.urls import *
from account.views import *

'''
urlpatterns = patterns('account.views',
    (r'^/user/(?P<user_name>[^/]+)/$', UserInfoView.as_view()),
    (r'^/user/id/(?P<uid>\d+)/$', UserInfoView.as_view()),
    (r'^/group/(?P<group_name>[^/]+)/$', GroupInfoView.as_view()),
    (r'^/group/id/(?P<gid>\d+)/$', GroupInfoView.as_view()),
    (r'^(?P<query>.+)/$', ExtraAcctView.as_view()),
)
'''
urlpatterns = [
    url(r'^user/(?P<user_name>[^/]+)/$', UserInfoView.as_view()),
    url(r'^user/id/(?P<uid>\d+)/$', UserInfoView.as_view()),
    url(r'^group/(?P<group_name>[^/]+)/$', GroupInfoView.as_view()),
    url(r'^group/id/(?P<gid>\d+)/$', GroupInfoView.as_view()),
    url(r'^(?P<query>.+)/$', ExtraAcctView.as_view()),
]
