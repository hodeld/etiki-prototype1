'''
Created on 26.8.2019

@author: daim
'''

from datetime import timedelta
from django.utils import timezone

from etilog.models import Country, SustainabilityCategory, SustainabilityDomain, SustainabilityTag

from etilog.ViewLogic.ViewDatetime import get_dateframe

def get_filterdict(request):
    reqdict =  request.GET 
    datef = False
    def set_value(keyname):
        filter_dict[keyname] = reqdict.get(keyname,'')
        
    if len(reqdict) == 0: #first time GET
        st, et = get_dateframe() #date as string '%d.%m.%Y'
        filter_dict = {'date_from': st, 'date_to': et} #needs to be correct format
        datef = True
    else:
        filter_dict = {}
        datef_str =  reqdict.get('i-datefilter', None) #string
        if datef_str:
            if datef_str == 'true':
                datef = True
                set_value('date_from')
                set_value('date_to')
                
    return filter_dict, datef