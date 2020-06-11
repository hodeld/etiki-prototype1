from django.urls import path


from . import views

app_name = 'etikicapture'
impev = 'impactevent/'
get_data = 'get_data/'

urlpatterns = [
    path(impev + 'new/', views.impact_event_create, name='newimpactevent'),
    path(impev + 'newfrom/<slug:ie_id>', views.impact_event_create, name='impactevent_copy'),
    path(impev + 'update/<slug:ie_id>', views.impact_event_update, name='impactevent_update'),
    path('<slug:main_model>/add/<slug:foreign_model>', views.add_foreignmodel, name='add_foreignmodel'),

    path('extract_text/<slug:ie_id>', views.extract_text, name='extract_text'),
    path('extract_text_all', views.extract_text_all, name='extract_text_all'),
    path('extract_text_url/', views.extract_text_from_url, name='extract_text_url'),

    path(get_data + 'get_susttags/', views.load_sust_tags, name='get_sust_tags'),





]
