'''
Created on 26.8.2019

@author: daim
'''

from datetime import timedelta
from django.utils import timezone

from etilog.models import Country, SustainabilityCategory, SustainabilityDomain, SustainabilityTag

def get_dateframe():
    now = timezone.localtime()
    #et = now
    et = None

  
    yearsdelta = 2
    daysdelta = yearsdelta*365
    st_dt = now - timedelta(days=daysdelta)
    st = st_dt.strftime('%d.%m.%Y')
    
    return st, et

def get_now():
    now = timezone.localtime()
    
    return now