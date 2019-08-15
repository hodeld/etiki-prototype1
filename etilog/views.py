from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

#from 3rd apps
from django_tables2 import RequestConfig

#models
from .models import ImpactEvent, Company, SustainabilityCategory
#tables
from .tables import ImpEvTable
#forms
from .forms import NewImpactEvent, NewSource, CompanyForm

#viewlogic
from etilog.ViewLogic.ViewImportDB import parse_xcl

# Create your views here.
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

def overview_impevs(request):
    
    table = ImpEvTable(ImpactEvent.objects.all())
    #table.order_by = 'start'
    RequestConfig(request, paginate={'per_page': 20}).configure(table) 
    
    return render(request, 'etilog/impactevents_overview.html', {'table': table})

def import_dbdata(request):
    
    parse_xcl()
    return HttpResponseRedirect(reverse('etilog:home'))

def impact_event_create(request):
    if request.method == 'POST':

        data_dict = request.POST.dict()
        company = Company.objects.get(name = data_dict['company'])
        data_dict ['company'] = company.id
        data_dict['sust_category'] = 1
        form = NewImpactEvent(data_dict)

        if form.is_valid():
            form.save() 
            print('valid', form.cleaned_data)
            message = 'Impact Event saved'
        else:
            message = form.errors
    
    else:
        message = ''
 
    form = NewImpactEvent()
    
    return render(request, 'etilog/newimpactevent.html', {'form': form,
                                                          'message': message,
                                                             })
        
def company_create(request):
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        instance = form.save()

        ## Change the value of the "#id_company". This is the element id in the form
        
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_author");</script>' % (instance.pk, instance))
    
    return render(request, "company_form.html", {"form" : form})

@csrf_exempt    
def get_company_id(request):
    if request.is_ajax():
        company_name = request.GET['company_name']
        company_id = Company.objects.get(name = company_name).id
        data = {'company_id':company_id,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    
def load_sustcategories(request): #, 
    domain_id_str = request.GET.get('domainId')
    domain_id = int(domain_id_str)
    sustcategories = SustainabilityCategory.objects.filter(sust_domain = domain_id)

    
    return render(request, 'etilog/select_sustcateg.html', {'susts': sustcategories})       