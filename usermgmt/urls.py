from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'usermgmt'
user_prefix = 'users/'

urlpatterns = [
    #path(user_prefix + 'default/', include('django.contrib.auth.urls')),
    path(user_prefix + 'login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(user_prefix + 'profile/', views.profile, name='profile'),
    path(user_prefix + 'update/', views.profile_update, name='profile_update'),
    path(user_prefix + 'create/', views.create_user, name='create_user'),
    path(user_prefix + 'create/save', views.create_user_save, name='create_user_save'),


]
