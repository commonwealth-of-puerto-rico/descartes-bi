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
import datetime
import logging
import json
import re

from django.db import connections
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from db_drivers.models import BACKEND_LIBRE

from .forms import FilterForm
from .models import Report, Menuitem, GroupPermission, UserPermission, User, SeriesStatistic, ReportStatistic
from .literals import FILTER_TYPE_DATE, FILTER_TYPE_COMBO
from .utils import get_allowed_object_for_user


logger = logging.getLogger(__name__)


def ajax_report_benchmarks(request, report_id):
    #TODO: change this to get values from serie_statistics instead
    report = get_object_or_404(Report, pk=report_id)
    result = ''
    if request.user.is_staff:
        result = '<ul>'
        for s in report.series.all():
            result += "<li>%s</li><br />" % _('"%(serie)s" = Lastest run: %(last)ss; Average: %(avg)ss') % {'serie': s.label or unicode(s), 'last': s.last_execution_time or '0', 'avg': s.avg_execution_time or '0'}

        result += '</ul>'

    return HttpResponse(result)


def ajax_filter_form(request, report_id):
    #TODO: access control
    if request.method == 'GET':
        query = request.GET

    report = get_object_or_404(Report, pk=report_id)

    if report not in get_allowed_object_for_user(request.user)['reports']:
        return render_to_response('messagebox-error.html',
                                  {'title': _(u'Permission error'),
                                   'message': _(u"Insufficient permissions to access this area.")})

    if query:
        filter_form = FilterForm(report.filtersets.all(), request.user, query)
    else:
        filter_form = FilterForm(report.filtersets.all(), request.user)

    return render_to_response('filter_form_subtemplate.html', {'filter_form': filter_form},
        context_instance=RequestContext(request))


def ajax_report_description(request, report_id):
    report = get_object_or_404(Report, pk=report_id)

    result = "<strong>%s</strong><br />%s" % (report.title, report.description or '')
    return HttpResponse(result)


def ajax_report_validation(request, report_id):
    report = get_object_or_404(Report, pk=report_id)

    result = ''

    for s in report.series.all():
        if s.validated:

            result += "<li>'%s' validated on %s" % (s.label or unicode(s),
                                                    s.validated_date)
            if s.validated_person:
                result += " by %s" % s.validated_person
            result += '</li><br />'

    if result:
        return HttpResponse('<ul>%s</ul>' % result)
    else:
        return HttpResponse(_(u'No element of this report has been validates.'))


