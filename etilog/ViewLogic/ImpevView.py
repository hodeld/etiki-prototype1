'''
Created on 26.8.2019

@author: daim
'''
import json

from django.template.loader import render_to_string
from django_tables2 import RequestConfig

from etilog.ViewLogic.ViewMessage import overview_message
from etilog.ViewLogic.caching import (get_cache, set_cache)
from etilog.ViewLogic.filtering import get_filterdict
from etilog.ViewLogic.queries import count_qs, prefetch_data, query_comp_details
from etilog.filters import ImpevOverviewFilter
from etilog.models import (ImpactEvent, Company, Reference, Country,
                           SustainabilityTag, FrequentAskedQuestions)
from etilog.tables import ImpEvTablePrivat, ImpEvTable, ImpEvDetails


def get_overview_qs(request, filter_dict, limit_filt):
    q_ie = ImpactEvent.objects.all() #  caching this does not help as will be filtered -> new hit in DB
    filt = ImpevOverviewFilter(filter_dict, queryset=q_ie) # needed first time for template
    q = filt.qs

    cnt_ies, cnt_comp = count_qs(q)  # one query too much
    if cnt_ies > limit_filt:
        last_ie = q[limit_filt]
        dt = last_ie.date_published
        q = q.filter(date_published__gte=dt)

    q = prefetch_data(q)
    cache_d = {
        'q_ie': q,
        'cnt_ies': cnt_ies,
        'cnt_comp': cnt_comp,
    }
    set_cache('impev_data', cache_d, request) #  _result_cache should be not None after evaluated

    return q, filt, cnt_ies, cnt_comp


def filter_results(request):

    key_totnr = 'tot_ies'
    cnt_tot = get_cache(key_totnr, request)
    if cnt_tot is None:
        cnt_tot = ImpactEvent.objects.all().count()
        set_cache(key_totnr, cnt_tot, request)

    filter_dict, filter_name_dict, result_type = get_filterdict(request)
    filt_data_json = json.dumps(filter_name_dict) # for setting filter visually
    if request.user.is_authenticated:
        limit_filt = 1000
    else:
        limit_filt = 50

    q_ov, filt, cnt_ies, cnt_comp = get_overview_qs(request, filter_dict, limit_filt)
    info_dict = overview_message(cnt_ies, cnt_comp, cnt_tot, limit_filt)

    d_dict = {}
    d_dict['filter_dict'] = filt_data_json # for setting filter visually

    set_cache('info_dict', info_dict, request)

    get_results(request, d_dict)
    return d_dict, filt


def get_results(request, d_dict):
    result_type = request.GET.get('result_type', 'count') # first time always count
    d_dict['result_type'] = result_type

    if result_type == 'count':
        info_dict = get_cache('info_dict', request)
        d_dict.update(info_dict)
        return

    dispatch_result = {

        'table': get_impev_table,
        'company': get_impev_company,
        'ie_detail': get_impev_detail,
        # 'count': get_impev_count,
    }
    dispatch_result[result_type](request, d_dict)


def get_impev_table(request, d_dict):
    impev_data = get_cache('impev_data', request)
    q = impev_data['q_ie']
    if request.user.is_authenticated:
        table_obj = ImpEvTablePrivat
    else:
        table_obj = ImpEvTable
    table = table_obj(q)
    RequestConfig(request, paginate=False).configure(table)
    rend_table = render_to_string('etilog/impev_table/impactevents_overview_table.html',
                                  {'table': table, }
                                  )
    d_dict['table_data'] = rend_table


def get_impev_company(request, d_dict):
    impev_data = get_cache('impev_data', request)
    q = impev_data['q_ie']
    comp_details, comp_ratings = get_comp_details(q)

    rend_comp = render_to_string('etilog/impev_company/company_show_each.html',
                                 {'comp_details': comp_details, }
                                 )
    d_dict['comp_ratings'] = comp_ratings
    d_dict['comp_details'] = rend_comp


def get_impev_detail(request, d_dict):
    impev_data = get_cache('impev_data', request)
    q = impev_data['q_ie']
    ie_details = load_ie_details(q)
    d_dict['ie_details'] = ie_details


def load_ie_details(qs, single_ie=False):
    ie_fields = ImpEvDetails(qs) # todo from cache
    ie_dt_dict = {}

    for row in ie_fields.paginated_rows:
        rec = row.record
        id_ie = rec.pk

        html_fields = render_to_string('etilog/impev_details/impev_show_fields.html', {'row': row,
                                                                         'rec': rec  # can be deleted
                                                                                       })

        if single_ie == True:
            return html_fields
        html_article = render_to_string('etilog/impev_details/impev_show_article.html', {'rec': rec
                                                                                         })

        html_header = render_to_string('etilog/impev_details/impev_show_article_hd.html', {'rec': rec
                                                                                           })
        ie_dt_dict[id_ie] = (html_fields, html_header, html_article)

    # data = json.dumps(list(q_names))
    data = json.dumps(ie_dt_dict)
    return data


def get_comp_details(q_impev):
    details, ratings = query_comp_details(q_impev)

    jsdata = json.dumps(ratings)
    return details, jsdata