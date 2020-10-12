from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'etikihead'


urlpatterns = [

    path('', views.entry_mask, name='entrymask'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.legal, name='legal'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),

    path('startinfo/', views.startinfo, name='startinfo'),  #

    ]
