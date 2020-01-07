'''
Created on 24 Jul 2019

@author: daim
'''
#django 
from django.utils.html import mark_safe
from django.urls import reverse
from django.template.loader import render_to_string

#3rd app
import django_tables2 as tables
#models
from .models import ImpactEvent
from .fields import dom_icon_dict


def get_hovertitle(*args, **kwargs):
    col = kwargs.get('bound_column', None) #value already changed through rendering
    
    record = kwargs.get('record', None) #value already changed through rendering
    stitle = ''
    if record and col:
        colname = col.accessor
        cellvalue = getattr(record, colname, None)
        if cellvalue:
            stitle = cellvalue
       
    return stitle

def get_sortname(*args, **kwargs):
    col = kwargs.get('bound_column', None) #value already changed through rendering
    colname = ''
    if  col:
        colname = col.name
    return colname
    
def get_attrs(hide_mobile = False, hide = False, hover = False, sort = False, datasort = None, add_attrs = {}, *args, **kwargs):
    if hide:
        attr_hide_always = {'td': {'class': 'd-none'}, #hide on screens smaller than ...
                 'th': {'class': 'd-none '}
                 }
        return attr_hide_always
    td_class = ''
    th_class = ''
    attrs_dic = {'td': {'class': '',
                        'onclick': lambda record:  'show_details(this, %d)' %record.pk
                        }, 
                 'th': {'class': ''}
                 }
    if hide_mobile:
        td_class = 'd-none d-lg-table-cell'
        th_class = 'd-none d-lg-table-cell'

    if hover:
        td_hover = {'title': get_hovertitle}
        
        attrs_dic['td'].update(td_hover)

    th_datasort = None
    if sort:
        th_class = ' '.join([th_class, 'sort'])
        if datasort:            
            th_datasort =  datasort #get_sortname
        else:
            th_datasort = get_sortname

    attrs_dic['td']['class'] =  td_class
    attrs_dic['th']['class'] =  th_class
    if th_datasort:
        attrs_dic['th']['data-sort'] =  th_datasort

    
    attrs_dic.update(add_attrs)
    return attrs_dic
        
    

class DefWidthColumn(tables.Column):

    def __init__(self, classname=None, *args, **kwargs):
        self.classname=classname
        super(DefWidthColumn, self).__init__(*args, **kwargs)

    def render(self, value):
        return mark_safe("<div class='" + self.classname + "' >" +value+"</div>")



class SustcatColumn2(tables.Column):

    def __init__(self, *args, **kwargs):
        def cssclass_sustcat(**kwargs):
            record = kwargs.get('record', None) #value already changed through rendering
            if record:
                sustcat = record.sust_category
                bntclass = 'sustbtn btn btn-' #.sustbtn in css
                if 'negativ' in sustcat.name :
                    return bntclass + 'danger'
                elif 'controv' in sustcat.name :
                    return bntclass + 'warning'
                elif 'positiv' in sustcat.name :
                    return bntclass + 'success'
            else:
                return ''
        super(SustcatColumn2, self).__init__(*args, **kwargs, 
                                            attrs={'td': {'class': cssclass_sustcat}}
                                            )

    def render(self, value):
        sustcat = value
        sustdomain = sustcat.sust_domain.name
        return sustdomain


tendency_id_dict = {1: 'success',
                         2: 'danger',
                         3: 'warning',
                         }

class BtnTendencyColumn(tables.Column):

    
        
    def render(self, value, record):
        
        btn_color = tendency_id_dict[record.sust_tendency.impnr]
        btnclass = 'sustbtn btn btn-sm disabled btn-block btn-' + btn_color
        iconname = dom_icon_dict[record.sust_domain.id]
        html_str = render_to_string('etilog/cell_button.html', 
                                    {'btnclass': btnclass,
                                     'iconname': iconname,
                                     'value': value
                                    })
        
        
        return html_str
    

class BtnTendencyColumn2(tables.TemplateColumn):

    def __init__(self, *args, **kwargs):
        
        #bntclass = 'sustbtn btn-sm btn-' #.sustbtn in css
        bntclass = 'sustbtn btn btn-sm disabled btn-block btn-' #.sustbtn in css, btn-block: expands
        extra_dict = {'clsneg': bntclass  + 'danger',
                      'clspos': bntclass + 'success',
                      'clscon': bntclass + 'warning',
                      }
        attrs = kwargs.get('attrs', None) #value already changed through rendering
        
        if attrs:
            td = attrs.get('td', None)
            if td:
                cls = td.get('class', None)
                if cls:
                    td['class'] = ' '.join(['sustcl', cls]) 
                else:
                    td['class'] = 'sustcl'
            else:
                attrs['td'] = {'class':'sustcl'}
                

                
        else:
            kwargs['attrs'] = {'td': {'class':'sustcl'}}

        super(BtnTendencyColumn2, self).__init__(  
                                             template_name= 'etilog/cell_button.html',
                                             extra_context=extra_dict,
                                             #attrs=attrs,
                                             *args, **kwargs,
                                             )
        
    

    
