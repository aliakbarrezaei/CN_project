from django.contrib.auth import views as auth_views

from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('register/', views.user_register),
]
