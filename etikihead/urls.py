from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'etikihead'


urlpatterns = [
    path('contact/', views.contact, name='contact'),

    ]
