# Generated by Django 2.2.4 on 2019-09-19 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('etilog', '0017_auto_20190912_1439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sustainabilitytendency',
            options={'ordering': ['-name']},
        ),
        migrations.AlterField(
            model_name='company',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='etilog.ActivityCategory'),
        ),
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='etilog.Country'),
        ),
        migrations.AlterField(
            model_name='impactevent',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='impevents',
                                    to='etilog.Company'),
        ),
        migrations.AlterField(
            model_name='impactevent',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='etilog.Reference'),
        ),
        migrations.AlterField(
            model_name='impactevent',
            name='sust_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='etilog.SustainabilityCategory'),
        ),
        migrations.AlterField(
            model_name='impactevent',
            name='sust_domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='etilog.SustainabilityDomain'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='reference', to='etilog.Company'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='country',
            field=models.ForeignKey(blank=True, help_text='optional', null=True,
                                    on_delete=django.db.models.deletion.PROTECT, to='etilog.Country'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='mediaform',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='etilog.Media'),
        ),
    ]
