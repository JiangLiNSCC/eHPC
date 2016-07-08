from django.conf.urls import patterns , url

from command.views import CommandView, CommandRootView, ExtraCommandView

'''
urlpatterns = patterns('command.views',
    (r'^/?$', CommandRootView.as_view()),
    (r'^/(?P<machine_name>[^/]+)$', CommandView.as_view()),
    (r'^(?P<query>.+)/$', ExtraCommandView.as_view()),
)
'''
urlpatterns = [
    url(r'^$', CommandRootView.as_view()),
    url(r'^/(?P<machine_name>[^/]+)$', CommandView.as_view()),
    url(r'^(?P<query>.+)/$', ExtraCommandView.as_view()),
]
