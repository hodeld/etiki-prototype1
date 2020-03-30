'''
Created on 15 Mar 2019

@author: daim
'''
from django import forms
from django.urls import reverse_lazy
from django.db.models import Count

#crispoy
from crispy_forms.layout import Layout, Field, Row, Column, Div, Button, HTML, ButtonHolder, Submit
from crispy_forms.bootstrap import  InlineRadios, FieldWithButtons, StrictButton, AppendedText
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
                     'useCurrent': False, #needed to take initial dat
                     'extraFormats': ['DD.MM.YY', 'DD.MM.YYYY' ], #javascript format
                     },
            )
class DateYearPickerField(Layout):
    def __init__(self, field_name, placeholder = '', *args, **kwargs):
        super(DateYearPickerField, self).__init__(           
            Field(field_name, autocomplete='off', wrapper_class='datepicker',
                  placeholder = placeholder, 
                   *args, **kwargs)
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
                                 parfield = '#id_row_f_',
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
class ColBtnSelect(Layout):
    def __init__(self, btn_list, col_class, labelname, 
                 btn_wrap_class,
                 twin_ele,
                 *args, **kwargs): 
        if col_class is None:
            col_class= 'col-12'
        if btn_wrap_class is None:
            btn_wrap_class = 'justify-content-around d-flex flex-wrap w-100'
            
        if labelname:    
            html_str = '<label class="col-form-label">%s</label>' % labelname
            label_html = HTML(html_str)
        else:
            label_html = ''
        if twin_ele == True:
            id_pref = 'twin-'
            twin_pref = ''
        else:
            id_pref = ''
            twin_pref = 'twin-'
        btn_ele_li = []
        for (cont, name, val, css_clss, css_id, targfield) in btn_list:
            
            btn = StrictButton(cont, name = name, 
                               value = val, 
                               css_class = css_clss,
                               css_id = id_pref+css_id,
                               data_toggle='button',
                               aria_pressed = "false",
                               targfield = targfield,
                               twin_id = twin_pref+css_id
                               ) 
            btn_ele_li.append(btn)
        
        super(ColBtnSelect, self).__init__( 
                           
            Column(label_html,
                   Div(*btn_ele_li, css_class = btn_wrap_class),
                css_class = col_class  ) 
            )    
                      
class ColDomainBtnSelect(ColBtnSelect):
    def __init__(self, col_class= None, labelname= None, 
                 btn_wrap_class = None,
                  ele_class = '',
                  twin_ele = False,
                 *args, **kwargs): #distribute buttons
        q = SustainabilityDomain.objects.all()
        btn_list = []
        icon_str = '<i class="fas %s mr-1"></i>' 
        for dom in q:
            
            icon_name = dom_icon_dict[dom.id]
            cont = icon_str % icon_name + dom.name 
            btn = (cont,  dom.id, dom.name, 
                    ele_class + ' btnselect btn-outline-info btn-sm',  #'active btn-light',  
                    'id_sust_domain-btn-' + str(dom.id),
                    'id_sust_domain',
                   ) 
            btn_list.append(btn)

        ColBtnSelect.__init__(self, btn_list, 
                              col_class, labelname,
                              btn_wrap_class,
                              twin_ele,
                              *args, **kwargs)  
 

class ColTendencyBtnSelect(ColBtnSelect):
    def __init__(self, col_class= None, labelname= None, 
                 btn_wrap_class = None,
                  ele_class = '',
                 twin_ele = False,                
                  *args, **kwargs): #distribute buttons
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
            cont = tend.name
            name = tend.id
            val = tend.name
            css_class= ' '.join([ele_class, csscls])
            css_id = 'id_sust_tendency-btn-' + str(tend.id)
            targfield = 'id_sust_tendency'
            
            btn_list.append((cont, name, val, css_class, css_id, targfield))

        ColBtnSelect.__init__(self, btn_list, 
                              col_class, labelname,
                              btn_wrap_class,
                              twin_ele,
                              *args, **kwargs)  

class TendencyLegende(Layout):
    def __init__(self, *args, **kwargs): 
        q = SustainabilityTendency.objects.all() #double query as above
        ele_list = []
        icon_name = 'fa-dot-circle'
        icon_str = '<i class="fas %s mr-1"></i>' % icon_name
        col_class = "col-12 d-flex flex-wrap justify-content-start chart-legend"
        for tend in q:
            eleclass = 'text-'
            if 'negativ' in tend.name :
                csscls =  'danger'
            
            elif 'positiv' in tend.name :
                csscls =   'success'
            else: # 'controv' in tend.name :
                csscls =  'warning'
            
            cont = icon_str +  tend.name
            css_class = eleclass + csscls + ' mx-3 text-uppercase'
            ele = HTML('<span class="%s"> %s </span>' % (css_class, cont)) 
            ele_list.append(ele)
            
        
        super(TendencyLegende, self).__init__( 
                           
            Div(*ele_list,
                css_class = col_class  ) 
            )  

class RowTopics(Layout):
    def __init__(self, col_class= 'col-12', labelname= '', *args, **kwargs): #distribute buttons
        #q = SustainabilityTag.objects.all()[:5]
        nr_tags = 2
        li_vals = []
        li_sustagsid = []
        #hits DB 5 times -> better 1 query
        for i in range(1,6):
            vals = ImpactEvent.objects.filter(
                        sust_domain = i).values_list(
                            'sust_tags__id', 'sust_tags__name').annotate(
                                tag_count=Count('sust_tags')).order_by(
                                    '-tag_count')[:nr_tags]
            

            li_vals.extend(vals)
        
        topics_list = []
        a_str = '''<a href="#" class="topic-link link-intern" tagid = "%d" tagname = "%s" >%s</a>'''
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
        
        cnt_filters = '<small id="filter-count">0</small>'
        super(SearchWBtn, self).__init__(           
            FieldWithButtons(
                Field(fieldname, *args, **kwargs),
                                        StrictButton(img_1 + img_2 + cnt_filters, 
                                         css_class='btn-dark m-0 px-3 py-0 z-depth-0', 
                                         css_id='btn_filter_toggle', 
                                         onclick="toggle_filter_frombtn()"),
                                    css_id='div_id_search'


                #for prepend: change template -> span before, prepend-class
                )
            )
class SearchWIcon(Layout):
    def __init__(self, fieldname,  *args, **kwargs):

        icon_str = '<i class="fa fa-search "></i>'
        super(SearchWIcon, self).__init__(           
            AppendedText(fieldname, icon_str, *args, **kwargs)
                #Field(fieldname, *args, **kwargs),
                #'icon_str')
            #, css_id='div_id_search')
            )


class BtnIcon(Layout):
    def __init__(self, col_class= 'col-12 ',
                 sname = 'Filter',
                 icon_name = 'fa-filter',
                  *args, **kwargs): #distribute buttons

        icon_str = '<i class="fas %s mr-1"></i>' 

        cont = icon_str % icon_name + sname
        btn = StrictButton(cont, name = 'btnfilter', value = 'filter', 
                           css_class='btn-outline-light btn-block',  #'active btn-light',  ) 
                           )

        super(BtnIcon, self).__init__(
            Column(
                btn, css_class = col_class + ' mt-1'
                )
            ) 

class LabelRow(Layout):   
    def __init__(self, rowcontent, labelname,
                 row_class = '',
                  *args, **kwargs): #distribute buttons
        
        name_stripped = labelname.replace(' ', '')
        div_id = 'row'+ name_stripped
        icon_str = '<i class="fas fa-chevron-down ml-1"></i> '
        cont = labelname + icon_str 
        btn = StrictButton(cont, name = 'btn'+ name_stripped, value = name_stripped, 
                            data_toggle='collapse', data_target='#' + div_id,
                           css_class='btn-link btn-filter-row btn-block btn-sm   mt-1',  #'active btn-light',  ) 
                           )
                
                
        
        super(LabelRow, self).__init__(
            Row(
                Column(
                    btn,
                    Div(
                        Row(rowcontent, *args, **kwargs),
                        css_class = 'collapse ', css_id = div_id
                        ),
                    css_class = 'col-12 col-md-10'
                    
                    ),
                css_class = 'justify-content-center ' + row_class
            )
            )

class LabelRowTagsInput(LabelRow):
    def __init__(self, field_name,  col_class, labelname, field_class = '',
                 placeholder = None,
                  field_id = None, 
                  *args, **kwargs):
        if field_id == None:
            field_id = 'id_f_' + field_name 
        if placeholder == None:
            placeholder = labelname
        name_stripped = labelname.replace(' ', '')
        parent_id = '#row'+ name_stripped #same as labelrow
        cls_taginp = 'f_tagsinput'
        rowcontent = Column(Field(field_name, id = field_id,
                                 parfield = parent_id,
                                 
                                 css_class = ' '.join([cls_taginp, field_class]) ,
                                 placeholder = 'Search ' + placeholder,
                           ),
                            css_class = col_class                             
                        )
        
        LabelRow.__init__(self, rowcontent, labelname)
        

        