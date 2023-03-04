from wsgi_framework.templator import render
from patterns.create_patterns import Engine, Logger
from patterns.struct_patterns import AppRoute, Debug

site = Engine()
logger = Logger('main')

routes = {}

@AppRoute(routes=routes, url='/')
class MainPage:
    @Debug(name='MainPage')
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))

@AppRoute(routes=routes, url='/teachers/')
class Teachers:
    @Debug(name='Teachers')
    def __call__(self, request):
        return '200 OK', render('teachers.html', objects_list=site.teachers)

#class Reiting:
#    def __call__(self, request):
#        return '200 OK', render('reiting.html', objects_list=site.ratings)

@AppRoute(routes=routes, url='/contacts/')
class Contacts:
    @Debug(name='Contacts')
    def __call__(self, request):
        return '200 OK', render('contacts.html', date=request.get('date', None))

@AppRoute(routes=routes, url='/create-rating/')
class CreateRating:

    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']
            month = data['month']
            month = site.decode_value(month)
            
            teacher = data['teacher']
            teacher = site.decode_value(teacher)

            score = data['score']
            score = site.decode_value(score)

            rating = site.create_rating(month, teacher, score)
            site.ratings.append(rating)

            return '200 OK', render('rating-list.html',
                                    objects_list=site.ratings)

        else:
            if len(site.ratings) > 0:
                ratings = site.ratings
                return '200 OK', render('create-rating.html',
                                    objects_list=ratings)
            else:
                return '200 OK', render('create-rating.html')


@AppRoute(routes=routes, url='/rating-list/')
class RatingList:
    def __call__(self, request):
        logger.log('Список рейтингов')
        if len(site.ratings) > 0:
            return '200 OK', render('rating-list.html',
                                objects_list=site.ratings)
        else:
            return '200 OK', render('rating-list.html')
