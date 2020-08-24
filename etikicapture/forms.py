from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, HTML, Div, Button
from django import forms
from django.urls import reverse_lazy, reverse

from etilog.forms.fields_filter import (DateYearPickerField, DateYearPicker)
from etikicapture.fields import  ImpactEventBtns, RowTagsButton, LabelInputRow, TagsButton, \
    ColDomainSelect, ColTendencySelect
from etilog.forms.forms_filter import NotReqCharF
from etilog.models import ImpactEvent, Company, SubsidiaryOwner, SupplierRecipient, Reference

CSS_COL_CLS = 'col-12 col-lg-6'

_PH_COMPANY = 'e.g. Coca Cola, Apple …'
_PH_COUNTRY = 'e.g. Switzerland, France … '
_PH_REFERENCE = 'e.g. New York Times, Guardian …'


class ImpactEventForm(forms.ModelForm):
    """
    model form to create an impact event.
    fields default -> validation correct.
    widgets customized.
    """
    tags_select = NotReqCharF()
    tags_drop = NotReqCharF()

    def __init__(self, *args, **kwargs):
        super(ImpactEventForm, self).__init__(*args, **kwargs)

        self.fields['source_url'].required = True

        # crispy form layout:
        self.helper = FormHelper()
        self.helper.form_id = 'id_impevform'
        #self.helper.form_action = reverse('etikicapture:newimpactevent',)
        self.helper.layout = Layout(

            RowTagsButton('source_url', 'col-12',
                          taginput=False,
                          addmodel=False,
                          icon_name='fas fa-sync',
                          placeholder='paste URL'),

            #first hidden
            Div(
                StrictButton('Article Preview', css_class='btn btn-sm btn-info',
                       data_toggle="modal", data_target="#modalFullArticle",
                       ),
                ImpEvMainFields(),

                Field('comment', rows=3),

                Div(
                    Row(Column(Field('date_text'), css_class=CSS_COL_CLS)),
                    Field('article_title'),
                    Field('article_text'),
                    Field('article_html'),
                    Field('result_parse_html'),
                    css_class='collapse',
                    css_id='div_article_fields'
                ),

                Submit('submit-name', 'Save Impact Event', css_class='btn btn-info'),

                style='display: none;',  # for fadeIn
                css_id='div_main_fields'

            ),
        )

    class Meta:  # only for model fields
        model = ImpactEvent
        fields = ['source_url',
                  # first part hidden
                  'date_published', 'date_impact', 'company', 'reference',
                  'country',
                  'sust_domain', 'sust_tendency', 'sust_tags',
                  'summary',
                  # from here only for etikis
                  'comment',
                  'article_text', 'article_title', 'date_text', 'article_html', 'result_parse_html'
                  ]

        widgets = {
            'source_url': forms.URLInput(attrs={'placeholder': 'url to the article',

                                                }),
            'country': forms.TextInput(),
            'company': forms.TextInput(),
            'reference': forms.TextInput(),
            'sust_tags': forms.TextInput(),
            'tags_select': forms.TextInput(),
            'tags_drop': forms.TextInput(),

            'sust_domain': forms.TextInput(),
            'sust_tendency': forms.TextInput(),

            'date_published': DateYearPicker(),
            'date_impact': DateYearPicker(),
            'comment': forms.Textarea(),
            'summary': forms.Textarea(),
            'article_html': forms.TextInput(),
        }

        # if added labels here -> correct required or not
        labels = {
            'date_published': (''),
            'date_impact': (''),
            'company': ('Which company was concerned'),
            'reference': ('Where was it published?'),
            'country':  'Where did it happen',
            'sust_domain': 'Which Category?',
            'sust_tendency': 'Which Tendency?',
            'sust_tags': '',
        }
        help_texts = {
            'date_published': (''),
            'date_impact': (''),
            'summary': (''),
        }


class ImpEvMainFields(Layout):
    def __init__(self):
        layout_list = [
            LabelInputRow(
                Column(
                    DateYearPickerField('date_published', 'when was it published', css_class='',
                                        data_category='date_from'
                                        ),
                    DateYearPickerField('date_impact', 'when did it happen', css_class='',
                                        data_category='date_to'
                                        ),
                    css_class='col-12 d-flex flex-wrap flex-wrap justify-content-around'  # wraps if needed
                ), labelname='Date'

            ),

            RowTagsButton('country', 'col-12',
                          placeholder=_PH_COUNTRY,
                          addmodel=False,
                          ),

            RowTagsButton('company', 'col-12',
                          placeholder=_PH_COMPANY),

            RowTagsButton('reference', 'col-12',
                          placeholder=_PH_REFERENCE),

            LabelInputRow(ColDomainSelect('sust_domain')),

            LabelInputRow(ColTendencySelect('sust_tendency')),

            LabelInputRow(
                rowcontent=[TagsButton('tags_select', 'col-12 div_tags_select', taginput='c_tags_select',
                                       addmodel=False, ),
                            Div(HTML('<h3><i class="fas fa-arrow-down"></i></h3>'), css_class='mx-auto'),

                            TagsButton('tags_drop', 'col-12 div_tags_drop',
                                       placeholder='Search Tags',
                                       taginput='c_tags_search_inp c_tags_drop',
                                       field_hidden='sust_tags'),
                            ],
                labelname='Select Sustainability Topics'
            ),

            Field('summary', rows=3, placeholder='Short summary of content'),

        ]
        super(ImpEvMainFields, self).__init__(*layout_list)



