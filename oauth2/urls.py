from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path("", auth_views.LogoutView.as_view(), name='index'),
]
