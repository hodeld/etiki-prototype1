from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

#from 3rd apps
from django_tables2 import RequestConfig

#models
from .models import ImpactEvent, Company, SustainabilityCategory, Reference, Country
from etilog.models import SustainabilityTag

#tables
from .tables import ImpEvTable
#forms
from .forms import NewImpactEvent, NewSource, CompanyForm, ReferenceForm, SearchForm, FreetextForm
#forms
from .filters import ImpevOverviewFilter

#viewlogic
from etilog.ViewLogic.ViewImportDB import parse_xcl
from etilog.ViewLogic.ViewMain import get_filterdict

#from etilog.ViewLogic.ViewAccessURL import parse_url

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
    #parse_url() -> to get pdfs / test
    
    filter_dict, js_tag_dict, js_btn_dict = get_filterdict(request) #hiddencompany
    limit_start = 21
    limit_filt = 50
    if  filter_dict:
        q_ie = ImpactEvent.objects.all()
        msg_base =  'shows %d filtered impact events'
    else:
        last_ies = ImpactEvent.objects.all().order_by('-updated_at')[:limit_start]
        dt = list(last_ies)[-1].updated_at
        q_ie = ImpactEvent.objects.filter(updated_at__gte = dt)
        msg_base = 'shows %d most recent added impact events'
    filt = ImpevOverviewFilter(filter_dict, queryset=q_ie) 
    table_qs =  filt.qs 
    cnt_ies = table_qs.count() #one query too much
    if cnt_ies > limit_filt:
        last_ies = table_qs.order_by('-date_published')[:limit_filt]
        dt = list(last_ies)[-1].date_published
        table_qs = table_qs.filter(date_published__gte = dt)
        msg_results = 'more than %d results! shows %d newest impact events' % (limit_filt, limit_filt)
    else:
        msg_results = msg_base % cnt_ies
         
    table = ImpEvTable(table_qs)
    table.order_by = '-date_published' #needed?
    #cnt_ies = filt.qs.count() 
    
    
    RequestConfig(request, paginate=False).configure(table) 
    
    searchform = SearchForm() #Filter ServerSide
    freetextform = FreetextForm()
    companies_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'company'})
    countries_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'country'})
    references_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'reference'})
    
    if filter_dict:
        return render(request, 'etilog/impactevents_overview_table.html', {'table': table,
                                                                           'message': msg_results})
        
    return render(request, 'etilog/impactevents_overview.html', {'table': table,
                                                                 'filter': filt,
                                                                 'searchform': searchform,
                                                                 'freetextform': freetextform,
                                                                 'companies_url': companies_url,
                                                                 'countries_url': countries_url,
                                                                 'references_url': references_url,
                                                                 'json_tag_dic': js_tag_dict,
                                                                 'json_btn_dic': js_btn_dict,
                                                                 'message': msg_results
                                                                 })

def import_dbdata(request):
    
    parse_xcl()
    return HttpResponseRedirect(reverse('etilog:home'))

def impact_event_create(request, impact_id = None):
    if request.method == 'POST':

        data_dict = request.POST.dict()
        company_names = ['company']
        data_dict = upd_datadict_company(company_names, data_dict)

        data_dict = upd_datadict_reference(data_dict)

        
        sust_tags_list = request.POST.getlist('sust_tags')
        data_dict ['sust_tags'] = sust_tags_list
        form = NewImpactEvent(data_dict)

        if form.is_valid():
            form.save() 
            print('valid', form.cleaned_data)
            message = 'Impact Event saved'
        else:
            message = form.errors
            form = NewImpactEvent(request.POST)
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
           
def add_foreignmodel(request, main_model, foreign_model):
    if request.POST:
        data_dict = request.POST.dict()
        if foreign_model == 'reference': 
            pass
            #reference = Reference.objects.get(name = data_dict['name'])
            #data_dict [foreign_model] = reference.id
            
        else: #company, owner, subsidiary, supplier, recipient
            comany_names = ['owner', 'subsidiary', 'supplier', 'recipient']
            data_dict = upd_datadict_company(comany_names, data_dict, m2m = True)

        id_field = 'id_' + foreign_model
        if foreign_model == 'reference': 
            form = ReferenceForm(data_dict)
        else:
            form = CompanyForm(data_dict)
        
        if form.is_valid():
            instance = form.save(commit = False) 
            instance.save()
            form.save_m2m() #due to many2many
            
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
    
        else:
            if foreign_model == 'reference': 
                form = ReferenceForm(request.POST)
            else:
                form = CompanyForm(request.POST)

    else:
        if foreign_model == 'reference': 
            form = ReferenceForm()
        
        else:
            form = CompanyForm()
    
    modelname = foreign_model[0].upper() + foreign_model[1:]

    
            #message = form.errors

    
    return render(request, 'etilog/addforeign_form.html', {'form' : form,
                                                           'modelname': modelname})

def upd_datadict_company(fieldlist, data_dict, m2m = False):
    for nam in fieldlist:
        if data_dict.get(nam):
            try:
                obj = Company.objects.get(name = data_dict.get(nam))
                if m2m:
                    comp_id = [obj.id] #needs to be a list
                else:
                    comp_id = obj.id
            except Company.DoesNotExist:
                comp_id = data_dict.get(nam) #send back wrong name
            data_dict[nam] = comp_id
    return data_dict

def upd_datadict_reference(data_dict):
    nam = 'reference'
    if data_dict.get(nam):
        try:
            obj = Reference.objects.get(name = data_dict.get(nam))
            obj_id = obj.id
        except Reference.DoesNotExist:
            obj_id = data_dict.get(nam) #send back wrong name
        data_dict[nam] = obj_id

    return data_dict
                
@csrf_exempt    
def get_company_notused(request):
    if request.is_ajax():
        company_name = request.GET['company_name']
        company_id = Company.objects.get(name = company_name).id
        data = {'company_id':company_id,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

def load_names(request, modelname):
    if modelname == 'company':
        q_names = Company.objects.values( 'id', 'name')
        #q_names = Company.objects.values_list( 'name', flat = True) #id
    elif modelname == 'reference':
        q_names = Reference.objects.values( 'id', 'name')
    elif modelname == 'country':
        q_names = Country.objects.values( 'id', 'name')
    else:
        return HttpResponse("/")
        
    #data = json.dumps(list(q_names))
    data = json.dumps(list(q_names))
    return HttpResponse(data, content_type='application/json')


#used in New IE Form     
def load_sustcategories_notusedanymore(request): #, 
    domain_id_str = request.GET.get('domainId')
    domain_id = int(domain_id_str)
    sustcategories = SustainabilityCategory.objects.filter(sust_domain = domain_id)

    
    return render(request, 'etilog/select_sustcateg.html', {'susts': sustcategories})       

#used in New IE Form  
def load_sust_tags(request): #, 
    tendency_id_str = request.GET.get('categoryId')
    lookup_dict = {}

    def lookup_many(name_s, val):
        id_list = [int(val)] #list
        lookup = '__'.join([name_s, 'in'])   
        lookup_dict[lookup] = id_list
    
    def lookup_one(name_s, val):
        f_id = int(val)
        lookup_dict[name_s] = f_id
    
    if len(tendency_id_str) > 0:
        lookup_one('sust_tendency', tendency_id_str)
    domain_id_str = request.GET.get('domainId')
    if len(domain_id_str) > 0:
        lookup_many('sust_domains', domain_id_str)
        
    sust_tags = SustainabilityTag.objects.filter(**lookup_dict).order_by('name')


    
    return render(request, 'etilog/select_sust_tags.html', {'tags': sust_tags})       