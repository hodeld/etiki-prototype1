from django.urls import path


from . import views

app_name = 'etilog'
urlpatterns = [
    path('', views.startinfo, name='startinfo'), #
    path('overview/', views.overview_impevs, name='home'),
    path('new_ie/', views.impact_event_create, name='newimpactevent'),
    path('importdbdata/', views.import_dbdata),
    path('get_sustcagories/', views.load_sustcategories, name = 'get_sustcagories'),

    
    
    
]
