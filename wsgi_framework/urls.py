from datetime import date, time
from views import MainPage, Teachers, Reiting, Contacts, CreateRating, RatingList

def date_front(request):
    request['date'] = date.today()

def something_front(request):
    request['something'] = 'some'

def time_front(request):
    request['time'] = time()

fronts = [date_front, something_front, time_front]

routes = {
        '/': MainPage(),
        '/teachers/': Teachers(),
        '/rating-list/': RatingList(),
        '/contacts/': Contacts(),
        '/create-rating/': CreateRating(),
        }
