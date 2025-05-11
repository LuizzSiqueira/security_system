from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Log, CustomPermission


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'created_at')
    list_filter = ('is_active', 'is_staff', 'groups')
    search_fields = ('username', 'email')
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informações de acesso', {'fields': ('login_attempts', 'locked_until')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'data_hora', 'ip_origem')
    search_fields = ('user__username', 'status')
    list_filter = ('data_hora',)


@admin.register(CustomPermission)
class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'permission_name', 'created_at')
    search_fields = ('user__username', 'permission_name')


admin.site.register(User, UserAdmin)
