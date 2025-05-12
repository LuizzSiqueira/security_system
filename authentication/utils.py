from .models import Log

def registrar_log(user, status, action_type, success, request=None):
    ip = None
    if request:
        ip = request.META.get('REMOTE_ADDR')  # Captura o IP de origem da requisição
    # Criando o log com os dados fornecidos
    Log.objects.create(
        user=user,
        status=status,
        action_type=action_type,  # Tipo da ação (Login, Logout, etc.)
        success=success,  # Indica se a ação foi bem-sucedida
        ip_origem=ip
    )
