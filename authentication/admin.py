from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Log, CustomPermission


# Customização do Admin para o modelo User
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'created_at', 'login_attempts', 'locked_until')
    list_filter = ('is_active', 'is_staff', 'groups', 'last_login', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)  # Ordenar por data de criação
    filter_horizontal = ('groups', 'user_permissions')
    
    # Campos para visualização detalhada de cada usuário
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informações de Acesso', {'fields': ('login_attempts', 'locked_until', 'last_login')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('created_at',)}),
    )
    
    # Campos para a criação de novos usuários
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


# Customização do Admin para o modelo Log
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'action_type', 'success', 'data_hora', 'ip_origem')  # Exibe mais informações sobre os logs
    search_fields = ('user__username', 'status', 'action_type', 'ip_origem')  # Pesquisa por tipo de ação, status e IP
    list_filter = ('data_hora', 'action_type', 'success', 'status', 'user')  # Filtros adicionais por status e usuário
    ordering = ('-data_hora',)  # Ordenação descendente para exibir os logs mais recentes

    # Adicionando campos e opções de filtro no admin para facilitar a análise de logs
    actions = ['mark_logs_as_successful', 'mark_logs_as_failed', 'clear_logs']  # Ações em massa para modificar os logs
    
    def mark_logs_as_successful(self, request, queryset):
        """Marcar os logs selecionados como 'Sucesso'"""
        queryset.update(success=True)
        self.message_user(request, "Logs marcados como bem-sucedidos.")
    
    def mark_logs_as_failed(self, request, queryset):
        """Marcar os logs selecionados como 'Falha'"""
        queryset.update(success=False)
        self.message_user(request, "Logs marcados como falha.")

    def clear_logs(self, request, queryset):
        """Excluir logs selecionados"""
        queryset.delete()
        self.message_user(request, "Logs excluídos com sucesso.")

    mark_logs_as_successful.short_description = "Marcar como bem-sucedidos"
    mark_logs_as_failed.short_description = "Marcar como falha"
    clear_logs.short_description = "Excluir logs selecionados"


# Customização do Admin para o modelo CustomPermission
@admin.register(CustomPermission)
class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'permission_name', 'created_at')
    search_fields = ('user__username', 'permission_name')
    list_filter = ('created_at', 'permission_name', 'user')  # Filtro por data de criação e permissão
    ordering = ('-created_at',)  # Ordenação pela data de criação das permissões

    # Adicionando ações personalizadas para o gerenciamento das permissões
    actions = ['assign_permission', 'revoke_permission', 'clear_permissions']
    
    def assign_permission(self, request, queryset):
        """Atribuir uma permissão a um ou mais usuários selecionados"""
        for permission in queryset:
            permission.user.user_permissions.add(permission.permission_name)
        self.message_user(request, "Permissões atribuídas com sucesso.")
    
    def revoke_permission(self, request, queryset):
        """Revogar uma permissão de um ou mais usuários selecionados"""
        for permission in queryset:
            permission.user.user_permissions.remove(permission.permission_name)
        self.message_user(request, "Permissões revogadas com sucesso.")
    
    def clear_permissions(self, request, queryset):
        """Excluir permissões selecionadas"""
        queryset.delete()
        self.message_user(request, "Permissões excluídas com sucesso.")

    assign_permission.short_description = "Atribuir permissão"
    revoke_permission.short_description = "Revogar permissão"
    clear_permissions.short_description = "Excluir permissões"


# Registrando os modelos no Django Admin
admin.site.register(User, UserAdmin)
