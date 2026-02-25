from django.contrib import admin
from .models import Watch

# Register your models here.
@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'discounted_price')
    search_fields = ('name', 'brand', 'category')