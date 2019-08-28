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



class SustcatColumn(tables.Column):

    def __init__(self, *args, **kwargs):
        def cssclass_sustcat(**kwargs):
            record = kwargs.get('record', None) #value already changed through rendering
            if record:
                sustcat = record.sust_category
                bntclass = 'btn disabled btn-sm '
                if 'negativ' in sustcat.name :
                    return bntclass + 'btn-danger'
                elif 'controv' in sustcat.name :
                    return bntclass + 'btn-warning'
                elif 'positiv' in sustcat.name :
                    return bntclass + 'btn-success'
            else:
                return ''
        super(SustcatColumn, self).__init__(*args, **kwargs, 
                                            attrs={'td': {'class': cssclass_sustcat}}
                                            )

    def render(self, value):
        sustcat = value
        sustdomain = sustcat.sust_domain.name
        return sustdomain


   
    
    
class ImpEvTable(tables.Table):
    '''
    basic table for impact events
    '''

    id = tables.Column(linkify = True )
    copy = tables.Column(verbose_name= 'copy',
                         accessor = 'id',
                         linkify = lambda record: reverse('etilog:impactevent_copy', args=(record.id,)))
       
    date_published = tables.DateColumn(verbose_name='Date of Impact', format = 'M Y')
    sust_category = SustcatColumn()
    summary = tables.Column(attrs ={'td': {'title': get_hovertitle}})
    country = tables.Column(accessor = 'company.country') 
    
    class Meta:
        model = ImpactEvent
        
        exclude = ('created_at', 'updated_at', )
        fields = ('id', 'copy', 'date_published', 'company', 'country', 
                  'sust_category', 'get_tags', 'reference',  'source_url', 'summary' )
        attrs = {'class': 'table table-hover table-sm'} #bootstrap4 classes 
        
    
    def render_source_url(self, value):
        val_short = str(value)[:20]
        return  val_short + '…'
    
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
    
    