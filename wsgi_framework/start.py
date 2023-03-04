from wsgiref.simple_server import make_server

from wsgi_framework.main import Framework
from urls import fronts
from views import routes


app = Framework(routes, fronts)

with make_server('', 8000, app) as httpd:
    print("Сервер запущен на порту 8000")
    httpd.serve_forever()
