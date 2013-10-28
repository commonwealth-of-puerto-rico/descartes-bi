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

from django import forms

from .literals import FILTER_TYPE_DATE, FILTER_TYPE_COMBO


class FilterForm(forms.Form):
    def __init__(self, filterset, user, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        for filterset_filter in filterset.filterset_filters.all():
            if filterset_filter.filter.filter_type == FILTER_TYPE_DATE:
                filterset_filter.filter.execute_function()
                #self.fields[filterset_filter.name] = forms.DateField(
                #    ('%m/%d/%Y',), initial=filterset_filter.default, required=False,
                #    label=filterset_filter.label, widget=forms.DateInput(format='%m/%d/%Y', attrs={'size': '10'})
                #)
                self.fields[filterset_filter.filter.name] = forms.DateField(
                    initial=filterset_filter.filter.default, required=False,
                    label=filterset_filter.filter.label, widget=forms.DateInput(attrs={'size': '10'})
                )
            elif filterset_filter.filter.filter_type == FILTER_TYPE_COMBO:
                try:
                    choices = []
                    for choice in eval(filterset_filter.filter.options, {}):
                        choices.append(choice)
                except:
                    choices = eval(filterset_filter.filter.options, {})

                #if filterset_filter.filter in results:
                #    if 'default' in results[filterset_filter.filter]:
                #        filterset_filter.filter.default = results[filterset_filter.filter]['default']

                self.fields[filterset_filter.filter.name] = forms.ChoiceField(
                    initial=filterset_filter.filter.default, required=False,
                    label=filterset_filter.filter.label, choices=choices
                )
