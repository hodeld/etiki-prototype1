from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, HTML, Div
from django import forms
from django.urls import reverse_lazy

from etilog.forms.fields_filter import (DateYearPickerField, DateYearPicker, LabelRow)
from etikicapture.fields import CompanyWidget, ReferenceWidget, CompanyWBtn, ReferenceWBtn, UrlWBtn, \
    ImpactEventBtns, RowTagsButton, LabelInputRow, TagsButton, ColDomainSelect, ColTendencySelect
from etilog.forms.forms_filter import NotReqCharF
from etilog.models import ImpactEvent, Company, SubsidiaryOwner, SupplierRecipient, Reference

CSS_COL_CLS = 'col-12 col-lg-6'


class ImpactEventForm(forms.ModelForm):
    '''
    model form to create an impact event.
    fields default -> validation correct.
    widgets customized.
    '''


    def __init__(self, *args, **kwargs):
        super(ImpactEventForm, self).__init__(*args, **kwargs)

        # crispy form layout:
        self.helper = FormHelper()
        self.helper.form_id = 'id_impevform'
        self.helper.layout = Layout(
            ImpactEventBtns(),

            RowTagsButton('source_url', 'col-12',
                          taginput=False,
                          addmodel=False,
                          icon_name='fas fa-sync',
                          labelname='paste URL'),


            #first hidden
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
                              labelname='Search Country',
                          addmodel=False,
                          ),

            RowTagsButton('company', 'col-12',
                              labelname='Search Company'),

            RowTagsButton('reference', 'col-12',
                          labelname='Search News Paper'),

            LabelInputRow(ColDomainSelect(), labelname='Category'),

            LabelInputRow(ColTendencySelect(), labelname='Which Tendency?'),


            Row(Field('sust_domain', id='id_sust_domain', type="hidden",),
                Column(Field('sust_tendency'
                             ),
                       css_class=CSS_COL_CLS)
            ),


            LabelInputRow(
                rowcontent=[TagsButton('tags_select', 'col-12 div_tags_select', taginput='c_tags_select',
                                       addmodel=False,),
                            Div(HTML('<h3><i class="fas fa-arrow-down"></i></h3>'), css_class='mx-auto'),

                TagsButton('sust_tags', 'col-12 div_tags_drop',
                           labelname='Search Tags',
                           taginput='c_tags_search_inp c_tags_drop'),
                            ],
                labelname='Select Sustainability Topics'
            ),

            Field('summary', rows=3, placeholder='Short summary of content'),


            Field('comment', rows=3),

            Row(Column(Field('date_text'), css_class=CSS_COL_CLS)),
            Field('article_title'),
            Field('article_text'),
            Field('article_html'),
            Field('result_parse_html'),

            ImpactEventBtns(),
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
            'company': forms.TextInput(),
            'reference': forms.TextInput(),
            'sust_tags': forms.TextInput(),
            'tags_select': forms.TextInput(),
            'sust_domain': forms.TextInput(),

            'date_published': DateYearPicker(),
            'date_impact': DateYearPicker(),
            'comment': forms.Textarea(),
            'summary': forms.Textarea(),
            'article_html': forms.TextInput(),
        }

        labels = {
            'date_published': (''),
            'date_impact': (''),
            'company': ('Which company was concerned'),
            'reference': ('Where was it published?'),
            'country':  'Where did it happen',
        }
        help_texts = {
            'date_published': (''),
            'date_impact': (''),
            'summary': (''),
        }


class CompanyForm(forms.ModelForm):
    '''
    form to create a company
    '''
    owner = forms.ModelMultipleChoiceField(queryset=Company.objects.all(),
                                           required=False)  # for validation
    subsidiary = forms.ModelMultipleChoiceField(queryset=Company.objects.all(),
                                                required=False)
    supplier = forms.ModelMultipleChoiceField(queryset=Company.objects.all(),
                                              required=False)
    recipient = forms.ModelMultipleChoiceField(queryset=Company.objects.all(),
                                               required=False)

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        self.fields['owner'].widget = CompanyWidget()
        self.fields['subsidiary'].widget = CompanyWidget()
        self.fields['supplier'].widget = CompanyWidget()
        self.fields['recipient'].widget = CompanyWidget()

        self.helper = FormHelper(self)
        self.helper['owner'].wrap(CompanyWBtn,  # fieldname is passed as arg
                                  mainmodel='company')
        self.helper['subsidiary'].wrap(CompanyWBtn,  # fieldname is passed as arg
                                       mainmodel='company')
        self.helper['supplier'].wrap(CompanyWBtn,  # fieldname is passed as arg
                                     mainmodel='company')
        self.helper['recipient'].wrap(CompanyWBtn,  # fieldname is passed as arg
                                      mainmodel='company')

        # adds a submit button at the end
        self.helper.layout.append(
            Row(Submit('submit', 'Save', css_class='btn btn-light'))
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


class ReferenceForm(forms.ModelForm):
    '''
    form to create a reference
    '''

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        # adds a submit button at the end
        self.helper.layout.append(
            Submit('submit', 'Save', css_class='btn btn-light')
        )

    class Meta:  # only for model fields
        model = Reference
        exclude = []

