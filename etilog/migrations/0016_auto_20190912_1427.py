# Generated by Django 2.2.4 on 2019-09-12 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('etilog', '0015_auto_20190820_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='SustainabilityTendency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impnr', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Import Number')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),

    ]