def ajax_report(request, report_id):
    start_time = datetime.datetime.now()

    report = get_object_or_404(Report, pk=report_id)

    if report not in get_allowed_object_for_user(request.user)['reports']:
        return render_to_response('messagebox-error.html',
         {'title': _(u'Permission error'),
          'message': _(u"Insufficient permissions to access this area.")})

    output_type = request.GET.get('output_type', 'chart')
    params = {}
    special_params = {}

    if report.filtersets.all():
        filtersets = report.filtersets
        if request.method == 'GET':
            filter_form = FilterForm(filtersets, request.user, request.GET)
        else:
            filter_form = FilterForm(filtersets, request.user)

        for set in filtersets.all():
            for filter in set.filters.all():

                if filter_form.is_valid():
                    value = filter_form.cleaned_data[filter.name]
                    if not value:
                        filter.execute_function()
                        value = filter.default

                else:
                    filter.execute_function()
                    value = filter.default

                if filter.type == FILTER_TYPE_DATE:
                    params[filter.name] = value.strftime("%Y%m%d")
                elif filter.type == FILTER_TYPE_COMBO:
                    special_params[filter.name] = '(' + ((''.join(['%s'] * len(value)) % tuple(value))) + ')'
                else:
                    params[filter.name] = value

    series_results = []
    tick_format1 = []
    tick_format2 = []
    labels = []
    for s in report.serietype_set.all():
        query = s.serie.query
        if re.compile("[^%]%[^%(]").search(query):
            return render_to_response('messagebox-error.html', {'title': _(u'Query error'), 'message': _(u"Single '%' found, replace with double '%%' to properly escape the SQL wildcard caracter '%'.")})

        cursor = s.serie.data_source.load_backend().cursor()

        if special_params:
            for sp in special_params.keys():
                query = re.compile('%\(' + sp + '\)s').sub(special_params[sp], query)
            try:
                serie_start_time = datetime.datetime.now()
                cursor.execute(query, params)
            except:
                import sys
                (exc_type, exc_info, tb) = sys.exc_info()
                return render_to_response('messagebox-error.html', {'title': exc_type, 'message': exc_info})

        else:
            cursor.execute(query, params)
            logger.debug('cursor.execute; query: %s, params: %s' % (query, params))
            serie_start_time = datetime.datetime.now()

        labels.append(re.compile('aS\s(\S*)', re.IGNORECASE).findall(query))

        #Temporary fix for Libre database
        if s.serie.data_source.backend == BACKEND_LIBRE:
            series_results.append(json.dumps(cursor.fetchall()))
        elif output_type == 'chart':
            series_results.append(data_to_js_chart(cursor.fetchall(), report.orientation))
        elif output_type == 'grid':
            series_results.append(data_to_js_grid(cursor.fetchall(), s.serie.tick_format1))
        #append tick formats

        tick_format1.append(s.serie.tick_format1)
        tick_format2.append(s.serie.tick_format2)
        s.serie.last_execution_time = (datetime.datetime.now() - serie_start_time).seconds
        s.serie.avg_execution_time = (s.serie.avg_execution_time or 0 + s.serie.last_execution_time) / 2
        s.serie.save()

        try:
            serie_statistics = SeriesStatistic()
            serie_statistics.serie = s.serie
            serie_statistics.user = request.user
            serie_statistics.execution_time = (datetime.datetime.now() - serie_start_time).seconds
            serie_statistics.params = ', '.join(["%s = %s" % (k, v) for k, v in filter_form.cleaned_data.items()])
            serie_statistics.save()
        except:
            pass

    try:
        report_statistics = ReportStatistic()
        report_statistics.report = report
        report_statistics.user = request.user
        report_statistics.execution_time = (datetime.datetime.now() - start_time).seconds
        report_statistics.params = "%s" % (', '.join(["%s = %s" % (k, v) for k, v in filter_form.cleaned_data.items()]))
        report_statistics.save()
    except:
        pass

    if report.orientation == 'v':
        h_axis = "x"
        v_axis = "y"
    else:
        h_axis = "y"
        v_axis = "x"

    if s.serie.data_source.backend == BACKEND_LIBRE:
        data = {
            'chart_data': s.serie.data_source.backend,
            'backend_libre': BACKEND_LIBRE,
            'tick_format1': tick_format1,
            'tick_format2': tick_format2,
            'series_results': series_results,
            'chart_series': report.serietype_set.all(),
            'ajax': True,
            'query': query,
            'chart': report,
        }
    else:
        data = {
            'chart_data': ','.join(series_results),
            'series_results': series_results,
            'chart_series': report.serietype_set.all(),
            'tick_format1': tick_format1,
            'tick_format2': tick_format2,
            'chart': report,
            'h_axis': h_axis,
            'v_axis': v_axis,
            'ajax': True,
            'query': query,
            'params': params,
            'series_labels': labels,
            'time_delta': datetime.datetime.now() - start_time,
        }

    if output_type == 'chart':
        return render_to_response('single_chart.html', data,
            context_instance=RequestContext(request))
    elif output_type == 'grid':
        return render_to_response('single_grid.html', data,
            context_instance=RequestContext(request))
    else:
        return render_to_response('messagebox-error.html', {'title': _(u'Error'), 'message': _(u"Unknown output type (chart, table, etc).")})


#TODO: Improve this further
def data_to_js_chart(data,  orientation='v'):
    if not data:
        return ''

    result = '['
    if orientation == 'v':
        for key, value in data:
            result += '["%s",%s],' % (key or '?', value)
            #result = [[k or '?',v, label_formar % v] for k,v in a]
    else:
        for key, value in data:
            try:
                # unicode(key.decode("utf-8")) Needed to handle non ascii
                result += '[%s,"%s","%s"],' % (value,
                      unicode(key.decode("utf-8")) or u'?', unicode(value))
            except:
                #However fails with long integer
                result += '[%s,"%s","%s"],' % (value, unicode(key or '?'),
                        unicode(value))

    result = result[:-1]
    result += ']'

    return result


def data_to_js_grid(data, label_format=None):
    if not data:
        return ''

    if not label_format:
        label_format = "%s"

    result = '['
    for key, value in data:
        result += '{key:"%s", value:"%s"},' % (key or '?', label_format % value)

    result = result[:-1]
    result += ']'

    return result
