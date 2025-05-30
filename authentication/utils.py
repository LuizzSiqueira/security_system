from .models import Log

def get_client_ip(request):
    """Obtém o IP real do cliente, verificando o cabeçalho X-Forwarded-For."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def registrar_log(user=None, status='', action_type='OTHER', success=False, request=None):
    """
    Cria um log customizado de qualquer ação no sistema.

    Parâmetros:
    - user: instância do usuário
    - status: mensagem descritiva da ação
    - action_type: tipo da ação, seguindo os definidos no modelo Log
    - success: se a ação foi bem-sucedida
    - request: necessário para capturar IP (pode ser omitido)
    """
    ip = get_client_ip(request) if request else None
    Log.objects.create(
        user=user,
        status=status,
        action_type=action_type,
        success=success,
        ip_origem=ip
    )

from .models import Log

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def register_log(user, status, request, action_type='OTHER', success=True):
    ip_origem = get_client_ip(request)
    Log.objects.create(
        user=user,
        status=status,
        action_type=action_type,
        success=success,
        ip_origem=ip_origem,
    )
