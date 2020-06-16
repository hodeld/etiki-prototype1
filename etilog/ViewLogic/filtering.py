'''
Created on 26.8.2019

@author: daim
'''

from django.db.models import Q

from etilog.ViewLogic.queries import get_name
from etilog.fields import D_FORMAT
from etilog.models import ImpactEvent
import json
from datetime import datetime


def get_filterdict(request):
    reqdict = request.GET

    def set_value(fname):
        val_r = reqdict.get(fname, '')
        if val_r:
            return val_r
        else:
            return None

    def get_idlist(fname):
        id_strli = reqdict.get(fname, '')  # can be list ['']
        if id_strli:  #
            value_list = json.loads(id_strli)
        else:
            value_list = None
        return value_list

    value_dict = dict(reqdict)
    filter_dict = {}
    filter_name_dict = {}  # for setting visually values

    result_type = reqdict.get('result_type', 'table')
    field_names = ['date_from', 'date_to']
    for fname in field_names:
        val = set_value(fname)
        if val:
            filter_name_dict[fname] = val
            filter_dict[fname] = val

    field_names = ['company', 'reference', 'country', 'tags',
                   'sust_domain', 'sust_tendency',
                   'summary'
                   ]

    for fname in field_names:
        value_list = get_idlist(fname)
        if value_list:
            filter_dict[fname] = value_list  # for multiple: needs to be a list
            if fname in ['company', 'reference', 'tags', 'country',]:
                tag_list = []
                for inst_id in value_list:
                    tag_dict = get_name(inst_id, fname)

                    tag_dict.update({'category': fname})
                    tag_list.append(tag_dict)
                filter_name_dict[fname] = tag_list
            elif fname in ['summary']:
                tag_list = []
                for text_str in value_list:
                    tag_dict = {'category': fname,
                                'id': text_str,
                                'name': text_str,
                                }
                    tag_list.append(tag_dict)
                filter_name_dict[fname] = tag_list

            else:
                filter_name_dict[fname] = value_list  # buttons only need ids

    qs = filter_queryset(filter_dict)
    return qs, filter_name_dict, result_type


def filter_queryset(filter_dict):
    qs = ImpactEvent.objects.all()  # caching this does not help as will be filtered -> new hit in DB


    filter_method = {'country': f_country_idlist,
                     'reference': f_multiple,
                     'tags': f_multiple,
                     'company': f_multiple,
                     'sust_domain': f_multiple,
                     'sust_tendency': f_multiple,
                     'summary': filter_summary_list,
                     'date_from': f_date_range,
                     'date_to': f_date_range,
                     }

    field_name_d = {'tags': 'sust_tags',
                    'date_from': 'date_published',
                    'date_to': 'date_published', }

    lookup_d = {'date_from': 'gt',
                'date_to': 'lt', }

    for fname, val in filter_dict.items():
        lookup_expr = lookup_d.get(fname, None)
        fn = field_name_d.get(fname, fname)
        qs = filter_method[fname](qs, fn, val, lookup_expr)

    return qs


def f_country_idlist(qs, name, id_list, *args):
    if len(id_list) > 0:
        qs = qs.filter(Q(country__in=id_list)
                             | Q(company__country__in=id_list, country__isnull=True)
                             )  # "name__in = id_list
    else:
        qs = qs
    return qs


def f_multiple(qs, name, id_list, *args):
    if len(id_list) > 0:
        lookup = '__'.join([name, 'in'])
        qs = qs.filter(**{lookup: id_list})
    else:
        qs = qs
    return qs


def filter_summary_list(queryset, name, val_list, *args):
    lookup = '__'.join([name, 'icontains'])
    conditions = (Q(**{lookup: val_list[0]}))
    for string in val_list[1:]:
        conditions |= Q(**{lookup: string})
    qs = queryset.filter(conditions)
    return qs


def f_date_range(qs, name, value, lookup_expr, *args):
    django_format = '%Y-%m-%d'  # YYYY-MM-DD
    val = datetime.strptime(value, D_FORMAT).strftime(django_format)
    lookup = '__'.join([name, lookup_expr])
    qs = qs.filter(**{lookup: val})
    return qs





