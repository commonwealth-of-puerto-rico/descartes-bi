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
import os
import re

from django import http
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, RequestContext

from common.models import Namespace
from dashboard.models import Dash
from website.views import get_website


def error500(request, template_name='500.html'):
    #TODO: if user is admin include debug info
    t = loader.get_template(template_name)

    return http.HttpResponseServerError(t.render(RequestContext(request, {
        'project_name': settings.PROJECT_TITLE})))


def get_svn_revision(path=None):
    rev = None
    entries_path = '%s/.svn/entries' % path

    if os.path.exists(entries_path):
        entries = open(entries_path, 'r').read()
        # Versions >= 7 of the entries file are flat text.  The first line is
        # the version number. The next set of digits after 'dir' is the revision.
        if re.match('(\d+)', entries):
            rev_match = re.search('\d+\s+dir\s+(\d+)', entries)
            if rev_match:
                rev = rev_match.groups()[0]
        # Older XML versions of the file specify revision as an attribute of
        # the first entries node.
        else:
            from xml.dom import minidom
            dom = minidom.parse(entries_path)
            rev = dom.getElementsByTagName('entry')[0].getAttribute('revision')

    if rev:
        return u'svn-r%s' % rev
    return u'svn-unknown'


def set_language(request):
    if request.method == "GET":
        request.session['django_language'] = request.GET.get('language', 'en')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def home(request):
    return render_to_response('home.html', {},
        context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', {'revision': get_svn_revision(settings.PROJECT_ROOT)},
        context_instance=RequestContext(request))


def get_project_root():
    """ get the project root directory """
    settings_mod = __import__(settings.SETTINGS_MODULE, {}, {}, [''])
    return os.path.dirname(os.path.abspath(settings_mod.__file__))


def get_dash_menu(request, namespace_id):
    node = Namespace.objects.get(pk=namespace_id)

    context = {}

    if node.is_leaf_node():
        #view_type 1 - Menu, view_type 2 - Dashboard
        if node.view_type == 1:
            context['menus'] = node.view_menu.all()
            page = 'sub_dash_menu.html'

        #Check if the view_type is a website and call the website view
        elif node.view_type == 3:
            website = node.view_website.all()[0]
            return get_website(request, website)

        elif node.view_type == 2:
            dash_id = node.view_dash_id
            dash_board = get_object_or_404(Dash, pk=dash_id)
            selected_reports = dash_board.selection_list.all()
            links = {}
            for sp in selected_reports:
                if sp.rep_id:
                    get_form = ""
                    if sp.filtersets:
                        filterform = sp.filtersets.filters.all()
                        values = sp.values.split(',')
                        for index in range(len(values)):
                            get_form += filterform[index].name + "=" + values[index] + "&"

                    lk = "reports/ajax/report/" + str(sp.rep_id.id) + "/?" + get_form + "output_type=" + sp.visual_type
                    links[str(sp.id)] = lk
                if sp.website:
                    query = sp.website.series.query
                    if sp.website.filterset.exists():
                        filterform = sp.filtersets.filters.all()
                        values = sp.values.split(',')
                        dic = {}
                        for index in range(len(values)):
                            if values[index].isdigit():
                                dic[filterform[index].name] = int(values[index])
                            else:
                                dic[filterform[index].name] = values[index]
                        query = query % dic
                    if sp.website.base_URL:
                        links["mapdiv" + str(sp.id)] = sp.website.base_URL + "/?" + query
                    else:
                        links["mapdiv" + str(sp.id)] = sp.website.series.data_source.load_backend().cursor().url + "/?" + query
            context = {'selected_reports': selected_reports,
                       'dash_board': dash_board, 'links': links}
            page = 'dashboard/dash_list.html'

        else:
            page = 'sub_dash_menu.html'
    else:
        context['nodes'] = node.get_children()
        page = 'sub_dash_menu.html'

    return render_to_response(page, context,
        context_instance=RequestContext(request))
