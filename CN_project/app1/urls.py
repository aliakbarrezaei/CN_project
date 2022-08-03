
from django.urls import path
from . import views
app_name='app1'
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('admin_signup/', views.adminsignup, name='adminsignup'),
    path('login/', views.user_login, name='login'),
    path('admin_login/', views.admin_login, name='adminlogin'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload_video, name='upload'),
    path('video/add_comment/', views.add_comment, name='add_comment'),
    path('video/add_like/', views.add_like, name='add_like'),
    path('video/add_dislike/', views.add_dislike, name='add_dislike'),
    path('video/add_lablel/', views.add_label, name='add_label'),
    path('video/make_unavailable/', views.video_status, name='status'),
]