from django.urls import path

from . import views

app_name = 'impexport'

export = 'export/'



urlpatterns = [

    path('importdbdata/', views.import_dbdata, name='import_dbdata'),
    path('updatedbdata/', views.update_db_internal, name='update_db_internal'),

    path(export + 'nlp', views.export_csv_nlp, name='export_csv_nlp'),
    path(export + 'base', views.export_csv_base, name='export_csv_base'),
    path(export + 'extracterrs', views.export_csv_extr, name='export_csv_exterrs'),



]
