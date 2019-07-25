from django.contrib import admin
from .models import ImpactEvent, SustainabilityDomain, SustainabilityCategory, SustainabilityTag
from .models import Company, Country,  ActivityCategory
from .models import Media, Reference
 


# Register your models here.
admin.site.register(ImpactEvent)
admin.site.register(SustainabilityCategory)
admin.site.register(SustainabilityDomain)
admin.site.register(SustainabilityTag)
admin.site.register(Reference)
admin.site.register(Company)

admin.site.register(Media)
admin.site.register(ActivityCategory)
admin.site.register(Country)

