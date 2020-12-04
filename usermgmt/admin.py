from etilog.admin import admin_site
from django.contrib import admin

from usermgmt.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'privilege_points', 'agree_terms', 'agree_privacy',)


admin_site.register(Profile, ProfileAdmin)
