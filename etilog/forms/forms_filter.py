'''
Created on 2.8.2019

@author: daim
'''
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column

# models
from etilog.models import (Source, SustainabilityDomain
                           )

from .fields_filter import (DateYearPicker, DateYearPickerField,
                            ColDomainBtnSelect, ColTendencyBtnSelect, SearchWIcon,
                            LabelRow,
                            TagField, AllTagsInput, LabelRowTagsInput)

DT_FORMAT = '%Y-%m-%d %H:%M:%S'
# D_FORMAT = '%Y-%m-%d'
D_FORMAT = '%d.%m.%Y'
D_FORMAT_EXTRA = '%d.%m.%y'
D_YEARFORMAT = '%Y'

domains = [('0', '----')]
domains.extend(list(SustainabilityDomain.objects.values_list('id', 'name')))

CHOICES = domains
datefiltername = 'datefilter'


class NotReqCharF(forms.CharField):
    def __init__(self, *args, **kwargs):
        lbl = kwargs.pop('label', '')
        super(NotReqCharF, self).__init__(required=False, label=lbl, *args, **kwargs)


class SearchForm(forms.Form):
    search = forms.CharField(label='', required=False)

    def __init__(self, landing=False, *args, **kwargs):
        #searchfield =
        super(SearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Row(
                Column(SearchWIcon(field_id='id_search', landing=landing),
                       css_class='col-12',
                       )
            ),
        )


class OverviewFForm(forms.Form):
    '''
    form for ImpevOverview Filter visible fields.
    '''
    date_from_pick = NotReqCharF()
    date_to_pick = NotReqCharF()

    reference_exc_tinp = NotReqCharF()

    sust_domain = NotReqCharF()
    sust_tendency = NotReqCharF()

    alltaginput1 = NotReqCharF()
    search = NotReqCharF()

    def __init__(self, *args, **kwargs):
        super(OverviewFForm, self).__init__(*args, **kwargs)

        self.fields['date_from_pick'].widget = DateYearPicker()
        self.fields['date_to_pick'].widget = DateYearPicker()

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id_filterform_visible'
        cls_filterinput = ''  # used for jquery submit

        self.helper.layout = Layout(

            Row(
                Column(
                    SearchWIcon(field_id='id_search2'),
                    css_class='col-12'
                ), css_class='d-flex d-md-none'
            ),
            Row(
                Column(
                    AllTagsInput('alltaginput1',
                                 wrapper_class='mt-3'),
                    css_class='col-12'
                ), css_class='d-flex'
            ),


            LabelRow(ColDomainBtnSelect(),
                     labelname='Category', row_class='d-flex d-md-none'),

            LabelRow(ColTendencyBtnSelect(),
                     labelname='Which Tendency', row_class='d-flex d-md-none'),

            LabelRow(
                Column(
                    DateYearPickerField('date_from_pick', 'from', css_class=cls_filterinput,
                                        data_category='date_from'
                                        ),
                    DateYearPickerField('date_to_pick', 'to', css_class=cls_filterinput,
                                        data_category='date_to'
                                        ),
                    css_class='col-12 d-flex flex-wrap flex-wrap justify-content-around'  # wraps if needed
                ), labelname='Date'

            ),

            LabelRowTagsInput('reference_exc_tinp', 'col-12',
                              labelname='Exclude Publishers'),

        )


class OverviewFHiddenForm(forms.Form):
    '''
    form for ImpevOverview Filter.
    '''
    date_from = NotReqCharF()
    date_to = NotReqCharF()

    company = NotReqCharF()
    reference = NotReqCharF()
    country = NotReqCharF()
    tags = NotReqCharF()
    summary = NotReqCharF()
    industry = NotReqCharF()

    reference_exc = NotReqCharF()

    sust_domain = NotReqCharF()
    sust_tendency = NotReqCharF()

    def __init__(self, *args, **kwargs):
        super(OverviewFHiddenForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_id = 'id_filterform'
        cls_filterinput = 'f_input'  # used for jquery submit

        self.helper.layout = Layout(

            Field('sust_tendency', id='id_sust_tendency', type="hidden",
                  css_class=cls_filterinput + ' btninput', parfield='#id_sust_tendency-btn-'),

            Field('sust_domain', id='id_sust_domain', type="hidden",
                  css_class=cls_filterinput + ' btninput', parfield='#id_sust_domain-btn-'),

            TagField('company', cls_filterinput),
            TagField('country', cls_filterinput),
            TagField('reference', cls_filterinput),
            TagField('tags', cls_filterinput),
            TagField('summary', cls_filterinput),
            TagField('industry', cls_filterinput),

            TagField('reference_exc', cls_filterinput),

            Field('date_from', id='id_f_date_from', type="hidden",
                  css_class=cls_filterinput + ' f_dateinput',
                  parfield='#id_date_from_pick'),
            Field('date_to', id='id_f_date_to', type="hidden",
                  css_class=cls_filterinput + ' f_dateinput',
                  parfield='#id_date_to_pick',
                  ),
        )


class OverviewFiltHeaderForm(forms.Form):
    alltaginput2 = NotReqCharF()

    def __init__(self, *args, **kwargs):
        super(OverviewFiltHeaderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_method = 'get'
        # self.helper.form_id = 'id_filterform'
        self.helper.form_tag = False

        self.helper.layout = Layout(

            Column(
                AllTagsInput('alltaginput2',
                             wrapper_class='justify-content-center d-flex my-2')
                , css_class='col-12 '),

            ColDomainBtnSelect(col_class='col-12 flex-nowrap',
                               labelname=None,
                               twin_ele=True,
                               btn_wrap_class='justify-content-center d-flex w-100'),
            ColTendencyBtnSelect(col_class='col-12 ',
                                 labelname=None,
                                 twin_ele=True,
                                 btn_wrap_class='justify-content-center d-flex w-100'),


        )



CSS_COL_CLS = 'col-12 col-lg-6'


class NewSource(forms.ModelForm):
    '''
    form to create an source
    '''

    class Meta:  # only for model fields
        model = Source
        fields = ['url', ]

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
            # 'url': 'urlblajsv',
        }


