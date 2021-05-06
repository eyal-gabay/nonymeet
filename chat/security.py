import os
from django.http import HttpResponse


if __name__ != '__main__':
    from nonymeat import settings


def remove_duplicate_cookies():
    cookies_file = open("database/cookies").read().splitlines()
    cookies_file.reverse()
    a = []
    b = []
    for line in cookies_file:
        if line.split(".")[0] not in b:
            a.append(line)
            b.append(line.split(".")[0])
    open("database/cookies", "w")
    for i in a:
        open("database/cookies", "a").write(i + "\n")


def remove_duplicate_agree():
    cookies_file = open("database/agree").read().splitlines()
    a = []
    b = []
    for line in cookies_file:
        if line.split(".")[0] not in b:
            a.append(line)
            b.append(line.split(".")[0])
    open("database/agree", "w")
    for i in a:
        open("database/agree", "a").write(i + "\n")


def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)
    return (
        '{method} HTTP/1.1\n'
        '{headers}\n\n'
        '{body}\n\n\n'
    ).format(
        method=request.method,
        headers=headers,
        body=request.body[2:-1],
    )


def error_500(request):
    if not settings.DEBUG:
        open("database/errors/500_error.txt", "a").write(pretty_request(request) + "\n")
    return ["bad request", 400]


def check_cookie(cookie: str):
    for line in open("database/cookies"):
        if line.strip() == cookie:
            return True
    else:
        return False


def admin(self):
    def verify_cookie(request, *args, **kwargs):
        try:
            if request.COOKIES["sid"].split(".")[0] in ["e"]:
                return self(request)
        except KeyError:
            return HttpResponse(status=401)
        else:
            return HttpResponse(status=401)
    return verify_cookie


def login(self):
    def verify_cookie(request, *args, **kwargs):
        if check_cookie(request.COOKIES["sid"]):
            return self(request, *args, **kwargs)
        else:
            return HttpResponse(status=401)
    return verify_cookie


class ScanForError:
    def see_dub(self):
        for file in os.popen("ls -p ../database/ | grep -v / "):
            if "\n\n" in open("../database/" + file.strip()).read():
                open("../database/errors/2_lines_in_database.txt", "a").write(file.strip())

    def __call__(self):
        self.see_dub()


scan = ScanForError()

if __name__ == '__main__':
    scan()
