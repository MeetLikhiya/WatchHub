from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path("watches/", views.all_categories, name="all_watches"),
    path("category/<str:category>/", views.CategoryView.as_view(), name="category"),
    path("watch/<int:pk>/", views.WatchDetailView.as_view(), name="watch_detail"),

    # Authentication URLs
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # profile
    path('profile/', views.profile, name='profile'),

    #addresss
    path('add-address/', views.add_address, name='add_address'),
    path('address/', views.address, name='address'),

    path('edit-address/<int:id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:id>/', views.delete_address, name='delete_address'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('add-to-cart/<int:watch_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),

    path('checkout/', views.checkout, name='checkout'),
    # Admin Watch Management
    path('admin-watches/', views.admin_watch_list, name='admin_watch_list'),
    path('admin-watches/add/', views.admin_add_watch, name='admin_add_watch'),
    path('admin-watches/edit/<int:pk>/', views.admin_edit_watch, name='admin_edit_watch'),
    path('admin-watches/delete/<int:pk>/', views.admin_delete_watch, name='admin_delete_watch'),



    # password reset
    # path(
    #     "password-reset/",
    #     auth_views.PasswordResetView.as_view(
    #         template_name="watches/password_reset.html"
    #     ),
    #     name="password_reset"
    # ),

]

# Serve media files (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)