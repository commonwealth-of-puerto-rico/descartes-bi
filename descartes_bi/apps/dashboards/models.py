from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from reports.models import Report

from .literals import DEFAULT_ELEMENT_HEIGHT


class Dashboard(models.Model):
    label = models.CharField(max_length=64, verbose_name=_(u'label'))

    def __unicode__(self):
        return self.label

    def active_elements(self):
        return self.elements.filter(enabled=True)

    def get_element_rows(self):
        rows = []
        row = []
        spans = 0
        for element in self.active_elements():
            spans += element.span
            if spans > 12:
                rows.append(row)
                spans = element.span
                row = []

            row.append(element)

        if row:
            rows.append(row)

        return rows

    class Meta:
        verbose_name = _('dashboard')
        verbose_name_plural = _('dashboards')


class DashboardElement(models.Model):
    dashboard = models.ForeignKey(Dashboard, verbose_name=_(u'dashboard'), related_name='elements')
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'))
    span = models.PositiveIntegerField(verbose_name=_(u'span'), help_text=_('The amount of columns in a 12 columns layout that this element should occupy.'))
    height = models.PositiveIntegerField(verbose_name=_(u'height'), default=DEFAULT_ELEMENT_HEIGHT)
    report = models.ForeignKey(Report, verbose_name=_(u'report'), blank=True, null=True)
    values = models.TextField(blank=True)

    @property
    def load_url(self):
        return self.report.get_absolute_url()

    def __unicode__(self):
        return unicode(self.report)

    class Meta:
        verbose_name = _('dashboard element')
