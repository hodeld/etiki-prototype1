'''
Created on 26.8.2019

@author: daim
'''

from django.core.cache import cache #default cache in locmem
from threading import Thread
from django.db.models import Count, Q

#models
from etilog.models import  (Company, Reference, SustainabilityTag, SustainabilityDomain,
                            Country, SustainabilityTendency)
import unicodedata


def get_filterdict(request):
    reqdict =  request.GET 
    def set_value(keyname):
        filter_dict[keyname] = reqdict.get(keyname,'')
    
    def get_idlist(fname):
        id_strli = filter_dict.get(fname, ['']) #can be list ['']
        id_str = id_strli[0] #','.join(id_list) 
        
        if len(id_str)> 0: #
            id_list = id_str.split(',')
        else:
            id_list = None           
        return id_list, id_str
    
    filter_dict = dict(reqdict)
    filter_name_dict = {} #for setting visually values
    set_value('date_from')
    set_value('date_to')
            
    field_names = [ ]

    for fname in field_names:
        id_list, id_str = get_idlist(fname)
        filter_dict[fname] = id_str #needs to be a string in CharFilter
                
                
    field_names = ['company', 'reference', 'country', 'sust_domain', 'sust_tendency', 'tags']
    
    for fname in field_names:
        id_list, id_str = get_idlist(fname)
        filter_dict[fname] = id_list #for multiple: needs to be a list
        if id_list: # and fname in ['company', 'reference', 'sust_tendency', 'tags']:
            if fname in ['company', 'reference', 'tags', 'country' ]:
                tag_list = []
                for inst_id in id_list:
                    tag_tupple = get_name (inst_id, fname)
                    tag_list.append(tag_tupple)
                filter_name_dict[fname] = tag_list
            else:
                filter_name_dict[fname] = id_list #buttons only need ids
    
    field_names = ['summary', ]
    for fname in field_names:
        text_str_li = filter_dict.get(fname, ['']) #can be list ['']
        text_str = text_str_li[0]
        filter_dict[fname] =  text_str
    
               
    return filter_dict, filter_name_dict

def get_name (inst_id, modelname):
    if modelname == 'company':
        mod = Company
    elif modelname == 'reference':
        mod = Reference
    elif modelname == 'country':
        mod = Country
    elif modelname == 'tags':
        mod = SustainabilityTag
    elif modelname == 'sust_domain':
        mod = SustainabilityDomain
    elif modelname == 'sust_tendency':
        mod = SustainabilityTendency
    else:
        return ''
    name = mod.objects.values( 'id', 'name').get(id = inst_id)
    return name

#view queries
def query_comp_details(q_impev):
    def strip_accents(text):        
        noacc =  ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')
        nowhite = noacc.lower().replace(' ', '') 
        return nowhite

    company_ids = q_impev.prefetch_related('company'
                            ).values_list('company', flat=True).distinct()
    
    num_pos = Count('impevents', filter=Q(impevents__sust_tendency__impnr=1)) 
    num_neg = Count('impevents', filter=Q(impevents__sust_tendency__impnr=2))
    num_con = Count('impevents', filter=Q(impevents__sust_tendency__impnr=3))  
    
    #q_comp = Company.objects.prefetch_related('impevents').filter(impevents__in = q_impev) #only counts nr of filtered impev
    
    #count all impev of filtered companies
    q_comp = Company.objects.prefetch_related('impevents__sust_tendency__impnr'
                            ).filter(
                            id__in = company_ids).annotate(
                                    num_pos=num_pos).annotate(
                                    num_neg=num_neg).annotate(
                                    num_con=num_con).annotate(
                                        )
    
    
    #list of dicts:   
    comp_details = q_comp.values('pk', 'name', 'num_pos', 'num_neg', 'num_con', 'domain') #  select_related('num_pos', 'num_neg', 'num_con'
    
    rating_dict = {}
    rating_list = list(comp_details)
    
    for co in comp_details:
        if co['domain'] == None:
            sname = strip_accents(str(co['name']))   
            co['domain'] = sname + '.com'
        rating_dict[co['pk']] = co #co as dict

        
                                    
    return comp_details, rating_list

def prefetch_data(qimpev):
    #after filter, before excuting
    q = qimpev.select_related('sust_domain', 'sust_tendency',
                            'sust_tendency', 
                           'company__activity', 'company__country',  
                   'country',   'reference',
        ).prefetch_related('sust_tags') #M2M
    #todo details: html, article_text article_title article_html
    
    #prefetch_related()
    return q
    
  

    
def set_cache(name, value, request, timeout = 3600):
    key_name = str(request.user.id) + name
    cache.set(key_name, value, timeout)

def get_cache(name, request):
    key_name = str(request.user.id) + name
    value = cache.get(key_name, None)
    return value

def postpone(function): #connection needs to be closed in function if db connection
    def decorator(*args, **kwargs):
        t = Thread(target = function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator     