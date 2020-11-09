from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Contact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # tz aware datetime
    subject = models.CharField(max_length=100)
    name_visitor = models.CharField(max_length=100)
    from_email = models.EmailField()
    message = models.TextField(max_length=500)
    sent_to_etiki = models.BooleanField(default=True)
    answer_etiki = models.TextField(max_length=1000, blank=True, null=True)
    answered = models.BooleanField(default=False)
    comment = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name_visitor
    
    
class ToDo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    active = models.BooleanField(default=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True, null=True)
    related_todo = models.ManyToManyField('self', blank=True,
                                              through='RelatedTodo',
                                              through_fields=('from_todos', 'to_todos'),
                                              symmetrical=False,
                                              related_name='to_master_todo'
                                              )

    def __str__(self):
        return ' '.join((str(self.id), self.name))


class RelatedTodo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # tz aware datetime
    active = models.BooleanField(default=True)
    from_todos = models.ForeignKey(ToDo, on_delete=models.CASCADE,
                                       related_name='from_todos',
                                       verbose_name='master_todo')
    to_todos = models.ForeignKey(ToDo, on_delete=models.CASCADE,
                                     related_name='to_todos',
                                     verbose_name='related_todo')

    def __str__(self):
        return self.from_todos.name



