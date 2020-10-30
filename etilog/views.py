from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
import json

# from 3rd apps

# models

from etilog.models import (Company, Reference, Country,
                           SustainabilityTag, ActivityCategory)

# forms
from etilog.forms.forms_filter import (SearchForm, OverviewFiltHeaderForm, OverviewFHiddenForm,
                                       OverviewFForm
                                       )
from etilog.forms.forms_suggestions import TopicForm

from etilog.ViewLogic.ImpevView import get_results, filter_results


def overview_impevs(request, reqtype=None):

    landing = False
    if len(request.GET) == 0:  # firsttime
        jsondata = json.dumps(False)  # False #Table(table_qs)
        landing = True

    else:
        d_dict = filter_results(request)
        jsondata = json.dumps(d_dict)

    searchform = SearchForm(landing)  # Filter ServerSide
    topicforms = []
    if landing:
        suggestions = ['tags', 'company', 'industry']

        for n in suggestions:
            tform = TopicForm(n)
            topicforms.append(tform)

    filtheader = OverviewFiltHeaderForm()
    filterhidden = OverviewFHiddenForm()
    filtform = OverviewFForm()

    return render(request, 'etilog/overview.html', {
        'filter': filterhidden,
        'filterform': filtform,
        'filtheader': filtheader,
        'searchform': searchform,
        'topicforms': topicforms,
        'landing': landing,
        'jsondata': jsondata,
    })


def filter_impevs(request):
    d_dict = filter_results(request)
    jsondata = json.dumps(d_dict)
    return HttpResponse(jsondata, content_type='application/json')


def get_result(request):
    d_dict = {}
    get_results(request, d_dict)
    jsondata = json.dumps(d_dict)
    return HttpResponse(jsondata, content_type='application/json')


def load_names(request, modelname, query=None):
    if modelname == 'company':
        q_names = Company.objects.exclude(impevents=None
                                          ).values('id', 'name')

    elif modelname == 'reference':
        q_names = Reference.objects.values('id', 'name')
    elif modelname == 'country':
        q_names = Country.objects.values('id', 'name')
    elif modelname == 'tags':
        q_names = SustainabilityTag.objects.values('id', 'name')
    elif modelname == 'industry':
        q_comps = Company.objects.exclude(impevents=None
                                          ).values_list('activity_id', flat=True).distinct()
        q_names = ActivityCategory.objects.filter(id__in=q_comps
                                          ).values('id', 'name')

    elif modelname == 'company_all':
        q_names = Company.objects.values('id', 'name')
    else:
        return HttpResponse("/")

    if query:
        q_names = q_names.filter(name__icontains=query)
    data = json.dumps(list(q_names))
    return HttpResponse(data, content_type='application/json')


