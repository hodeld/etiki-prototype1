from django.contrib import admin
from etilog.admin import admin_site
from etikihead.models import Contact, ToDo, RelatedTodo
# Register your models here.


class RelatedToDoInLine(admin.TabularInline):
    model = RelatedTodo
    fk_name = 'from_todos'
    extra = 1
    verbose_name_plural = 'Related ToDo'


class TodosAdmin(admin.ModelAdmin):
    model = ToDo
    inlines = (RelatedToDoInLine, )
    list_display = ('name', 'description', 'active',)

# Register your models here.
admin_site.register(Contact)
admin_site.register(ToDo, TodosAdmin)