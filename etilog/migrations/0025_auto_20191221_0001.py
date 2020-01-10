# Generated by Django 2.2.8 on 2019-12-20 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('etilog', '0024_auto_20191220_0653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='owner',
            new_name='owner_old',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='subsidiary',
            new_name='subsidiary_old',
        ),
        migrations.CreateModel(
            name='SubsidiaryOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('owner_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_company', to='etilog.Company', verbose_name='owned by')),
                ('subsidiary_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subsidiary_company', to='etilog.Company', verbose_name='owns')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='subsidiary_to_owner',
            field=models.ManyToManyField(blank=True, related_name='owner_to_subsidiary', through='etilog.SubsidiaryOwner', to='etilog.Company'),
        ),
    ]