from __future__ import absolute_import

import json
import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .base import ChartBackend

logger = logging.getLogger(__name__)

CHART_TYPE_STANDARD_X_Y = 'SI'
CHART_TYPE_LINE_CHART = 'LI'
CHART_TYPE_PIE_CHART = 'PI'

CHART_TYPE_CHOICES = (
    (CHART_TYPE_STANDARD_X_Y, _('Standard X, Y')),
    (CHART_TYPE_LINE_CHART, _('Line chart')),
    (CHART_TYPE_PIE_CHART, _('Pie chart')),
)

# TODO: Add support for the remaining chart types
# ('SH', _('Horizontal X,Y')),
# ('LB', _('Line Plus Bar Chart')),
# ('LF', _('Line chart with Focus')),


class NovusD3(ChartBackend):
    label = _('Novus D3')

    options = [
        {
            'name': 'chart_type',
            'label': _('chart type'),
            'choices': CHART_TYPE_CHOICES,
            'default': CHART_TYPE_LINE_CHART,
        },
        {
            'name': 'chart_options',
            'label': _('chart options'),
        }
    ]

    chart_template = {
        CHART_TYPE_STANDARD_X_Y: 'charts/novus/multiBarChart.html',  # 'Standard X,Y'
        CHART_TYPE_LINE_CHART: 'charts/novus/lineChart.html',  # Line chart
        CHART_TYPE_PIE_CHART: 'charts/novus/pieChart.html',  # Pie chart
    }

    def process_series(self, series):
        result = []
        for data_element in series:
            result.append({'x': data_element[0], 'y': data_element[1]})

        return result

    def process_data(self):
        report_series_all = self.report.execute()

        if self.chart_type == CHART_TYPE_PIE_CHART:
            # Pie chart needs a single flat list of dictionary values
            return self.process_series(report_series_all[0]['results'])
        else:
            # The other charts needs nested flat list of series' values
            result = []
            for report_series in report_series_all:
                result.append({'values': self.process_series(report_series['results'])})

        return result

    def render(self, request):
        # TODO: Error handling
        context = {
            'series_results': """%s;\n""" % json.dumps(self.process_data()),
            'chart_options': self.chart_options,
            'report': self.report,
        }

        logger.debug('context: %s' % context)

        return render_to_response(self.chart_template.get(self.chart_type), context, context_instance=RequestContext(request))
