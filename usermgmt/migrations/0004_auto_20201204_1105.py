# Generated by Django 2.2.9 on 2020-12-04 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0003_auto_20201012_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='aggree_privacy',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='aggree_terms',
            field=models.BooleanField(default=True),
        ),
    ]