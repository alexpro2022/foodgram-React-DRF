import re

from django.core.exceptions import ValidationError


def validate_username(username):
    regex = r'[\w.@+-]+'
    if username == 'me':
        raise ValidationError(
            'Неверное имя пользователя: "me" зарезервировано')
    invalid_symbols = ''.join(set(re.sub(regex, '', username)))
    if invalid_symbols:
        raise ValidationError(
            f'Неверные символы {invalid_symbols} '
            f'в имени пользователя: "{username}"')
    return username
