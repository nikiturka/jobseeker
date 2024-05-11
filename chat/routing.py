from django.urls import path
from chat import consumers
from django.conf import settings
from django.conf.urls.static import static

websocket_urlpatterns = [
    path(r'ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
