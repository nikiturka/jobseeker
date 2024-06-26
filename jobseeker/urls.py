from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = ([
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('', include("main.urls")),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('chats/', include('chat.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
