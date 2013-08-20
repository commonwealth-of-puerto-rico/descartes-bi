from django.conf.urls import patterns, url
from libre_driver import views

urlpatterns = patterns('',
                       # ex: /libre/
                       url(r'^$', views.IndexView, name='index'),
                       # ex: /libre/2
                       url(r'^(?P<json_id>\d+)/$', views.DetailView, name='detail'),
                       # ex: /libre/query
                       url(r'^query/$', views.QueryView, name='query'),
                       )
