#from django.conf.urls import patterns , url
from django.conf.urls import *
from async.views import AsyncView, ExtraAsyncView

'''
urlpatterns = patterns('command.views',
    (r'^/?$', CommandRootView.as_view()),
    (r'^/(?P<machine_name>[^/]+)$', CommandView.as_view()),
    (r'^(?P<query>.+)/$', ExtraCommandView.as_view()),
)
'''
urlpatterns = [
    url(r'^(?P<async_id>[^/]+)/$', AsyncView.as_view()),
    url(r'^(?P<async_id>[^/]+)$', AsyncView.as_view()),
    url(r'^(?P<query>.+)/$', ExtraAsyncView.as_view()),
]
