from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import etikicapture.views
import impexport.views
from . import views

app_name = 'etilog'
load_data = 'load_data/'


prototype = 'prototype/'

urlpatterns = [
    path('startinfo/', views.startinfo, name='startinfo'),  #
    path('', views.entry_mask, name='entrymask'),

    path(prototype, views.overview_impevs, name='home'),
    path(prototype+'<slug:reqtype>', views.overview_impevs, name='home_filtered'),

    path(load_data + '<slug:modelname>', views.load_names, name='load_jsondata'),


    path('logout/', views.logout_view, name='logout'),
    path('privacy/', views.legal, name='legal'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),

    #  not used:
    path('impactevent/' + '<slug:ie_id>', views.impact_event_show, name='impactevent_show'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # for development only
