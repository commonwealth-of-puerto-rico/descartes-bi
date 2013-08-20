from django.db import models
from django.utils.translation import ugettext_lazy as _


class Website(models.Model):
    label = models.CharField(max_length=32)
    base_URL = models.CharField(max_length=256, blank=True)
    series = models.ForeignKey('reports.Serie', verbose_name=_(u"series"), blank=True, null=True)
    filterset = models.ManyToManyField('reports.Filterset', verbose_name=_(u'filterset'), blank=True, null=True)

    def __unicode__(self):
        return self.label
