from django.shortcuts import render


def index(request):
    return render(request, 'stats/main.html', {})


def room(request, room_name):
    return render(request, 'stats/chatroom.html', {
        'room_name': room_name
    })
