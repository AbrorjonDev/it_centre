from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

#local imports
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    list_display = ("username", "is_superuser", "is_director", "is_admin")
    list_filter = ("is_superuser", "is_director", "is_admin")
    search_fields = ("username", "first_name", "last_name")
    readonly_fields = ("password", )
    fieldsets = (
        ("", {
            "fields": ("username", "password")
        }), 
        ("PERMISSIONS", {
            "fields":("is_superuser", "is_staff", "is_active", "is_director", "is_admin")
        }),
        ("IMPORTANT", {
            "fields":(("date_joined", "last_login"), "created_by")
        })
    )