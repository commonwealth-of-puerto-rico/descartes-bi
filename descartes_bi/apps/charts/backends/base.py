from ast import literal_eval
import logging

from django.utils.translation import ugettext_lazy as _

from ..exceptions import ChartError

logger = logging.getLogger(__name__)


class ChartBackend(object):
    """
    Base class for the chart rendering backend.
    """
    label = _('Chart base class')

    def __init__(self, report):
        self.report = report
        if report.renderer_options:
            try:
                self.option_values = literal_eval(report.renderer_options)
            except Exception as exception:
                error_messagse = 'Exception while evaluating renderer_options; %s' % exception
                logger.error(error_messagse)
                raise ChartError(error_messagse)
        else:
            self.option_values = {}

        for option in self.__class__.options:
            setattr(self, option['name'], self.option_values.get(option['name'], option.get('default')))

    def render(self, request):
        """Each backend must override this method. Method must return an
        HttpResponse or subclass, which is passed directly to the calling
        view.
        """
        raise NotImplemented
