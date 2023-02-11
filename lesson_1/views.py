from wsgi_framework.templator import render

class MainPage:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))

class Teachers:
    def __call__(self, request):
        return '200 OK', render('teachers.html', date=request.get('date', None))

class Reiting:
    def __call__(self, request):
        return '200 OK', render('reiting.html', date=request.get('date', None))

