from datetime import date

from wsgi_framework.templator import render
from patterns.create_patterns import Engine, Logger
from patterns.struct_patterns import AppRoute, Debug
from patterns.behavior_patterns import EmailNotifier, SmsNotifier, BaseSerializer, ListView, CreateView

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


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
            
            teacher_name = data['teacher']
            teacher_name = site.decode_value(teacher_name)
            teacher_obj = site.get_teacher(teacher_name)

            score = data['score']
            score = site.decode_value(score)

            rating = site.create_rating(month, teacher_obj, score)
            
            rating.observers.append(email_notifier)
            rating.observers.append(sms_notifier)

#            rating.add_teacher
            rating.add_teacher(rating.teacher)
            site.ratings.append(rating)
            logger.log(f'Добавлен рейтинг для преподавателя {teacher_name}')

            

            return '200 OK', render('rating-list.html',
                                    objects_list=site.ratings)

        else:
            if len(site.ratings) > 0:
                ratings = site.ratings
                return '200 OK', render('create-rating.html',
                                    objects_list=ratings, teachers_obj=site.teachers)
            else:
                return '200 OK', render('create-rating.html', teachers_obj=site.teachers)


@AppRoute(routes=routes, url='/rating-list/')
class RatingList:
    def __call__(self, request):
        logger.log('Список рейтингов')
        if len(site.ratings) > 0:
            return '200 OK', render('rating-list.html',
                                objects_list=site.ratings)
        else:
            return '200 OK', render('rating-list.html')

@AppRoute(routes=routes, url='/teachers-list/')
class TeacherListView(ListView):
    queryset = site.teachers
    template_name = 'teachers-list.html'

@AppRoute(routes=routes, url='/create-teacher/')
class TeacherCreateView(CreateView):
    template_name = 'create-teacher.html'
    
    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('teacher', name)
        print("create new obj", new_obj, new_obj.name)
        site.teachers.append(new_obj)

@AppRoute(routes=routes, url='/api/')
class RatingApi:
    @Debug(name='RatingApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.ratings).save()






