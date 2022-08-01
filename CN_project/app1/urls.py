
from django.urls import path,re_path
from . import views
app_name='app1'
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    #path('login/', views.user_login, name='login'),
    #path('logout/', views.user_logout, name='logout'),
    #path('upload/', views.upload_video, name='upload'),
]