from django.middleware.csrf import _get_new_csrf_token
from django.http import HttpResponse
from django.shortcuts import render, redirect

import hashlib
import requests
import random

from chat import security
from chat.message import add


def register(request):
    try:
        if security.check_cookie(request.COOKIES["sid"]):
            return redirect("/home/")
    except KeyError:
        pass
    if request.method == "GET":
        return render(request, "register/login.html")
    elif request.method == "POST":
        username, password = request.POST['username'], str(hashlib.sha3_256(bytes(request.POST['password'].strip(), 'utf-8')).hexdigest())
        for line in open("database/register").read().splitlines():
            line = line.split()
            try:
                if line[0] == username and line[1] == password:
                    ran = line[0] + "." + str(random.random())[2:]
                    open("database/cookies", "a").write(ran + "\n")
                    security.remove_duplicate_cookies()
                    r = redirect("/home/")
                    r.set_cookie("sid", ran)
                    return r
            except IndexError:
                pass
        return render(request, "register/login.html", {"warning": "bad username or password"})


def logout(request):
    r = redirect("/home")
    # db = open("database/chat_number", "r").read()
    # open("database/chat_number", "w").write(db.replace(request.COOKIES["sid"], ""))
    r.delete_cookie("sid")
    return r


def register_account(request):
    if request.method == "GET":
        return render(request, "register/register_account.html")
    elif request.method == "POST":
        try:
            rc = request.POST["g-recaptcha-response"]
            req = requests.post(f"https://www.google.com/recaptcha/api/siteverify?secret=6Lfdzv8ZAAAAAAuFeenJ2r5-r4sAaI7L_m5bOz5d&response={rc}")
        except KeyError:
            pass
            # return HttpResponse(status=400)
        if not req.json()["success"]:
            pass
            # return HttpResponse(status=400)
        if not request.POST["username"].isalnum():
            return render(request, "register/register_account.html", {"c": "not the same password :("})
        if request.POST["password"] != request.POST["passwordagain"]:
            return render(request, "register/register_account.html", {"c": "password and password again can't be the same :("})
        for line in open("database/register"):
            if line.split()[0] == request.POST["username"]:
                return render(request, "register/register_account.html", {"c": "we got this username :("})
            if " " in request.POST['username'].strip() or " " in request.POST['password'].strip() or " " in request.POST['nickname'].strip():
                return render(request, "register/register_account.html", {"c": "can't put spaces :("})
            if " " in request.POST['username'].strip():
                return render(request, "register/register_account.html", {"c": "can't put . in username :("})
        open("database/register", "a").write(
            f"\n{request.POST['username'].strip()} {str(hashlib.sha3_256(bytes(request.POST['password'].strip(), 'utf-8')).hexdigest())} {request.POST['nickname'].strip()}")
        add(request.POST['username'].strip(), "hello " + request.POST['username'].strip())
        r = redirect("/")
        return r


# add php
def not_found(request, path):
    if request.GET.keys():
        q = "?"
        k_v = []
        f = ""
        for t in list(zip(request.GET.keys(), request.GET.values())):
            for va in t:
                k_v.append(va)
        for i in range(len(k_v)):
            if not i % 2:
                f = f.__add__(k_v[i] + "=")
            else:
                f = f.__add__(k_v[i] + "&")
        f = f[0:-1]
    else:
        q = ""
        f = ""
    r = requests.get(f"http://192.168.10.9/{path}{q}{f}")
    return HttpResponse(r.text, status=r.status_code)


def mobile_register(request):
    r = render(request, "mobile/register/login.html")
    r.set_cookie("csrftoken", _get_new_csrf_token())
    return r
