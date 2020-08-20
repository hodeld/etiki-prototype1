from crispy_forms.bootstrap import FieldWithButtons, StrictButton, AppendedText
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, HTML, Column, Field, Row, Div
from django import forms
from django.urls import reverse_lazy

from etilog.forms.fields_filter import dom_icon_dict
from etilog.models import Company, Reference, SustainabilityDomain, SustainabilityTendency


class CharF(forms.CharField):
    def __init__(self, *args, **kwargs):
        lbl = kwargs.pop('label', '')
        req = kwargs.pop('required', True)
        super(CharF, self).__init__(required=req, label=lbl, *args, **kwargs)


class AutocompleteWidget(forms.TextInput):
    def __init__(self, data_list, placeholder, *args, **kwargs):
        super(AutocompleteWidget, self).__init__(*args, **kwargs)

        sepa = ';'
        list_str = sepa.join(list(data_list))

        self.attrs.update({'autocomplete': 'off',
                           'data_list': list_str,
                           'placeholder': placeholder,
                           'class': 'autocompwidget'})  # used for jquery


class CompanyWidget(AutocompleteWidget):
    def __init__(self, *args, **kwargs):
        # when excluding companies in Reference -> excludes also companies which are both.
        q_comp_val = Company.objects.values_list('name', flat=True)
        AutocompleteWidget.__init__(self, data_list=q_comp_val,
                                    placeholder='Company', *args, **kwargs)


class ReferenceWidget(AutocompleteWidget):
    def __init__(self, *args, **kwargs):
        q_references = Reference.objects.values_list('name', flat=True)
        AutocompleteWidget.__init__(self, data_list=q_references,
                                    placeholder='Newspaper', *args, **kwargs)


class CompanyWBtn(Layout):
    def __init__(self, fieldname, mainmodel, *args, **kwargs):
        super(CompanyWBtn, self).__init__(
            FieldWithButtons(fieldname,
                             StrictButton("+", css_class='btn btn-light add_foreignmodel',  # class for jquery
                                          # css_id='add_id_company',
                                          add_url=reverse_lazy('etikicapture:add_foreignmodel',
                                                               kwargs={'main_model': mainmodel,
                                                                       'foreign_model': fieldname})
                                          ))
        )


