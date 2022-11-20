from django.core.exceptions import ValidationError


class ValidationUser:
    """Validation username."""

    def validate_username(self, username):
        if username == '':
            raise ValidationError('поле username не заполненно')
        elif username == 'me':
            raise ValidationError('me недопустимо в username')
        return username
