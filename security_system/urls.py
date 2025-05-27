from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Importe sua view terms_view do app authentication
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redireciona '/' para 'home'
    path('', lambda request: redirect('home')),

    # Inclui URLs do app de autenticação
    path('', include('authentication.urls')),

    # Endpoints JWT (API)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Rota para a página de termos de uso (você pode manter aqui ou mover para authentication.urls)
    path('terms/', views.terms_view, name='terms'),
]
