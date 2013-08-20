from django.shortcuts import render, get_object_or_404

from dashboard.models import Dash


def index(request):
    dash_list = Dash.objects.all()
    context = {'dash_list': dash_list}
    return render(request, 'dashboard/test.html', context)


def display(request, dash_id):
    dash_board = get_object_or_404(Dash, pk=dash_id)
    selected_reports = dash_board.selection_list.all()

    links = {}
    print "Create Links list"

    for sp in selected_reports:
    	links.append("reports/ajax/report/" + sp.rep_id.id)

    print "links: ", links

    context = {'selected_reports': selected_reports, 'dash_board': dash_board, 'links' : links, }
    return render(request, 'dashboard/dash_list.html', context)