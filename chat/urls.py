from django.urls import path
from . import views

urlpatterns = [
    path('user_id=<int:user_id>', views.user_all_chats, name='user-chats'),
    path('user_id=<int:user_id>/chat_id=<int:chat_id>', views.user_chat, name='user-chat'),
]
