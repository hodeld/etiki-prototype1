# Generated by Django 2.2.4 on 2019-09-19 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('etilog', '0018_auto_20190919_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impactevent',
            name='sust_tendency',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to='etilog.SustainabilityTendency'),
            preserve_default=False,
        ),
    ]
