import re

from django.core.exceptions import ValidationError


def validate_slug(slug):
    regex = r'[-a-zA-Z0-9_]+'
    invalid_symbols = ''.join(set(re.sub(regex, '', slug)))
    if invalid_symbols:
        raise ValidationError(
            f'Неверные символы {invalid_symbols} в слаге: "{slug}"')
    return slug


def validate_color(hex_color):
    regex = r'^[#A-Fa-f0-9]{7}$'
    invalid_symbols = ''.join(set(re.sub(regex, '', hex_color)))
    if invalid_symbols:
        raise ValidationError(
            f'Неверные символы {invalid_symbols} '
            f'в цветовом HEX-коде: "{hex_color}"')
    return hex_color
