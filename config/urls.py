from django.contrib import admin
from django.urls import path, include
from django.conf import settings # For serving media files during development
from django.conf.urls.static import static #

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("watches.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
