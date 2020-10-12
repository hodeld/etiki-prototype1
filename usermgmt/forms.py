#forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse


class UserForm(forms.ModelForm):
    """
    model form to create or update user (profile).
    fields default -> validation correct.
    widgets customized.
    """

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # crispy form layout:
        self.helper = FormHelper(self)  # self needed as argument for default layout
        self.helper.form_id = 'id_userform'
        self.helper.form_action = reverse('usermgmt:profile_update')
        self.helper.layout.append(
            Submit('submit-user', 'Save Changes', css_class='btn btn-info'),
        )

    class Meta:  # only for model fields
        model = User
        fields = ['username',  'email', 'first_name', 'last_name',]
