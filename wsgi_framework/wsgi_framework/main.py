from quopri import decodestring
from .request_util import get_post_content, get_get_content

class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        
        if not path.endswith('/'):
            path = f'{path}/'
        
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()
        
        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = get_post_content(environ)
            request['data'] = Framework.decode_value(data)
            print(f'Нам пришёл post-запрос: {Framework.decode_value(data)}')
        if method == 'GET':
            request_params = get_get_content(environ)
            request['request_params'] = Framework.decode_value(request_params)
            print(f'Нам пришли GET-параметры:'
                  f' {Framework.decode_value(request_params)}')

            
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    def print_message(self, data: dict):
        if len(data) > 0:
            print(f"Пользователь: {data['email']}\nСообщение: {data['mess']} ")


    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
