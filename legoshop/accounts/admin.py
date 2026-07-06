from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin

from .models import User as CustomUser  # если у вас своя модель User


@admin.register(User)  # или CustomUser, если своя модель
class CustomUserAdmin(UserAdmin, ModelAdmin):
    # Используем unfold-стили для отображения списков
    list_display = ("username", "email", "role", "is_active", "date_joined")
    list_filter = ("role", "is_active")

    # Дополняем стандартные fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ("Shop Role", {"fields": ("role", "phone", "address")}),
    )