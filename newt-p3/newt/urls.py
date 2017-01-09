#from django.conf.urls import patterns, include, url
from django.conf.urls import *
from newt.views import RootView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns =[
  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
  url(r'^admin/', include(admin.site.urls)),
   url(r'^api/$', RootView.as_view()),
    url(r'^api/status/', include('status.urls')),
    url(r'^api/file', include('file.urls')),
    url(r'^api/auth', include('authnz.urls')),
    url(r'^api/command', include('command.urls')),
    url(r'^api/store', include('store.urls')),
    url(r'^api/account/', include('account.urls')),
    url(r'^api/job', include('job.urls')),
    url(r'^api/async',include('async.urls')),
]
