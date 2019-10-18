from django.urls import path


from . import views

app_name = 'etilog'
get_data = 'get_data/'
load_data = 'load_data/'
export = 'export/'
impev = 'impactevent/'


urlpatterns = [
    path('', views.startinfo, name='startinfo'), #
    path('overview/', views.overview_impevs, name='home'),
    path(impev + 'new/', views.impact_event_create, name='newimpactevent'),
    path(impev + 'newfrom/<slug:ie_id>', views.impact_event_create, name='impactevent_copy'),
    path(impev + 'update/<slug:ie_id>', views.impact_event_update, name='impactevent_update'),
    path('<slug:main_model>/add/<slug:foreign_model>', views.add_foreignmodel, name='add_foreignmodel'),
    path('importdbdata/', views.import_dbdata),
    path('extract_text/<slug:ie_id>', views.extract_text, name='extract_text'),
    path('extract_text_url/', views.extract_text_from_url, name='extract_text_url'),
    
    path(impev + 'html/', views.article_html, name='article_html'),
     
    path(get_data + 'get_susttags/', views.load_sust_tags, name = 'get_sust_tags'),
    path(load_data + '<slug:modelname>', views.load_names, name = 'load_jsondata'),
    path(export + 'nlp', views.export_csv_nlp, name = 'export_csv_nlp'),
    path(export + 'base', views.export_csv_base, name = 'export_csv_base'),
    
    path('logout/', views.logout_view, name='logout'),

    

    
    
    
]
