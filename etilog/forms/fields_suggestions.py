from crispy_forms.layout import Layout, HTML, Div, Row, Column
from django.db.models import Count

from etilog.models import ImpactEvent, Company


def get_topic_vals(nr_instances):
    nr_tags = nr_instances//5
    li_vals = []
    impevs = ImpactEvent.objects.select_related(
        'sust_domain').prefetch_related('sust_tags'
                                        ).annotate(
        tag_count=Count('sust_tags')).order_by(
            '-tag_count')
    # hits DB 5 times -> better 1 query
    for i in range(1, 6):
        vals = impevs.filter(
            sust_domain=i).values_list(
            'sust_tags__id', 'sust_tags__name')[:nr_tags]

        li_vals.extend(vals)
    return li_vals


def get_company_vals(nr_instances):
    li_vals = []
    inst = Company.objects.select_related(
        'impevents').annotate(
        impev_count=Count('impevents', distinct=True)).order_by(
            '-impev_count')
    vals = inst.values_list(
        'pk', 'name')[:nr_instances]

    li_vals.extend(vals)
    return li_vals


vals_dispatch_d = {'tags': get_topic_vals,
                   'company': get_company_vals}


class RowTopics(Layout):
    """
    tagname, tagid, tag-category used for tagsinput
    topic-link class for tagsinput function
    """
    def __init__(self, tag_category='tags', col_class='col-12', labelname='',
                 nr_insts=10, *args, **kwargs):  # distribute buttons

        nr_tags = nr_insts/5
        li_sustagsid = []
        
        li_vals = vals_dispatch_d[tag_category](nr_insts)
        div_list = []
        a_str = '''<a href="#" class="topic-link link-intern" 
                    tag-category = "%s"
                    tagid = "%d" tagname = "%s" >%s</a>
                    '''
        k = 1
        for tag in li_vals:
            stag_id = tag[0]
            if stag_id in li_sustagsid:  # no double entries
                k += 1
                continue
            li_sustagsid.append(stag_id)
            addclass = ''
            if (k % nr_tags == 0 and tag_category) == 'tags' or (
                    k > nr_insts/2 and tag_category in ['company', ]):
                addclass = ' d-none d-md-block'  # only show on larger screens

            html_str = a_str % (tag_category, stag_id, tag[1], tag[1])  # (tag.id, tag.name, tag.name)
            a_link = HTML(html_str)
            div_a = Div(a_link, css_class='div_topic_li' + addclass)
            div_list.append(div_a)
            k += 1

        html_str = '<label class="col-form-label">%s</label>' % labelname
        super(RowTopics, self).__init__(
            Row(

                Column(HTML(html_str),
                       Div(*div_list, css_class='d-flex flex-wrap'),  # to wrap elements
                       css_class=col_class,
                       )
            )
        )