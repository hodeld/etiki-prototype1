'''
Created on 25 Jul 2019

@author: daim
'''
from threading import Thread

from etilog.models import (Country, SustainabilityDomain, SustainabilityTag,
                           SustainabilityTendency, ImpactEvent,
                           Company, SubsidiaryOwner, SupplierRecipient
                           )
from django.db.models.functions import Trim
import string


def update_internal():
    upd_tags_names()


def upd_tags_names():
    for obj in SustainabilityTag.objects.all():
        new_name = string.capwords(obj.name)
        new_name.strip()
        obj.name = new_name
        obj.save()


def postpone(function):  # connection needs to be closed in function if db connection
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator

