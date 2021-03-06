# Generated by Django 2.2.9 on 2020-04-30 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etilog', '0030_frequentaskedquestions'),
    ]

    operations = [
        migrations.AddField(
            model_name='frequentaskedquestions',
            name='image_bottom',
            field=models.ImageField(blank=True, height_field='img_bottom_width', null=True, upload_to='uploads/faq/', width_field='img_bottom_height'),
        ),
        migrations.AddField(
            model_name='frequentaskedquestions',
            name='image_top',
            field=models.ImageField(blank=True, height_field='img_top_width', null=True, upload_to='uploads/faq/', width_field='img_top_height'),
        ),
        migrations.AddField(
            model_name='frequentaskedquestions',
            name='img_bottom_height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='frequentaskedquestions',
            name='img_bottom_width',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='frequentaskedquestions',
            name='img_top_height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='frequentaskedquestions',
            name='img_top_width',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
