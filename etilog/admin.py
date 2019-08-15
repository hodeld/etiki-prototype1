from django.contrib import admin
from django.contrib.admin import AdminSite
from django import forms
from django.urls import reverse_lazy

#models
from .models import ImpactEvent, SustainabilityDomain, SustainabilityCategory, SustainabilityTag
from .models import Company, Country,  ActivityCategory
from .models import Media, Reference, Source

class EtilogAdminSite(AdminSite):
    site_header = 'Etiki Admin'
    site_url = reverse_lazy('etilog:home')



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
    


#customized admin    
admin_site = EtilogAdminSite(name = 'etilog_admin')

# Register your models here.
admin_site.register(ImpactEvent, ImpactEventAdmin) #default is admin.site.register
admin_site.register(SustainabilityCategory)
admin_site.register(SustainabilityDomain)
admin_site.register(SustainabilityTag)
admin_site.register(Source)
admin_site.register(Reference)
admin_site.register(Company)

admin_site.register(Media)
admin_site.register(ActivityCategory)
admin_site.register(Country)

