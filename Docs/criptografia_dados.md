# Criptografia de Dados Pessoais em Repouso

Este documento descreve a abordagem adotada para criptografar dados sensíveis no banco de dados.

---

## 🔐 Escopo da Criptografia

| Campo  | Tipo de Dado  | Necessidade de Criptografia        |
| ------ | ------------- | ---------------------------------- |
| Senha  | Autenticação  | ✔️ Hash com PBKDF2 (Django padrão) |
| E-mail | Pessoal       | ✔️ AES                             |
| Nome   | Identificação | ⚠️ Opcional                        |

---

## 🔧 Implementação

```python
from encrypted_model_fields.fields import EncryptedEmailField

class User(models.Model):
    email = EncryptedEmailField(unique=True)
```

```bash
pip install django-encrypted-model-fields
```

---

## 🔑 Gerenciamento de Chaves

* As chaves de criptografia são armazenadas em variáveis de ambiente.
* O acesso às chaves é restrito e auditado.

---

## 📌 Detalhes Técnicos

* O campo `email` é criptografado em repouso com AES.
* As senhas são hasheadas, não criptografadas, utilizando o algoritmo PBKDF2.
* O campo `nome` pode ser incluído na criptografia conforme necessidade do projeto.
