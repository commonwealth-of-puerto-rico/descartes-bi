from django.db import models
from django.utils.translation import ugettext_lazy as _

from reports.models import Report, Filterset


class Selected_report(models.Model):
    rep_id = models.ForeignKey(Report, verbose_name=_(u"report"), blank=True, null=True)
    website = models.ForeignKey('website.Website', verbose_name=_(u"website"), blank=True, null=True)
    filtersets = models.ForeignKey(Filterset, null=True, blank=True)
    values = models.CharField(max_length=200, blank=True)
    #from_date = models.DateField('From Date')
    #to_date = models.DateField('To Date')
    #id_regional = models.PositiveSmallIntegerField('Regional ID')
    visual_type = models.CharField(max_length=7, choices=(('chart', 'chart'), ('grid', 'grid'), ('website', 'website')), default='chart')
    refresh_rate = models.PositiveSmallIntegerField('Refresh Rate')

    def __unicode__(self):
        if self.rep_id:
            return self.rep_id.title + "{ " + self.values + " }"
        else:
            return self.website.label

    class Meta:
        verbose_name = _('dashboard report')
        verbose_name_plural = _('dashboard reports')


class Dash(models.Model):
    name = models.CharField(max_length=50)
    selection_list = models.ManyToManyField(Selected_report)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('dashboard')
        verbose_name_plural = _('dashboards')
