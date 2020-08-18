from crispy_forms.bootstrap import FieldWithButtons, StrictButton, AppendedText
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, HTML, Column, Field, Row, Div
from django import forms
from django.urls import reverse_lazy

from etilog.models import Company, Reference


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
    def __init__(self, rowcontent, labelname,
                 row_class='',
                 *args, **kwargs):  # distribute buttons

        name_stripped = labelname.replace(' ', '')
        div_id = 'row' + name_stripped
        div_class = 'div_c_taginput' # 'taginput-row'

        super(LabelInputRow, self).__init__(
            Row(
                Column(
                    Div(
                        Row(rowcontent, *args, **kwargs),
                        css_class=' '.join([ div_class, ]),
                        css_id=div_id
                    ),
                    css_class='col-12'

                ),
                css_class='justify-content-center ' + row_class
            )
        )


class TagsButton(Layout):
    def __init__(self, field_name, col_class, labelname, field_class='',
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
        name_stripped = labelname.replace(' ', '')
        parent_id = '#row' + name_stripped  # same as labelrow
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
            html_str = '<span class="%s" add-url="%s">%s</span' % (h_css_class, add_url, icon_str)
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
            css_class=col_class
        )
        super(TagsButton, self).__init__(rowcontent)


class RowTagsButton(LabelInputRow):
    def __init__(self, *args, **kwargs):
        labelname = kwargs.get('labelname')
        LabelInputRow.__init__(self, TagsButton(*args, **kwargs), labelname)



