from django.core.exceptions import ValidationError


class ValidationUser:
    """Валидатор username."""

    def validate_username(self, username):
        if username == '':
            raise ValidationError('необходимо заполнить поле username')
        elif username == 'me':
            raise ValidationError('me недопустимо в username')
        return username
