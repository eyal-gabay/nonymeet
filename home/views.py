from django.shortcuts import render, redirect
from urllib.parse import unquote_plus
from django.http import HttpResponse, HttpResponseBadRequest

from chat.security import check_cookie, login

import html


def home(request):
    try:
        if not check_cookie(request.COOKIES["sid"]):
            re = redirect("/register")
            re.delete_cookie("sid")
            return re
    except KeyError:
        re = redirect("/register")
        re.delete_cookie("sid")
        return re
    if request.method == "GET":
        for line in open("database/profile"):
            try:
                if request.COOKIES["sid"].split(".")[0] == line.split("username=")[1].split("&")[0]:
                    try:
                        if line.split("mygender=")[1].split("&")[0] == "male":
                            mg1 = "checked=checked"
                            mg2 = ""
                        else:
                            mg1 = ""
                            mg2 = "checked=checked"
                        if line.split("genderiwant=")[1].split("&")[0] == "male":
                            giw1 = "checked=checked"
                            giw2 = ""
                        else:
                            giw1 = ""
                            giw2 = "checked=checked"
                        return render(request, "home/myself.html", {"cant": "",
                                                                  "nn": line.split("nickname=")[1].split("&")[0],
                                                                  "ma": line.split("myage=")[1].split("&")[0],
                                                                  "maiw": line.split("minage=")[1].split("&")[0],
                                                                  "aiw": line.split("maxage=")[1].split("&")[0],
                                                                  "mg1": mg1,
                                                                  "mg2": mg2,
                                                                  "giw1": giw1,
                                                                  "giw2": giw2,
                                                                  "abm": html.unescape(line.split("aboutme=")[1].strip("\n")),
                                                                  })
                    except IndexError:
                        return render(request, "home/home.html")
            except KeyError:
                return redirect("/")

        else:
            return render(request, "home/home.html")
    elif request.method == "POST":
        with open("database/profile") as profile:
            r = profile.read()
            a = []
            for line in r.splitlines():
                if not line == "":
                    a.append(line)
            open("database/profile", "w")
            for i in a:
                open("database/profile", "a").write(i + "\n")
            try:
                is_he = False
                for line in open("database/profile"):
                    if request.COOKIES["sid"].split(".")[0] == line.split("username=")[1].split("&")[0]:
                        is_he = True
                if not is_he:
                    open("database/profile", "a").write(unquote_plus("username=" + request.COOKIES["sid"].split(".")[0] + "&" + str(request.body)[2:-1].replace(str(request.body)[2:-1].split("&")[0] + "&", "")))
                else:
                    for user in r.splitlines():
                        if user[9:].split("&")[0] == request.COOKIES["sid"].split(".")[0]:
                            if not str(request.body)[2:-1].split("myage=")[1].split("&")[0].isdigit():
                                return HttpResponseBadRequest()
                            open("database/profile", "w").write(unquote_plus(r.replace(user, "username=" + request.COOKIES["sid"].split(".")[0] + "&" + str(request.body)[2:-1].replace(str(request.body)[2:-1].split("&")[0] + "&", ""))))
            finally:
                for line in open("database/profile"):
                    if request.COOKIES["sid"].split(".")[0] == line.split("&")[0][9:]:
                        if line.split("mygender=")[1].split("&")[0] == "male":
                            mg1 = "checked=checked"
                            mg2 = ""
                        else:
                            mg1 = ""
                            mg2 = "checked=checked"
                        if line.split("genderiwant=")[1].split("&")[0] == "male":
                            giw1 = "checked=checked"
                            giw2 = ""
                        else:
                            giw1 = ""
                            giw2 = "checked=checked"
                        return render(request, "home/myself.html",
                                      {"cant": "",
                                       "nn": line.split("nickname=")[1].split("&")[0],
                                       "ma": line.split("myage=")[1].split("&")[0],
                                       "maiw": line.split("minage=")[1].split("&")[0],
                                       "aiw": line.split("maxage=")[1].split("&")[0],
                                       "mg1": mg1,
                                       "mg2": mg2,
                                       "giw1": giw1,
                                       "giw2": giw2,
                                       "abm": html.unescape(line.split("aboutme=")[1].strip("\n")),
                                       }
                                      )
                return render(request, "home/home.html", {"cant": ""})


@login
def edit(request):
    if request.method == "GET":
        for line in open("database/profile"):
            try:
                if request.COOKIES["sid"].split(".")[0] == line.split("username=")[1].split("&")[0]:
                    try:
                        if line.split("mygender=")[1].split("&")[0] == "male":
                            mg1 = "checked=checked"
                            mg2 = ""
                        else:
                            mg1 = ""
                            mg2 = "checked=checked"
                        if line.split("genderiwant=")[1].split("&")[0] == "male":
                            giw1 = "checked=checked"
                            giw2 = ""
                        else:
                            giw1 = ""
                            giw2 = "checked=checked"
                        return render(request, "home/home.html", {"cant": "",
                                                                  "nn": line.split("nickname=")[1].split("&")[0],
                                                                  "ma": line.split("myage=")[1].split("&")[0],
                                                                  "maiw": line.split("minage=")[1].split("&")[0],
                                                                  "aiw": line.split("maxage=")[1].split("&")[0],
                                                                  "mg1": mg1,
                                                                  "mg2": mg2,
                                                                  "giw1": giw1,
                                                                  "giw2": giw2,
                                                                  "abm": html.unescape(line.split("aboutme=")[1].strip("\n")),
                                                                  })
                    except IndexError:
                        return render(request, "home/home.html")
            except KeyError:
                return redirect("/")
        else:
            return render(request, "home/home.html")
    else:
        return redirect("/home")


@login
def settings(request):
    return render(request, "home/settings.html")

