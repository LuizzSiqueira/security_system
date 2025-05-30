from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, label="Nome")
    last_name = forms.CharField(max_length=30, label="Sobrenome")

    terms_accepted_at = forms.BooleanField(
        label='Eu li e aceito os <a href="../terms" target="_blank">Termos de Uso</a>',
        required=True,
        error_messages={'required': 'Você deve aceitar os Termos de Uso para prosseguir.'}
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'terms_accepted_at',)