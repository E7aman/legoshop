from django.contrib import admin
from .models import Category, Product

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import LegoSet

@admin.register(LegoSet)
class LegoSetAdmin(ModelAdmin):  # Наследуемся от Unfold
    list_display = ['name', 'price', 'stock']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
