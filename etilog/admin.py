from django.contrib import admin
from django import forms

#models
from .models import ImpactEvent, SustainabilityDomain, SustainabilityCategory, SustainabilityTag
from .models import Company, Country,  ActivityCategory
from .models import Media, Reference
 
class ImpactEventAdminForm(forms.ModelForm):
    class Meta:
        model = ImpactEvent
        exclude = ()
        widgets = {
            'summary': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }

class ImpactEventAdmin(admin.ModelAdmin):
    form = ImpactEventAdminForm



# Register your models here.
admin.site.register(ImpactEvent, ImpactEventAdmin)
admin.site.register(SustainabilityCategory)
admin.site.register(SustainabilityDomain)
admin.site.register(SustainabilityTag)
admin.site.register(Reference)
admin.site.register(Company)

admin.site.register(Media)
admin.site.register(ActivityCategory)
admin.site.register(Country)

