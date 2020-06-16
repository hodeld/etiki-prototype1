'''
Created on 26.8.2019

@author: daim
'''

from threading import Thread
from django.db.models import Count, Q, Sum

from etilog.ViewLogic.queries import get_name
import json

def get_filterdict(request):
    reqdict = request.GET

    def set_value(keyname):
        filter_dict[keyname] = reqdict.get(keyname, '')

    def get_idlist(fname):
        id_strli = filter_dict.get(fname, [''])  # can be list ['']
        id_str = id_strli[0]  # ','.join(id_list)

        if len(id_str) > 0:  #
            value_list = json.loads(id_str)
        else:
            value_list = None
        return value_list

    filter_dict = dict(reqdict)
    filter_name_dict = {}  # for setting visually values
    set_value('date_from')
    set_value('date_to')

    result_type = reqdict.get('result_type', 'table')
    #filter_dict.pop('result_type', None)


    field_names = ['company', 'reference', 'country', 'tags',
                   'sust_domain', 'sust_tendency',
                   'summary'
                   ]

    for fname in field_names:
        value_list = get_idlist(fname)
        filter_dict[fname] = value_list  # for multiple: needs to be a list
        if value_list:  # and fname in ['company', 'reference', 'sust_tendency', 'tags']:
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
                filter_dict[fname] = ','.join(value_list)

            else:
                filter_name_dict[fname] = value_list  # buttons only need ids

    return filter_dict, filter_name_dict, result_type

