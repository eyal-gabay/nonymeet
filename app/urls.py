from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.mobile_register, name='index'),
    path("login/", views.login, name='index'),
    path("login_redirect/", views.login_redirect, name='index'),
]
