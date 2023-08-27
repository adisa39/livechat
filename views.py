from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html",)


def room(request, room_name):
    # we will get the chatbox name from the url
    return render(request, "chat/room.html", {"room_name": room_name})
