'''
Created on 15 Mar 2019

@author: daim
'''
from django import forms
from django.urls import reverse_lazy
from django.db.models import Count

#crispoy
from crispy_forms.layout import Layout, Field, Row, Column, Div, Button, HTML, ButtonHolder, Submit
from crispy_forms.bootstrap import  InlineRadios, FieldWithButtons, StrictButton
#datepicker
from bootstrap_datepicker_plus import DatePickerInput

#models
from etilog.models import Company, Reference, SustainabilityDomain, SustainabilityTendency, SustainabilityTag
from etilog.models import ImpactEvent

D_FORMAT = '%d.%m.%Y'
D_YEARFORMAT = '%Y'

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
class UrlWBtn(Layout):
    def __init__(self, fieldname, *args, **kwargs):
        super(UrlWBtn, self).__init__(
            FieldWithButtons(fieldname, 
                                        StrictButton('get', css_class='btn btn-light',
                                        onclick="extract_text(this);",                                      
                                        url_get=reverse_lazy('etilog:extract_text_url',)
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
class DateYearPickerField(Layout):
    def __init__(self, field_name,  *args, **kwargs):
        super(DateYearPickerField, self).__init__(           
            Field(field_name, autocomplete='off', wrapper_class='datepicker')
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

dom_icon_dict ={1: 'fa-users',  #People
                2:  'fa-hippo', #   Animals
                3: 'fa-tree', #  Environment
                4: 'fa-balance-scale-left', #   Politics
                5: 'fa-store',#   Products& Services                
                }  
              
class ColDomainBtnSelect(Layout):
    def __init__(self, col_class= 'col-12 col-lg-6', labelname= 'Category', *args, **kwargs): #distribute buttons
        q = SustainabilityDomain.objects.all()
        btn_list = []
        icon_str = '<i class="fas %s mr-1"></i>' 
        for dom in q:
            
            icon_name = dom_icon_dict[dom.id]
            cont = icon_str % icon_name + dom.name 
            btn = StrictButton(cont, name = dom.id, value = dom.name, css_class='btnselect btn-outline-info btn-sm',  #'active btn-light',  
                               css_id = 'id-sust_domain-btn-' + str(dom.id),
                               data_toggle='button',
                               aria_pressed = "false",
                               targfield = 'id_sust_domain') 
            btn_list.append(btn)
            
        html_str = '<label class="col-form-label">%s</label>' % labelname
        super(ColDomainBtnSelect, self).__init__( 
                           
            Column(HTML(html_str),
                   ButtonHolder(*btn_list),
                css_class = col_class  ) 
            )    

class ColTendencyBtnSelect(Layout):
    def __init__(self, col_class= 'col-12 col-lg-6', labelname= 'Which Tendency', *args, **kwargs): #distribute buttons
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
            
        html_str = '<label class="col-form-label">%s</label>' % labelname
        super(ColTendencyBtnSelect, self).__init__( 
                           
            Column(HTML(html_str),
                   ButtonHolder(*btn_list),
                css_class = col_class  ) 
            )   

class RowTopics(Layout):
    def __init__(self, col_class= 'col-12', labelname= '', *args, **kwargs): #distribute buttons
        #q = SustainabilityTag.objects.all()[:5]
        nr_tags = 2
        li_vals = []
        li_sustagsid = []
        for i in range(1,6):
            vals = ImpactEvent.objects.filter(
                        sust_domain = i).values_list(
                            'sust_tags__id', 'sust_tags__name').annotate(
                                tag_count=Count('sust_tags')).order_by(
                                    '-tag_count')[:nr_tags]
            

            li_vals.extend(vals)
        
        topics_list = []
        a_str = '''<a href="#" class="topic-link" tagid = "%d" tagname = "%s" >%s</a>'''
        k = nr_tags
        for tag in li_vals:
            stag_id = tag[0]           
            if stag_id in li_sustagsid: #no double entries
                k +=  1
                continue
            li_sustagsid.append(stag_id)
            if k%nr_tags == 0:
                addclass = '' 
            else:
                addclass = ' d-none d-md-block' #only show on larger screens
            html_str = a_str % (stag_id, tag[1], tag[1]) #(tag.id, tag.name, tag.name)           
            a_link = HTML(html_str)
            div_a = Div(a_link, css_class = 'div_topic_li' + addclass)
            topics_list.append(div_a)
            k += 1
            
        html_str = '<label class="col-form-label">%s</label>' % labelname
        super(RowTopics, self).__init__( 
            Row(
                           
                Column(HTML(html_str),
                       Div(*topics_list, css_class = 'd-flex flex-wrap'), #to wrap elements
                    css_class = col_class  )  
                )
            )                           

class ImpactEventBtns(Layout):
    def __init__(self):
        super(ImpactEventBtns, self).__init__( 
            ButtonHolder(
                Submit('submit', 'Save Impact Event', css_class='btn btn-secondary' ),
                Button('new', 'New', css_class='btn btn-secondary', onclick="new_ie();" ),
                Button('next', 'Next', css_class='btn btn-light', onclick="next_ie();" )
                )
            ) 
class Readonly(Layout):

    
    def __init__(self, fieldname,  *args, **kwargs):
        html_str = '<p class="rdonly">{{ form.initial.reference }}</p>' #% fieldname
        super(Readonly, self).__init__(
            HTML(html_str)           
            )
            #)
class SearchWBtn(Layout):
    def __init__(self, fieldname,  *args, **kwargs):
        
        img_1 = '<img class="icon collapse" id="icon_filter_active" alt="icon-filter" src="/static/etilog/img/icon/filter_active.png">'
        img_2 = '<img class="icon collapse show" id="icon_filter" alt="icon-filter" src="/static/etilog/img/icon/filter_nonact.png">'
        
        super(SearchWBtn, self).__init__(           
            FieldWithButtons(
                Field(fieldname, *args, **kwargs),
                            StrictButton(img_1+img_2, css_class='btn-dark m-0 px-3 py-0 z-depth-0', 
                            css_id='btn_filter_toggle', 
                            onclick="toggle_filter_frombtn()"),
                            css_id='div_id_search'
                #for prepend: change template -> span before, prepend-class
                )
            )

