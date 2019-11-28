from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout
from django.forms.models import model_to_dict
import json

#from 3rd apps
from django_tables2 import RequestConfig

#models
from .models import ImpactEvent, Company, SustainabilityCategory, Reference, Country
from etilog.models import SustainabilityTag

#tables
from .tables import ImpEvTable, ImpEvTablePrivat
#forms
from .forms import (ImpactEventForm, NewSource, CompanyForm, ReferenceForm, 
                    SearchForm, FreetextForm, TopicForm,
                    ImpEvShow)
#forms
from .filters import ImpevOverviewFilter

#viewlogic
from etilog.ViewLogic.ViewImportDB import parse_xcl
from etilog.ViewLogic.ViewMain import get_filterdict, set_cache, get_cache
from etilog.ViewLogic.ViewExport import exp_csv_nlp, exp_csv_basedata, extract_err_file
from etilog.ViewLogic.ViewDatetime import get_now

from etilog.ViewLogic.ViewAccessURL import parse_url, parse_url_all, extract_text_rpy

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
    form = NewSource() #for testing
    key_totnr = 'cnties'
    cnt_tot = get_cache(key_totnr, request)
    if cnt_tot == None:
        cnt_tot = ImpactEvent.objects.all().count()
    filter_dict = get_filterdict(request) #hiddencompany
    limit_start = 21
    
    if request.user.is_authenticated:
        limit_filt = 1000
        Table = ImpEvTablePrivat
    else:
        limit_filt = 50
        Table = ImpEvTable
        
    if  filter_dict:
        q_ie = ImpactEvent.objects.all()
        msg_base =  'shows %d filtered impact events'
    else: #newly loaded time on site
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
         
    table = Table(table_qs)
    table.order_by = '-date_published' #needed?
    #cnt_ies = filt.qs.count() 
    
    
    RequestConfig(request, paginate=False).configure(table) 
    
    searchform = SearchForm() #Filter ServerSide
    topicform = TopicForm()
    freetextform = FreetextForm()
    companies_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'company'})
    countries_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'country'})
    references_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'reference'})
    tags_url = reverse_lazy('etilog:load_jsondata', kwargs={'modelname': 'tags'})
    
    msg_results = msg_results + ' of %d in total' % cnt_tot
    
    if filter_dict:
        d_dict = {}
        rend =  render_to_string( 'etilog/impactevents_overview_table.html', {'table': table,
                                                                           }
                                                                           )
        d_dict['data'] = rend
        d_dict['message'] = msg_results
        return HttpResponse(json.dumps(d_dict), content_type='application/json')

                                                                           
      
        
    return render(request, 'etilog/impactevents_overview.html', {'table': table,
                                                                 'filter': filt,
                                                                 'searchform': searchform,
                                                                 'topicform': topicform,
                                                                 'freetextform': freetextform,
                                                                 'companies_url': companies_url,
                                                                 'countries_url': countries_url,
                                                                 'references_url': references_url,
                                                                 'tags_url': tags_url,
                                                                 'message': msg_results,
                                                                 'form': form
                                                                 })

def impact_event_show(request, ie_id):
    if request.user.is_authenticated:
        limit_filt = 1000
        Table = ImpEvTablePrivat
    else:
        limit_filt = 50
        Table = ImpEvTable
    table_qs = ImpactEvent.objects.filter(id = ie_id)   
    table = Table(table_qs)
    row = table.paginated_rows[0]
    items = row.items
    ie = ImpactEvent.objects.get(id = ie_id)
    ie_dict = model_to_dict(ie)
    
    return render(request, 'etilog/impev_show.html', {'ie_dict': ie_dict,
                                                      'items': items})

    
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
    filename ='extracterr_' + date_str
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename
    response = extract_err_file(response)
    return response  
    
       
@permission_required('etilog.impactevent')   
def import_dbdata(request):#
    parse_xcl()
    return HttpResponseRedirect(reverse('etilog:home'))

@permission_required('etilog.impactevent')   
def extract_text(request, ie_id = None):

    try:
        ie = ImpactEvent.objects.get(id = ie_id)
    except ImpactEvent.DoesNotExist:
        return HttpResponseRedirect(reverse('etilog:home'))           
    parse_url(ie) 
        
    return HttpResponseRedirect(reverse('etilog:home'))

@permission_required('etilog.impactevent')   
def extract_text_all(request):
    parse_url_all()
    return HttpResponseRedirect(reverse('etilog:home'))
        
        
    
