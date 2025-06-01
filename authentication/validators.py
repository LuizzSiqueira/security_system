import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('A senha deve conter pelo menos uma letra maiúscula.'))
        if not re.search(r'[a-z]', password):
            raise ValidationError(_('A senha deve conter pelo menos uma letra minúscula.'))
        if not re.search(r'\d', password):
            raise ValidationError(_('A senha deve conter pelo menos um número.'))
        if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
            raise ValidationError(_('A senha deve conter pelo menos um caractere especial.'))

    def get_help_text(self):
        return _(
            "A senha deve conter pelo menos uma letra maiúscula, "
            "uma letra minúscula, um número e um caractere especial."
        )
