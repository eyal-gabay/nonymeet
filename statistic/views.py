from django.shortcuts import render

from chat.security import admin


@admin
def statistic(request):
    if request.method == "GET":
        log_in_users = str(len("".join(line for line in open("database/profile") if not line.isspace()).splitlines()))
        number_of_connected_users = open("database/connected").read()
        return render(request, "statistic/statistic.html", {"number_of_login_users": log_in_users,
                                                            "number_of_connected_users": number_of_connected_users},)
