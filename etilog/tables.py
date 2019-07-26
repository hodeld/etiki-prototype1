'''
Created on 24 Jul 2019

@author: daim
'''
import django_tables2 as tables
from .models import ImpactEvent

class ImpEvTable(tables.Table):
    '''
    basic table for impact events
    '''

    id = tables.Column( linkify = True )
    class Meta:
        model = ImpactEvent
        attrs = {'class': 'table table-hover table-sm' } #bootstrap4 classes
        exclude = (  'created_at', 'updated_at', )
        fields = ('id', 'date_impact', 'company', 'country', 
                  'sust_category', 'all_tags', 'reference', 'source_link', 'comment' )
    