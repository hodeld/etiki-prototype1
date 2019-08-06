from django.urls import path


from . import views

app_name = 'etilog'
urlpatterns = [
    path('', views.startinfo, name='startinfo'), #
    path('overview/', views.overview_impevs, name='home'),
    path('new_ie/', views.new_impact_event, name='newimpactevent'),
    path('importdbdata/', views.import_dbdata)
    
    
    
    
]
