# Generated by Django 2.2.9 on 2020-11-09 09:35

from django.db import migrations
from django.contrib.auth import get_user_model


class Migration(migrations.Migration):
    def add_user(apps, schema_editor):
        # We can't import the Person model directly as it may be a newer
        # version than this migration expects. We use the historical version.
        user = get_user_model()
        admin_id = user.objects.get(username='admin').id

        impevs = apps.get_model('etilog', 'ImpactEvent')
        for ie in impevs.objects.filter(user=None):
            ie.user_id = admin_id
            ie.save()

    dependencies = [
        ('etilog', '0038_impactevent_article_byline'),
    ]

    operations = [
        migrations.RunPython(add_user),
    ]
