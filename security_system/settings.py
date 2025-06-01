from logging import config
from pathlib import Path
from decouple import config, Csv
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Leitura da chave secreta do .env
SECRET_KEY = config('SECRET_KEY')

# Modo de Debug
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=lambda v: [s.strip() for s in v.split(',')])

# Aplicações instaladas
INSTALLED_APPS = [
    'authentication.apps.AuthenticationConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'widget_tweaks',  # Para manipulação de widgets no Django
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'security_system.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Caminho global dos templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'security_system.wsgi.application'

# Configuração do banco de dados com Supabase
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='postgres'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'authentication.validators.ComplexPasswordValidator',  # 👈 Aqui está o novo validador
    },
]


# Usar variáveis de ambiente para as credenciais de e-mail
FROM_EMAIL = os.getenv("FROM_EMAIL", "central.seguranca.app@gmail.com")
FROM_PASSWORD = os.getenv("FROM_PASSWORD", "iuhl pemq gurn mqls")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Configurações do back-end de envio de e-mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = SMTP_SERVER
EMAIL_PORT = SMTP_PORT
EMAIL_USE_TLS = True  # Usar TLS para segurança
EMAIL_HOST_USER = FROM_EMAIL
EMAIL_HOST_PASSWORD = FROM_PASSWORD
DEFAULT_FROM_EMAIL = FROM_EMAIL

# settings.py

AUTH_USER_MODEL = 'authentication.User'  # Aqui 'authentication' é o nome da sua app


# Arquivos estáticos (CSS, JS, imagens)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'authentication', 'static'),  # Agora aponta para a pasta correta
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Apenas usuários autenticados podem acessar
    ],
}
