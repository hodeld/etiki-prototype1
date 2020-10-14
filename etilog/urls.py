from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import etikicapture.views
import etikihead.views
import impexport.views
from . import views

app_name = 'etilog'
load_data = 'load_data/'


prototype = 'view/'  # already in etikprtype1_urls

urlpatterns = [


    path(prototype, views.overview_impevs, name='home'),
    path(prototype+'<slug:reqtype>', views.overview_impevs, name='home_filtered'),

    path(prototype+'filter/', views.filter_impevs, name='filter'),
    path(prototype+'results/', views.get_result, name='results'),

    path(load_data + '<slug:modelname>', views.load_names, name='load_jsondata'),


]
