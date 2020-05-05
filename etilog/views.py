from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import logout
import json

# from 3rd apps

# models

from etilog.models import (ImpactEvent, Company, Reference, Country,
                           SustainabilityTag, FrequentAskedQuestions)

# tables
# forms
from .forms import (NewSource, SearchForm, FreetextForm, TopicForm, TendencyLegendeDiv,
                    OverviewFiltHeaderForm
                    )
# forms
from .filters import ImpevOverviewFilter

# viewlogic
from etilog.ViewLogic.ViewImportDB import parse_xcl
from etilog.ViewLogic.ImpevView import (overview_filter_results, load_ie_details)

from etilog.ViewLogic.ViewExport import exp_csv_nlp, exp_csv_basedata, extract_err_file
from etilog.ViewLogic.ViewDatetime import get_now

from etilog.ViewLogic.ViewUpdateDB import update_internal


def entry_mask(request):
    return render(request, 'etilog/entrymask/main.html', )


def overview_impevs(request, reqtype=None):

    landing = False

    if len(request.GET) == 0:  # firsttime
        filt = ImpevOverviewFilter({}, queryset=ImpactEvent.objects.none())  # needed, as should be shown imm.
        jsondata = json.dumps(False)  # False #Table(table_qs)
        landing = True

    else:
        d_dict, filt = overview_filter_results(request)
        jsondata = json.dumps(d_dict)
        if reqtype is None:  # load directly data
            return HttpResponse(jsondata, content_type='application/json')

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


def impact_event_show(request, ie_id):
    table_qs = ImpactEvent.objects.filter(id=ie_id)
    html_str = load_ie_details(table_qs, single_ie=True)  # same as in table
    ie = table_qs[0]

    return render(request, 'etilog/impev_show.html', {'ie_details': html_str,
                                                      'ie': ie
                                                      })


def export_csv_nlp(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    now = get_now()
    date_str = now.strftime('%Y%m%d')
    filename = 'impevs_nlp_' + date_str
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename
    response = exp_csv_nlp(response)

    return response


def export_csv_base(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    now = get_now()
    date_str = now.strftime('%Y%m%d')
    filename = 'base_nlp_' + date_str
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename
    response = exp_csv_basedata(response)

    return response


def export_csv_extr(request):
    response = HttpResponse(content_type='text/csv')
    now = get_now()
    date_str = now.strftime('%Y%m%d')
    filename = 'extracterr_' + date_str
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename
    response = extract_err_file(response)
    return response


@permission_required('etilog.impactevent')
def import_dbdata(request):  #
    parse_xcl()
    return HttpResponseRedirect(reverse('etilog:home'))


@csrf_exempt
def get_company_notused(request):
    if request.is_ajax():
        company_name = request.GET['company_name']
        company_id = Company.objects.get(name=company_name).id
        data = {'company_id': company_id, }
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


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





def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
    # Redirect to a success page.


def legal(request):
    return render(request, 'legal.html', )


def about(request):
    return render(request, 'etilog/about.html', )


def faq(request):
    faqs = FrequentAskedQuestions.objects.all().order_by('question')
    return render(request, 'etilog/faq.html', {'faqs': faqs})


def startinfo(request):
    if request.method == 'POST':
        form = NewSource(request.POST)
        if form.is_valid():
            form.save()
            print('valid', form.cleaned_data)
            message = 'you are helping creating a new platform, thank you!'
        else:
            message = 'oh, this did not work!'

    else:
        message = ''
    form = NewSource()
    return render(request, 'etilog/comingsoon.html', {'form': form,
                                                      'message': message
                                                      })


def update_db_internal(request):
    update_internal()
    return HttpResponseRedirect(reverse('etilog:home'))