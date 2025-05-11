from .models import Log

def registrar_log(user, status, request=None):
    ip = None
    if request:
        ip = request.META.get('REMOTE_ADDR')
    Log.objects.create(user=user, status=status, ip_origem=ip)