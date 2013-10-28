from __future__ import absolute_import

from django.conf.urls import patterns, url

from .views import dashboard_view

urlpatterns = patterns('',
    url(r'^dashboard/(?P<dashboard_pk>\d+)/$', dashboard_view, (), 'dashboard_view'),
)
