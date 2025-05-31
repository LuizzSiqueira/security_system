from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta


# Gerenciador customizado para o modelo User
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        if not username:
            raise ValueError("O nome de usuário é obrigatório.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Modelo de Usuário customizado
from django.utils import timezone

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    consent_given = models.BooleanField(default=False)
    terms_accepted_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )

    class Meta:
        db_table = 'users'
        managed = True
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def reset_login_attempts(self):
        self.login_attempts = 0
        self.save()

    def increment_login_attempts(self):
        self.login_attempts += 1
        self.save()

    def lock_account(self, minutes=30):
        self.locked_until = timezone.now() + timedelta(minutes=minutes)
        self.save()

    def is_locked(self):
        return self.locked_until and timezone.now() < self.locked_until



# Modelo de Log para rastrear atividades dos usuários
class Log(models.Model):
    ACTION_TYPES = [
    ('LOGIN', 'Login'),
    ('LOGOUT', 'Logout'),
    ('PASSWORD_RESET', 'Redefinição de senha'),
    ('PASSWORD_CHANGE', 'Alteração de senha'),
    ('PERMISSION_CHANGE', 'Mudança de permissão'),
    ('ACCOUNT_LOCKED', 'Conta bloqueada'),
    ('REGISTER', 'Cadastro'),
    ('CREATE', 'Criação'),
    ('READ', 'Consulta'),
    ('UPDATE', 'Atualização'),
    ('DELETE', 'Exclusão'),
    ('OTHER', 'Outro'),
]


    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=255)
    action_type = models.CharField(
        max_length=50,
        choices=ACTION_TYPES,
        default='LOGIN'  # Valor padrão para o campo action_type, caso não seja especificado
    )
    success = models.BooleanField(default=False)
    data_hora = models.DateTimeField(auto_now_add=True)
    ip_origem = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'logs'
        managed = True
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    def __str__(self):
        return f"{self.user.username if self.user else 'Usuário não definido'} - {self.action_type} - {self.status} - {self.data_hora}"

    # Anotação explicativa:
    # Adicionamos o valor padrão 'LOGIN' no campo 'action_type'. Isso garante que, quando um novo log for criado
    # e o campo 'action_type' não for especificado, o Django automaticamente irá atribuir o valor 'LOGIN' a ele.
    # Isso pode ser útil para manter a consistência no registro de atividades, especialmente para logs que não
    # exigem um tipo de ação específico, como no caso de eventos genéricos de login.

# Modelo personalizado de Permissões por usuário
class CustomPermission(models.Model):  # Renomeado para evitar conflito com modelo nativo
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'custom_permissions'
        managed = True
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'

    def __str__(self):
        return f"{self.user.username} - {self.permission_name}"
