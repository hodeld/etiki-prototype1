from django.db import models

from etilog.models import Company


class Metric(models.Model):
    name = models.CharField(max_length=100)
    wr_id = models.PositiveSmallIntegerField(unique=True)
    min = models.FloatField()
    max = models.FloatField()

    def __str__(self):
        return self.name


class Answer(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    wr_id = models.PositiveSmallIntegerField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='impevents')
    year = models.DateField(help_text='year of answer')
    value = models.CharField(max_length=30)

    def __str__(self):
        return self.metric

    class Meta:
        ordering = ['name', ]