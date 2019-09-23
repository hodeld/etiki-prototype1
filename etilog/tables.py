'''
Created on 24 Jul 2019

@author: daim
'''
#django 
from django.utils.html import mark_safe
from django.urls import reverse
#3rd app
import django_tables2 as tables
#models
from .models import ImpactEvent

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

class BtnTendencyColumn(tables.TemplateColumn):

    def __init__(self, *args, **kwargs):
        
        #bntclass = 'sustbtn btn-sm btn-' #.sustbtn in css
        bntclass = 'sustbtn btn btn-sm disabled btn-block btn-' #.sustbtn in css, btn-block: expands
        extra_dict = {'clsneg': bntclass  + 'danger',
                      'clspos': bntclass + 'success',
                      'clscon': bntclass + 'warning',
                      }
        super(BtnTendencyColumn, self).__init__(  
                                             template_name= 'etilog/cell_button.html',
                                             extra_context=extra_dict,
                                             attrs={'td': {'class':'sustcl'}},
                                             *args, **kwargs,
                                             )
          
    

class ImpEvTable(tables.Table):
    '''
    basic table for impact events
    '''
    CLS_HIDE_COLS = {'td': {'class': 'd-none d-lg-table-cell'}, #hide on screens smaller than ...
                 'th': {'class': 'd-none d-lg-table-cell'}
                 }  
    cls_hide_hover_cols =   {'td': {'class': 'd-none d-lg-table-cell', #hide on screens smaller than ...
                                'title': get_hovertitle, },
                                 'th': {'class': 'd-none d-lg-table-cell'}
                                 } 
    cls_hover_cols =   {'td': {'title': get_hovertitle, }} 
    
    id = tables.Column(linkify = True )
    copy = tables.Column(verbose_name= 'copy',
                         accessor = 'id',
                         linkify = lambda record: reverse('etilog:impactevent_copy', args=(record.id,)))
       
    date_published = tables.DateColumn(verbose_name='Date', format = 'M Y')
    btncol = BtnTendencyColumn(accessor = 'sust_domain', verbose_name = 'Categ.',)
    #sust_category = tables.TemplateColumn('<button class="badge sustbtn badge-danger">Detail</button>')
    summary = tables.Column(attrs =cls_hide_hover_cols)
    
    country = tables.Column(accessor = 'country_display', attrs = CLS_HIDE_COLS) 
    get_tags = tables.Column(verbose_name = 'Tags', orderable = False, attrs = cls_hover_cols)
    reference = tables.Column(linkify = lambda record: record.source_url,  verbose_name = 'Published in', ) #
    
    class Meta:
        model = ImpactEvent
        
        exclude = ('created_at', 'updated_at', )
        #defines also order of columns
        fields = ('id', 'copy', 'date_published', 'company',
                  'btncol', 'country', 'get_tags',  'reference', 'summary' )
        attrs = {'class': 'table table-hover table-sm'} #bootstrap4 classes ;table-responsive: not working with sticky
        
    
    def render_source_url(self, value, record):
        #val_short = str(value)[:20] + '…'
        val_short = str(record.reference.name)
        return  val_short 
    
    def render_copy(self):
        return 'copy!'
    def render_summary(self, value):
        val_short = str(value)[:40]
        return  val_short + '…'
    
    def value_date_published(self, value, record): #only value changed, rendering normal
        if record.date_impact:
            value = record.date_impact
        return  value
    
    def render_country(self, value, record): #render_foo works only if there is a value
        if record.country:
            value = record.country
        return  value
    
    #adds column name as css class in td tag -> for List.js:
    def get_column_class_names(self, classes_set, bound_column):
                    classes_set = super().get_column_class_names(classes_set, bound_column)
                    classes_set.add(bound_column.name)

                    return classes_set
    
    