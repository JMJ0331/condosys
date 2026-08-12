from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model"""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'document')}),
        ('Role & Status', {'fields': ('role', 'status', 'garden')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'status'),
        }),
    )
    list_display = ('email', 'get_full_name', 'role', 'status', 'is_active')
    list_filter = ('role', 'status', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'document')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'

