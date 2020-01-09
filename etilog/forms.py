'''
Created on 2.8.2019

@author: daim
'''
from django import forms
from django.urls import reverse_lazy


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, HTML

#models
from .models import (Source, Company, ImpactEvent, SustainabilityDomain, Reference,
                     SubsidiaryOwner, SupplierRecipient
                     )
            
from .fields import (ReferenceWidget, CompanyWidget, CompanyWBtn, ReferenceWBtn, UrlWBtn,
                     DateYearPicker, DateYearPickerField,
                     RowTagsInput, ColDomainBtnSelect, ColTendencyBtnSelect, RowTopics, ImpactEventBtns,
                     Readonly, SearchWBtn
                     )


    
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

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
            

        
        self.helper = FormHelper()
        
        self.helper.layout = Layout(
        Row(
                Column(SearchWBtn('search', id = 'id_search', autocomplete="off", 
                             placeholder = 'Search Companies, Countries, Topics, Newspaper …'
                       ),
                        css_class='col-12'                             
                    )
                ),  
        
        )
        
class TopicForm(forms.Form):


    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
            

        
        self.helper = FormHelper()
        
        self.helper.layout = Layout(
 
        RowTopics(),
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
        self.fields['tags'].widget = forms.TextInput() 
        self.fields['summary'].widget = forms.TextInput() 
        self.fields['sust_domain'].widget = forms.HiddenInput() 
        self.fields['sust_tendency'].widget = forms.HiddenInput() 
        

        
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_id = 'id_filterform'
        cls_filterinput = 'f_input' #used for jquery submit
        
        
        self.helper.layout = Layout(
            
            #RowTagsInput('summary',  'col-12', field_class = cls_filterinput),
            Row(
                Column(Field('summary', id = 'id_f_summary', 
                             css_class =  ' '.join([cls_filterinput, 'f_tagsinput']), #f_tagsinput for removing div                          
                             data_role='tagsinput'
                       ),
                        css_class='col-12'                             
                    ), id = 'id_row_f_summary', css_class='row_tags_class'
                ),
            
            RowTagsInput('tags',  'col-12', field_class = cls_filterinput),
            RowTagsInput('company',  'col-12', field_class = cls_filterinput),
            RowTagsInput('country',  'col-12', field_class = cls_filterinput),
            RowTagsInput('reference',  'col-12', field_class = cls_filterinput),
            
            Field('sust_domain', id='id_sust_domain', 
                  css_class=cls_filterinput + 'btninput', parfield='#id_sust_domain-btn-' ),
            Field('sust_tendency', id='id_sust_tendency', 
                  css_class=cls_filterinput + 'btninput', parfield='#id_sust_domain-btn-'), 
            Row(ColDomainBtnSelect(labelname = 'Category'),
                ColTendencyBtnSelect(labelname = 'Which Tendency')
                ),
            
            Row(
                Column(
                    DateYearPickerField('date_from', css_class=cls_filterinput),
                    DateYearPickerField('date_to', css_class=cls_filterinput),
                    css_class = 'col-12 d-flex flex-wrap' #wraps if needed
                    )

            ),
         
            )
    
    
  
CSS_COL_CLS = 'col-12 col-lg-6'
class ImpactEventForm(forms.ModelForm):
    '''
    form to create an impact event
    '''

    def __init__(self, *args, **kwargs):
        super (ImpactEventForm,self ).__init__(*args,**kwargs) 
              
        self.fields['company'].widget = CompanyWidget()
        self.fields['reference'].widget = ReferenceWidget()
        self.fields['article_html'].widget = forms.TextInput() 

           
        
        #crispy form layout:
        self.helper = FormHelper()
        self.helper.form_id = 'id_impevform'
        self.helper.layout = Layout(
            ImpactEventBtns(),
            Row(
                Column(UrlWBtn('source_url'), 
                       css_class='col-12', )
                ),            
            Row(
                Column(DateYearPickerField('date_published'), css_class=CSS_COL_CLS),
                Column(DateYearPickerField('date_impact'), css_class=CSS_COL_CLS)
            ),
            Row(
                Column(Field('country'), 
                       css_class='col-12', )
                ), 
            Row(
                Column(CompanyWBtn(fieldname = 'company',
                                   mainmodel = 'impev'), 
                       css_class=CSS_COL_CLS, ),
                
                Column(ReferenceWBtn(), 
                       css_class=CSS_COL_CLS, )
            ),
            
            Row(
                Column(Field('sust_domain'
                             ),                           
                             css_class=CSS_COL_CLS),
                Column(Field('sust_tendency'
                             ),                           
                             css_class=CSS_COL_CLS)
            ),

            
            Field('sust_tags', data_url=reverse_lazy('etilog:get_sust_tags')),
            Field('summary', rows= 3),
            Field('comment', rows= 3),
            
            Row(Column(Field('date_text'), css_class=CSS_COL_CLS)),
            Field('article_title'),
            Field('article_text'),
            Field('article_html'),
            Field('result_parse_html'),
            
            ImpactEventBtns(),
        )
        
                  
    class Meta: #only for model fields
        model = ImpactEvent
        fields = ['source_url', 'date_published', 'date_impact', 'company', 'reference', 
                  'country',
                  'sust_domain', 'sust_tendency', 'sust_tags',
                  'summary', 'comment',
                  'article_text', 'article_title', 'date_text', 'article_html', 'result_parse_html'
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
            'country': ('where did it happen'),
        }
        help_texts = {
           'date_published': (''),
           'date_impact': (''),
        }
        


class CompanyForm(forms.ModelForm):
    '''
    form to create a company
    '''
    owner = forms.ModelMultipleChoiceField(queryset=Company.objects.all(),
                                           required = False) #for validation
    subsidiary = forms.ModelMultipleChoiceField(queryset=Company.objects.all(),
                                                required = False)
    supplier = forms.ModelMultipleChoiceField(queryset=Company.objects.all(),
                                              required = False)
    recipient = forms.ModelMultipleChoiceField(queryset=Company.objects.all(),
                                               required = False)
    def __init__(self, *args, **kwargs):
        super (CompanyForm,self ).__init__(*args,**kwargs) 
        
        self.fields['owner'].widget = CompanyWidget()
        self.fields['subsidiary'].widget = CompanyWidget()
        self.fields['supplier'].widget = CompanyWidget()
        self.fields['recipient'].widget = CompanyWidget()
        
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
    
    def save(self, commit=True):
        main = self.instance
        main.save() #save main instance
        #add relations:
        if self.cleaned_data['subsidiary'] is not None:
            for comp in self.cleaned_data['subsidiary']: #comes as queryset
                SubsidiaryOwner.objects.update_or_create(owner_company = main, 
                                                         subsidiary_company = comp )
        if self.cleaned_data['owner'] is not None:
            for comp in self.cleaned_data['owner']: #comes as queryset
                SubsidiaryOwner.objects.update_or_create(owner_company = comp, 
                                                         subsidiary_company = main)
        if self.cleaned_data['supplier'] is not None:
            for comp in self.cleaned_data['supplier']: #comes as queryset
                SupplierRecipient.objects.update_or_create(recipient_company = main, 
                                                         supplier_company = comp)
        if self.cleaned_data['recipient'] is not None:
            for comp in self.cleaned_data['recipient']: #comes as queryset
                SupplierRecipient.objects.update_or_create(recipient_company = comp, 
                                                         supplier_company = main)
        return main
    
    class Meta: #only for model fields
        model = Company
        exclude = ['owner_old', 'subsidiary_old', 'supplier_old', 'recipient_old',
                   'subsidiary_to_owner', 'supplier_to_recipient'
                   ]





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

        
class ImpEvShow(forms.ModelForm):
    '''
    form to show details of impact event
    '''
    def __init__(self, *args, **kwargs):
        super(ImpEvShow, self).__init__(*args, **kwargs)
        
        
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'col-12 d-flex flex-wrap'
        self.helper.layout = Layout(
            Readonly('reference'),
            HTML("""
            <p>, <strong>please help us {{  form.initial.article_title }}</strong></p>
        """),
            )
            
            
            
    class Meta: #only for model fields
        model = ImpactEvent
        fields = ['source_url', 'date_published', 'date_impact', 'company', 'reference', 
                  'country',
                  'sust_domain', 'sust_tendency', 'sust_tags',
                  'summary', 'comment',
                  'article_text', 'article_title', 'date_text', 'article_html', 'result_parse_html'
                  ]
    
        
        

        labels = {
            'date_published': ('when was it published'),
            'date_impact': ('when did it happen'),
            'reference': ('where was it published'),
            'company': ('which company was concerned'),
            'country': ('where did it happen'),
        }
        help_texts = {
           'date_published': (''),
           'date_impact': (''),
        }