etiki_table_classes =  'table table-hover table-sm table-etiki' #bootstrap classes, plus own tbl class   
class ImpEvTable(tables.Table):
    '''
    basic table for impact events
    '''
    #names of columns need to be in prepare_list as valueNames
    date = tables.DateColumn(verbose_name='Date', accessor='date_display', format = 'M Y', 
                                       attrs = get_attrs(sort = True, datasort = 'date_sort'))

    date_sort = tables.DateColumn(accessor='date_display', format = 'Ymd',
                                  attrs = get_attrs(hide = True)
                                  )
    
    sust_domain = BtnTendencyColumn(accessor = 'sust_domain', verbose_name = 'Category',
                               attrs = get_attrs(sort = True, datasort = 'sudom_sort'))
    sudom_sort = tables.Column(accessor='sust_domain', attrs = get_attrs(hide = True))
    
    summary = tables.Column(accessor = 'summary_display', attrs = get_attrs(hide_mobile = True, hover = True))
    
    country = tables.Column(accessor = 'country_display', 
                            attrs = get_attrs(hide_mobile = True, sort = True))
    
    company = tables.Column(attrs = get_attrs(sort = True))
    topics = tables.Column(accessor = 'get_tags', verbose_name = 'Topics', 
                             attrs = get_attrs(hover = True, sort = True))
    reference = tables.Column(linkify = lambda record: record.source_url,  
                              verbose_name = 'Published in', 
                              attrs = get_attrs(sort = True, hide_mobile = True,
                                                 datasort = 'reference_sort',
                                                 add_attrs = {'a':{'target':'_blank'}},
                                                 )
                              )
    reference_sort = tables.Column(accessor='reference', attrs = get_attrs(hide = True))

    details = tables.Column(verbose_name= '',
                            accessor = 'id',
                            attrs = get_attrs()
                            )

    
    class Meta:
        model = ImpactEvent
        
        exclude = ('created_at', 'updated_at', )
        #defines also order of columns
        fields = ('sust_domain', 'topics', 'company', 'date', 
                   'country',   'reference', 'summary')
        #orderable = False #for all columns
        attrs = {'class': etiki_table_classes, #bootstrap4 classes ;table-responsive: not working with sticky
                }
        template_name = 'etilog/etilog_djangotable.html'
        
    
    def render_source_url(self, value, record):
        #val_short = str(value)[:20] + '…'
        val_short = str(record.reference.name)
        return  val_short 
    
    def render_copy(self):
        return 'copy!'
    def render_details(self):
        return '…'
    
    def render_summary(self, value, record):
        #if record.summara
        val_short = str(value)[:40]
        return  val_short + '…'

    
    #adds column name as css class in td tag -> for List.js:
    def get_column_class_names(self, classes_set, bound_column):
                    classes_set = super().get_column_class_names(classes_set, bound_column)
                    classes_set.add(bound_column.name)

                    return classes_set
        
        
class ImpEvTablePrivat(ImpEvTable):
    '''
    table for impact events for internal use
    subclassing from public table
    '''
    
    id = tables.Column(attrs = get_attrs(sort = True),
                       linkify = lambda record: reverse('etilog:impactevent_update', args=(record.id,)))
    copy = tables.Column(verbose_name= 'copy',
                         accessor = 'id',  orderable = False,
                         linkify = lambda record: reverse('etilog:impactevent_copy', args=(record.id,)))  
    
    class Meta:
        #css stuff needed in inherited table as well!
        attrs = {'class': etiki_table_classes, #bootstrap4 classes ;table-responsive: not working with sticky
                }
        template_name = 'etilog/etilog_djangotable.html'  
        sequence = ('id', 'copy', '...')

class ImpEvDetails(ImpEvTable):
    '''
    fields for impact events details
    subclassing from public table
    '''
    sudom_sort = None
    reference_sort = None
    date_sort = None
    details = None

    
    def render_summary(self, value, record):
        #if record.summara
        val_long = str(value)[:300]
        return  val_long 
    
    class Meta:

        sequence = ('sust_domain', 'company', 'date', 
                   'country',   'reference', 'topics', 'summary', '...')

    
