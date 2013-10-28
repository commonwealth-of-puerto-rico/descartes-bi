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
from multiprocessing import Pipe, Process
import re

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from charts.literals import BACKEND_CHOICES
from charts.utils import import_backend
from db_drivers.models import DataSource

from .exceptions import SeriesError
from .literals import (FILTER_FIELD_CHOICES, SERIES_TYPE_CHOICES, UNION_CHOICES)

logger = logging.getLogger(__name__)
SERIES_TIMEOUT = None


class Filter(models.Model):
    label = models.CharField(max_length=32, help_text=_('Text label that will be presented to the user.'), verbose_name=_('label'))
    name = models.CharField(max_length=48, help_text=_('Name of the parameter to be used in the queries.  Do not use spaces or special symbols.'), verbose_name=_('name'))
    description = models.CharField(max_length=32, blank=True, verbose_name=_('description'))
    filter_type = models.PositiveIntegerField(choices=FILTER_FIELD_CHOICES, verbose_name=_('filter type'))
    default = models.CharField(max_length=32, blank=True, help_text=_('Default value or one the special functions [this_day, this_month, this_year].'), verbose_name=_('default'))
    options = models.TextField(blank=True, verbose_name=_('options'))

    def __unicode__(self):
        if self.description:
            return '%s "%s"' % (self.name, self.description)
        else:
            return self.name

    def execute_function(self):
        # TODO: don't hardcode functions, move elsewhere
        today = datetime.date.today()
        if self.default == 'function:this_day':
            self.default = today

        if self.default == 'function:this_month':
            self.default = datetime.date(today.year, today.month, 1)

        if self.default == 'function:this_year':
            self.default = datetime.date(today.year, 1, 1)

    class Meta:
        ordering = ['name']
        verbose_name = _('filter')
        verbose_name_plural = _('filters')


