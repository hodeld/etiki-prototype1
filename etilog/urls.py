from django.urls import path


from . import views

app_name = 'etilog'
urlpatterns = [
    path('', views.overview_impevs, name='home'), #= login-redirect in settings
    
]
