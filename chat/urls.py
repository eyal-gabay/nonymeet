from django.urls import path
from . import views


urlpatterns = [
    path("", views.chat, name='index'),
    path("accept/<str:path>/", views.chat, name='users'),
    path("likes/", views.likes, name='index'),
    path('likes/<str:path>/', views.likes, name='room'),
    path("profile/", views.profile, name='profile'),
    path('<str:room_name>/', views.room, name='room'),
]

