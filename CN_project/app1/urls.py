from django.urls import path
from . import views

app_name = 'app1'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),

    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('admin_login/', views.admin_login, name='adminlogin'),
    path('admin_signup/', views.adminsignup, name='adminsignup'),
    path('logout/', views.user_logout, name='logout'),

    path('upload/', views.upload_video, name='upload'),

    path('video/<int:video_id>/', views.watch_video, name='watch_video'), # with socket

    path('watch/<int:video_id>/', views.stream_video, name='stream_video'), # with html
    path('watch/<int:video_id>/f/', views.fstream, name='fstream'),
    path('watch/<int:video_id>/add_like/', views.add_like, name='add_like'),
    path('watch/<int:video_id>/add_dislike/', views.add_dislike, name='add_dislike'),
    path('watch/<int:video_id>/add_comment/', views.add_comment, name='add_comment'),

    path('video/add_lablel/', views.add_label, name='add_label'),
    path('video/make_unavailable/', views.video_status, name='status'),
    path('strike_resolving/<str:username>', views.strike_resolving, name='strike_resolving'),

]
