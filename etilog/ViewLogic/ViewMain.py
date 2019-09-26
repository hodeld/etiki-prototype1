'''
Created on 26.8.2019

@author: daim
'''

from django.core.cache import cache #default cache in locmem
import json

from etilog.models import Country, Company, Reference

from etilog.ViewLogic.ViewDatetime import get_dateframe

def get_filterdict(request):
    reqdict =  request.GET 
    tag_dict ={}
    btn_dict = {}
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
        
    if len(reqdict) == 0: #first time GET
        filter_dict = None
    else:
        filter_dict = dict(reqdict)
        set_value('date_from')
        set_value('date_to')
                
        field_names = ['company', 'reference', 'country']
        modelarr = {'company': Company.objects.all(), 
                    'reference': Reference.objects.all(),
                     'country': Country.objects.all()
                     }
        
        for fname in field_names:
            id_list, id_str = get_idlist(fname)
            filter_dict[fname] = id_str #needs to be a string in CharFilter
            if id_list:
                q = modelarr[fname]
                id_dict = {}
                for id_val in id_list:
                    idname_dict = {}
                    id_int = int(id_val)
                    ele = q.get(id = id_int)
                    name_s = ele.name
                    idname_dict['id'] = id_int
                    idname_dict['name'] = name_s
                    id_dict[id_int] = idname_dict
                    
                    
                tag_dict[fname] = id_dict
        field_names = ['sust_domain', 'sust_tendency']
        
        for fname in field_names:
            id_list, id_str = get_idlist(fname)
            filter_dict[fname] = id_list #for multiple: needs to be a list
            btn_dict[fname] = id_list

    js_tag_dict = json.dumps(tag_dict)
    js_btn_dict = json.dumps(btn_dict)
    
               
    return filter_dict, js_tag_dict, js_btn_dict

def set_cache(name, value, request, timeout = 3600):
    key_name = str(request.user.id) + name
    cache.set(key_name, value, timeout)

def get_cache(name, request):
    key_name = str(request.user.id) + name
    value = cache.get(key_name, None)
    return value