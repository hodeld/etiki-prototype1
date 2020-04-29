from django.urls import path

from . import views

app_name = 'etilog'
get_data = 'get_data/'
load_data = 'load_data/'
export = 'export/'
impev = 'impactevent/'
prototype = 'prototype/'

urlpatterns = [
    path('startinfo/', views.startinfo, name='startinfo'),  #
    path('', views.entry_mask, name='entrymask'),

    path(prototype, views.overview_impevs, name='home'),
    path(prototype+'<slug:reqtype>', views.overview_impevs, name='home_filtered'),

    path(impev + 'new/', views.impact_event_create, name='newimpactevent'),
    path(impev + 'newfrom/<slug:ie_id>', views.impact_event_create, name='impactevent_copy'),
    path(impev + 'update/<slug:ie_id>', views.impact_event_update, name='impactevent_update'),
    path('<slug:main_model>/add/<slug:foreign_model>', views.add_foreignmodel, name='add_foreignmodel'),

    path('importdbdata/', views.import_dbdata, name='import_dbdata'),
    path('extract_text/<slug:ie_id>', views.extract_text, name='extract_text'),
    path('extract_text_all', views.extract_text_all, name='extract_text_all'),
    path('extract_text_url/', views.extract_text_from_url, name='extract_text_url'),


    path(impev + '<slug:ie_id>', views.impact_event_show, name='impactevent_show'),

    path(get_data + 'get_susttags/', views.load_sust_tags, name='get_sust_tags'),
    path(load_data + '<slug:modelname>', views.load_names, name='load_jsondata'),
    path(export + 'nlp', views.export_csv_nlp, name='export_csv_nlp'),
    path(export + 'base', views.export_csv_base, name='export_csv_base'),
    path(export + 'extracterrs', views.export_csv_extr, name='export_csv_exterrs'),

    path('logout/', views.logout_view, name='logout'),
    path('privacy/', views.legal, name='legal'),
    path('about/', views.about, name='about'),

]
