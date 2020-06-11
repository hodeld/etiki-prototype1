'''
Created on 25 Jul 2019

@author: daim
'''

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



