'''
Created on 26.8.2019

@author: daim
'''

from threading import Thread
from django.db.models import Count, Q, Sum

from etilog.ViewLogic.queries import get_name


def get_filterdict(request):
    reqdict = request.GET

    def set_value(keyname):
        filter_dict[keyname] = reqdict.get(keyname, '')

    def get_idlist(fname):
        id_strli = filter_dict.get(fname, [''])  # can be list ['']
        id_str = id_strli[0]  # ','.join(id_list)

        if len(id_str) > 0:  #
            id_list = id_str.split(',')
        else:
            id_list = None
        return id_list, id_str

    filter_dict = dict(reqdict)
    filter_name_dict = {}  # for setting visually values
    set_value('date_from')
    set_value('date_to')

    result_type = reqdict.get('result_type', 'table')
    #filter_dict.pop('result_type', None)

    field_names = []

    for fname in field_names:
        id_list, id_str = get_idlist(fname)
        filter_dict[fname] = id_str  # needs to be a string in CharFilter

    field_names = ['company', 'reference', 'country', 'sust_domain', 'sust_tendency', 'tags']

    for fname in field_names:
        id_list, id_str = get_idlist(fname)
        filter_dict[fname] = id_list  # for multiple: needs to be a list
        if id_list:  # and fname in ['company', 'reference', 'sust_tendency', 'tags']:
            if fname in ['company', 'reference', 'tags', 'country']:
                tag_list = []
                for inst_id in id_list:
                    tag_dict = get_name(inst_id, fname)
                    tag_dict.update({'category': fname})
                    tag_list.append(tag_dict)
                filter_name_dict[fname] = tag_list
            else:
                filter_name_dict[fname] = id_list  # buttons only need ids

    field_names = ['summary', ]
    for fname in field_names:
        text_str_li = filter_dict.get(fname, [''])  # can be list ['']
        text_str = text_str_li[0]
        filter_dict[fname] = text_str

    return filter_dict, filter_name_dict, result_type

