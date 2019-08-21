from django.urls import path


from . import views

app_name = 'etilog'


urlpatterns = [
    path('', views.startinfo, name='startinfo'), #
    path('overview/', views.overview_impevs, name='home'),
    path('new_ie/', views.impact_event_create, name='newimpactevent'),
    path('new_ie/<slug:impact_id>', views.impact_event_create, name='impactevent_copy'),
    path('<slug:main_model>/add/<slug:foreign_model>', views.add_foreignmodel, name='add_foreignmodel'),
    path('importdbdata/', views.import_dbdata),
    path('get_sustcagories/', views.load_sustcategories, name = 'get_sustcagories'),
    path('get_susttags/', views.load_sust_tags, name = 'get_sust_tags'),

    
    
    
]
