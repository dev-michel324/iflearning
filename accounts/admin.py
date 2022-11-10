from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(auth_admin.UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    # fieldsets = auth_admin.UserAdmin.fieldsets + (
    #     ("Campos personalizados", {
    #      "fields": ("birth", "school_grade",)}),
    # )
