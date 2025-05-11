from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

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
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

# Logout de usuário
def logout_view(request):
    """Realiza o logout do usuário"""
    logout(request)
    messages.info(request, 'Você saiu com sucesso.')
    return redirect('login')

# Registro de usuário
def register_view(request):
    """Realiza o registro de um novo usuário"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})
