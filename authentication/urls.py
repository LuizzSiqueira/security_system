from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    JWTProtectedView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    verify_mfa_view  # ✅ View de verificação do código MFA
)

urlpatterns = [
    # 🌐 Páginas principais
    path('home/', views.home_view, name='home'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('terms/', views.terms_view, name='terms'),
    path('delete-account/', views.delete_account_view, name='delete_account'),

    # 🔐 Verificação MFA (após login)
    path('verify-mfa/', verify_mfa_view, name='verify_mfa'),

    # 🔑 Recuperação de senha (default)
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='authentication/recovery_password.html',
        email_template_name='authentication/password_reset_email.html',
        subject_template_name='authentication/password_reset_subject.txt'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='authentication/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='authentication/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='authentication/password_reset_complete.html'
    ), name='password_reset_complete'),

    # 🔐 Rota protegida por JWT
    path('api/protected/', JWTProtectedView.as_view(), name='jwt_protected'),

    # 🔐 Recuperação de senha com logging
    path('log-password-reset/', CustomPasswordResetView.as_view(), name='log_password_reset'),
    path('log-password-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='log_password_reset_confirm'),
]
