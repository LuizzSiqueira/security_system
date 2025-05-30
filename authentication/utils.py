from .models import Log

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def registrar_log(user, status, action_type, success, request=None):
    ip = get_client_ip(request) if request else None
    Log.objects.create(
        user=user,
        status=status,
        action_type=action_type,
        success=success,
        ip_origem=ip
    )
