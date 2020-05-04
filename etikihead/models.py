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