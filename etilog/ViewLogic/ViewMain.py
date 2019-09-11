'''
Created on 26.8.2019

@author: daim
'''

from datetime import timedelta
from django.utils import timezone
import json

from etilog.models import Country, Company, Reference

from etilog.ViewLogic.ViewDatetime import get_dateframe

def get_filterdict(request):
    reqdict =  request.GET 
    datef_str = 'false'
    tag_dict ={}
    def set_value(keyname):
        filter_dict[keyname] = reqdict.get(keyname,'')
        
    if len(reqdict) == 0: #first time GET
        st, et = get_dateframe() #date as string '%d.%m.%Y'
        filter_dict = {'date_from': st, 'date_to': et} #needs to be correct format
        datef_str = 'true'
    else:
        filter_dict = dict(reqdict)
        datef_str =  reqdict.get('i-datefilter', None) #string
        if datef_str:
            if datef_str == 'true':
                set_value('date_from')
                set_value('date_to')
            else:
                datef_str = 'false'
                filter_dict['date_from'] = ''
                filter_dict['date_to'] = ''
                
        field_names = ['company', 'reference', 'country']
        modelarr = {'company': Company.objects.all(), 
                    'reference': Reference.objects.all(),
                     'country': Country.objects.all()
                     }
        
        for fname in field_names:
            id_strli = filter_dict.get(fname, ['']) #can be list ['']
            id_str = id_strli[0] #','.join(id_list) #needs to be a string in CharFilter
            
            filter_dict[fname] = id_str
            if len(id_str)> 0: #
                id_list = id_str.split(',')
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
    js_tag_dict = json.dumps(tag_dict)
               
    return filter_dict, datef_str, js_tag_dict