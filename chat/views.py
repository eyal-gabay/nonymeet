from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest

from .likes import likes_page, names, room_name, take_text, last_msg
from .add_to_lobby import add, get_info, two_agree
from .security import login, admin


@login
def chat(request, path=""):
    if request.method == "GET":
        e = add(request.COOKIES["sid"], False)
        if e:
            user, gender, age, about = get_info(e)
            return render(request, "chat/accept.html", {"name": user, "gender": gender, "age": age, "about": about})
        else:
            # mo match
            pass
        return render(request, "chat/chat.html")
    if request.method == "POST":
        try:
            if request.POST["agree"] == "yes":
                agree = True
            else:
                agree = False
            try:
                two_agree(request.COOKIES["sid"].split(".")[0], request.POST["user"], agree)
            except IndexError:
                return HttpResponseBadRequest()
            return redirect("/chat/")
        except ValueError:
            return HttpResponseBadRequest()
        except KeyError:
            return HttpResponseBadRequest()


@admin
@login
def room(request, room_name=""):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


@login
def profile(request):
    return render(request, "chat/profile.html")


@login
def likes(request, path=""):
    user = request.COOKIES["sid"].split(".")[0]
    matches = likes_page(user)
    all_the_names = names(matches, user)
    all_before = all_the_names
    all_the_names = list(zip(tuple(all_the_names), tuple(last_msg(user, all_the_names))))
    if len(all_before) > len(last_msg(user, all_before)):
        all_the_names.append((all_before[-1], ""))
    if path:
        the_room = room_name(user, path)
        text = take_text(user, the_room)
        if text == "error":
            return HttpResponse(status=404)
    else:
        return render(request, "chat/likes.html", {"names": all_the_names})
    return render(request, "chat/likes.html", {"names": all_the_names,
                                               "room_name": the_room,
                                               "text": text,
                                               "date": ["e"],
                                               })
