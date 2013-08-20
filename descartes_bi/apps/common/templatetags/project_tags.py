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

from django import template
from django.template import Library

from common.models import Namespace

register = Library()


@register.simple_tag
def project_name():
    """Tag to return the current project's title"""
    from django.conf import settings
    return settings.PROJECT_TITLE


class get_root_menu_node(template.Node):
    def render(self, context):

        context['root_menu'] = [i for i in Namespace.objects.all()
                                        if i.is_root_node()]
        return ''


@register.tag(name='get_root_menu')
def get_root_menu(parser, token):
    return get_root_menu_node()