'''
Created on 15 Mar 2019

@author: daim
'''
from django import forms
from django.urls import reverse_lazy

#crispoy
from crispy_forms.layout import Layout, Field, Row, Column, Submit, Button, HTML, ButtonHolder
from crispy_forms.bootstrap import  InlineRadios, FieldWithButtons, StrictButton
#datepicker
from bootstrap_datepicker_plus import DatePickerInput

#models
from .models import Company, Reference, SustainabilityDomain, SustainabilityTendency

D_FORMAT = '%d.%m.%Y'
D_YEARFORMAT = '%Y'

class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)

class AutocompleteWidget(forms.TextInput):
    def __init__(self, data_list, placeholder, *args, **kwargs):
        super(AutocompleteWidget, self).__init__(*args, **kwargs)
        
        sepa = ';'
        list_str = sepa.join(list(data_list))
        
        self.attrs.update({'autocomplete': 'off',
                      'data_list': list_str,
                      'placeholder': placeholder,
                      'class': 'autocompwidget'}) #used for jquery

class CompanyWidget(AutocompleteWidget):
    def __init__(self, *args, **kwargs):       
        #when excluding companies in Reference -> excludes also companies which are both.
        q_comp_val = Company.objects.values_list('name', flat = True)
        AutocompleteWidget.__init__(self, data_list = q_comp_val, 
                                    placeholder = 'Company', *args, **kwargs)
        
class ReferenceWidget(AutocompleteWidget):
    def __init__(self, *args, **kwargs):
        q_references = Reference.objects.values_list('name', flat = True)
        AutocompleteWidget.__init__(self, data_list = q_references, 
                                    placeholder = 'Newspaper', *args, **kwargs)
                

class CompanyWBtn(Layout):
    def __init__(self, fieldname, mainmodel,  *args, **kwargs):
        super(CompanyWBtn, self).__init__(
            FieldWithButtons(fieldname, 
                                    StrictButton("+", css_class='btn btn-light add_foreignmodel', #class for jquery
                                    #css_id='add_id_company',
                                    add_url=reverse_lazy('etilog:add_foreignmodel', 
                                                         kwargs={'main_model': mainmodel,
                                                             'foreign_model': fieldname})
                                        ))
                        )


class ReferenceWBtn(Layout):
    def __init__(self, *args, **kwargs):
        super(ReferenceWBtn, self).__init__(
            FieldWithButtons('reference', 
                                        StrictButton("+", css_class='btn btn-light add_foreignmodel',
                                        #css_id='add_id_reference',                                       
                                        add_url=reverse_lazy('etilog:add_foreignmodel', 
                                                             kwargs={'main_model': 'impev',
                                                                 'foreign_model': 'reference'})
                                            ))                                       
                        )
                            
                                    
class DateYearPicker(DatePickerInput):
    def __init__(self, *args, **kwargs):
        super(DateYearPicker, self).__init__(
            format = D_FORMAT, #django datetime format
                
            options={'viewMode': 'years', 
                     'useCurrent': False, #needed to take initial date
                     'extraFormats': ['DD.MM.YY', 'DD.MM.YYYY' ], #javascript format
                     },
            )
        
class RowTagsInput(Layout):
    def __init__(self, field_name,  col_class,  field_class = '', field_id = None, row_id=None, *args, **kwargs):
        if field_id == None:
            field_id = 'id_f_' + field_name 
        if row_id == None:
            row_id = 'id_row_f_' + field_name
        cls_taginp = 'f_tagsinput'
        super(RowTagsInput, self).__init__(           
            Row(
                    Column(Field(field_name, id = field_id,
                            #data_role='tagsinput',  
                             #disabled=True, 
                             #readonly=True,
                             css_class = ' '.join([cls_taginp, field_class]) 
                           ),
                            css_class = col_class                             
                        ),
                css_class='row_tags_class',
                id = row_id
                )
            )
                    
class ColDomainBtnSelect(Layout):
    def __init__(self, col_class= 'col-12 col-lg-6', *args, **kwargs): #distribute buttons
        q = SustainabilityDomain.objects.all()
        btn_list = []
        for dom in q:
            btn = Button(dom.id, dom.name, css_class='btnselect btn-outline-info btn-sm',  #'active btn-light',  
                               css_id = 'id-sust_domain-btn-' + str(dom.id),
                               data_toggle='button',
                               aria_pressed = "false",
                               targfield = 'id_sust_domain') 
            btn_list.append(btn)
            
        html_str = '<label class="col-form-label">Which Field</label>'
        super(ColDomainBtnSelect, self).__init__( 
                           
            Column(HTML(html_str),
                   ButtonHolder(*btn_list),
                css_class = col_class  ) 
            )    

class ColTendencyBtnSelect(Layout):
    def __init__(self, col_class= 'col-12 col-lg-6', *args, **kwargs): #distribute buttons
        q = SustainabilityTendency.objects.all()
        btn_list = []
        for tend in q:
            bntclass = 'btnselect btn-sm btn-outline-'
            if 'negativ' in tend.name :
                csscls =  bntclass + 'danger'
            
            elif 'positiv' in tend.name :
                csscls =  bntclass + 'success'
            else: # 'controv' in tend.name :
                csscls =  bntclass +'warning'
            btn = Button(tend.id, tend.name, css_class=csscls,  #'active btn-light',  
                               css_id = 'id-sust_tendency-btn-' + str(tend.id),
                               data_toggle='button',
                               aria_pressed = "false",
                               targfield = 'id_sust_tendency') 
            btn_list.append(btn)
            
        html_str = '<label class="col-form-label">Which Tendency</label>'
        super(ColTendencyBtnSelect, self).__init__( 
                           
            Column(HTML(html_str),
                   ButtonHolder(*btn_list),
                css_class = col_class  ) 
            )                           
