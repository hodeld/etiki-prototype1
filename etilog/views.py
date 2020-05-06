from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
import json

# from 3rd apps

# models

from etilog.models import (ImpactEvent, Company, Reference, Country,
                           SustainabilityTag)

# tables
# forms
from .forms import (SearchForm, FreetextForm, TopicForm, TendencyLegendeDiv,
                    OverviewFiltHeaderForm
                    )

from .filters import ImpevOverviewFilter

from etilog.ViewLogic.ImpevView import get_results, filter_results


def overview_impevs(request, reqtype=None):

    landing = False

    if len(request.GET) == 0:  # firsttime
        filt = ImpevOverviewFilter({}, queryset=ImpactEvent.objects.none())  # needed, as should be shown imm.
        jsondata = json.dumps(False)  # False #Table(table_qs)
        landing = True

    else:
        d_dict, filt = filter_results(request)
        jsondata = json.dumps(d_dict)

    searchform = SearchForm()  # Filter ServerSide
    topicform = TopicForm()
    freetextform = FreetextForm()
    tendlegend = TendencyLegendeDiv()
    filtheader = OverviewFiltHeaderForm()

    companies_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'company'})
    countries_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'country'})
    references_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'reference'})
    tags_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'tags'})

    return render(request, 'etilog/overview.html', {
        'filter': filt,
        'filtheader': filtheader,
        'searchform': searchform,
        'topicform': topicform,
        'freetextform': freetextform,
        'tendlegend': tendlegend,
        'companies_url': companies_url,
        'countries_url': countries_url,
        'references_url': references_url,
        'tags_url': tags_url,
        'landing': landing,
        'jsondata': jsondata,
    })


def filter_impevs(request):
    d_dict, filt = filter_results(request)
    jsondata = json.dumps(d_dict)
    return HttpResponse(jsondata, content_type='application/json')


def get_result(request):
    d_dict = {}
    get_results(request, d_dict)
    jsondata = json.dumps(d_dict)
    return HttpResponse(jsondata, content_type='application/json')


def load_names(request, modelname):
    if modelname == 'company':
        q_names = Company.objects.exclude(impevents=None
                                          ).values('id', 'name')
    elif modelname == 'reference':
        q_names = Reference.objects.values('id', 'name')
    elif modelname == 'country':
        q_names = Country.objects.values('id', 'name')
    elif modelname == 'tags':
        q_names = SustainabilityTag.objects.values('id', 'name')
    else:
        return HttpResponse("/")

    data = json.dumps(list(q_names))
    return HttpResponse(data, content_type='application/json')


