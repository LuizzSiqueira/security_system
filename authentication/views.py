# Python padrão / built-in
from functools import cache

# Django - atalhos, mensagens, utilitários
from django import forms
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.cache import cache   # <=== Import correto do cache do Django

# Django - autenticação
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)

# Django REST framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# App local - formulários, modelos e utilitários
from .forms import CustomUserCreationForm
from .models import Log
from .utils import get_client_ip, register_log
from django.core.mail import send_mail



# --------------------------------------
# Página inicial (home)
# --------------------------------------
def home_view(request):
    return render(request, 'authentication/home.html')


# --------------------------------------
# Login de usuário
# Registra sucesso e falha no log
# --------------------------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        username = request.POST.get('username')
        ip = get_client_ip(request)
        cache_key = f'login_attempts_{username}_{ip}'
        attempts = cache.get(cache_key, 0)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            register_log(user, 'Login realizado com sucesso', request, action_type='LOGIN', success=True)
            messages.success(request, 'Login realizado com sucesso!')
            cache.delete(cache_key)
            return redirect('home')
        else:
            attempts += 1
            cache.set(cache_key, attempts, timeout=3600)

            if attempts >= 3:
                try:
                    user = User.objects.get(username=username)  # usa User do get_user_model()
                    send_mail(
                        subject='Alerta de segurança: Tentativas de login falhas',
                        message=(
                            f'Olá {user.get_full_name() or user.username},\n\n'
                            'Detectamos 3 ou mais tentativas falhas de login na sua conta.\n'
                            'Se não foi você, recomendamos alterar sua senha o quanto antes.\n\n'
                            'Atenciosamente,\nSecurity System'
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                except User.DoesNotExist:
                    pass

            register_log(None, f'Falha ao tentar realizar login para {username}', request, action_type='LOGIN', success=False)
            messages.error(request, 'Usuário ou senha inválidos.')

    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})



# --------------------------------------
# Logout de usuário
# Registra a ação no log
# --------------------------------------
def logout_view(request):
    user = request.user
    logout(request)
    register_log(user, 'Logout realizado com sucesso', request, action_type='LOGOUT', success=True)
    messages.info(request, 'Você saiu com sucesso.')
    return redirect('login')


# --------------------------------------
# Registro de usuário
# Registra sucesso e falha no log
# --------------------------------------
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Não salva ainda

            # Captura o consentimento (campo booleano do form)
            consent = form.cleaned_data.get('consent_given', False)
            user.consent_given = consent

            # Registra o horário do aceite dos termos (se consentido)
            if consent:
                user.terms_accepted_at = timezone.now()
            else:
                user.terms_accepted_at = None

            user.save()  # Salva o usuário com os campos ajustados

            register_log(user, 'Usuário registrado com sucesso', request, action_type='CREATE', success=True)
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')
        else:
            register_log(None, 'Falha ao registrar usuário', request, action_type='CREATE', success=False)
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


# --------------------------------------
# Visualização da lista de usuários (consulta)
# Registra a ação no log
# --------------------------------------
@login_required
def user_list_view(request):
    users = User.objects.all()
    register_log(request.user, 'Usuário visualizou a lista de usuários', request, action_type='READ', success=True)
    return render(request, 'authentication/user_list.html', {'users': users})


# --------------------------------------
# View protegida por JWT
# Registra o acesso no log
# --------------------------------------
class JWTProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        register_log(request.user, 'Acesso autenticado via JWT', request, action_type='READ', success=True)
        return Response({
            "message": f"Olá, {request.user.username}. Você acessou com um token JWT válido."
        })


# --------------------------------------
# Custom Password Reset View
# Registra solicitação de redefinição no log, com sucesso ou falha
# --------------------------------------
class CustomPasswordResetView(PasswordResetView):
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'  # versão em texto (fallback)
    html_email_template_name = 'authentication/password_reset_email_html.html'  # ✅ versão HTML
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            register_log(user, 'Solicitou redefinição de senha', self.request, action_type='PASSWORD_RESET', success=True)
        except User.DoesNotExist:
            register_log(None, f'Tentativa de redefinição para e-mail não cadastrado: {email}', self.request, action_type='PASSWORD_RESET', success=False)
        return super().form_valid(form)



# --------------------------------------
# Custom Password Reset Confirm View
# Registra sucesso da redefinição de senha no log
# --------------------------------------
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        user = form.user
        register_log(user, 'Senha redefinida com sucesso', self.request, action_type='PASSWORD_RESET', success=True)
        return super().form_valid(form)


# --------------------------------------
# Custom Password Change View
# Registra sucesso e falha na alteração de senha no log
# --------------------------------------
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


# --------------------------------------
# Termos de uso
# --------------------------------------
def terms_view(request):
    return render(request, 'authentication/terms.html')


# --------------------------------------
# Formulário de edição de perfil
# --------------------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# --------------------------------------
# Atualização do perfil do usuário
# Registra sucesso e falha no log
# --------------------------------------
@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            register_log(user, 'Perfil atualizado com sucesso', request, action_type='UPDATE', success=True)
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
        else:
            register_log(user, 'Falha ao atualizar perfil', request, action_type='UPDATE', success=False)
            messages.error(request, 'Erro ao atualizar perfil.')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'authentication/profile.html', {
        'form': form,
        'user': user,
    })


# --------------------------------------
# Exclusão da conta do usuário
# Registra a ação no log antes de deletar
# --------------------------------------
@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        register_log(user, 'Solicitou exclusão da conta', request, action_type='DELETE', success=True)
        logout(request)  # Desloga antes de deletar
        user.delete()
        messages.success(request, 'Sua conta foi deletada com sucesso. Sentiremos sua falta!')
        return redirect('home')
    else:
        return redirect('profile')

