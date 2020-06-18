from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms

from etilog.forms.fields_suggestions import RowTopics


class TopicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(

            RowTopics(labelname='Frequent Searched Topics'),
        )