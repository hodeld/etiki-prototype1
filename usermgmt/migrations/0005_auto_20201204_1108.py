# Generated by Django 2.2.9 on 2020-12-04 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0004_auto_20201204_1105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='aggree_privacy',
            new_name='agree_privacy',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='aggree_terms',
            new_name='agree_terms',
        ),
    ]
