from django.urls import path


from . import views

app_name = 'etilog'
get_data = 'get_data/'
load_data = 'load_data/'


urlpatterns = [
    path('', views.startinfo, name='startinfo'), #
    path('overview/', views.overview_impevs, name='home'),
    path('new_ie/', views.impact_event_create, name='newimpactevent'),
    path('new_ie/<slug:impact_id>', views.impact_event_create, name='impactevent_copy'),
    path('<slug:main_model>/add/<slug:foreign_model>', views.add_foreignmodel, name='add_foreignmodel'),
    path('importdbdata/', views.import_dbdata),
    
    path(get_data + 'get_susttags/', views.load_sust_tags, name = 'get_sust_tags'),
    path(load_data + '<slug:modelname>', views.load_names, name = 'load_jsondata'),
    path('exportdata', views.export_csv_nlp, name = 'export_csv_nlp'),
    
    path('logout/', views.logout_view, name='logout'),
    #path(load_data + 'reference.json', views.load_references, name = 'load_references'),
    #path(load_data + 'country.json', views.load_countries, name = 'load_countries'),
    #path(get_data + 'get_sustcagories/', views.load_sustcategories, name = 'get_sustcagories'),
    

    
    
    
]
