from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms

from etilog.forms.fields_suggestions import RowTopics

label_dict = {'tags': 'Frequent Searched Topics',
              'company': 'Frequent Searched Companies',
              'industry': 'Frequent Searched Industries'
              }
nr_inst_dict = {'tags': 10,
                'company': 14,
                'industry': 12,
                }


class TopicForm(forms.Form):
    def __init__(self, tag_category, *args, **kwargs):
        labeln = label_dict[tag_category]
        nr_insts = nr_inst_dict.get(tag_category, 10)
        super(TopicForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(

            RowTopics(tag_category=tag_category, labelname=labeln,
                      nr_insts=nr_insts),
        )