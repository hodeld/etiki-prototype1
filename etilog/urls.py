from django.urls import path


from . import views

app_name = 'etilog'
urlpatterns = [
    #path('', views.startinfo, name='startinfo'), #
    path('', views.overview_impevs, name='home'),
    
    
    
    
]
