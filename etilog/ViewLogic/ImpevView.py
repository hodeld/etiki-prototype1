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
    filt = ImpevOverviewFilter(filter_dict, queryset=q_ie)
    q = filt.qs

    cnt_ies, cnt_comp = count_qs(q)  # one query too much
    if cnt_ies > limit_filt:
        last_ie = q[limit_filt]
        dt = last_ie.date_published
        q = q.filter(date_published__gte=dt)

    # todo setting cache if withou new filter for different views
    # set_cache('q_ie', q_ie, request) #  _result_cache should be not None after evaluated
    # set_cache('cnt_ies', cnt_ies, request)
    # set_cache('cnt_comp', cnt_comp, request)
    q = prefetch_data(q)

    return q, filt, cnt_ies, cnt_comp


def overview_filter_results(request):
    key_totnr = 'cnties'
    cnt_tot = get_cache(key_totnr, request)
    if cnt_tot is None:
        cnt_tot = ImpactEvent.objects.all().count()
        set_cache(key_totnr, cnt_tot, request)

    filter_dict, filter_name_dict, result_type = get_filterdict(request)
    filt_data_json = json.dumps(filter_name_dict)
    if request.user.is_authenticated:
        limit_filt = 1000
        Table = ImpEvTablePrivat
    else:
        limit_filt = 50
        Table = ImpEvTable

    q_ov, filt, cnt_ies, cnt_comp = get_overview_qs(request, filter_dict, limit_filt)
    msg_results, msg_count = overview_message(cnt_ies, cnt_comp, cnt_tot, limit_filt)
    d_dict = {}

    if result_type == 'count':
        d_dict['result_type'] = result_type
        d_dict['msg_count'] = msg_count
        return d_dict

    elif result_type == 'table':

        table = Table(q_ov)
        RequestConfig(request, paginate=False).configure(table)
        rend_table = render_to_string('etilog/impev_table/impactevents_overview_table.html',
                                      {'table': table, }
                                      )
        d_dict['result_type'] = 'table'
        d_dict['table_data'] = rend_table

    # elif result_type == 'ie_detail':
    # takes about .5 of 1s seconds to load! (when 200 loaded) -> better load them indiv.
        ie_details = load_ie_details(q_ov)
        d_dict['ie_details'] = ie_details
    # elif result_type == 'companies':
        comp_details, comp_ratings = get_comp_details(q_ov)

        rend_comp = render_to_string('etilog/impev_company/company_show_each.html',
                                     {'comp_details': comp_details,}
                                     )
        d_dict['comp_ratings'] = comp_ratings
        d_dict['comp_details'] = rend_comp


    d_dict['message'] = msg_results

    d_dict['filter_dict'] = filt_data_json
    d_dict['ie_count'] = cnt_ies
    d_dict['company_count'] = cnt_comp

    return d_dict, filt


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