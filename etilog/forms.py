'''
Created on 2.8.2019

@author: daim
'''
from django import forms

from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
#models
from .models import ImpactEvent, Source
from .fields import ListTextWidget


    
DT_FORMAT = '%Y-%m-%d %H:%M:%S'
D_FORMAT = '%Y-%m-%d'
D_YEARFORMAT = '%Y'

class NewImpactEvent(forms.ModelForm):
    '''
    form to create an impact event
    '''

    year = forms.CharField(label = 'year published', )
    def __init__(self, *args,**kwargs):
        super (NewImpactEvent,self ).__init__(*args,**kwargs) 
        self.fields['year'].widget = DatePickerInput( 
                format = D_YEARFORMAT, #django datetime format
                options={'viewMode': 'years', 
                         })
    class Meta: #only for model fields
        model = ImpactEvent
        fields = ['source_url', 'year', 'date_published', 'company', 'reference', 'sust_category', 
                  'comment' ]
    

        widgets = {
            'source_url': forms.URLInput(attrs={'placeholder': 'url to the article',
                                                
                                                }),
            'company': ListTextWidget(data_list=["hal","halol","hall"], name='company_list',),
            'date_published': DatePickerInput( #startperiod
                format = D_FORMAT, #django datetime format
                options={'viewMode': 'years', 
                         'useCurrent': False #needed to take initial date
                         },
                
            
            ),
            
            }

        labels = {
            'date_published': ('exact date'),
        }
        help_texts = {
           'date_published': (''),
        }

        

class NewSource(forms.ModelForm):
    '''
    form to create an source
    '''

    class Meta: #only for model fields
        model = Source
        fields = ['url',]
    

        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'https://… link to the article ',
                                                'size': '60',
                                                'title': 'just copy/paste your link here',
                                                'class': 'form-control',
                                            
                                                }),

            }
        labels = {
            'url': (''),
        }
        help_texts = {
            #'url': 'urlblajsv',
        }

        


