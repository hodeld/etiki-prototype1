'''
Created on 2.8.2019

@author: daim
'''
from django import forms

from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
#models
from .models import ImpactEvent, Source


    
DT_FORMAT = '%Y-%m-%d %H:%M:%S'
D_FORMAT = '%Y-%m-%d'
D_YEARFORMAT = '%Y'

class NewImpactEvent(forms.ModelForm):
    '''
    form to create an impact event
    '''
    #gs = forms.CharField(required=False, label = 'N-Nr.', )
    year = forms.CharField( label = 'N-Nr.', )
    def __init__(self, *args,**kwargs):
        super (NewImpactEvent,self ).__init__(*args,**kwargs) # populates the post
        self.fields['year'].widget = DatePickerInput( #startperiod
                format = D_YEARFORMAT, #django datetime format
                options={#'calendarWeeks': True,
                         'viewMode': 'years', 
                         #'daysOfWeekDisabled': [0,6], #datepicker options
                         #'defaultDate': start.strftime(DT_FORMAT), #'19-03-03 00:00:00'
                         #'useCurrent': False #needed to take initial date
                         })
    class Meta: #only for model fields
        model = ImpactEvent
        fields = ['source_url', 'year', 'date_published', 'company', 'reference', 'sust_category', 
                  'comment' ]
    

        widgets = {
            'source_url': forms.URLInput(attrs={'placeholder': 'www.bla.ch',
                                                'size': '30',
                                                'onchange' : 'change_gs(this, value)'}),
            'date_published': DatePickerInput( #startperiod
                format = D_FORMAT, #django datetime format
                options={#'calendarWeeks': True,
                         'viewMode': 'years', 
                         #'daysOfWeekDisabled': [0,6], #datepicker options
                         #'defaultDate': start.strftime(DT_FORMAT), #'19-03-03 00:00:00'
                         #'useCurrent': False #needed to take initial date
                         },
                
            attrs={'size': '30'}
            ),
            
            }

        labels = {
            'gszemis': ('Zemis'),
        }
        

class NewSource(forms.ModelForm):
    '''
    form to create an source
    '''

    class Meta: #only for model fields
        model = Source
        fields = ['url',]
    

        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'link to the article',
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

        


