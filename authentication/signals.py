from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import localtime, now
from .models import Log

def get_client_ip(request):
    """Obtém o IP real do cliente, verificando o cabeçalho X-Forwarded-For."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Pega o primeiro IP da lista
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    Log.objects.create(user=user, status='Login realizado', ip_origem=ip)

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    Log.objects.create(user=user, status='Logout realizado', ip_origem=ip)
