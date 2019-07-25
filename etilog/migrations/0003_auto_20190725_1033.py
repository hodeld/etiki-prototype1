# Generated by Django 2.2.3 on 2019-07-25 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etilog', '0002_auto_20190725_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='SustainabilityDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impnr', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Import Number')),
                ('name', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='activitycategory',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='impactevent',
            options={'ordering': ['date_impact', 'company']},
        ),
        migrations.AlterModelOptions(
            name='media',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='reference',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='sustainabilitycategory',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='sustainabilitytag',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='country',
            name='alpha2code',
            field=models.CharField(default='te', max_length=2, unique=True, verbose_name='alpha-2-code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='numeric',
            field=models.PositiveSmallIntegerField(default=1000, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sustainabilitycategory',
            name='impnr',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Import Number'),
        ),
        migrations.AddField(
            model_name='sustainabilitytag',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sustainabilitytag',
            name='impnr',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Import Number'),
        ),
        migrations.AddField(
            model_name='sustainabilitytag',
            name='sust_categories',
            field=models.ManyToManyField(blank=True, to='etilog.SustainabilityCategory'),
        ),
    ]