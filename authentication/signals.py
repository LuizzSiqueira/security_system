from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Log
from .utils import get_client_ip  # Importa a função auxiliar

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    Log.objects.create(
        user=user,
        status='Login realizado',
        action_type='login',
        success=True,
        ip_origem=ip
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    Log.objects.create(
        user=user,
        status='Logout realizado',
        action_type='logout',
        success=True,
        ip_origem=ip
    )
