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
from common.models import Namespace, TYPE_MENU, TYPE_WIDGETS, TYPE_WEBSITES


class UploadFileForm(forms.Form):
    file = forms.FileField()


class NamespaceForm(forms.ModelForm):
    class Meta:
        model = Namespace

    def clean(self):
        super(NamespaceForm, self).clean()
        has_selected_type = self.cleaned_data.get('view_type', None)
        has_selected_menu = self.cleaned_data.get('view_menu', None)
        has_selected_dash = self.cleaned_data.get('view_dash', None)
        has_selected_website = self.cleaned_data.get('view_website', None)

        if has_selected_type:
            #view type and menu item should match
            if has_selected_type == TYPE_MENU and not has_selected_menu:
                message = ("""View type is Menu. Please select Menu.""")
                raise forms.ValidationError(message)
            if has_selected_type == TYPE_WIDGETS and not has_selected_dash:
                message = ("""View type is Dashboard. Please select Dashboard.""")
                raise forms.ValidationError(message)
            if has_selected_type == TYPE_WEBSITES and not has_selected_website:
                message = ("""View type is Website. Please select Website.""")
                raise forms.ValidationError(message)
        else:
            #No menu item w/o view type
            if has_selected_menu or has_selected_dash or has_selected_website:
                message = ("""Please select a view type for Menu/Dashboard/Website item.""")
                raise forms.ValidationError(message)

        #Should not save multiple menu items
        # TODO: Improve
        if ((has_selected_menu and (has_selected_dash or has_selected_website))
            or (has_selected_dash and (has_selected_menu or has_selected_website))
            or (has_selected_website and (has_selected_menu or has_selected_dash))):
                message = ("""Multiple menu items.""")
                raise forms.ValidationError(message)

        return self.cleaned_data