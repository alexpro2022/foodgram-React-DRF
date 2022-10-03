from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ValidationError


def info(value, value_name=None):
    raise Exception(f'={value_name}= {value}')


def request_info(request):
    raise Exception(
        f'=request= {request},\n'
        f'=request.data= {request.data},\n'
        f'=request.user= {request.user},\n'
        f'=query_params= {request.query_params}\n')


def fail(msg=None):
    raise ValidationError(f'ОШИБКА: {msg}')


def delete_object_or_400(klass, *args, **kwargs):
    try:
        instance = klass.objects.get(*args, **kwargs)
    except ObjectDoesNotExist:
        fail('Отсутствует объект удаления')
    instance.delete()


def get_request(self):
    if not hasattr(self, 'context'):
        fail(f'{self.__class__} => No "context" in "self": ')
    request = self.context.get('request')
    if request is None:
        fail(f'{self.__class__} => No "request" in "context": ')
    return request


def get_request_user(self, request=None):
    if request is None:
        request = get_request(self)
    if not hasattr(request, 'user'):
        fail(f'{self.__class__} => No "user" in "request": ')
    return request.user
