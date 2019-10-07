'''
Created on 03 oct 2019

@author: daim
'''

import csv

from etilog.models import ImpactEvent
from etilog.models  import SustainabilityDomain, SustainabilityTendency, SustainabilityTag
from etilog.models  import Company
from etilog.models  import  Reference

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
                 'article_text',
                 'date_text'
                 ]
    
    val_ie = ImpactEvent.objects.exclude(article_text__isnull = True).exclude(article_text__exact = '').values_list(*val_names)
    writer.writerow(header)
    for ie in val_ie:
        writer.writerow(ie)

    return response

def exp_csv_basedata(response):
    
    writer = csv.writer(response)
    
    def writerow(modelname, header, vallist):
        writer.writerow(modelname)
        writer.writerow(header)
        for row in vallist:
            writer.writerow(row)
    
    
    #topics
    modelname = ['TOPICS',]        
    header = ['ID', 
              'NAME', 
              'CATEGORY_ID',  
              'CATEGORY_NAME',  
              'TENDENCY_ID',  
              'TENDENCY_NAME',
              ]
    val_names = ['id', 
                 'name',
                 'sust_domains', 
                 'sust_domains__name',
                 'sust_tendency', 
                 'sust_tendency__name',
                 ]
    vallist = SustainabilityTag.objects.values_list(*val_names)
    writerow(modelname, header, vallist)
    
    #domains
    modelname = ['CATEGORY',]        
    header = ['ID', 
              'NAME',  
              ]
    val_names = ['id', 
                 'name',
                 ]
    vallist = SustainabilityDomain.objects.values_list(*val_names)
    writerow(modelname, header, vallist)
    
    #tendency
    modelname = ['TENDENCY',]        
    header = ['ID', 
              'NAME',  
              ]
    val_names = ['id', 
                 'name',
                 ]
    vallist = SustainabilityTendency.objects.values_list(*val_names)
    writerow(modelname, header, vallist)
    
    #companies
    modelname = ['COMPANIES / ORGANISATIONS',]        
    header = ['ID', 
              'NAME',  
              ]
    val_names = ['id', 
                 'name',
                 ]
    vallist = Company.objects.values_list(*val_names)
    writerow(modelname, header, vallist)
    
    #references
    modelname = ['REFERENCE',]        
    header = ['ID', 
              'NAME',  
              ]
    val_names = ['id', 
                 'name',
                 ]
    vallist = Reference.objects.values_list(*val_names)
    writerow(modelname, header, vallist)

    return response
