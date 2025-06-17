from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('employee_id', 'username', 'email', 'first_name', 'last_name', 'role', 'department', 'manager')
    list_filter = ('role', 'department', 'is_active')
    search_fields = ('employee_id', 'username', 'email', 'first_name', 'last_name')
    ordering = ('employee_id',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Employee Information', {
            'fields': ('employee_id', 'role', 'phone', 'department', 'designation', 'manager')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Employee Information', {
            'fields': ('employee_id', 'role', 'phone', 'department', 'designation', 'manager')
        }),
    )

admin.site.register(User, CustomUserAdmin)