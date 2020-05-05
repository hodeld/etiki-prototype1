'''
Created on 26.8.2019

@author: daim
'''

from threading import Thread
from django.db.models import Count, Q, Sum

# models
from etilog.models import (Company, Reference, SustainabilityTag, SustainabilityDomain,
                           Country, SustainabilityTendency)
import unicodedata


def get_name(inst_id, modelname):
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
    name = mod.objects.values('id', 'name').get(id=inst_id)
    return name


# view queries
def query_comp_details(q_impev):
    def strip_accents(text):
        noacc = ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')
        nowhite = noacc.lower().replace(' ', '')
        return nowhite

    company_ids = q_impev.prefetch_related('company'
                                           ).values_list('company', flat=True).distinct()

    num_pos = Count('impevents', filter=Q(impevents__sust_tendency__impnr=1))
    num_neg = Count('impevents', filter=Q(impevents__sust_tendency__impnr=2))
    num_con = Count('impevents', filter=Q(impevents__sust_tendency__impnr=3))

    num_tot = Count('impevents')

    # q_comp = Company.objects.prefetch_related('impevents').filter(impevents__in = q_impev) #only counts nr of filtered impev

    # count all impev of filtered companies
    q_comp = Company.objects.prefetch_related('impevents__sust_tendency__impnr'
                                              ).filter(
        id__in=company_ids).annotate(
        num_pos=num_pos).annotate(
        num_neg=num_neg).annotate(
        num_con=num_con).annotate(
        num_tot=num_tot).annotate(
    )

    # list of dicts:
    comp_details = q_comp.values('pk', 'name', 'num_pos', 'num_neg', 'num_con',
                                 'num_tot',
                                 'domain')  # select_related('num_pos', 'num_neg', 'num_con'

    rating_dict = {}
    rating_list = list(comp_details)

    for co in comp_details:
        if co['domain'] == None:
            sname = strip_accents(str(co['name']))
            co['domain'] = sname + '.com'
        rating_dict[co['pk']] = co  # co as dict

    return comp_details, rating_list


def prefetch_data(qimpev):
    # after filter, before excuting
    q = qimpev.select_related('sust_domain', 'sust_tendency',
                              'sust_tendency',
                              'company__activity', 'company__country',
                              'country', 'reference',
                              ).prefetch_related('sust_tags')  # M2M
    # todo details: html, article_text article_title article_html

    # prefetch_related()
    return q


def count_qs(qimpev):
    ie_ids = qimpev.values_list('id', flat=True)  # .count()
    cnt_ies = len(ie_ids)
    cnt_comp = Company.objects.filter(impevents__in=ie_ids).distinct().count()

    vals = (cnt_ies, cnt_comp)
    return vals



