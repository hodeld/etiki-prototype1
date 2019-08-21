from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

#from 3rd apps
from django_tables2 import RequestConfig

#models
from .models import ImpactEvent, Company, SustainabilityCategory, Reference
#tables
from .tables import ImpEvTable
#forms
from .forms import NewImpactEvent, NewSource, CompanyForm, ReferenceForm

#viewlogic
from etilog.ViewLogic.ViewImportDB import parse_xcl
from etilog.models import SustainabilityTag

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

def impact_event_create(request, impact_id = None):
    if request.method == 'POST':

        data_dict = request.POST.dict()
        company = Company.objects.get(name = data_dict['company'])
        reference = Reference.objects.get(name = data_dict['reference'])
        data_dict ['company'] = company.id
        data_dict ['reference'] = reference.id
        sust_tags_list = request.POST.getlist('sust_tags')
        data_dict ['sust_tags'] = sust_tags_list
        form = NewImpactEvent(data_dict)

        if form.is_valid():
            form.save() 
            print('valid', form.cleaned_data)
            message = 'Impact Event saved'
        else:
            message = form.errors
            return render(request, 'etilog/newimpactevent.html', {'form': form,
                                                          'message': message,
                                                             })
    
    else:
        message = ''
    
    if impact_id:
        init_data = {}
        impev = ImpactEvent.objects.get(id = impact_id)
        init_data ['company'] = impev.company.name
        init_data ['sust_domain'] = impev.sust_category.sust_domain.id
        init_data ['sust_category'] = impev.sust_category.id
        init_data ['sust_tags'] = list(impev.sust_tags.all())
        init_data ['summary'] = impev.summary
        
        form = NewImpactEvent(initial = init_data)
    else:
        form = NewImpactEvent()
    
    return render(request, 'etilog/newimpactevent.html', {'form': form,
                                                          'message': message,
                                                             })
def impact_event_copy(request):
    if request.method == 'POST':

        data_dict = request.POST.dict()
        company = Company.objects.get(name = data_dict['company'])
        reference = Reference.objects.get(name = data_dict['reference'])
        data_dict ['company'] = company.id
        data_dict ['reference'] = reference.id
        sust_tags_list = request.POST.getlist('sust_tags')
        data_dict ['sust_tags'] = sust_tags_list
        form = NewImpactEvent(data_dict)

        if form.is_valid():
            form.save() 
            print('valid', form.cleaned_data)
            message = 'Impact Event saved'
        else:
            message = form.errors
            return render(request, 'etilog/newimpactevent.html', {'form': form,
                                                          'message': message,
                                                             })
    
    else:
        message = ''
 
    form = NewImpactEvent()
    
    return render(request, 'etilog/newimpactevent.html', {'form': form,
                                                          'message': message,
                                                             })
           
def add_foreignmodel(request, main_model, foreign_model):
    if foreign_model == 'company':        
        form = CompanyForm(request.POST or None)
        id_field = 'id_company'
        modelname = 'Company'
    elif foreign_model == 'reference': 
        form = ReferenceForm(request.POST or None)
        id_field = 'id_reference'
        modelname = 'Reference'
    else:
        modelname = 'Company'
        form = CompanyForm(request.POST or None)
            
    if form.is_valid():
        instance = form.save()

        ## Change the value of the "#id_company". This is the element id in the form
        
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
    
    return render(request, 'etilog/addforeign_form.html', {'form' : form,
                                                           'modelname': modelname})

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

def load_sust_tags(request): #, 
    category_id_str = request.GET.get('categoryId')
    category_id = int(category_id_str)
    sust_tags = SustainabilityTag.objects.filter(Q(sust_categories = category_id)
                                                 |Q(sust_categories__isnull = True)
                                                 ).order_by('name')

    
    return render(request, 'etilog/select_sust_tags.html', {'tags': sust_tags})       