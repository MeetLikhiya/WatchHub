from django.contrib import admin
from django.urls import path, include
from django.conf import settings # For serving media files during development
from django.conf.urls.static import static #
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("watches.urls")),

    # Password Reset URLs

    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='watches/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='watches/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='watches/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset_done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='watches/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
