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
from crispy_forms.layout import Layout, Field, Row, Column, Submit, Hidden, Div, Button, ButtonHolder, HTML
from crispy_forms.bootstrap import  FormActions, FieldWithButtons, StrictButton

#models
from .models import Source, Company, ImpactEvent, SustainabilityDomain, Reference
from .fields import ReferenceWidget, CompanyWidget, CompanyWBtn, ReferenceWBtn
from .fields import DateYearPicker
from .fields import RowTagsInput, ColDomainBtnSelect, ColTendencyBtnSelect


    
DT_FORMAT = '%Y-%m-%d %H:%M:%S'
#D_FORMAT = '%Y-%m-%d'
D_FORMAT = '%d.%m.%Y'
D_FORMAT_EXTRA = '%d.%m.%y'
D_YEARFORMAT = '%Y'

domains = [('0', '----')]
domains.extend(list(SustainabilityDomain.objects.values_list('id', 'name')))

CHOICES = domains
datefiltername = 'datefilter'

class SearchForm(forms.Form):

    search = forms.CharField(label = '', required=False)
    freetext = forms.CharField(label = 'freetext', required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
            

        
        self.helper = FormHelper()
        
        self.helper.layout = Layout(
            
        Row(
                Column(Field('search', id = 'id_search', autocomplete="off", 
                             placeholder = 'Search Companies, Countries, Newspaper …'
                       ),
                        css_class='col-12'                             
                    )
                ),
        Row(
                Column(Field('freetext', id = 'id_f_freetext', 
                             
                             data_role='tagsinput'
                       ),
                        css_class='col-12'                             
                    ), id = 'id_row_f_freetext', css_class='row_tags_class'
                ),
        )
        

class FreetextForm(forms.Form):

    freetext = forms.CharField(label = 'freetext', required=False)

    def __init__(self, *args, **kwargs):
        super(FreetextForm, self).__init__(*args, **kwargs)
       
        self.helper = FormHelper()
        
        self.helper.layout = Layout(
            
        Row(
                Column(Field('freetext', id = 'id_f_freetext', 
                             
                             data_role='tagsinput'
                       ),
                        css_class='col-12'                             
                    ), id = 'id_row_f_freetext', css_class='row_tags_class'
                ),
        )
            
           
            
        
class ImpevOverviewFForm(forms.Form):

    #datefiltersub = forms.CharField(label = '', required=False)

    def __init__(self, *args, **kwargs):
        super(ImpevOverviewFForm, self).__init__(*args, **kwargs)
        
        self.fields['date_from'].widget = DateYearPicker()
        self.fields['date_to'].widget = DateYearPicker()
        self.fields['company'].widget = forms.TextInput() 
        self.fields['country'].widget = forms.TextInput() 
        self.fields['reference'].widget = forms.TextInput() 
        #self.fields['sust_domain'].widget = forms.TextInput() 
        

        
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_id = 'id_filterform'

        self.helper.layout = Layout(
            
            RowTagsInput('company',  'col-12'),
            RowTagsInput('country',  'col-12'),
            RowTagsInput('reference',  'col-12'),
            #Row(Column('sust_domain'),  css_class='col-12'),
            Hidden('sust_domain', '', id='id_sust_domain'), #, id='id_sust_domain' ),
            Hidden('sust_tendency', '', id='id_sust_tendency'), 
            Row(ColDomainBtnSelect(),ColTendencyBtnSelect()),
            
         
            Row(
                Column('date_from', css_class='col-12 col-lg-6'),
                Column('date_to', css_class='col-12 col-lg-6')
            ),
            Row(
                Column(
                    
                        Submit('submit', 'Apply Filter', css_class='btn btn-secondary btn-block',),    
                    css_class='col-12'
                    )
                )
            )
    
    
  
CSS_COL_CLS = 'col-12 col-lg-6'
class NewImpactEvent(forms.ModelForm):
    '''
    form to create an impact event
    '''
    sust_domain = forms.ChoiceField(label = 'which field of impact',
                                    choices = CHOICES,
                                    required=False)

    def __init__(self, *args, **kwargs):
        super (NewImpactEvent,self ).__init__(*args,**kwargs) 
              
        self.fields['company'].widget = CompanyWidget()
        self.fields['reference'].widget = ReferenceWidget()
           
        
        #crispy form layout:
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'source_url',
            
            Row(
                Column('date_published', css_class=CSS_COL_CLS),
                Column('date_impact', css_class=CSS_COL_CLS)
            ),
            
            Row(
                Column(CompanyWBtn(fieldname = 'company',
                                   mainmodel = 'impev'), 
                       css_class=CSS_COL_CLS, ),
                
                Column(ReferenceWBtn(), 
                       css_class=CSS_COL_CLS, )
            ),
            
            Row(
                Column('sust_domain', 
                       css_class=CSS_COL_CLS),
                Column(Field('sust_category', 
                             data_susts_url=reverse_lazy('etilog:get_sustcagories')
                             ),                           
                             css_class=CSS_COL_CLS)
            ),

            
            Field('sust_tags', data_tags_url=reverse_lazy('etilog:get_sust_tags')),
            Field('summary', rows= 3),
            Field('comment', rows= 3),
            
            Submit('submit', 'Save Impact Event', css_class='btn btn-light' )
        )
        
                  
    class Meta: #only for model fields
        model = ImpactEvent
        fields = ['source_url', 'date_published', 'date_impact', 'company', 'reference', 
                  'sust_category', 'sust_tags',
                  'summary', 'comment' 
                  ]
    

        widgets = {
            'source_url': forms.URLInput(attrs={'placeholder': 'url to the article',
                                                
                                                }),
            'date_published': DateYearPicker(),
            'date_impact': DateYearPicker(),
            'comment' : forms.Textarea() ,
            'summary' : forms.Textarea() 
            }

        labels = {
            'date_published': ('when was it published'),
            'date_impact': ('when did it happen'),
            'reference': ('where was it published'),
            'company': ('which company was concerned'),
        }
        help_texts = {
           'date_published': (''),
           'date_impact': (''),
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

        


