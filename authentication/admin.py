from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Log, Permission


# Classe Customizada para User no Admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_active', 'is_staff', 'created_at', 'login_attempts')  # Exibindo mais informações
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Segurança', {'fields': ('login_attempts', 'locked_until')}),
        ('Outros', {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
    )

    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')


# Classe Customizada para Log no Admin
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'data_hora', 'ip_origem')
    list_filter = ('status', 'data_hora')
    search_fields = ('user__username', 'status')


# Classe Customizada para Permissão no Admin
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'permission_name')


# Registro dos modelos no Admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Permission, PermissionAdmin)
