# Generated by Django 2.2.8 on 2019-12-20 23:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('etilog', '0025_auto_20191221_0001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='recipient',
            new_name='recipient_old',

        ),
        migrations.RenameField(
            model_name='company',
            old_name='supplier',
            new_name='supplier_old',

        ),
    ]
