from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path("watches/", views.all_categories, name="all_watches"),
    path("category/<str:category>/", views.CategoryView.as_view(), name="category"),
    path("watch/<int:pk>/", views.WatchDetailView.as_view(), name="watch_detail"),

    # ✅ Authentication URLs
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]

# Serve media files (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)