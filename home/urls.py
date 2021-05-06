from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='index'),
    path("edit/", views.edit, name='index'),
    path("settings/", views.settings, name='index'),
]
