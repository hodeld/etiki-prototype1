'''
Created on 2.8.2019

@author: daim
'''
#fjango
from django import forms
from django.db.models import OuterRef
from django.urls import reverse_lazy
import json
#filter
from django_filters import FilterSet, DateFromToRangeFilter, DateFilter
#form
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit


#models
from .models import Source, Company, ImpactEvent, SustainabilityDomain, Reference
#forms
from .forms import ImpevOverviewFForm


    
DT_FORMAT = '%Y-%m-%d %H:%M:%S'
#D_FORMAT = '%Y-%m-%d'
D_FORMAT = '%d.%m.%Y'
D_FORMAT_EXTRA = '%d.%m.%y'
D_YEARFORMAT = '%Y'

domains = [('0', '----')]
domains.extend(list(SustainabilityDomain.objects.values_list('id', 'name')))

CHOICES = domains



class ImpevOverviewFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super(ImpevOverviewFilter, self).__init__(*args, **kwargs)
        
    date_from = DateFilter(field_name = 'date_published',
                           lookup_expr='gt',
                           label = 'from')
    date_to = DateFilter(field_name = 'date_published',
                         lookup_expr='lt',
                         label = 'to')

    
    
    class Meta:
        model = ImpactEvent
        fields = [ 'date_from', 'date_to',]
        form = ImpevOverviewFForm
 
class ImpevOverviewFilter2(FilterSet):
    
    class Meta:
        model = ImpactEvent

        exclude = [ '', ]
        #form = ImpevOverviewFForm        
                  
