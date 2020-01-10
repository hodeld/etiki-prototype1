# Generated by Django 2.2.8 on 2020-01-10 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etilog', '0027_auto_20191221_0100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impactevent',
            name='sust_category',
        ),
        migrations.RemoveField(
            model_name='sustainabilitytag',
            name='sust_categories',
        ),
        migrations.AlterField(
            model_name='company',
            name='recipient_old',
            field=models.ManyToManyField(blank=True, related_name='_company_recipient_old_+', to='etilog.Company', verbose_name='delivers to'),
        ),
        migrations.AlterField(
            model_name='company',
            name='supplier_old',
            field=models.ManyToManyField(blank=True, related_name='_company_supplier_old_+', to='etilog.Company', verbose_name='supplied by'),
        ),
        migrations.DeleteModel(
            name='SustainabilityCategory',
        ),
    ]