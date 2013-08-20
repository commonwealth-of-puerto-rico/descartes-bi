from django.utils.translation import ugettext_lazy as _

FILTER_TYPE_DATE = 'DA'
FILTER_TYPE_COMBO = 'DR'
FILTER_TYPE_MONTH = 'MO'

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

CHART_TYPE_CHOICES = (
    ('SI', _('Standard X,Y')),
    ('PI', _('Pie chart')),
    ('LB', _('Line Plus Bar Chart')),
    ('LI', _('Line chart')),
    ('LF', _('Line chart with Focus')),
)
LEGEND_LOCATION_CHOICES = (
    ('nw', _('North-West')),
    ('n', _('North')),
    ('ne', _('North-East')),
    ('e', _('East')),
    ('se', _('South-East')),
    ('s', _('South')),
    ('sw', _('South-West')),
    ('w', _('West')),
)
ORIENTATION_CHOICES = (
    ('h', _('Horizontal')),
    ('v', _('Vertical')),
)

UNION_CHOICES = (
    ('E', _('Exclusive')),
    ('I', _('Inclusive')),
    ('O', _('Override')),
)
