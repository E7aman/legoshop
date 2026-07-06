from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product  # Импортируем твои настоящие модели


@admin.register(Category)
class CategoryAdmin(ModelAdmin):  # Наследуемся от Unfold ModelAdmin
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(ModelAdmin):  # Наследуемся от Unfold ModelAdmin
    list_display = ("name", "category", "price", "stock", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}