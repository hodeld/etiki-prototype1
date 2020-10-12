from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'usermgmt'
user_prefix = 'users/'

urlpatterns = [
    #path(user_prefix + 'default/', include('django.contrib.auth.urls')),
    path(user_prefix + 'login/', auth_views.LoginView.as_view(), name='login'),
    path(user_prefix + 'profile/' + '<slug:user_id>', views.profile, name='profile'),
    path(user_prefix + 'update/', views.profile_update, name='profile_update'),

]
