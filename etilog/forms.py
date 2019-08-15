'''
Created on 2.8.2019

@author: daim
'''
from django import forms
from django.db.models import OuterRef
from django.urls import reverse_lazy

from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, Button, HTML
from crispy_forms.bootstrap import  InlineRadios, FieldWithButtons, StrictButton

#models
from .models import Source, Company, ImpactEvent, SustainabilityDomain, Reference
from .fields import ListTextWidget


    
DT_FORMAT = '%Y-%m-%d %H:%M:%S'
#D_FORMAT = '%Y-%m-%d'
D_FORMAT = '%d.%m.%Y'
D_YEARFORMAT = '%Y'

domains = [('0', '----')]
domains.extend(list(SustainabilityDomain.objects.values_list('id', 'name')))

CHOICES = domains

class NewImpactEvent(forms.ModelForm):
    '''
    form to create an impact event
    '''

    year = forms.CharField(label = 'year published', )
    sust_domain = forms.ChoiceField(label = 'Domain',
                                    choices = CHOICES,
                                    required=False)
    
    def __init__(self, *args, **kwargs):
        super (NewImpactEvent,self ).__init__(*args,**kwargs) 
        self.fields['year'].widget = DatePickerInput( 
                format = D_YEARFORMAT, #django datetime format
                options={'viewMode': 'years', 
                         })
        #more complicate solution:
        reference_pks = Reference.objects.values_list('pk', flat = True) #all ids
        companies = Company.objects.exclude(reference__pk__in = reference_pks).distinct()
        #companies = ImpactEvent.objects.order_by().values_list('company__name', flat = True).distinct()
        self.fields['company'].widget = ListTextWidget(data_list=companies
                                                       , name='company_list',
                                                       attrs={'placeholder': 'Company',}
                                                       )
        #crispy form layout:
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'source_url',
            
            Row(
                Column('year', css_class='col-6'),
                Column('date_published', css_class='col-6')
            ),
            Row(
                Column('sust_domain', 
                       css_class='col-6'),
                Column(Field('sust_category', 
                             data_susts_url=reverse_lazy('etilog:get_sustcagories')
                             ),                           
                             css_class='col-6')
            ),
            #InlineRadios('sust_domain'), 
            #Field('sust_category', data_susts_url=reverse_lazy('etilog:get_sustcagories')), #reverse_lazy('etilog:get_sustcagories') does not work
            #Field('sust_category', template="custom-slider.html"),
            Row(
                Column(FieldWithButtons('company', 
                                        StrictButton("Go!", css_class='btn btn-light',
                                        css_id='id_btn_company',
                                        admin_add_url=reverse_lazy('admin:etilog_company_add')+'?_to_field=id&_popup=1' 
                                            )), 
                       css_class='col-6', ),
                Column('reference', css_class='col-6')
            ),
            'sust_tags',
            'summary', 
            'comment',
            HTML("""<a class="classes-for-styling" href="{% url 'admin:etilog_company_add' %}"
            onclick='return showAddAnotherPopup(this);'
            >addcompany</a>"""),
            
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
        
        
class NewImpactEvent(forms.ModelForm):
    '''
    form to create an impact event
    '''

    year = forms.CharField(label = 'year published', )
    sust_domain = forms.ChoiceField(label = 'Domain',
                                    choices = CHOICES,
                                    required=False)
    
    def __init__(self, *args, **kwargs):
        super (NewImpactEvent,self ).__init__(*args,**kwargs) 
        self.fields['year'].widget = DatePickerInput( 
                format = D_YEARFORMAT, #django datetime format
                options={'viewMode': 'years', 
                         })
        #more complicate solution:
        reference_pks = Reference.objects.values_list('pk', flat = True) #all ids
        companies = Company.objects.exclude(reference__pk__in = reference_pks).distinct()
        #companies = ImpactEvent.objects.order_by().values_list('company__name', flat = True).distinct()
        self.fields['company'].widget = ListTextWidget(data_list=companies
                                                       , name='company_list',
                                                       attrs={'placeholder': 'Company',}
                                                       )
        #crispy form layout:
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'source_url',
            
            Row(
                Column('year', css_class='col-6'),
                Column('date_published', css_class='col-6')
            ),
            Row(
                Column('sust_domain', 
                       css_class='col-6'),
                Column(Field('sust_category', 
                             data_susts_url=reverse_lazy('etilog:get_sustcagories')
                             ),                           
                             css_class='col-6')
            ),
            #InlineRadios('sust_domain'), 
            #Field('sust_category', data_susts_url=reverse_lazy('etilog:get_sustcagories')), #reverse_lazy('etilog:get_sustcagories') does not work
            #Field('sust_category', template="custom-slider.html"),
            Row(
                Column(FieldWithButtons('company', 
                                        StrictButton("Go!", css_class='btn btn-light',
                                        css_id='id_btn_company',
                                        admin_add_url=reverse_lazy('admin:etilog_company_add')+'?_to_field=id&_popup=1' 
                                            )), 
                       css_class='col-6', ),
                Column('reference', css_class='col-6')
            ),
            'sust_tags',
            'summary', 
            'comment',
            HTML("""<a class="classes-for-styling" href="{% url 'admin:etilog_company_add' %}"
            onclick='return showAddAnotherPopup(this);'
            >addcompany</a>"""),
            
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
        
            
     
class NewImpactEvent_old(forms.ModelForm):
    '''
    form to create an impact event
    '''

    year = forms.CharField(label = 'year published', )
    sust_domain = forms.ChoiceField(label = 'Domain',
                                    choices = CHOICES,
                                    required=False,
                                    widget = forms.RadioSelect())
                                        #attrs={'class': 'form-check-input radio-inline',}))
    def __init__(self, *args,**kwargs):
        super (NewImpactEvent,self ).__init__(*args,**kwargs) 
        self.fields['year'].widget = DatePickerInput( 
                format = D_YEARFORMAT, #django datetime format
                options={'viewMode': 'years', 
                         })
        #more complicate solution:
        #impev_pks = ImpactEvent.objects.values_list('pk', flat = True) #all ids
        #companies = Company.objects.filter(impevents__pk__in = impev_pks).distinct()
        companies = ImpactEvent.objects.order_by().values_list('company__name', flat = True).distinct()
        self.fields['company'].widget = ListTextWidget(data_list=companies
                                                       , name='company_list',
                                                       attrs={'placeholder': 'Company',}
                                                       )
        self.helper = FormHelper()
        self.helper.layout = Layout(InlineRadios('sust_domain'))
        
                  
    class Meta: #only for model fields
        model = ImpactEvent
        fields = ['source_url', 'year', 'date_published', 'company', 'reference', 'sust_category', 
                  'comment' ]
    

        widgets = {
            'source_url': forms.URLInput(attrs={'placeholder': 'url to the article',
                                                
                                                }),
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
        
    
    #helper = FormHelper()
    #helper.layout = Layout(
     #   Field('sust_domain', css_class='form-check-input radio-inline'), InlineRadios('field_name')
     #   )

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

        