class Filterset(models.Model):
    # TODO: rename 'name' field to 'label'
    name = models.CharField(max_length=64, verbose_name=_('name'), help_text=_('A simple name for your convenience.'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('filters set')
        verbose_name_plural = _('filters sets')


class FiltersetFilters(models.Model):
    filterset = models.ForeignKey(Filterset, verbose_name=_('filterset'), related_name='filterset_filters')
    filter = models.ForeignKey(Filter, verbose_name=_('filter'))
    order = models.IntegerField(default=0, verbose_name=_('order'))

    def __unicode__(self):
        return unicode(self.filter)

    class Meta:
        ordering = ['order']
        verbose_name = _('filterset filter')
        verbose_name_plural = _('filterset filters')


class Serie(models.Model):
    data_source = models.ForeignKey(DataSource, verbose_name=_('data source'))

    name = models.CharField(max_length=64, help_text='Internal name.  Do not use spaces or special symbols.', verbose_name=_('name'))
    label = models.CharField(max_length=24, null=True, blank=True, help_text='Label to be shown to the user and to be used for the legend.', verbose_name=_('label'))

    # TODO: Remove these, move them to the specific chart backend
    tick_format1 = models.CharField(max_length=8, choices=SERIES_TYPE_CHOICES, verbose_name=_('tick format 1'))
    tick_format2 = models.CharField(max_length=8, choices=SERIES_TYPE_CHOICES, verbose_name=_('tick format 2'))

    query = models.TextField(verbose_name=_('query'), help_text=_('SQL query, that returns only 2 fields and may of may be a parameter query.  Include parameters in the format: <field> LIKE %(parameter)s.  Also the SQL wildcard character % must be escaped as %%.'))
    description = models.TextField(null=True, blank=True, help_text='Description of the query, notes and observations.', verbose_name=_('description'))

    validated = models.BooleanField(default=False, verbose_name=_('validated?'))
    validated_date = models.DateField(blank=True, null=True, verbose_name=_('validation date'))
    validated_person = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('validated by'))
    validation_description = models.TextField(blank=True, null=True, verbose_name=_('validation description'), help_text=_('An explanation or description about how this series was validated.'))

    def __unicode__(self):
        return self.name

    def execute(self, **kwargs):
        params = kwargs.get('params')
        pipe = kwargs.get('pipe')

        if re.compile(r'[^%]%[^%(]').search(self.query):
            SeriesError(_('Single \'%\'found, replace with double \'%%\' to properly escape the SQL wildcard caracter \'%\'.'))

        cursor = self.data_source.load_backend().cursor()
        if not params:
            params = {}

        try:
            logger.debug('self.query: %s, params: %s' % (self.query, params))
            cursor.execute(self.query, params)
        except Exception as exception:
            raise SeriesError('Cursor error: %s' % exception)

        if pipe:
            pipe.send(cursor.fetchall())

        return cursor

    class Meta:
        ordering = ['name']
        verbose_name = _('serie')
        verbose_name_plural = _('series')


class Report(models.Model):
    # Base properties
    title = models.CharField(max_length=128, verbose_name=_('title'), help_text=_('Chart title.'))
    description = models.TextField(blank=True, verbose_name=_('description'), help_text=_('A description of the report. This description will also be presented to the user.'))

    # Data
    filterset = models.ForeignKey(Filterset, null=True, blank=True, verbose_name=_('filterset'))

    # Renderer properties
    renderer = models.PositiveIntegerField(choices=BACKEND_CHOICES, verbose_name=_('renderer'))
    renderer_options = models.TextField(blank=True, verbose_name=_('renderer options'), help_text=_('Python dictionary of options.'))

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('reports:ajax_report_view', args=[self.pk])

    def get_backend(self):
        return import_backend(self.renderer)

    def render(self, request):
        backend_class = self.get_backend()
        backend = backend_class(self)
        return backend.render(request)

    def execute(self, params=None, deferred=True):
        """
        The 'deferred' boolean control whether or not the series will be
        execute concurrently as subprocesses
        """
        series_results = []
        deferred_list = []

        logger.debug('params: %s' % params)

        if deferred:
            for report_series in self.report_series.all():
                # Launch all serie queries in parallel
                pipe_a, pipe_b = Pipe()
                process = Process(
                    target=report_series.series.execute,
                    kwargs={'pipe': pipe_a, 'params': params})
                process.start()
                deferred_list.append({'report_series': report_series, 'pipe': pipe_b, 'process': process})

            for deferred in deferred_list:
                try:
                    # Collect the serires queries results
                    deferred['process'].join(SERIES_TIMEOUT)
                except Exception as exception:
                    logger.error('Series subprocess exception; %s' % exception)
                else:
                    series_results.append(
                        {
                            'results': deferred['pipe'].recv(),
                            'report_series': deferred['report_series'],
                        }
                    )
        else:
            for report_series in self.report_series.all():
                series_results.append(
                    {
                        'results': report_series.series.execute(params=params).fetchall(),
                        'report_series': report_series
                    }
                )

        logger.debug('report results: %s' % series_results)
        return series_results

    class Meta:
        ordering = ['title']
        verbose_name = _('report')
        verbose_name_plural = _('reports')


class ReportSeries(models.Model):
    report = models.ForeignKey(Report, verbose_name=_('report'), related_name='report_series')
    series = models.ForeignKey(Serie, verbose_name=_('series'))

    properties = models.TextField(blank=True, verbose_name=_('properties'))

    def __unicode__(self):
        return unicode(self.series)

    class Meta:
        verbose_name = _('report series')
        verbose_name_plural = _('reports series')


class Menuitem(models.Model):
    title = models.CharField(max_length=64, verbose_name=_('title'))
    reports = models.ManyToManyField(Report, verbose_name=_('chart'), blank=True, null=True)
    order = models.IntegerField(default=0, verbose_name=_('order'))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['order', 'title']
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')


class UserPermission(models.Model):
    # TODO: access_unpublished_reports = models.BooleanField(default = False)
    user = models.ForeignKey(User, unique=True)
    union = models.CharField(max_length=1, choices=UNION_CHOICES, default='I', verbose_name=_('Group/user permissions union type'), help_text=_('Determines how the user permissions interact with the group permissions of this user.'))
    reports = models.ManyToManyField(Report, blank=True, null=True, verbose_name=_('charts'))

    def get_reports(self):
        return ', '.join(['"%s"' % r.title for r in self.reports.all()])
    get_reports.short_description = _('charts')

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _('user permission')
        verbose_name_plural = _('user permissions')


class GroupPermission(models.Model):
    # TODO: access_unpublished_reports = models.BooleanField(default = False)
    group = models.ForeignKey(Group, unique=True, verbose_name=_('group'))
    reports = models.ManyToManyField(Report, blank=True, null=True, verbose_name=_('reports'))

    def __unicode__(self):
        return unicode(self.group)

    class Meta:
        verbose_name = _('group permissions')
        verbose_name_plural = _('groups permissions')

    def get_reports(self):
        return ', '.join(['"%s"' % r.title for r in self.reports.all()])
    get_reports.short_description = _('charts')
