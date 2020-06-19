'''
Created on 15 Mar 2019

@author: daim
'''

# crispoy
from crispy_forms.layout import Layout, Field, Row, Column, Div, HTML
from crispy_forms.bootstrap import StrictButton, AppendedText
# datepicker
from bootstrap_datepicker_plus import DatePickerInput

# models
from etilog.models import SustainabilityDomain, SustainabilityTendency

D_FORMAT = '%d.%m.%Y'
D_YEARFORMAT = '%Y'


class DateYearPicker(DatePickerInput):
    def __init__(self, *args, **kwargs):
        super(DateYearPicker, self).__init__(

            format=D_FORMAT,  # django datetime format

            options={'viewMode': 'years',
                     'useCurrent': False,  # needed to take initial dat
                     'extraFormats': ['DD.MM.YY', 'DD.MM.YYYY'],  # javascript format
                     },
        )


class DateYearPickerField(Layout):
    def __init__(self, field_name, placeholder='', *args, **kwargs):
        super(DateYearPickerField, self).__init__(
            Field(field_name, autocomplete='off', wrapper_class='datepicker',
                  placeholder=placeholder,
                  *args, **kwargs)
        )


dom_icon_dict = {1: 'fa-users',  # People
                 2: 'fa-hippo',  # Animals
                 3: 'fa-tree',  # Environment
                 4: 'fa-balance-scale-left',  # Politics
                 5: 'fa-store',  # Products& Services
                 }


class ColBtnSelect(Layout):
    def __init__(self, btn_list, col_class, labelname,
                 btn_wrap_class,
                 twin_ele,
                 *args, **kwargs):
        if col_class is None:
            col_class = 'col-12'
        if btn_wrap_class is None:
            btn_wrap_class = 'justify-content-around d-flex flex-wrap w-100'

        if twin_ele == True:
            id_pref = 'twin-'
            twin_pref = ''
        else:
            id_pref = ''
            twin_pref = 'twin-'
        btn_ele_li = []
        for (cont, name, val, css_clss, css_id, targfield) in btn_list:
            btn = StrictButton(cont, name=name,
                               value=val,
                               css_class=css_clss,
                               css_id=id_pref + css_id,
                               data_toggle='button',
                               aria_pressed="false",
                               targfield=targfield,
                               twin_id=twin_pref + css_id
                               )
            btn_ele_li.append(btn)
        # due to key error -> no string (which is not field name) as 1st argument
        if labelname:
            html_str = '<label class="col-form-label">%s</label>' % labelname
            label_html = HTML(html_str)
            col = Column(label_html,
                         Div(*btn_ele_li, css_class=btn_wrap_class),
                         css_class=col_class)

        else:
            col = Column(Div(*btn_ele_li, css_class=btn_wrap_class),
                         css_class=col_class)

        super(ColBtnSelect, self).__init__(col)


