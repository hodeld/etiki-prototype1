from crispy_forms.layout import Layout, HTML, Div, Row, Column
from django.db.models import Count

from etilog.models import ImpactEvent


class RowTopics(Layout):
    def __init__(self, col_class='col-12', labelname='', *args, **kwargs):  # distribute buttons
        # q = SustainabilityTag.objects.all()[:5]
        nr_tags = 2
        li_vals = []
        li_sustagsid = []
        # hits DB 5 times -> better 1 query
        for i in range(1, 6):
            vals = ImpactEvent.objects.filter(
                sust_domain=i).values_list(
                'sust_tags__id', 'sust_tags__name').annotate(
                tag_count=Count('sust_tags')).order_by(
                '-tag_count')[:nr_tags]

            li_vals.extend(vals)

        topics_list = []
        a_str = '''<a href="#" class="topic-link link-intern" 
                    tag-category = "tags"
                    tagid = "%d" tagname = "%s" >%s</a>
                    '''
        k = nr_tags
        for tag in li_vals:
            stag_id = tag[0]
            if stag_id in li_sustagsid:  # no double entries
                k += 1
                continue
            li_sustagsid.append(stag_id)
            if k % nr_tags == 0:
                addclass = ''
            else:
                addclass = ' d-none d-md-block'  # only show on larger screens
            html_str = a_str % (stag_id, tag[1], tag[1])  # (tag.id, tag.name, tag.name)
            a_link = HTML(html_str)
            div_a = Div(a_link, css_class='div_topic_li' + addclass)
            topics_list.append(div_a)
            k += 1

        html_str = '<label class="col-form-label">%s</label>' % labelname
        super(RowTopics, self).__init__(
            Row(

                Column(HTML(html_str),
                       Div(*topics_list, css_class='d-flex flex-wrap'),  # to wrap elements
                       css_class=col_class,
                       )
            )
        )