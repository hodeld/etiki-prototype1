from django.contrib import admin
from django import forms

#models
from .models import ImpactEvent, SustainabilityDomain, SustainabilityCategory, SustainabilityTag
from .models import Company, Country,  ActivityCategory
from .models import Media, Reference, Source

class SourceInLine (admin.TabularInline):

    model = Source.impevents.through
    fieldsets = (
        (None, {
            'fields': (('url', 'di_vm', 'mi_vm', 'do_vm', 'fr_vm'),),
            }),
        (None, {
            'fields': (('comment', 'di_nm', 'mi_nm', 'do_nm', 'fr_nm'),),
            }),
        )
    
class ImpactEventAdminForm(forms.ModelForm):
    
    
    class Meta:
        
        exclude = ()
        widgets = {
            'summary': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            
        }

class ImpactEventAdmin(admin.ModelAdmin):
    model = ImpactEvent
    form = ImpactEventAdminForm
    


    

# Register your models here.
admin.site.register(ImpactEvent, ImpactEventAdmin)
admin.site.register(SustainabilityCategory)
admin.site.register(SustainabilityDomain)
admin.site.register(SustainabilityTag)
admin.site.register(Source)
admin.site.register(Reference)
admin.site.register(Company)

admin.site.register(Media)
admin.site.register(ActivityCategory)
admin.site.register(Country)

