from django.urls import path
from . import views

urlpatterns = [
    path("", views.register, name='index'),
    path("register/mobile_phone_", views.mobile_register, name='index'),
    path("register/logout/", views.logout, name='index'),
    path("register/register/", views.register_account, name='index'),
    # path("<str:path>", views.not_found, name='index'),
]

