from django.utils.translation import ugettext_lazy as _

FILTER_TYPE_COMBO = 1
FILTER_TYPE_DATE = 2

FILTER_FIELD_CHOICES = (
    (FILTER_TYPE_DATE, _('Date field')),
    (FILTER_TYPE_COMBO, _('Simple drop down')),

    # Other future improvements
    # ('SE', _('Separator  *N/A*')),
    # ('DQ', _('Simple drop down from query *N/A*')),
    # ('SI', _('Drop down with hidden index  *N/A*')),
    # ('SI', _('Drop down with hidden index from query *N/A*')),
    # ('TX', _('Text field *N/A*')),
    # ('NU', _('Number field *N/A*')),
    # ('MO', _('Month name drop down *N/A*')),
)

SERIES_TYPE_CHOICES = (
    ('Ye', _('Year')),
    ('My', _('Year-Month')),
    ('St', _('String')),
    ('To', _('Total')),
    ('C', _('Currency')),

)

UNION_CHOICES = (
    ('E', _('Exclusive')),
    ('I', _('Inclusive')),
    ('O', _('Override')),
)
