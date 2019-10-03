'''
Created on 03 oct 2019

@author: daim
'''

import os

import csv
from django.http import HttpResponse
from etilog.models import ImpactEvent

def exp_csv_nlp(response):
    
    writer = csv.writer(response)
    header = ['ID', 
              'date_published', 
              'CompanyID',  
              'CompanyName', 
              'ReferenceID', 
              'ReferenceName', 
              'URL', 
              'pub_text', 
              'date_text'
              ]
    val_names = ['id', 
                 'date_published',
                 'company__id', 
                 'company__name', 
                 'reference__id', 
                 'reference__name',
                 'source_url',
                 #'article_text',
                 #'pub_date_string'
                 ]
    
    val_ie = ImpactEvent.objects.values_list(*val_names)[:5]
    writer.writerow(header)
    for ie in val_ie:
        writer.writerow(ie)

    return response
