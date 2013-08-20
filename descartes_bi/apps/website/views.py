from django.shortcuts import render_to_response
from django.template import RequestContext

from reports.forms import FilterForm


def get_website(request, website):
    context = {}
    context['website'] = website.filterset.exists()
    context['label'] = website.label
    #Compose the URL to create LQL queries
    if website.series:
        url = website.series.data_source.load_backend().cursor().url
        query = website.series.query

        if request.method == 'GET' and website.filterset.exists():
            filtersets = website.filterset

            if request.GET:
                filter_form = FilterForm(filtersets, request.user, request.GET)
                query = query % get_dict(filter_form)
                context['url'] = url + "/?" + query
            else:
                filter_form = FilterForm(filtersets, request.user)

            context['filter_form'] = filter_form
        else:
            context['url'] = url + "/?" + query

    #Display the website in base_URL
    else:
        context['url'] = website.base_URL

    page = 'website/website.html'

    return render_to_response(page, context,
                              context_instance=RequestContext(request))

#Use function to convert string to int.
def get_dict(filter_form):
    value = {}
    for key in filter_form.data:
        if filter_form.data[key].isdigit():
            value[key] = int(filter_form.data[key])
        else:
            value[key] = filter_form.data[key]

    return value