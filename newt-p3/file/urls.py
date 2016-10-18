#from django.conf.urls import patterns ,url
from django.conf.urls import *
from file.views import FileView, FileRootView, ExtraFileView

'''
urlpatterns = patterns('file.views',
    (r'^/?$', FileRootView.as_view()),
    (r'^/(?P<machine_name>[^/]+)(?P<path>/.*)$', FileView.as_view()),
    (r'^(?P<query>.+)/$', ExtraFileView.as_view()),
)
'''
urlpatterns = [
    url(r'^$', FileRootView.as_view()),
    url(r'^/(?P<machine_name>[^/]+)(?P<path>/.*)$', FileView.as_view()),
    url(r'^(?P<query>.+)/$', ExtraFileView.as_view()),
]
    
