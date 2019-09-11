'''
Created on 2.8.2019

@author: daim
'''
#fjango
from django.db.models import Q
from django import forms
from django.db.models import OuterRef
from django.urls import reverse_lazy
import json
#filter
from django_filters import FilterSet, DateFilter, CharFilter
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

        
    date_from = DateFilter(field_name = 'date_published',
                           lookup_expr='gt',
                           label = 'from')
    date_to = DateFilter(field_name = 'date_published',
                         lookup_expr='lt',
                         label = 'to')
    company = CharFilter(field_name = 'company',
                         method = 'filter_idlist')
    country = CharFilter(field_name = 'country_display',
                         label = 'Country',
                         method = 'filter_country_idlist')

    def filter_idlist(self,queryset, name, value):
        #value = value.replace('[','') #comes as "['3',]"
        #value = value.replace(']','')
        id_list = list(value.split(',')) #1,2,4"
        if len(id_list) > 0:
            lookup = '__'.join([name, 'in'])   
            qs = queryset.filter(**{lookup: id_list}) #"name__in = id_list
        else:
            qs = queryset
        return qs
    
    def filter_country_idlist(self,queryset, name, value):
        id_list = list(value.split(',')) #1,2,4"
        if len(id_list) > 0:
            qs = queryset.filter(Q(country__in = id_list)
                                 | Q(company__country__in = id_list)
                                 )  #"name__in = id_list
        else:
            qs = queryset
        return qs

    
    
    class Meta:
        model = ImpactEvent
        fields = ['date_from', 'date_to', 'company', 'country', 'reference', ]
        form = ImpevOverviewFForm
 
