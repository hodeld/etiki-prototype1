'''
Created on 2.8.2019

@author: daim
'''
# fjango
from django.db.models import Q

# filter
from django_filters import FilterSet, DateFilter, CharFilter, ModelMultipleChoiceFilter, MultipleChoiceFilter

# models
from django_filters.fields import MultipleChoiceField

from etilog.models import (Company, ImpactEvent, SustainabilityDomain, Reference,
                           SustainabilityTendency, SustainabilityTag, Country
                           )
# forms
from .forms import ImpevOverviewFForm

DT_FORMAT = '%Y-%m-%d %H:%M:%S'
# D_FORMAT = '%Y-%m-%d'
D_FORMAT = '%d.%m.%Y'
D_FORMAT_EXTRA = '%d.%m.%y'
D_YEARFORMAT = '%Y'

domains = [('0', '----')]
domains.extend(list(SustainabilityDomain.objects.values_list('id', 'name')))

CHOICES = domains

class CharListFilter(CharFilter):
    pass

    #field_class = MultipleChoiceField










class ImpevOverviewFilter(FilterSet):
    date_from = DateFilter(field_name='date_published',
                           lookup_expr='gt',
                           label='Date from')
    date_to = DateFilter(field_name='date_published',
                         lookup_expr='lt',
                         label='Date to')

    company = ModelMultipleChoiceFilter(field_name='company',  # ModelMultiple... -> accepts list
                                        label='',
                                        queryset=Company.objects.all())
    reference = ModelMultipleChoiceFilter(field_name='reference',
                                          label='',
                                          queryset=Reference.objects.all())
    country = ModelMultipleChoiceFilter(field_name='country',  # can be country
                                        label='',
                                        queryset=Country.objects.all(),
                                        method='filter_country_idlist')
    summary = CharListFilter(field_name='sust_tags',  # can be country
                                         label='',
                                         #queryset=Country.objects.all(),
                                        method='filter_summary_list'
                             )
    summary2 = ModelMultipleChoiceFilter(field_name='sust_tags',  # can be country
                                        label='',
                                        queryset=Country.objects.all(),

                                         )

    tags = ModelMultipleChoiceFilter(field_name='sust_domain',
                                     label='',
                                     queryset=SustainabilityTag.objects.all())

    sust_domain = ModelMultipleChoiceFilter(field_name='sust_domain',  # ModelMultiple... -> accepts list
                                            label='',
                                            queryset=SustainabilityDomain.objects.all())
    sust_tendency = ModelMultipleChoiceFilter(field_name='sust_tendency',  # ModelMultiple... -> accepts list
                                              label='',
                                              queryset=SustainabilityTendency.objects.all())

    def filter_country_idlist(self, queryset, name, value):
        id_list = value
        if len(id_list) > 0:
            qs = queryset.filter(Q(country__in=id_list)
                                 | Q(company__country__in=id_list, country__isnull=True)
                                 )  # "name__in = id_list
        else:
            qs = queryset
        return qs

    def filter_summary_list(self, queryset, name, value):

        if len(value) > 0:
            val_list = value.split(',')  # prepared in filtering
            lookup = '__'.join(['summary', 'icontains'])
            conditions = (Q(**{lookup: val_list[0]}))
            for string in val_list[1:]:
                conditions |= Q(**{lookup: string})
            qs = queryset.filter(conditions)
        else:
            qs = queryset
        return qs

    class Meta:
        model = ImpactEvent
        fields = ['date_from', 'date_to', 'company', 'country', 'reference', 'sust_domain']
        form = ImpevOverviewFForm
