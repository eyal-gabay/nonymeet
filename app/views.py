from django.middleware.csrf import _get_new_csrf_token

from django.shortcuts import render, redirect
from django.http import HttpResponse


def mobile_register(request):
    r = render(request, "mobile/register/login.html")
    r.set_cookie("csrf", _get_new_csrf_token())
    return r


def login(request):
    r = render(request, "mobile/register/login.html")
    r.set_cookie("csrf", _get_new_csrf_token())
    return r


def login_redirect(request):
    r = redirect("/mobile_phone_/login/")
    r.set_cookie("csrf", _get_new_csrf_token())
    return r
