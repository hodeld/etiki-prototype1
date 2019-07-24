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

    
    class Meta:
        model = ImpactEvent
        attrs = {'class': 'table table-sm'}
        #exclude = (  'deleted', 'eventcat', 'masterevent')
    