from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('', include("main.urls")),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
