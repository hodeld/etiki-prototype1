'''
Created on 04.05.20

@author: daim
'''


def overview_message(share_d, cnt_tot, limit_filt):
    cnt_ies = share_d['cnt_ies']
    cnt_comp = share_d['cnt_comp']
    msg_impev = '<strong class="text-uppercase">%d Impact Events</strong>' % cnt_ies
    str_comp = 'Companies'
    if cnt_comp == 1:
        str_comp = 'Company'
        tip_str = '<br/>' + 'Tip: you can compare companies by searching for another one!'
    else:
        tip_str = ''
    msg_company = '<strong class="text-uppercase">%d %s</strong>' % (cnt_comp, str_comp)

    if cnt_ies > limit_filt:

        msg_results = '''
        <strong class="text-uppercase">more than %d Impact Events!</strong> shows %d newest        
        ''' % (
            limit_filt, limit_filt)
        cnt_ies = limit_filt

    else:

        msg_results = ' '.join(('shows', msg_company, 'and', msg_impev))

    msg_tot = ' '.join((msg_results, 'of %d in total' % cnt_tot, tip_str))
    msg_count = ' '.join(('show', msg_company, 'and', msg_impev))

    info_dict = {}
    info_dict['message'] = msg_tot
    info_dict['msg_count'] = msg_count
    info_dict['ie_count'] = cnt_ies
    info_dict['company_count'] = cnt_comp
    return info_dict


