from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.layout import Layout
from django import forms
from django.urls import reverse_lazy

from etilog.models import Company, Reference


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