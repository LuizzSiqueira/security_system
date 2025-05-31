# Security System - Sistema de Autenticação Seguro

O **Security System** é um sistema de autenticação e administração de usuários desenvolvido com Django, com foco em segurança, usabilidade e conformidade com a LGPD. O sistema oferece funcionalidades como login, registro de usuários, recuperação de senha, autenticação de dois fatores (2FA) e proteção contra tentativas de login inválidas.

## Funcionalidades

- **Registro de usuários**: Permite que novos usuários se registrem com nome, email e senha.
- **Login de usuários**: Usuários podem acessar suas contas com autenticação via email e senha.
- **Logout**: Usuários podem sair de suas contas com segurança.
- **Recuperação de senha**: Permite que o usuário recupere sua senha via email.
- **Autenticação de dois fatores (2FA)**: Proporciona uma camada adicional de segurança no processo de login.

## Tecnologias Utilizadas

- **Django**: Framework de alto nível para desenvolvimento rápido e eficiente.
- **PostgreSQL**: Banco de dados relacional utilizado para armazenar dados do sistema.
- **JWT (JSON Web Tokens)**: Usado para autenticação e gerenciamento de sessões.
- **Django Rest Framework**: Para criação de APIs RESTful e integração com JWT.
- **HTML, CSS**: Para construção da interface do usuário.

## Instalação

### Pré-requisitos

Certifique-se de ter o Python 3.x e o PostgreSQL instalados em sua máquina. Caso contrário, siga as instruções nos links abaixo:

- [Instalar Python](https://www.python.org/downloads/)
- [Instalar PostgreSQL](https://www.postgresql.org/download/)

### Passos para instalação

1. Clone este repositório:
   ```bash
   git clone git@github.com:LuizzSiqueira/security_system.git

2. Instale os requerimentos
   ```bash
   pip install -r requirements.txt   