_FOREIGN_MODEL_CLS = 'foreignModel'


class CompanyForm(forms.ModelForm):
    '''
    form to create a company
    '''

    owner = forms.ModelMultipleChoiceField(queryset=Company.objects.none(),
                                           required=False)  # for validation
    subsidiary = forms.ModelMultipleChoiceField(queryset=Company.objects.none(),
                                                required=False)
    supplier = forms.ModelMultipleChoiceField(queryset=Company.objects.none(),
                                              required=False)
    recipient = forms.ModelMultipleChoiceField(queryset=Company.objects.none(),
                                               required=False)

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        # as they are not model fields -> widget needs to be adapet here
        self.fields['owner'].widget = forms.TextInput()
        self.fields['subsidiary'].widget = forms.TextInput()
        self.fields['supplier'].widget = forms.TextInput()
        self.fields['recipient'].widget = forms.TextInput()

        self.helper = FormHelper(self)
        self.helper.form_class = _FOREIGN_MODEL_CLS
        self.helper.form_action = reverse_lazy('etikicapture:add_foreignmodel',
                                   kwargs={'main_model': 'impev',
                                           'foreign_model': 'company'})

        self.helper.layout = Layout(
            RowTagsButton('name', 'col-12',
                          taginput=False,
                          addmodel=False,
                          placeholder=_PH_COMPANY,),

            RowTagsButton('country', 'col-12',
                          placeholder=_PH_COUNTRY,
                          addmodel=False,
                          ),

            Field('activity'),
            Field('comment', rows=3),

            RowTagsButton('owner', 'col-12',
                          placeholder=_PH_COMPANY,
                          addmodel=False,),
            RowTagsButton('subsidiary', 'col-12',
                          placeholder=_PH_COMPANY,
                          addmodel=False,),
            RowTagsButton('supplier', 'col-12',
                          placeholder=_PH_COMPANY,
                          addmodel=False,),
            RowTagsButton('recipient', 'col-12',
                          placeholder=_PH_COMPANY,
                          addmodel=False,),

            Submit('submit-name', '', css_id='id_submit_fm', css_class='d-none'),

        )

    def save(self, commit=True):
        main = self.instance
        main.save()  # save main instance
        # add relations:
        if self.cleaned_data['subsidiary'] is not None:
            for comp in self.cleaned_data['subsidiary']:  # comes as queryset
                SubsidiaryOwner.objects.update_or_create(owner_company=main,
                                                         subsidiary_company=comp)
        if self.cleaned_data['owner'] is not None:
            for comp in self.cleaned_data['owner']:  # comes as queryset
                SubsidiaryOwner.objects.update_or_create(owner_company=comp,
                                                         subsidiary_company=main)
        if self.cleaned_data['supplier'] is not None:
            for comp in self.cleaned_data['supplier']:  # comes as queryset
                SupplierRecipient.objects.update_or_create(recipient_company=main,
                                                           supplier_company=comp)
        if self.cleaned_data['recipient'] is not None:
            for comp in self.cleaned_data['recipient']:  # comes as queryset
                SupplierRecipient.objects.update_or_create(recipient_company=comp,
                                                           supplier_company=main)
        return main

    class Meta:  # only for model fields
        model = Company
        exclude = ['owner_old', 'subsidiary_old', 'supplier_old', 'recipient_old',
                   'subsidiary_to_owner', 'supplier_to_recipient'
                   ]

        widgets = {

            'country': forms.TextInput(),



            'comment': forms.Textarea(),

        }


class ReferenceForm(forms.ModelForm):
    '''
    form to create a reference
    '''

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = _FOREIGN_MODEL_CLS
        self.helper.form_action = reverse_lazy('etikicapture:add_foreignmodel',
                                               kwargs={'main_model': 'impev',
                                                       'foreign_model': 'reference'})
        self.helper.layout = Layout(

            RowTagsButton('name', 'col-12',
                          taginput=False,
                          addmodel=False,
                          placeholder=_PH_REFERENCE, ),

            Field('mediaform'),

            RowTagsButton('company', 'col-12',
                          addmodel=False,
                          placeholder=_PH_COMPANY),

            RowTagsButton('country', 'col-12',
                          placeholder=_PH_COUNTRY,
                          addmodel=False,
                          ),

            Field('comment', rows=3),
            Submit('submit-name', '', css_id='id_submit_fm', css_class='d-none'),


        )

    class Meta:  # only for model fields
        model = Reference
        exclude = []

        widgets = {

            'company': forms.TextInput(),
            'country': forms.TextInput(),

            'comment': forms.Textarea(),

        }
