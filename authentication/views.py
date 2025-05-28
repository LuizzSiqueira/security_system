# Django - atalhos, mensagens, utilitários
from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone

# Django - autenticação
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView
)

# Django REST framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# App local - formulários e modelos
from .forms import CustomUserCreationForm
from .models import Log

# Função para obter o IP do cliente da requisição
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Função para registrar logs de atividade com o IP correto
def register_log(user, status, request, action_type='OTHER', success=True):
    ip_origem = get_client_ip(request)
    Log.objects.create(
        user=user,
        status=status,
        action_type=action_type,
        success=success,
        ip_origem=ip_origem,
    )


# Página inicial
def home_view(request):
    return render(request, 'authentication/home.html')


# Login de usuário
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            register_log(user, 'Login realizado com sucesso', request, action_type='LOGIN', success=True)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            register_log(None, 'Falha ao tentar realizar login', request, action_type='LOGIN', success=False)
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})


# Logout de usuário
def logout_view(request):
    user = request.user
    logout(request)
    register_log(user, 'Logout realizado com sucesso', request, action_type='READ', success=True)
    messages.info(request, 'Você saiu com sucesso.')
    return redirect('login')


# Registro de usuário
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            register_log(user, 'Usuário registrado com sucesso', request, action_type='CREATE', success=True)
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
            register_log(None, 'Falha ao registrar usuário', request, action_type='CREATE', success=False)
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


# Lista de usuários (consulta - READ)
@login_required
def user_list_view(request):
    users = User.objects.all()
    register_log(request.user, 'Usuário visualizou a lista de usuários', request, action_type='READ', success=True)
    return render(request, 'authentication/user_list.html', {'users': users})


# View protegida por JWT
class JWTProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        register_log(request.user, 'Acesso autenticado via JWT', request, action_type='READ', success=True)
        return Response({
            "message": f"Olá, {request.user.username}. Você acessou com um token JWT válido."
        })


# Custom Password Reset View
class CustomPasswordResetView(PasswordResetView):
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            register_log(user, 'Solicitou redefinição de senha', self.request, action_type='PASSWORD_RESET', success=True)
        except User.DoesNotExist:
            register_log(None, f'Tentativa de redefinição de senha para e-mail não cadastrado: {email}', self.request, action_type='PASSWORD_RESET', success=False)
        return super().form_valid(form)


# Custom Password Reset Confirm View
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        user = form.user
        register_log(user, 'Senha redefinida com sucesso', self.request, action_type='PASSWORD_RESET', success=True)
        return super().form_valid(form)


# Custom Password Change View
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'authentication/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        user = self.request.user
        register_log(user, 'Senha alterada com sucesso', self.request, action_type='UPDATE', success=True)
        return super().form_valid(form)

    def form_invalid(self, form):
        user = self.request.user
        register_log(user, 'Falha ao tentar alterar a senha', self.request, action_type='UPDATE', success=False)
        return super().form_invalid(form)

def terms_view(request):
    return render(request, 'authentication/terms.html')
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

@login_required
def profile_view(request):
    user = request.user  # 👈 garante que estamos lidando com o usuário autenticado

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'authentication/profile.html', {
        'form': form,
        'user': user  # 👈 envia o usuário pro template, se quiser mostrar outras infos
    })