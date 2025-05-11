from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Log
from django.utils import timezone

# Função para registrar logs de atividade com o IP correto
def register_log(user, status, request):
    ip_origem = get_client_ip(request)  # Obtém o IP correto
    Log.objects.create(
        user=user,
        status=status,
        ip_origem=ip_origem,
    )

# Página inicial
def home_view(request):
    """Renderiza a página inicial"""
    return render(request, 'authentication/home.html')  # Templates organizados em authentication/

# Login de usuário
def login_view(request):
    """Realiza o login do usuário"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Registrar log de login bem-sucedido
            register_log(user, f'Login realizado com sucesso', request.META.get('REMOTE_ADDR'))
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            # Registrar falha no login
            register_log(None, 'Falha ao tentar realizar login', request.META.get('REMOTE_ADDR'))
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

# Logout de usuário
def logout_view(request):
    """Realiza o logout do usuário"""
    user = request.user
    logout(request)
    # Registrar log de logout
    register_log(user, 'Logout realizado', request.META.get('REMOTE_ADDR'))
    messages.info(request, 'Você saiu com sucesso.')
    return redirect('login')

# Registro de usuário
def register_view(request):
    """Realiza o registro de um novo usuário"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Registrar log de criação de usuário
            register_log(user, 'Cadastro realizado com sucesso', request.META.get('REMOTE_ADDR'))
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})
