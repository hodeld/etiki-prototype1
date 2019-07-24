from django.contrib import admin
from .models import ImpactEvent, SustainabilityCategory
from .models import Company, Country,  ActivityCategory
from .models import Media, Reference
 


# Register your models here.
admin.site.register(ImpactEvent)
admin.site.register(SustainabilityCategory)
admin.site.register(Reference)
admin.site.register(Company)

admin.site.register(Media)
admin.site.register(ActivityCategory)
admin.site.register(Country)

