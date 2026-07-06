from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Order, OrderItem  # Импортируем твои настоящие модели


class OrderItemInline(TabularInline):  # Наследуемся от TabularInline из unfold
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "price", "quantity")


@admin.register(Order)
class OrderAdmin(ModelAdmin):  # Наследуемся от ModelAdmin из unfold
    list_display = ("id", "user", "status", "total_price", "created_at")
    list_filter = ("status",)
    inlines = [OrderItemInline]