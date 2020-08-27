from django.urls import path


from . import views

app_name = 'prediki'

urlpatterns = [
    path('predict/<slug:text>', views.predict_text, name='predict_text'),





]
