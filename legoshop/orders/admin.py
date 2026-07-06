from django.contrib import admin
from .models import Order, OrderItem

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import LegoSet

@admin.register(LegoSet)
class LegoSetAdmin(ModelAdmin):  # Наследуемся от Unfold
    list_display = ['name', 'price', 'stock']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]