class ColDomainBtnSelect(ColBtnSelect):
    def __init__(self, col_class=None, labelname=None,
                 btn_wrap_class=None,
                 ele_class='',
                 twin_ele=False,
                 *args, **kwargs):  # distribute buttons
        q = SustainabilityDomain.objects.all()
        btn_list = []
        icon_str = '<i class="fas %s mr-1"></i>'
        for dom in q:
            icon_name = dom_icon_dict[dom.id]
            cont = icon_str % icon_name + dom.name
            btn = (cont, dom.id, dom.name,
                   ele_class + ' btnselect btn-outline-info btn-sm',  # 'active btn-light',
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
    def __init__(self, col_class=None, labelname=None,
                 btn_wrap_class=None,
                 ele_class='',
                 twin_ele=False,
                 *args, **kwargs):  # distribute buttons
        q = SustainabilityTendency.objects.all()
        btn_list = []
        for tend in q:
            bntclass = 'btnselect btn-sm btn-outline-'
            if 'negativ' in tend.name:
                csscls = bntclass + 'danger'

            elif 'positiv' in tend.name:
                csscls = bntclass + 'success'
            else:  # 'controv' in tend.name :
                csscls = bntclass + 'warning'
            cont = tend.name
            name = tend.id
            val = tend.name
            css_class = ' '.join([ele_class, csscls])
            css_id = 'id_sust_tendency-btn-' + str(tend.id)
            targfield = 'id_sust_tendency'

            btn_list.append((cont, name, val, css_class, css_id, targfield))

        ColBtnSelect.__init__(self, btn_list,
                              col_class, labelname,
                              btn_wrap_class,
                              twin_ele,
                              *args, **kwargs)


SEARCH_WRAP_ClS = 'div_search_typeahead'  # for css


class SearchWIcon(Layout):
    def __init__(self, field_id, landing=False, *args, **kwargs):

        ph_filter = 'FILTER BY'
        ph_base = ' Companies, Countries, Topics, Newspaper …'
        ph_search = 'Search'
        icon_search = 'fa fa-search'
        if landing:
            ph = ph_search + ph_base
        else:
            ph = ph_filter + ph_base
        icon_str = '''<i class="%s" ></i>''' % icon_search
        super(SearchWIcon, self).__init__(
            AppendedText('search', icon_str,
                         id=field_id, autocomplete="off",
                         placeholder=ph,
                         data_phbase=ph_base,
                         data_phsearch=ph_search,
                         data_phfilter=ph_filter,
                         css_class='tt-input f_search',
                         wrapper_class=' '.join([SEARCH_WRAP_ClS, 'free_input']),

                         *args, **kwargs)
        )


class LabelRow(Layout):
    def __init__(self, rowcontent, labelname,
                 row_class='',
                 *args, **kwargs):  # distribute buttons

        name_stripped = labelname.replace(' ', '')
        div_id = 'row' + name_stripped
        div_class = 'taginput-row'
        icon_str = '<i class="fas fa-chevron-down ml-1"></i> '
        cont = labelname + icon_str
        btn = StrictButton(cont, name='btn' + name_stripped, value=name_stripped,
                           data_toggle='collapse', data_target='#' + div_id,
                           css_class='btn-link btn-block btn-sm mt-1',  # 'active btn-light',  )
                           )

        super(LabelRow, self).__init__(
            Row(
                Column(
                    btn,
                    Div(
                        Row(rowcontent, *args, **kwargs),
                        css_class=' '.join(['collapse show', div_class]),
                        css_id=div_id
                    ),
                    css_class='col-12 col-md-10'

                ),
                css_class='justify-content-center ' + row_class
            )
        )


class TagField(Layout):
    def __init__(self, field_name, cls_filterinput):
        super(TagField, self).__init__(
            Field(field_name, id='id_f_' + field_name,
                  css_class=cls_filterinput + ' f_tagsinput', type="hidden"),
        )


class AllTagsInput(Layout):
    def __init__(self, field_name, *args, **kwargs):
        wrapper_cls = ' '.join([kwargs.pop('wrapper_class', ''), 'alltaginput'])
        super(AllTagsInput, self).__init__(
            Field(field_name, id='id_f_' + field_name, css_class='f_alltagsinput',
                  wrapper_class=wrapper_cls,
                  *args, **kwargs
                  )
        )


class LabelRowTagsInput(LabelRow):
    def __init__(self, field_name, col_class, labelname, field_class='',
                 placeholder=None,
                 field_id=None,
                 *args, **kwargs):
        if field_id == None:
            field_id = 'id_f_' + field_name
        if placeholder == None:
            placeholder = labelname
        name_stripped = labelname.replace(' ', '')
        parent_id = '#row' + name_stripped  # same as labelrow
        cls_taginp = 'f_tags_search_inp'
        icon_search = 'fa fa-search'
        icon_str = '''<i class="%s" ></i>''' % icon_search

        rowcontent = Column(
            AppendedText(field_name, icon_str,
                         parfield=parent_id,
                         id=field_id, autocomplete="off",
                         placeholder=placeholder,
                         css_class=' '.join([cls_taginp, field_class]),
                         wrapper_class=' '.join([SEARCH_WRAP_ClS, 'not_free_input']),
                         *args, **kwargs
                         ),
            css_class=col_class
        )

        LabelRow.__init__(self, rowcontent, labelname)




