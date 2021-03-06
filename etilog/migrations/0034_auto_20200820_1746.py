# Generated by Django 2.2.9 on 2020-08-20 15:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('etilog', '0033_auto_20200504_1114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='impactevent',
            options={'ordering': ['-date_published', 'company']},
        ),
        migrations.AddField(
            model_name='company',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
