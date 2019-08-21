'''
Created on 2.8.2019

@author: daim
'''
from django import forms
from django.db.models import OuterRef
from django.urls import reverse_lazy
import json

from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, Button, HTML
from crispy_forms.bootstrap import  InlineRadios, FieldWithButtons, StrictButton

#models
from .models import Source, Company, ImpactEvent, SustainabilityDomain, Reference
from .fields import ReferenceWidget, CompanyWidget, CompanyWBtn, ReferenceWBtn


    
DT_FORMAT = '%Y-%m-%d %H:%M:%S'
#D_FORMAT = '%Y-%m-%d'
D_FORMAT = '%d.%m.%Y'
D_FORMAT_EXTRA = '%d.%m.%y'
D_YEARFORMAT = '%Y'

domains = [('0', '----')]
domains.extend(list(SustainabilityDomain.objects.values_list('id', 'name')))

CHOICES = domains



class NewImpactEvent(forms.ModelForm):
    '''
    form to create an impact event
    '''

    year = forms.CharField(label = 'year published', required=False)
    sust_domain = forms.ChoiceField(label = 'Domain',
                                    choices = CHOICES,
                                    required=False)

    def __init__(self, *args, **kwargs):
        super (NewImpactEvent,self ).__init__(*args,**kwargs) 
        self.fields['year'].widget = DatePickerInput( 
                format = D_YEARFORMAT, #django datetime format
                options={'viewMode': 'years', 
                         })
              
        self.fields['company'].widget = CompanyWidget()
        self.fields['reference'].widget = ReferenceWidget()
           
        
        #crispy form layout:
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'source_url',
            
            Row(
                Column('year', css_class='col-6'),
                Column('date_published', css_class='col-6')
            ),
            
            Row(
                Column(CompanyWBtn(fieldname = 'company',
                                   mainmodel = 'impev'), 
                       css_class='col-6', ),
                
                Column(ReferenceWBtn(), 
                       css_class='col-6', )
            ),
            
            Row(
                Column('sust_domain', 
                       css_class='col-6'),
                Column(Field('sust_category', 
                             data_susts_url=reverse_lazy('etilog:get_sustcagories')
                             ),                           
                             css_class='col-6')
            ),

            
            Field('sust_tags', data_tags_url=reverse_lazy('etilog:get_sust_tags')),
            Field('summary', rows= 3),
            Field('comment', rows= 3),
            
            Submit('submit', 'Save Impact Event', css_class='btn btn-light' )
        )
        
                  
    class Meta: #only for model fields
        model = ImpactEvent
        fields = ['source_url', 'year', 'date_published', 'company', 'reference', 
                  'sust_category', 'sust_tags',
                  'summary', 'comment' 
                  ]
    

        widgets = {
            'source_url': forms.URLInput(attrs={'placeholder': 'url to the article',
                                                
                                                }),
            'date_published': DatePickerInput( #startperiod
                format = D_FORMAT, #django datetime format
                
                options={'viewMode': 'years', 
                         'useCurrent': False, #needed to take initial date
                         'extraFormats': ['DD.MM.YY', 'DD.MM.YYYY' ], #javascript format
                         },
                ),
            'comment' : forms.Textarea() ,
            'summary' : forms.Textarea() 
            }

        labels = {
            'date_published': ('exact date'),
        }
        help_texts = {
           'date_published': (''),
        }
        
        
class CompanyForm(forms.ModelForm):
    '''
    form to create a company
    '''
    def __init__(self, *args, **kwargs):
        super (CompanyForm,self ).__init__(*args,**kwargs) 
        
        self.fields['owner'].widget = CompanyWidget()
        self.fields['subsidiary'].widget = CompanyWidget()
        self.fields['supplier'].widget = CompanyWidget()
        self.fields['recipient'].widget = CompanyWidget()
        
        #self.helper = FormHelper(self)
        self.helper = FormHelper(self)
        self.helper['owner'].wrap(CompanyWBtn,  #fieldname is passed as arg
                        mainmodel = 'company')
        self.helper['subsidiary'].wrap(CompanyWBtn,  #fieldname is passed as arg
                        mainmodel = 'company')
        self.helper['supplier'].wrap(CompanyWBtn,  #fieldname is passed as arg
                        mainmodel = 'company')
        self.helper['recipient'].wrap(CompanyWBtn,  #fieldname is passed as arg
                        mainmodel = 'company')
        
            
        #adds a submit button at the end
        self.helper.layout.append(
            Row(Submit('submit', 'Save', css_class='btn btn-light' ))
        )           

                  
    class Meta: #only for model fields
        model = Company
        exclude = ['',]
        
class ReferenceForm(forms.ModelForm):
    '''
    form to create a reference
    '''
    def __init__(self, *args, **kwargs):
        super (ReferenceForm,self ).__init__(*args,**kwargs) 
        
        
        self.helper = FormHelper(self)
        #adds a submit button at the end
        self.helper.layout.append(
            Submit('submit', 'Save', css_class='btn btn-light' )
            )
                  

                  
    class Meta: #only for model fields
        model = Reference
        exclude = []    


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

        


