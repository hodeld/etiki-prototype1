# Generated by Django 2.2.9 on 2020-05-04 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etikihead', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='sent_to_etiki',
            field=models.BooleanField(default=True),
        ),
    ]