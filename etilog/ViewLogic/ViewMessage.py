'''
Created on 04.05.20

@author: daim
'''



def overview_message(cnt_ies, cnt_comp, cnt_tot, limit_filt):
    msg_impev = '<strong>%d Impact Events</strong>' % cnt_ies
    str_comp = 'Companies'
    if cnt_comp == 1:
        str_comp = 'Company'
        tip_str = '<br/>' + 'Tip: you can search for more than one Company!'
    else:
        tip_str = ''
    msg_company = '<strong>%d %s</strong>' % (cnt_comp, str_comp)

    if cnt_ies > limit_filt:
        msg_count = ' '.join(('show', msg_company, 'and', msg_impev, tip_str))
        msg_results = '''
        more than <strong>%d</strong> results! shows %d newest Impact Events       
        ''' % (
            limit_filt, limit_filt)

    else:
        msg_count = None
        msg_results = ' '.join(('shows', msg_company, 'and', msg_impev))

    msg_tot = ' '.join((msg_results, 'of %d in total' % cnt_tot, tip_str))

    return msg_tot, msg_count