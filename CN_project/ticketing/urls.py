from django.urls import path
from ticketing import views

urlpatterns = [

    path('my/', views.my_tickets_view),
    path('my/new/', views.create_ticket),
    path('my/<int:pk>/', views.my_ticket_view),
    path('my/<int:pk>/reply/', views.my_ticket_reply),

    path('users/', views.assigned_tickets_view),
    path('users/all/', views.unassigned_tickets_view),
    path('users/<int:pk>/', views.user_ticket_view),
    path('users/<int:pk>/assign/', views.assign_ticket),
    path('users/<int:pk>/reply/', views.user_ticket_reply),
    path('users/<int:pk>/close/', views.user_ticket_close),

]

