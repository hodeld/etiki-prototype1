from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, HTML, Column, Field, Row, Div
from django import forms
from django.urls import reverse_lazy, reverse

from etilog.forms.fields_filter import dom_icon_dict
from etilog.models import  SustainabilityDomain, SustainabilityTendency


class CharF(forms.CharField):
    def __init__(self, *args, **kwargs):
        lbl = kwargs.pop('label', '')
        req = kwargs.pop('required', True)
        super(CharF, self).__init__(required=req, label=lbl, *args, **kwargs)


class ImpactEventBtns(Layout):
    def __init__(self, request):
        submit_str = 'Save and Approve Impact Event'
        if request.user.is_authenticated:
            eles = [Submit('submit-name', submit_str, css_class='btn btn-info'), ]
        else:
            login_url = reverse('usermgmt:login')
            login_str = '''
                            <a  href="%s" title="Login">
                            registred in</a>

                            ''' % login_url
            info_str = 'To release this Impact Event a %s user needs to approve it.' % login_str
            text_str = '<h6 class="text-muted">%s</h6>' % info_str
            eles = [
                Submit('submit-name', 'Save Impact Event', css_class='btn btn-info'),

                Div(

                    HTML(text_str),
                    StrictButton(submit_str, css_class='btn btn-info disabled', ),
                    css_class='my-5'

                )]


        allbtns = ButtonHolder(
                Submit('submit-name', 'Save Impact Event', css_class='btn btn-secondary'),
                Button('new', 'New', css_class='btn btn-secondary', onclick="new_ie();"),
                Button('next', 'Next', css_class='btn btn-light', onclick="next_ie();")
            )
        super(ImpactEventBtns, self).__init__(*eles

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
                 row_class='mt-4',
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
    def __init__(self, field_name, col_class, field_class='',
                 placeholder='',
                 field_id=None,
                 taginput=True,
                 addmodel=True,
                 icon_name=None,
                 field_hidden=None,
                 autofocus=False,
                 *args, **kwargs):
        if field_id == None:
            field_id = 'id_' + field_name
        name_stripped = field_name
        parent_id = 'id_parent_' + name_stripped  # same as labelrow
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
            html_str = '''
            <span class="%s" add-url="%s" field-id="%s" field-name="%s">%s</span
            ''' % (h_css_class, add_url, field_id, 'ADD ' + field_name.upper(), icon_str)
        else:
            if icon_name:
                onclick = 'extract_text();'
                #url_get = reverse_lazy('etikicapture:extract_text_url')
                h_css_class = 'input-group-text'
                icon_str = '''<i class="%s" ></i>''' % icon_name
                html_str = '<span class="%s" onclick="%s">%s</span' % (h_css_class, onclick, icon_str)
            else:
                html_str = ''
        if field_hidden:
            f2 = Field(field_hidden, css_class="input-behind many-values", parent_id=parent_id)
        else:
            f2 = None

        if autofocus:
            autofocus_d = {'autofocus': '',}
        else:
            autofocus_d = {'': ''}

        rowcontent = Column(f2,

            FieldWithButtons(
                Field(field_name,

                  id=field_id,
                  parent_id=parent_id,

                  css_class=' '.join([cls_taginp, field_class]),
                  placeholder=placeholder,
                      **autofocus_d
                  ),

                HTML(html_str),
                css_id=parent_id,
            ),

            css_class=div_class,
            css_id=div_id,
        )
        super(TagsButton, self).__init__(rowcontent)


class RowTagsButton(LabelInputRow):
    def __init__(self, *args, **kwargs):
        LabelInputRow.__init__(self, TagsButton(*args, **kwargs))


class ColBtnSwitch(Layout):
    def __init__(self, field_name,
                 btn_list,
                 col_class=None,
                 wrap_class=None,
                 id_prefix='',
                 field_css_class=''):
        if col_class is None:
            col_class = 'col-12'
        if wrap_class is None:
            wrap_class = ' '.join(['justify-content-around d-flex flex-wrap w-100', 'switches_wrap'])

        btn_ele_li = []
        sw_cls = 'custom-control-input swselect'
        parent_id = id_prefix + 'id_parent_' + field_name
        field_id = id_prefix + 'id_' + field_name
        targfield = field_id
        for (cont, name, val, css_clss, css_id) in btn_list:
            css_id = id_prefix + css_id#

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



        col = Column(
            Field(field_name, css_class=' '.join(['input-behind', field_css_class]),
                  parent_id=parent_id, id=field_id),  # for client side validation
            Div(*btn_ele_li,
                         css_class=wrap_class),
                     css_class=col_class, css_id=parent_id)

        super(ColBtnSwitch, self).__init__(col)


class ColDomainSelect(ColBtnSwitch):
    def __init__(self, field_name,
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
                   field_name + '_sw' + str(dom.id),
                   #'id_sust_domain',
                   )
            ele_list.append(ele)

        ColBtnSwitch.__init__(self, field_name, ele_list,
                              *args, **kwargs)


class ColTendencySelect(ColBtnSwitch):
    def __init__(self, field_name,
                 ele_class='',
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
            css_id = field_name + str(tend.id)
            #targfield = 'id_sust_tendency'

            btn_list.append((cont, name, val, css_class, css_id))

        ColBtnSwitch.__init__(self, field_name,
                              btn_list,
                              *args, **kwargs)