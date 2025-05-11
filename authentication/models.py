from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth import get_user_model


# Gerenciador customizado para User
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        if not username:
            raise ValueError("O nome de usuário é obrigatório.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)  # Armazena senha com hash
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Modelo User customizado
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    # Define as relações com os grupos e permissões
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Adicione um related_name para evitar o conflito
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Adicione um related_name para evitar o conflito
        blank=True,
    )

    class Meta:
        db_table = 'users'
        managed = True
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username

    def reset_login_attempts(self):
        self.login_attempts = 0
        self.save()

    def increment_login_attempts(self):
        self.login_attempts += 1
        self.save()

    def lock_account(self, minutes=30):
        self.locked_until = timezone.now() + timezone.timedelta(minutes=minutes)
        self.save()

    def is_locked(self):
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False


# Modelo Log para registrar atividades do usuário
class Log(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)
    ip_origem = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'logs'
        managed = True
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    def __str__(self):
        return f"{self.user.username} - {self.status} - {self.data_hora}"


# Modelo de Permissões dos usuários (personalizado)
class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'permissions'
        managed = True
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'

    def __str__(self):
        return f"{self.user.username} - {self.permission_name}"
