from django.conf.urls import patterns , url

from job.views import *

'''
urlpatterns = patterns('command.views',
    (r'^/?$', JobRootView.as_view()),
    (r'^/(?P<machine>[^/]+)/$', JobQueueView.as_view()),
    (r'^/(?P<machine>[^/]+)/(?P<job_id>[^/]+)/$', JobDetailView.as_view()),
    (r'^(?P<query>.+)/$', ExtraJobView.as_view()),
)
'''
urlpatterns = [
    url(r'^$', JobRootView.as_view()),
    url(r'^(?P<machine>[^/]+)/$', JobQueueView.as_view()),
    url(r'^(?P<machine>[^/]+)/(?P<job_id>[^/]+)/$', JobDetailView.as_view()),
    url(r'^(?P<query>.+)/$', ExtraJobView.as_view()),
]
