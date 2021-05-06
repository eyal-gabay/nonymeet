from django.urls import path, include
from django.http import HttpResponse

import random
from chat.security import error_500


def not_found(request, exception=None):
    stat = [200, 302]
    all_chars = "zxc vbnm,./asdfg hjkl;'qw ertyui op[\n]12345 60-=Z XCVBNM<>?AS D FGHJKL:\"QWE RTYUIOP{}! @#$%^& *()_+"
    r = ""
    for i in range(random.randrange(5000)):
        for word in random.choice(all_chars):
            r += word
            if random.randrange(5) == 4:
                r += "<br>"
    r = "<h1>not found</h1><br><p hidden>" + r + "</p>"
    return HttpResponse(r, status=random.choice(stat))


def error500(request):
    r = error_500(request)
    return HttpResponse(r[0], status=r[1])


handler500 = error500
handler404 = not_found

urlpatterns = [
    path("chat/", include("chat.urls")),
    path("mobile_phone_/", include("app.urls")),
    path("home/", include("home.urls")),
    path("register/", include("register.urls")),
    path("oauth2/", include("oauth2.urls")),
    path("statistic", include("statistic.urls")),
    path("", include("register.urls")),
]

# start

open("database/connected", "w").write("0")
