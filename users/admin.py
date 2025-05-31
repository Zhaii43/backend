from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'gender')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

    # Fields to display in the admin detail view
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Personal Info', {'fields': ('first_name', 'middle_name', 'last_name', 'contact', 'address', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Password Reset', {'fields': ('password_reset_token', 'password_reset_expiry')}),
    )

    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'contact', 'address', 'gender', 'password1', 'password2'),
        }),
    )

    # Ensure password is not displayed as a raw field
    readonly_fields = ('password_reset_token', 'password_reset_expiry')

admin.site.register(CustomUser, CustomUserAdmin)