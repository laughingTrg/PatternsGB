from wsgi_framework.templator import render
from patterns.create_patterns import Engine, Logger

site = Engine()
logger = Logger('main')

class MainPage:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))

class Teachers:
    def __call__(self, request):
        return '200 OK', render('teachers.html', objects_list=site.teachers)

class Reiting:
    def __call__(self, request):
        return '200 OK', render('reiting.html', objects_list=site.ratings)

class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', date=request.get('date', None))

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


class RatingList:
    def __call__(self, request):
        logger.log('Список рейтингов')
        return '200 OK', render('rating-list.html', objects_list=site.ratings)
