def add_ip(request):
    ip = request.META["REMOTE_HOST"]
    open("database/ip/all_the_ip", "a").write(ip + "\n")
