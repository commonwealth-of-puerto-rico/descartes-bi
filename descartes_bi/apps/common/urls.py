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

from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.views.generic.base import RedirectView

urlpatterns = patterns('common.views',
    url(r'^set_language/$', 'set_language', (), name='set_language'),
    url(r'^about/$', 'about', (), 'about_view'),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login_view'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout_view'),
    url(r'^myaccount/password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'password_change_form.html'}, name='password_change_view'),
    url(r'^accounts/password_change_ok/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_change_done.html'}),

    (r'^favicon\.ico$', RedirectView.as_view(url='%simages/favicon.png' % settings.STATIC_URL)),
)
