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

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from charts.exceptions import ChartError

from .exceptions import SeriesError
from .models import Report
from .utils import get_allowed_object_for_user

logger = logging.getLogger(__name__)


def ajax_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)

    if report not in get_allowed_object_for_user(request.user)['reports']:
        return render_to_response('messagebox-error.html',
         {'title': _(u'Permission error'),
          'message': _(u"Insufficient permissions to access this area.")})

    try:
        return report.render(request)
    except ChartError as exception:
        return render_to_response('messagebox-error.html', {'title': _('Chart error'), 'message': exception},
            context_instance=RequestContext(request))
    except SeriesError as exception:
        return render_to_response('messagebox-error.html', {'title': _('Series error'), 'message': exception},
            context_instance=RequestContext(request))
