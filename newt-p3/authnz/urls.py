#from django.conf.urls import patterns , url 
from django.conf.urls import * 
from authnz.views import AuthView, ExtraAuthView

'''
urlpatterns = patterns('auth.views',
     url( r'^/$',AuthView.as_view()  ),
     url( r'^(?P<query>.+)/$', ExtraAuthView.as_view()  ),
#    (r'^/?$', AuthView.as_view()),
#    (r'^(?P<query>.+)/$', ExtraAuthView.as_view()),
)
'''
urlpatterns =[
    url( r'^/$',AuthView.as_view()  ),
    url( r'^$',AuthView.as_view()  ),
     url( r'^(?P<query>.+)/$', ExtraAuthView.as_view()  ),
] 
