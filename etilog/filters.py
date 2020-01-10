'''
Created on 2.8.2019

@author: daim
'''
#fjango
from django.db.models import Q

#filter
from django_filters import FilterSet, DateFilter, CharFilter, ModelMultipleChoiceFilter

#models
from etilog.models import (Company, ImpactEvent, SustainabilityDomain, Reference, 
                            SustainabilityTendency, SustainabilityTag, Country
                            )
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
                           label = 'Date from')
    date_to = DateFilter(field_name = 'date_published',
                         lookup_expr='lt',
                         label = 'Date to')
    
    #todo (evtl needed): handling error messages needed
    company = ModelMultipleChoiceFilter(field_name = 'company', #ModelMultiple... -> accepts list
                         label = 'Company',
                         queryset=Company.objects.all())
    reference = ModelMultipleChoiceFilter(field_name = 'reference',
                           label = 'Where was it published',
                         queryset=Reference.objects.all())
    country = ModelMultipleChoiceFilter(field_name = 'country_display', #can be country
                         label = 'Country',
                         queryset= Country.objects.all(),
                         method = 'filter_country_idlist')
    summary = CharFilter(field_name = 'summary', 
                         label = 'Text only',
                         lookup_expr='icontains')
    
    tags = ModelMultipleChoiceFilter(field_name = 'sust_tags',
                         label = 'Topics',
                         queryset=SustainabilityTag.objects.all())
    
    sust_domain = ModelMultipleChoiceFilter(field_name = 'sust_domain', #ModelMultiple... -> accepts list
                         label = '',
                         queryset=SustainabilityDomain.objects.all()) 
    sust_tendency = ModelMultipleChoiceFilter(field_name = 'sust_tendency', #ModelMultiple... -> accepts list
                         label = '',
                         queryset=SustainabilityTendency.objects.all())
    
    def filter_country_idlist(self,queryset, name, value):
        #id_list = list(value.split(',')) #1,2,4"
        id_list = value
        if len(id_list) > 0:
            qs = queryset.filter(Q(country__in = id_list)
                                 | Q(company__country__in = id_list, country__isnull = True)
                                 )  #"name__in = id_list
        else:
            qs = queryset
        return qs

    class Meta:
        model = ImpactEvent
        fields = ['date_from', 'date_to', 'company', 'country', 'reference', 'sust_domain', 'summary']
        form = ImpevOverviewFForm
 
