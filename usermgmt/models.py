#models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from etilog.models import ImpactEvent, Reference


class Privilege(models.Model):
    min_points = models.PositiveIntegerField(default=1, unique=True)
    name = models.CharField(unique=True, max_length=100)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    privilege_points = models.PositiveIntegerField(default=1)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Relevance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    relevance_point = models.SmallIntegerField()
    impact_event = models.ForeignKey(ImpactEvent, models.CASCADE, blank=True, null=True)
    reference = models.ForeignKey(Reference, models.CASCADE, blank=True, null=True)