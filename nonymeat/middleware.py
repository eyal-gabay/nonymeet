from django.http import HttpResponseBadRequest, HttpResponse

from statistic import ip


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


class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.domain = "10.0.0.1"

    def __call__(self, request):
        ip.add_ip(request)

        # main domain
        return self.get_response(request)
        if self.domain in request.headers["host"]:
            return self.get_response(request)
        else:
            return HttpResponseBadRequest()
