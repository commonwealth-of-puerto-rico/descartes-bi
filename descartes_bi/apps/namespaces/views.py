from __future__ import absolute_import
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
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from dashboards.models import Dashboard
from dashboards.views import dashboard_view

from .literals import TYPE_DASHBOARD, TYPE_MENU
from .models import Namespace

logger = logging.getLogger(__name__)


@login_required
def node_view(request, node_pk=None):
    context = {}

    if node_pk:
        node = get_object_or_404(Namespace, pk=node_pk)
    else:
        try:
            node = Namespace.objects.get(parent=None)
        except Namespace.MultipleObjectsReturned:
            messages.error(request, _('Define just one root node.'))
            node = None
        except Namespace.DoesNotExist:
            messages.warning(request, _('You must define one root node.'))
            node = None

    logger.debug('node_pk: %s' % node_pk)
    logger.debug('node: %s' % node)

    context['node'] = node

    if node:
        if node.view_type == TYPE_MENU:
            context['menus'] = node.view_menu.all()
        elif node.view_type == TYPE_DASHBOARD:
            dashboard = get_object_or_404(Dashboard, pk=node.view_dash_id)
            return dashboard_view(request, dashboard.pk, extra_context=context)

    return render_to_response('namespaces/node.html', context,
        context_instance=RequestContext(request))
