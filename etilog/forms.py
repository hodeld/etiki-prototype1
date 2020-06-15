'''
Created on 2.8.2019

@author: daim
'''
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, HTML, Div

# models
from .models import (Source, ImpactEvent, SustainabilityDomain
                     )

from .fields import (DateYearPicker, DateYearPickerField,
                     ColDomainBtnSelect, ColTendencyBtnSelect, RowTopics, Readonly, SearchWIcon, TendencyLegende,
                     LabelRow, LabelRowTagsInput
                     )

DT_FORMAT = '%Y-%m-%d %H:%M:%S'
# D_FORMAT = '%Y-%m-%d'
D_FORMAT = '%d.%m.%Y'
D_FORMAT_EXTRA = '%d.%m.%y'
D_YEARFORMAT = '%Y'

domains = [('0', '----')]
domains.extend(list(SustainabilityDomain.objects.values_list('id', 'name')))

CHOICES = domains
datefiltername = 'datefilter'


class SearchForm(forms.Form):
    search = forms.CharField(label='', required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Row(
                Column(SearchWIcon('search', id='id_search', autocomplete="off",
                                   placeholder='Search Companies, Countries, Topics, Newspaper …',
                                   css_class='tt-input'   # to have correct from beginning
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
    freetext = forms.CharField(label='freetext', required=False)

    def __init__(self, *args, **kwargs):
        super(FreetextForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(

            Row(
                Column(Field('freetext', id='id_f_freetext',

                             data_role='tagsinput'
                             ),
                       css_class='col-12'
                       ), id='id_row_f_freetext', css_class='row_tags_class'
            ),

        )


class ImpevOverviewFForm(forms.Form):
    '''
    form for ImpevOverview filter. labels are defined in filter.
    '''

    def __init__(self, *args, **kwargs):
        super(ImpevOverviewFForm, self).__init__(*args, **kwargs)

        self.fields['date_from'].widget = DateYearPicker()
        self.fields['date_to'].widget = DateYearPicker()
        self.fields['date_from'].label = ''
        self.fields['date_to'].label = ''

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
        cls_filterinput = 'f_input'  # used for jquery submit

        self.helper.layout = Layout(

            Field('sust_tendency', id='id_sust_tendency',
                  css_class=cls_filterinput + ' btninput', parfield='#id_sust_tendency-btn-'),

            # in one so whole row could get be fetched with .parent(SELECTOR)
            LabelRow(
                Div(Field('sust_domain', id='id_sust_domain',
                          css_class=cls_filterinput + ' btninput', parfield='#id_sust_domain-btn-'),

                    ColDomainBtnSelect(), ),
                labelname='Category', row_class='d-flex d-md-none'),

            LabelRow(ColTendencyBtnSelect(),
                     labelname='Which Tendency', row_class='d-flex d-md-none'),

            LabelRow(
                Column(
                    DateYearPickerField('date_from', 'from', css_class=cls_filterinput),
                    DateYearPickerField('date_to', 'to', css_class=cls_filterinput),
                    css_class='col-12 d-flex flex-wrap flex-wrap justify-content-around'  # wraps if needed
                ), labelname='Date'

            ),

            LabelRowTagsInput('tags', 'col-12', field_class=cls_filterinput
                              , labelname='Topics'),

            LabelRowTagsInput('company', 'col-12',
                              labelname='Company', field_class=cls_filterinput
                              ),

            LabelRowTagsInput('country', 'col-12', field_class=cls_filterinput
                              , labelname='Country'),

            LabelRowTagsInput('reference', 'col-12', field_class=cls_filterinput
                              , labelname='Published In', placeholder='Publisher'),

            LabelRowTagsInput('summary', 'col-12', field_class=cls_filterinput
                              , labelname='Fulltext'),

        )


class OverviewFiltHeaderForm(forms.Form):
    alltaginput = forms.CharField(required=False, label='',)

    def __init__(self, *args, **kwargs):
        super(OverviewFiltHeaderForm, self).__init__(*args, **kwargs)

        element_class = 'gettable '

        self.helper = FormHelper()
        # self.helper.form_method = 'get'
        # self.helper.form_id = 'id_filterform'
        self.helper.form_tag = False

        self.helper.layout = Layout(

            ColDomainBtnSelect(col_class='col-12 flex-nowrap',
                               labelname=None,
                               ele_class=element_class,
                               twin_ele=True,
                               btn_wrap_class='justify-content-center d-flex w-100'),
            ColTendencyBtnSelect(col_class='col-12 ',
                                 labelname=None,
                                 ele_class=element_class,
                                 twin_ele=True,
                                 btn_wrap_class='justify-content-center d-flex w-100'),
            Column(Field('alltaginput', id='id_alltaginput', css_class='f_alltagsinput',
                         wrapper_class='alltaginput justify-content-center d-flex my-2')
                   , css_class='col-12 '),

        )



CSS_COL_CLS = 'col-12 col-lg-6'


class TendencyLegendeDiv(forms.Form):

    def __init__(self, *args, **kwargs):
        super(TendencyLegendeDiv, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(

            TendencyLegende(),
        )


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

    class Meta:  # only for model fields
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
