from .request_util import get_post_content, get_get_content

class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        print('method =', method)

        get_params = get_get_content(environ) 
        print('dict_get_params =', get_params)

        post_params = get_post_content(environ) 
        print('dict_post_params =', post_params)
        self.print_message(post_params)

        path = environ['PATH_INFO']
        
        if not path.endswith('/'):
            path = f'{path}/'
        
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()
        
        request = {}
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    def print_message(self, data: dict):
        if len(data) > 0:
            print(f"Пользователь: {data['email']}\nСообщение: {data['mess']} ")