@permission_required('etilog.impactevent')   
def extract_text_from_url(request):
    url = request.GET.get('sourceurl')
    d_dict = {}
    if url is not '':
        save_article, parse_res, article = extract_text_rpy(url)
    else:
        save_article = False
    if save_article == True:
        msg = 'extracted'
        text_str, stitle, sdate, html_simple = article
        d_dict['is_valid'] = 'true'
        d_dict['stext'] = text_str
        d_dict['stitle'] = stitle
        d_dict['sdate'] = sdate
        d_dict['shtml'] = html_simple

    else:
        msg = 'not extracted'
    d_dict['parse_res'] = parse_res
    d_dict['message'] = msg
    return HttpResponse(json.dumps(d_dict), content_type='application/json')



@permission_required('etilog.impactevent') 
def impact_event_create(request, ie_id = None):
    if ie_id:
        ietype = 'copy'
    else:
        ietype = 'new'
    response = impact_event_change(request, ietype = ietype, ie_id = ie_id)
    return response 
    
@permission_required('etilog.impactevent') 
def impact_event_update(request, ietype = 'new', ie_id = None):
    ietype = 'update'
    response = impact_event_change(request, ietype = ietype, ie_id = ie_id)
    return response 
    
def impact_event_change(request, ietype = 'new', ie_id = None):
    shtml = ''
    if request.method == 'POST':
        data_dict = get_ie_form_data(request)
        if ietype == 'update':
            message = 'Impact Event updated' 
            ie = ImpactEvent.objects.get(id = ie_id)
            form = ImpactEventForm(data_dict, instance = ie) #if ie = None
        else: #new / new from copy
            message = 'Impact Event saved' 
            form = ImpactEventForm(data_dict)
            
            
        to_json = {}
        if form.is_valid():
            newie = form.save()  
            newie_id = newie.pk          
            to_json['is_valid'] = 'true'
            to_json['message'] = message  
            update_url = reverse('etilog:impactevent_update', kwargs={'ie_id': newie_id} ) 
            to_json['upd_url'] = update_url           
                 
            
        else:
            message = form.errors.__html__() #html
            err_items = list(form.errors.keys())
            
            to_json['is_valid'] = 'false'
            to_json['err_items'] = err_items
            to_json['message'] = message
        return HttpResponse(json.dumps(to_json), content_type='application/json')
    
    else:
        message = ''
        init_data = {}
        if ietype == 'update':
            init_data = get_ie_init_data(ie_id, update = True)
            next_id = ImpactEvent.objects.filter(id__gt = ie_id).order_by('id').values_list('id', flat = True).first()
            next_id_url = reverse_lazy('etilog:impactevent_update', kwargs={'ie_id': next_id})
        else:
            if ietype == 'copy':
                init_data = get_ie_init_data(ie_id, update = False)
            #else:
                #form = ImpactEventForm()
            first_id = ImpactEvent.objects.order_by('id').values_list('id', flat = True).first()
            next_id_url = reverse_lazy('etilog:impactevent_update', kwargs={'ie_id': first_id})
        form = form = ImpactEventForm(initial = init_data)
        shtml = init_data.get('article_html', '') 
    return render(request, 'etilog/impev_upd_base.html', {'form': form, #for form.media
                                                          'message': message   ,
                                                          'next_id_url': next_id_url ,
                                                          'shtml': shtml                                                 
                                                            })
        
def get_ie_form_data(request):
    data_dict = request.POST.dict()
    company_names = ['company']
    data_dict = upd_datadict_company(company_names, data_dict)

    data_dict = upd_datadict_reference(data_dict)

    
    sust_tags_list = request.POST.getlist('sust_tags')
    data_dict ['sust_tags'] = sust_tags_list
    return data_dict

def get_ie_init_data(ie_id, update = False):
    init_data = {}
    impev = ImpactEvent.objects.get(id = ie_id)
    init_data ['company'] = impev.company.name
    init_data ['sust_domain'] = impev.sust_domain.id
    init_data ['sust_tendency'] = impev.sust_tendency.id
    init_data ['sust_tags'] = list(impev.sust_tags.all())
    init_data ['summary'] = impev.summary
    if update:
        init_data ['article_text'] = impev.article_text
        init_data ['article_title'] = impev.article_title
        init_data ['article_html'] = impev.article_html
        init_data ['result_parse_html'] = impev.result_parse_html
        init_data ['source_url'] = impev.source_url
        init_data ['date_published'] = impev.date_published
        init_data ['date_impact'] = impev.date_impact
        init_data ['date_text'] = impev.date_text
        init_data ['comment'] = impev.comment
        init_data ['reference'] = impev.reference.name
        
       
    #form = ImpactEventForm(initial = init_data)
    return init_data
    
    
@permission_required('etilog.impactevent')           
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
            
            #handles the result of the foreign model in the original one
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
    elif modelname == 'tags':
        q_names = SustainabilityTag.objects.values( 'id', 'name')
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

def logout_view(request): 
    logout(request)
    return HttpResponseRedirect(reverse('login'))
    # Redirect to a success page.
    