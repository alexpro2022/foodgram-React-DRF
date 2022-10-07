from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import APIException


class GenericAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'ERROR from GenericAPIException'
    default_code = 'GenericAPIException'


def fail(msg=None):
    raise GenericAPIException(f'ОШИБКА: {msg}')


def delete_object_or_400(model, *args, **kwargs):
    try:
        model.objects.get(*args, **kwargs).delete()
    except ObjectDoesNotExist:
        fail(f'Отсутствует объект удаления в модели: {model.__name__}')
