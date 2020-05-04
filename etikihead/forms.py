'''
Created on 2.8.2019

@author: daim
'''
from django import forms
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, HTML, Div, Hidden

# models
from .models import (Contact
                     )


from crispy_forms.templatetags.crispy_forms_field import css_class

DT_FORMAT = '%Y-%m-%d %H:%M:%S'
# D_FORMAT = '%Y-%m-%d'
D_FORMAT = '%d.%m.%Y'
D_FORMAT_EXTRA = '%d.%m.%y'
D_YEARFORMAT = '%Y'

datefiltername = 'datefilter'


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'etiki-form'
        # adds a submit button at the end
        self.helper.layout.extend(
            (
            HTML('<h3 id="form-message"></h3>'),
            Submit('submit', 'Send', css_class='btn btn-info')
            )
        )

    class Meta:
        model = Contact
        fields = ['subject', 'name_visitor', 'from_email', 'message',
                  ]
        labels = {
            'name_visitor': ('Your Name'),
            'from_email': 'email',
        }
