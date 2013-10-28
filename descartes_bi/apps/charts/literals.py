from django.utils.translation import ugettext_lazy as _

BACKEND_NVD3 = 1
BACKEND_WEBSITE = 2

BACKEND_CHOICES = (
    (BACKEND_NVD3, _('Novus D3')),
    (BACKEND_WEBSITE, _('Website')),
)

BACKEND_CLASSES = {
    BACKEND_NVD3: 'charts.backends.nvd3.NovusD3',
    BACKEND_WEBSITE: 'charts.backends.websites.Website',
}
