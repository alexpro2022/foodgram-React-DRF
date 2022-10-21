from rest_framework import status

from fixtures import print_


FORMAT = 'json'


def _response(self, response, status_code, response_sample=None):
    self.assertEqual(response.status_code, status_code)
    if response_sample is not None:
        print_(f'=response.data: {self}\n', response.data)
        print_('-------------------')
        print_('=response_sample: \n', response_sample)
        print_('===================')
        self.assertEqual(response.data, response_sample)
    return response


def GET_query(self, client, url, status_code=status.HTTP_200_OK, response_sample=None):
    return _response(self, client.get(url), status_code, response_sample)


def POST_query(self, client, url, payload=None, status_code=status.HTTP_201_CREATED, response_sample=None):
    return _response(self, client.post(url, payload, format=FORMAT), status_code, response_sample)


def PUT_query(self, client, url, payload, status_code=status.HTTP_200_OK, response_sample=None):
    return _response(self, client.put(url, payload, format=FORMAT), status_code, response_sample)


def PATCH_query(self, client, url, payload, status_code=status.HTTP_200_OK, response_sample=None):
    return _response(self, client.patch(url, payload, format=FORMAT), status_code, response_sample)


def DELETE_query(self, client, url, status_code):
    return _response(self, client.delete(url), status_code)


def query(self, method, client, url, payload=None, status_code=status.HTTP_200_OK, response_sample=None):
    method = method.upper()
    if method == 'DELETE':
        return _response(self, client.delete(url), status_code)
    if method == 'GET':
        return _response(self, client.get(url), status_code, response_sample)
    if method == 'PATCH':
        return _response(self, client.patch(url, payload, format=FORMAT), status_code, response_sample)
    if method == 'POST':
        return _response(self, client.post(url, payload, format=FORMAT), status_code, response_sample)
    if method == 'PUT':
        return _response(self, client.put(url, payload, format=FORMAT), status_code, response_sample)
