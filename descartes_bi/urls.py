#
#    Copyright (C) 2010  Roberto Rosario
#    This file is part of descartes-bi.
#
#    descartes-bi is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    descartes-bi is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with descartes-bi.  If not, see <http://www.gnu.org/licenses/>.
#
from django.conf.urls.defaults import include, patterns, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()

handler500 = 'common.views.error500'
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^dashboard/', include('dashboard.urls', namespace='dashboard')),

    (r'^reports/', include('reports.urls', namespace='reports')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^', include('common.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='my_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='user_logout'),
    url(r'^myaccount/password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'password_change_form.html'}, name='my_password_change'),
    url(r'^accounts/password_change_ok/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_change_done.html'}),

    (r'^favicon\.ico$', RedirectView.as_view(url='%simages/favicon.ico' % settings.MEDIA_URL)),
    url(r'^libre/', include('libre_driver.urls', namespace="libre")),
)

if settings.DEVELOPMENT:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls'), name='rosetta'),
        )
