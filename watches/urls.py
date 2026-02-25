from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("watches/", views.all_categories, name="all_watches"),
    path("category/<str:category>/", views.CategoryView.as_view(), name="category"),
]