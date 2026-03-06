from django.contrib import admin
from .models import Watch,Customer, Product

# Register your models here.
@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'discounted_price')
    search_fields = ('name', 'brand', 'category')

# -----------------------------
# Customer Admin
# -----------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'name',
        'locality',
        'city',
        'state',
        'zipcode'
    )

    search_fields = (
        'name',
        'city',
        'state'
    )

    list_filter = (
        'state',
        'city'
    )


# -----------------------------
# Product Admin
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'brand',
        'category',
        'price',
        'discounted_price'
    )

    search_fields = (
        'name',
        'brand',
        'category'
    )

    list_filter = (
        'category',
        'brand'
    )