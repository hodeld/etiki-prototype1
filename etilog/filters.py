'''
Created on 2.8.2019

@author: daim
'''
#fjango
from django.db.models import Q

#filter
from django_filters import FilterSet, DateFilter, CharFilter, ModelMultipleChoiceFilter
from django_filters import MultipleChoiceFilter

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
    
    #company, reference, country could be done like sust_domain -> but handling error messages needed
    company = CharFilter(field_name = 'company',
                         method = 'filter_idlist')
    reference = CharFilter(field_name = 'reference',
                           label = 'Where was it published',
                         method = 'filter_idlist')
    country = CharFilter(field_name = 'country_display', #can be country
                         label = 'Country',
                         method = 'filter_country_idlist')
    sust_domain = ModelMultipleChoiceFilter(field_name = 'sust_category__sust_domain', #ModelMultiple... -> accepts list
                         label = '',
                         queryset=SustainabilityDomain.objects.all()) #any queryset

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
                                 | Q(company__country__in = id_list, country__isnull = True)
                                 )  #"name__in = id_list
        else:
            qs = queryset
        return qs

    def filter_sust_domains(self,queryset, name, value):
        pass
        
                            
    
    class Meta:
        model = ImpactEvent
        fields = ['date_from', 'date_to', 'company', 'country', 'reference', 'sust_domain', 'sust_category']
        form = ImpevOverviewFForm
 
