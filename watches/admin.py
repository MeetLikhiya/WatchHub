from django.contrib import admin
from .models import (
    Watch,
    Customer,
    Product,
    Cart,
    Address,
    Order,
    Wishlist,
    ContactMessage,
)


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
        'zipcode',
    )

    search_fields = (
        'name',
        'city',
        'state',
    )

    list_filter = (
        'state',
        'city',
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
        'discounted_price',
    )

    search_fields = (
        'name',
        'brand',
        'category',
    )

    list_filter = (
        'category',
        'brand',
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'watch', 'quantity', 'added_at')
    list_filter = ('added_at',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'city', 'state', 'pincode')
    search_fields = ('name', 'city', 'state', 'pincode')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'watch', 'quantity', 'total_amount', 'status', 'ordered_date')
    list_filter = ('status', 'ordered_date')
    search_fields = ('user__username', 'watch__name')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'watch', 'created_at')
    search_fields = ('user__username', 'watch__name')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')