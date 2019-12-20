# Generated by Django 2.2.8 on 2019-12-20 05:53

from django.db import migrations, models
import etilog.models


class Migration(migrations.Migration):

    dependencies = [
        ('etilog', '0023_impactevent_result_parse_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='domain',
            field=models.CharField(blank=True, help_text='companydomain.com', max_length=255, null=True, validators=[etilog.models.full_domain_validator]),
        ),
        migrations.AlterField(
            model_name='impactevent',
            name='result_parse_html',
            field=models.PositiveSmallIntegerField(choices=[(0, 'not parsed'), (1, 'success'), (2, 'error'), (3, 'PDF'), (4, 'ConnErr'), (5, 'readabErr'), (6, 'emptyText'), (7, 'timeout'), (8, 'doublepara'), (9, 'longtext'), (10, 'inlongp'), (11, 'parsed manually')], default=0),
        ),
    ]