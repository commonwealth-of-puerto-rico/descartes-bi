from __future__ import absolute_import

import logging

import requests

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from reports.forms import FilterForm

from .base import ChartBackend

logger = logging.getLogger(__name__)


class Website(ChartBackend):
    label = _('Website')

    options = [
        {
            'name': 'base_url',
            'label': _('Base URL'),
        },
        {
            'name': 'username',
            'label': _('Username'),
        },
        {
            'name': 'password',
            'label': _('Password'),
        },
    ]

    def render(self, request):
        if self.report.filterset:
            if request.GET:
                form = FilterForm(self.report.filterset, request.user, request.GET)
                if form.is_valid():
                    logger.debug('self.base_url: %s' % self.base_url)
                    logger.debug('form.cleaned_data: %s' % form.cleaned_data)
                    website_url = self.base_url % form.cleaned_data
                else:
                    website_url = ''
            else:
                form = FilterForm(self.report.filterset, request.user)
                website_url = ''
        else:
            form = None
            website_url = self.base_url

        logger.debug('website_url: %s' % website_url)
        if website_url:
            if self.username:
                response = requests.get(website_url, auth=(self.username, self.password))
            else:
                response = requests.get(website_url)

            content = response.content.encode('base64')
        else:
            content = ''

        context = {
            'report': self.report,
            'content': content,
            'form': form,
        }
        #logger.debug('context: %s' % context)

        return render_to_response('charts/website/website.html', context,
            context_instance=RequestContext(request))