class ReferenceWBtn(Layout):
    def __init__(self, *args, **kwargs):
        super(ReferenceWBtn, self).__init__(
            FieldWithButtons('reference',

                             StrictButton("+", css_class='btn btn-light add_foreignmodel',
                                          # css_id='add_id_reference',
                                          add_url=reverse_lazy('etikicapture:add_foreignmodel',
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
                                          url_get=reverse_lazy('etikicapture:extract_text_url', )
                                          ))
        )


class ImpactEventBtns(Layout):
    def __init__(self):
        super(ImpactEventBtns, self).__init__(
            ButtonHolder(
                Submit('submit', 'Save Impact Event', css_class='btn btn-secondary'),
                Button('new', 'New', css_class='btn btn-secondary', onclick="new_ie();"),
                Button('next', 'Next', css_class='btn btn-light', onclick="next_ie();")
            )
        )


class Readonly(Layout):

    def __init__(self, fieldname, *args, **kwargs):
        html_str = '<p class="rdonly">{{ form.initial.reference }}</p>'  # % fieldname
        super(Readonly, self).__init__(
            HTML(html_str)
        )


class LabelInputRow(Layout):
    def __init__(self, rowcontent,
                 labelname=None,
                 row_class='',
                 *args, **kwargs):  # distribute buttons

        if not isinstance(rowcontent, list):
            rowcontent = [rowcontent]

        if labelname:
            html_str = '<label class="col-form-label">%s</label>' % labelname
            label_html = HTML(html_str)
        else:
            label_html = HTML('')

        super(LabelInputRow, self).__init__(
            Row(
                Column(
                    label_html,
                    Div(
                        Row(*rowcontent, *args, **kwargs),
                        #css_class=' '.join([div_class, ]),
                        #css_id=div_id
                    ),
                    css_class='col-12'

                ),
                css_class='justify-content-center ' + row_class
            )
        )


class TagsButton(Layout):
    def __init__(self, field_name, col_class, labelname='', field_class='',
                 placeholder=None,
                 field_id=None,
                 taginput=True,
                 addmodel=True,
                 icon_name=None,
                 *args, **kwargs):
        if field_id == None:
            field_id = 'id_c_' + field_name
        if placeholder == None:
            placeholder = labelname
        name_stripped = field_name
        parent_id = '#id_parent_' + name_stripped  # same as labelrow
        div_id = 'row' + name_stripped  # needed for set placeholder

        div_class = ' '.join([col_class, 'div_c_taginput'])

        if taginput:
            if isinstance(taginput, str):
                cls_taginp = taginput
            else:
                cls_taginp = 'c_tags_search_inp'
        else:
            cls_taginp = ''

        if addmodel:
            icon_name = 'fas fa-plus-square'
            icon_str = '''<i class="%s" ></i>''' % icon_name

            add_url = reverse_lazy('etikicapture:add_foreignmodel',
                                   kwargs={'main_model': 'impev',
                                           'foreign_model': field_name})
            h_css_class = 'input-group-text add_foreignmodel'
            html_str = '<span class="%s" add-url="%s" field-id="%s">%s</span' % (h_css_class, add_url, field_id, icon_str)
        else:
            if icon_name:
                onclick = 'extract_text(this);'
                url_get = reverse_lazy('etikicapture:extract_text_url')
                h_css_class = 'input-group-text'
                icon_str = '''<i class="%s" ></i>''' % icon_name
                html_str = '<span class="%s" url-get="%s" onclick="%s">%s</span' % (h_css_class, url_get,
                                                                                    onclick, icon_str)
            else:
                html_str = ''

        rowcontent = Column(
            FieldWithButtons(
                Field(field_name,

                  id=field_id,
                  parfield=parent_id,

                  css_class=' '.join([cls_taginp, field_class]),
                  placeholder=placeholder,
                  ),

                HTML(html_str
                             )
            ),
            css_class=div_class,
            css_id=div_id,
        )
        super(TagsButton, self).__init__(rowcontent)


class RowTagsButton(LabelInputRow):
    def __init__(self, *args, **kwargs):
        LabelInputRow.__init__(self, TagsButton(*args, **kwargs))


class ColBtnSwitch(Layout):
    def __init__(self, btn_list, col_class, labelname,
                 wrap_class,
                 *args, **kwargs):
        if col_class is None:
            col_class = 'col-12'
        if wrap_class is None:
            wrap_class = ' '.join(['justify-content-around d-flex flex-wrap w-100', 'switches_wrap'])

        btn_ele_li = []
        sw_cls = 'custom-control-input swselect'
        for (cont, name, val, css_clss, css_id, targfield) in btn_list:

            sw_div_cls = 'custom-control custom-switch my-auto'
            div_css_clss = ' '.join([sw_div_cls, css_clss])
            inp_str = '''
            <input type="checkbox" 
            class="%s" id="%s" name="%s" data-value="%s" data-target="%s">
            ''' % (sw_cls, css_id, name, val, targfield)
            inp = HTML(inp_str)
            lab_str = '<label class="custom-control-label" for="%s"><span>%s</span></label>' % (css_id, cont)
            lab = HTML(lab_str)
            div = Div(inp, lab, css_class=div_css_clss,
                      )
            div_frame = Div(div, css_class='switch-wrapper py-2 ml-3')

            # $('#id_sust_domain-btn-2')[0].checked

            btn_ele_li.append(div_frame)
        # due to key error -> no string (which is not field name) as 1st argument
        if labelname:
            html_str = '<label class="col-form-label">%s</label>' % labelname
            label_html = HTML(html_str)
            col = Column(label_html,
                         Div(*btn_ele_li, css_class=wrap_class,),
                         css_class=col_class)

        else:
            col = Column(Div(*btn_ele_li, css_class=wrap_class),
                         css_class=col_class)

        super(ColBtnSwitch, self).__init__(col)


class ColDomainSelect(ColBtnSwitch):
    def __init__(self, col_class=None, labelname=None,
                 btn_wrap_class=None,
                 ele_class='',
                 *args, **kwargs):  # distribute buttons
        q = SustainabilityDomain.objects.all()
        ele_list = []
        icon_str = '<i class="fas %s mr-1"></i>'
        sw_cls = 'switch-etiki'
        for dom in q:
            icon_name = dom_icon_dict[dom.id]
            cont = icon_str % icon_name + dom.name
            ele = (cont, dom.id, dom.name,
                   ' '.join([ele_class, sw_cls]),
                   'id_sust_domain_sw' + str(dom.id),
                   'id_sust_domain',
                   )
            ele_list.append(ele)

        ColBtnSwitch.__init__(self, ele_list,
                              col_class, labelname,
                              btn_wrap_class,
                              *args, **kwargs)


class ColTendencySelect(ColBtnSwitch):
    def __init__(self, col_class=None, labelname=None,
                 btn_wrap_class=None,
                 ele_class='',
                 twin_ele=False,
                 *args, **kwargs):  # distribute buttons
        q = SustainabilityTendency.objects.all()
        btn_list = []
        ele_base_cls = 'switch-'
        for tend in q:
            if 'negativ' in tend.name:
                csscls = ele_base_cls + 'danger'

            elif 'positiv' in tend.name:
                csscls = ele_base_cls + 'success'
            else:  # 'controv' in tend.name :
                csscls = ele_base_cls + 'warning'
            css_class = ' '.join([csscls, ele_class])

            cont = tend.name
            name = tend.id
            val = tend.name
            css_id = 'id_sust_tendency_sw' + str(tend.id)
            targfield = 'id_sust_tendency'

            btn_list.append((cont, name, val, css_class, css_id, targfield))

        ColBtnSwitch.__init__(self, btn_list,
                              col_class, labelname,
                              btn_wrap_class,
                              twin_ele,
                              *args, **kwargs)