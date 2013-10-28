from __future__ import absolute_import

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from .models import Dashboard

logger = logging.getLogger(__name__)


@login_required
def dashboard_view(request, dashboard_pk, extra_context=None):
    dashboard = get_object_or_404(Dashboard, pk=dashboard_pk)

    context = {'dashboard': dashboard, 'rows': dashboard.get_element_rows(), 'query_string': request.META['QUERY_STRING']}

    if extra_context:
        context.update(extra_context)

    return render_to_response('dashboards/dashboard.html', context,
        context_instance=RequestContext(request))
