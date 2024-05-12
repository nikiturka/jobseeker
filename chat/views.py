from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from chat.models import Room
from main.models import CustomUser


def user_all_chats(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    chats = Room.objects.filter(users=user)

    return render(request, 'chat/user_chats.html', {'chats': chats})


def user_chat(request, user_id, chat_id):
    user = CustomUser.objects.get(pk=user_id)
    chat = Room.objects.get(pk=chat_id)

    return render(request, 'chat/user_chat.html', {'chat': chat})
