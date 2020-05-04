from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django import forms
from django.urls import reverse_lazy

# models
from .models import (ImpactEvent,
                     SustainabilityDomain, SustainabilityTendency, SustainabilityTag,
                     Company, Country, ActivityCategory,
                     Media, Reference, Source,
                     SubsidiaryOwner, SupplierRecipient,
                     FrequentAskedQuestions, RelatedQuestion
                     )


class EtilogAdminSite(AdminSite):
    site_header = 'Etiki Admin'
    site_url = reverse_lazy('etilog:home')


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
    list_display = ('id', '__str__', 'company', 'updated_at',
                    'sust_domain', 'sust_tendency', 
                    )
    list_filter = ('sust_domain', 'sust_tendency', 'sust_tags', 'company')


class TagsAdmin(admin.ModelAdmin):
    model = SustainabilityTag
    list_display = ('name', 'get_domains', 'sust_tendency')


class SubsidiaryInLine(admin.TabularInline):
    model = SubsidiaryOwner
    fk_name = 'owner_company'
    extra = 1
    verbose_name_plural = 'Subsidiaries'


class OwnerInLine(admin.TabularInline):
    model = SubsidiaryOwner
    fk_name = 'subsidiary_company'
    extra = 1
    verbose_name_plural = 'Owners'


class SupplierInLine(admin.TabularInline):
    model = SupplierRecipient
    fk_name = 'recipient_company'
    extra = 1
    verbose_name_plural = 'Suppliers'


class RecipientInLine(admin.TabularInline):
    model = SupplierRecipient
    fk_name = 'supplier_company'
    extra = 1
    verbose_name_plural = 'Recipients'


class CompanyAdmin(admin.ModelAdmin):
    inlines = (SubsidiaryInLine, OwnerInLine, SupplierInLine, RecipientInLine)


class SubsidiaryOwnerAdmin(admin.ModelAdmin):
    model = SubsidiaryOwner
    list_display = ('owner_company', 'subsidiary_company', 'active', 'created_at')


class SupplierRecipientAdmin(admin.ModelAdmin):
    model = SupplierRecipient
    list_display = ('recipient_company', 'supplier_company', 'active', 'created_at')


class RelatedQuestionInLine(admin.TabularInline):
    model = RelatedQuestion
    fk_name = 'from_questions'
    extra = 1
    verbose_name_plural = 'Related Question'


class FrequentAskedQuestionsAdmin(admin.ModelAdmin):
    model = FrequentAskedQuestions
    inlines = (RelatedQuestionInLine, )
    list_display = ('question', 'answer', 'active',)


# customized admin
admin_site = EtilogAdminSite(name='etilog_admin')

admin_site.register(User)
admin_site.register(Group)
# Register your models here.
admin_site.register(ImpactEvent, ImpactEventAdmin)  # default is admin.site.register
admin_site.register(SustainabilityDomain)
admin_site.register(SustainabilityTendency)
admin_site.register(SustainabilityTag, TagsAdmin)
admin_site.register(Source)
admin_site.register(Reference)
admin_site.register(Company, CompanyAdmin)
admin_site.register(SubsidiaryOwner, SubsidiaryOwnerAdmin)
admin_site.register(SupplierRecipient, SupplierRecipientAdmin)

admin_site.register(Media)
admin_site.register(ActivityCategory)
admin_site.register(Country)

admin_site.register(FrequentAskedQuestions, FrequentAskedQuestionsAdmin)
