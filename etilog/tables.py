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

class DefWidthColumn(tables.Column):

    def __init__(self, classname=None, *args, **kwargs):
        self.classname=classname
        super(DefWidthColumn, self).__init__(*args, **kwargs)

    def render(self, value):
        return mark_safe("<div class='" + self.classname + "' >" +value+"</div>")
    
    
class ImpEvTable(tables.Table):
    '''
    basic table for impact events
    '''

    id = tables.Column(linkify = True, attrs={'td': {'class': 'my-class'}} )
    copy = tables.Column(verbose_name= 'copy IE',
                         accessor = 'id',
                         linkify = lambda record: reverse('etilog:impactevent_copy', args=(record.id,)))
    #source_url = DefWidthColumn(classname='limited_width')
       
    date_published = tables.Column(verbose_name='Date of Impact')
    class Meta:
        model = ImpactEvent
        
        exclude = ('created_at', 'updated_at', )
        fields = ('id', 'copy', 'date_published', 'company', 'country', 
                  'sust_category', 'get_tags', 'reference',  'source_url', 'summary' )
        attrs = {'class': 'table table-hover table-sm'} #bootstrap4 classes }  #used for list filtering
        
    
    def render_source_url(self, value):
        val_short = str(value)[:20]
        return  val_short
    
    def render_copy(self):
        return 'copy!'
    
    #adds column name as css class in td tag:
    def get_column_class_names(self, classes_set, bound_column):
                    classes_set = super().get_column_class_names(classes_set, bound_column)
                    classes_set.add(bound_column.name)

                    return classes_set
    
    