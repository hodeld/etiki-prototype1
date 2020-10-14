#forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.urls import reverse

USERFORM_ID = 'id_userform'
PH_EMAIL = 'name@mail.org'
PH_USERNAME = 'UserName'


class UserForm(forms.ModelForm):
    """
    model form to create or update user (profile).
    fields default -> validation correct.
    widgets customized.
    """

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

        # crispy form layout:
        self.helper = FormHelper(self)  # self needed as argument for default layout
        self.helper.form_id = USERFORM_ID
        self.helper.form_action = reverse('usermgmt:profile_update')
        self.helper.layout = Layout(
            Field('username', placeholder=PH_USERNAME),
            Field('email', placeholder=PH_EMAIL),
            Field('first_name', placeholder='First Name'),
            Field('last_name', placeholder='Last Name'),
            Submit('submit-user', 'Save Changes', css_class='btn btn-info'),
        )

    class Meta:  # only for model fields
        model = User
        fields = ['username',  'email', 'first_name', 'last_name',]


class UserCreateForm(UserCreationForm):
    """
        model form to create user (profile).
        fields default -> validation correct.
        widgets customized.
        """

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)  # self needed as argument for default layout
        self.helper.form_id = USERFORM_ID
        self.helper.form_action = reverse('usermgmt:create_user_save')
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = PH_EMAIL
        self.helper.layout.fields[0] = Field('username', placeholder=PH_USERNAME)

        self.helper.layout.append(
            Submit('submit-create', 'Create', css_class='btn btn-info'),
        )

    class Meta:
        model = User
        fields = ('username', 'email')
        field_classes = {'username': UsernameField}


